import logging
import os
import shutil
import subprocess
import tempfile
from datetime import datetime

from celery import shared_task
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)


def get_docker_client():
    """Get Docker client. Import here to avoid issues if docker isn't installed."""
    try:
        import docker
        return docker.from_env()
    except Exception as e:
        logger.error(f"Failed to connect to Docker: {e}")
        raise


def append_log(deployment, message):
    """Append a message to the deployment build log."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] {message}\n"
    deployment.build_log += log_line
    deployment.save(update_fields=["build_log"])
    logger.info(f"[{deployment.project.slug}] {message}")


@shared_task(bind=True, max_retries=3)
def build_and_deploy(self, deployment_id):
    """
    Clone repository, build Docker image, and start container.

    This task handles the full deployment pipeline:
    1. Clone the GitHub repository
    2. Build a Docker image from the repo
    3. Start the container with Traefik labels for routing
    """
    from .models import ProjectDeployment

    try:
        deployment = ProjectDeployment.objects.select_related("project").get(id=deployment_id)
    except ProjectDeployment.DoesNotExist:
        logger.error(f"Deployment {deployment_id} not found")
        return

    # Clear previous log
    deployment.build_log = ""
    deployment.status = "cloning"
    deployment.save(update_fields=["build_log", "status"])

    temp_dir = None

    try:
        # Step 1: Clone repository
        append_log(deployment, f"Cloning repository: {deployment.github_repo_url}")
        append_log(deployment, f"Branch: {deployment.github_branch}")

        temp_dir = tempfile.mkdtemp(prefix=f"deploy-{deployment.project.slug}-")

        clone_cmd = [
            "git", "clone",
            "--depth", "1",
            "--branch", deployment.github_branch,
            deployment.github_repo_url,
            temp_dir
        ]

        result = subprocess.run(
            clone_cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )

        if result.returncode != 0:
            append_log(deployment, f"Clone failed: {result.stderr}")
            deployment.status = "failed"
            deployment.save(update_fields=["status"])
            return

        append_log(deployment, "Repository cloned successfully")

        # Step 2: Build Docker image
        deployment.status = "building"
        deployment.save(update_fields=["status"])
        append_log(deployment, f"Building Docker image: {deployment.image_name}")

        client = get_docker_client()

        # Check if Dockerfile exists
        dockerfile_path = os.path.join(temp_dir, "Dockerfile")
        if not os.path.exists(dockerfile_path):
            append_log(deployment, "ERROR: No Dockerfile found in repository root")
            deployment.status = "failed"
            deployment.save(update_fields=["status"])
            return

        # Build the image
        try:
            image, build_logs = client.images.build(
                path=temp_dir,
                tag=deployment.image_name,
                rm=True,
                forcerm=True,
            )

            for log in build_logs:
                if "stream" in log:
                    log_line = log["stream"].strip()
                    if log_line:
                        append_log(deployment, log_line)

            append_log(deployment, f"Image built successfully: {image.id[:12]}")

        except Exception as e:
            append_log(deployment, f"Build failed: {str(e)}")
            deployment.status = "failed"
            deployment.save(update_fields=["status"])
            return

        # Step 3: Stop existing container if running
        if deployment.container_id:
            append_log(deployment, f"Stopping existing container: {deployment.container_id[:12]}")
            try:
                old_container = client.containers.get(deployment.container_id)
                old_container.stop(timeout=10)
                old_container.remove(force=True)
                append_log(deployment, "Old container removed")
            except Exception as e:
                append_log(deployment, f"Note: Could not remove old container: {e}")

        # Step 4: Start new container
        deployment.status = "starting"
        deployment.save(update_fields=["status"])
        append_log(deployment, "Starting container...")

        # Traefik labels for path-based routing
        preview_path = f"{deployment.project.slug}-preview"
        slug = deployment.project.slug

        container_labels = {
            "traefik.enable": "true",
            # HTTP router (for local dev)
            f"traefik.http.routers.{slug}.rule": f"PathPrefix(`/{preview_path}`)",
            f"traefik.http.routers.{slug}.entrypoints": "web",
            f"traefik.http.routers.{slug}.middlewares": f"{slug}-strip",
            # HTTPS router (for production)
            f"traefik.http.routers.{slug}-secure.rule": f"PathPrefix(`/{preview_path}`)",
            f"traefik.http.routers.{slug}-secure.entrypoints": "web-secure",
            f"traefik.http.routers.{slug}-secure.middlewares": f"{slug}-strip",
            f"traefik.http.routers.{slug}-secure.tls": "true",
            f"traefik.http.routers.{slug}-secure.tls.certresolver": "letsencrypt",
            # Service (shared by both routers)
            f"traefik.http.services.{slug}.loadbalancer.server.port": str(deployment.internal_port),
            # Strip the prefix so app receives clean paths
            f"traefik.http.middlewares.{slug}-strip.stripprefix.prefixes": f"/{preview_path}",
            # Labels for identification
            "cactuscat.project": slug,
            "cactuscat.managed": "true",
        }

        # Container configuration
        container = client.containers.run(
            deployment.image_name,
            detach=True,
            name=f"client-{deployment.project.slug}",
            labels=container_labels,
            mem_limit=deployment.memory_limit,
            cpu_period=100000,
            cpu_quota=int(deployment.cpu_limit * 100000),
            network="traefik-public",  # Must be on same network as Traefik
            restart_policy={"Name": "unless-stopped"},
            environment={
                "PREVIEW_MODE": "true",
                "PROJECT_SLUG": deployment.project.slug,
            },
        )

        deployment.container_id = container.id
        deployment.status = "running"
        deployment.last_deployed_at = timezone.now()
        deployment.save(update_fields=["container_id", "status", "last_deployed_at"])

        append_log(deployment, f"Container started: {container.id[:12]}")
        append_log(deployment, f"Preview available at: /{preview_path}/")
        append_log(deployment, "Deployment complete!")

        return f"Deployed {deployment.project.slug} successfully"

    except Exception as e:
        logger.exception(f"Deployment failed for {deployment_id}")
        append_log(deployment, f"FATAL ERROR: {str(e)}")
        deployment.status = "failed"
        deployment.save(update_fields=["status"])
        raise self.retry(exc=e, countdown=60)

    finally:
        # Cleanup temp directory
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)


@shared_task()
def stop_deployment(deployment_id):
    """Stop and remove a running container."""
    from .models import ProjectDeployment

    try:
        deployment = ProjectDeployment.objects.select_related("project").get(id=deployment_id)
    except ProjectDeployment.DoesNotExist:
        logger.error(f"Deployment {deployment_id} not found")
        return

    if not deployment.container_id:
        append_log(deployment, "No container to stop")
        deployment.status = "stopped"
        deployment.save(update_fields=["status"])
        return

    try:
        client = get_docker_client()
        container = client.containers.get(deployment.container_id)

        append_log(deployment, f"Stopping container: {deployment.container_id[:12]}")
        container.stop(timeout=30)
        container.remove(force=True)

        deployment.container_id = ""
        deployment.status = "stopped"
        deployment.save(update_fields=["container_id", "status"])

        append_log(deployment, "Container stopped and removed")
        return f"Stopped {deployment.project.slug}"

    except Exception as e:
        append_log(deployment, f"Error stopping container: {e}")
        # Still mark as stopped if container doesn't exist
        deployment.container_id = ""
        deployment.status = "stopped"
        deployment.save(update_fields=["container_id", "status"])
        return f"Container may have been removed externally"


@shared_task()
def check_container_health():
    """
    Periodic task to check health of all running deployment containers.
    Updates status if containers have died unexpectedly.
    """
    from .models import ProjectDeployment

    running_deployments = ProjectDeployment.objects.filter(status="running").exclude(container_id="")

    if not running_deployments.exists():
        return "No running deployments to check"

    try:
        client = get_docker_client()
    except Exception as e:
        logger.error(f"Cannot connect to Docker for health check: {e}")
        return f"Docker connection failed: {e}"

    checked = 0
    updated = 0

    for deployment in running_deployments:
        checked += 1
        try:
            container = client.containers.get(deployment.container_id)
            if container.status != "running":
                append_log(deployment, f"Container state changed: {container.status}")
                deployment.status = "stopped" if container.status == "exited" else "failed"
                deployment.save(update_fields=["status"])
                updated += 1
        except Exception:
            # Container doesn't exist
            append_log(deployment, "Container no longer exists")
            deployment.container_id = ""
            deployment.status = "stopped"
            deployment.save(update_fields=["container_id", "status"])
            updated += 1

    return f"Checked {checked} deployments, updated {updated}"


@shared_task()
def redeploy_from_webhook(deployment_id):
    """
    Triggered by GitHub webhook to redeploy after push to main.
    Simply calls build_and_deploy.
    """
    from .models import ProjectDeployment

    try:
        deployment = ProjectDeployment.objects.get(id=deployment_id)
    except ProjectDeployment.DoesNotExist:
        return f"Deployment {deployment_id} not found"

    append_log(deployment, "Webhook triggered - starting redeploy...")

    # Queue the build
    build_and_deploy.delay(deployment_id)

    return f"Redeploy queued for {deployment.project.slug}"
