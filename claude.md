Project: software dev, digital marketing, and cybersecurity website using django tech stack
Tech: django-cookie-cutter, Django, html, css, JS.
Goals for session: Improve beta dashboard to also accomodate Beta Server Deployment System. Clients can see their website as its produced 
Architecture:

Your VPS runs a main Django app (your admin dashboard)
Each client project is a separate Docker container
Nginx reverse proxy routes yourdomain.com/user/theirwebsite → container 1, yourdomain.com/user/theirwebsite2 → container 2
Each project gets its own subdomain or path

Admin workflow:

You add a project in your Django admin
Provide GitHub repo URL + branch
System clones repo, builds Docker image, spins up container
Automatically provisions subdomain and SSL cert (Let's Encrypt)
Client gets access via their project dashboard

Key components to research:

Docker SDK for Python - lets Django control Docker programmatically
GitHub webhooks - auto-deploy on push to specific branch
Traefik or Nginx - dynamic routing to containers
Celery - handle builds/deployments as background tasks so admin doesn't hang

Security considerations:

Each container isolated
Client-specific authentication
Resource limits per container (CPU/memory) Keep it low
Separate networks for each project


Preferences: Simple solutions that work.  Front end design and UX that WOWS. 


I will run all migrations as necessary. 







Required VPS Setup                                                            
                                                                                
  1. Create the Docker Network (one-time)                                       
                                                                                
  The client containers need to join the traefik-public network to be routable  
  via Traefik. Create it before deploying:                                      
                                                                                
  docker network create traefik-public                                          
                                                                                
  This network is referenced in your compose file but external containers       
  spawned by Celery need it to exist.                                           
                                                                                
  2. Verify Docker Socket Permissions                                           
                                                                                
  Your celeryworker mounts /var/run/docker.sock. The container process needs    
  permission to use it. Two options:                                            
                                                                                
  Option A: Add the celeryworker user to the docker group inside the container  
  Option B: Ensure the socket is readable (less secure):                        
  chmod 666 /var/run/docker.sock                                                
                                                                                
  3. Schedule the Health Check Task                                             
                                                                                
  Since you're using DatabaseScheduler, add the periodic health check via Django
   admin:                                                                       
  - Go to Admin → Periodic Tasks → Add                                          
  - Task: cactus_cat_software.projects.tasks.check_container_health             
  - Schedule: Every 5 minutes (or your preference)                              
                                                                                
  4. Ensure Git is Installed                                                    
                                                                                
  The build_and_deploy task runs git clone. Git should be in your               
  Django/celeryworker Docker image (likely already there).                      
                                                                                
  ---                                                                           
  What's Already Configured Correctly                                           
                                                                                
  - Traefik Docker provider (docker-compose.production.yml:49)                  
  - Path-based routing exclusion in traefik.yml:35 for *-preview paths          
  - Celeryworker Docker socket mount (docker-compose.production.yml:69)         
  - Celeryworker on traefik-public network (docker-compose.production.yml:71-72)
  - docker Python package in dependencies (pyproject.toml:180)                  
                                                                                
  ---                                                                           
  Security Consideration                                                        
                                                                                
  Client containers on traefik-public can potentially reach your internal       
  services (postgres, redis). Consider adding network policies or running client
   containers on a separate isolated network if this is a concern.              
                                                                                
  ---                                                                           
  Testing                                                                       
                                                                                
  After deploying, test with a simple project that has a Dockerfile. Create a   
  ProjectDeployment in admin, then trigger build_and_deploy manually via Flower 
  or Django shell:                                                              
                                                                                
  from cactus_cat_software.projects.tasks import build_and_deploy               
  build_and_deploy.delay(deployment_id)   