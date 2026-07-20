from django.db import migrations

PACKAGES = [
    # ── Custom Software Development ──────────────────────────────
    {
        "name": "Business Web Application",
        "slug": "business-web-application",
        "category_slug": "custom-software-development",
        "short_description": "A full-featured web application built around how your business operates: portals, dashboards, internal tools, or customer-facing apps.",
        "features": (
            "Django + PostgreSQL backend, React or server-rendered frontend\n"
            "Role-based auth with admin panel\n"
            "Full source code transferred on day one\n"
            "Plain-English technical documentation\n"
            "Two weeks of post-launch support included\n"
            "Hosted on infrastructure you control"
        ),
        "who_its_for": (
            "Business owners replacing manual or spreadsheet-based workflows\n"
            "Teams that need a client or staff portal\n"
            "Founders building an internal operations tool"
        ),
        "description": (
            "Off-the-shelf software makes you adapt to it. We flip that. "
            "Your business web application is engineered around how you actually operate, "
            "whether that's a customer portal, an internal ops tool, or a workflow dashboard. "
            "We handle backend, frontend, auth, and deployment, then hand you the keys with full source code "
            "and documentation. No subscriptions. No lock-in. Yours outright."
        ),
        "price": "7500.00",
        "setup_fee": "2500.00",
        "monthly_price": "550.00",
        "is_price_starting_from": True,
        "display_order": 1,
        "estimated_delivery_days": 42,
    },
    {
        "name": "SaaS Platform Build",
        "slug": "saas-platform-build",
        "category_slug": "custom-software-development",
        "short_description": "A production-ready SaaS platform with multi-tenant architecture, Stripe billing, and an admin dashboard. Built to scale from day one.",
        "features": (
            "Multi-tenant Django architecture\n"
            "Stripe subscription billing with plan management\n"
            "Full user auth: sign-up, login, MFA, and password reset\n"
            "Admin dashboard with usage analytics\n"
            "REST or GraphQL API included\n"
            "CI/CD pipeline and staging environment\n"
            "Full source code and documentation delivered"
        ),
        "who_its_for": (
            "Founders turning a manual service into a software product\n"
            "Businesses building a productised offering for clients\n"
            "Teams that need recurring billing infrastructure"
        ),
        "description": (
            "We build production-grade SaaS platforms that are ready to charge customers from day one. "
            "Multi-tenant architecture, Stripe billing, role-based auth, and an admin panel are all included as standard. "
            "You own the codebase outright. No platform fees, no revenue share, no lock-in. "
            "We build it, document it, deploy it, and hand it over."
        ),
        "price": "15000.00",
        "setup_fee": "5000.00",
        "monthly_price": "1200.00",
        "is_price_starting_from": True,
        "display_order": 2,
        "estimated_delivery_days": 84,
    },

    # ── Automation & AI Systems ──────────────────────────────────
    {
        "name": "Workflow Automation Script",
        "slug": "workflow-automation-script",
        "category_slug": "automation-ai-systems",
        "short_description": "A custom script that automates one recurring process: CRM sync, report generation, invoice reconciliation, or any manual task your team runs on a schedule.",
        "features": (
            "Single process automated end-to-end\n"
            "Platform integrations included (Stripe, HubSpot, QuickBooks, Slack, and more)\n"
            "Scheduled execution with error alerting\n"
            "Slack or email notification on run completion\n"
            "Full source code and documentation delivered\n"
            "One week of post-launch monitoring included"
        ),
        "who_its_for": (
            "Operations teams running the same task every day or every week\n"
            "Finance teams reconciling data between platforms\n"
            "Businesses spending hours on manual reporting"
        ),
        "description": (
            "If your team is doing something on a schedule that a script could handle, "
            "that's recoverable time. We identify the exact process, build the automation, "
            "connect it to your existing platforms, and schedule it to run without human input. "
            "You get the source code, the documentation, and the hours back."
        ),
        "price": "1800.00",
        "setup_fee": None,
        "monthly_price": None,
        "is_price_starting_from": True,
        "display_order": 1,
        "estimated_delivery_days": 14,
    },
    {
        "name": "AI-Powered Workflow Integration",
        "slug": "ai-workflow-integration",
        "category_slug": "automation-ai-systems",
        "short_description": "Bring AI into your operations through document processing, intelligent routing, auto-generated reports, or natural language interfaces built into your existing stack.",
        "features": (
            "Claude or OpenAI API integrated into your workflow\n"
            "Document parsing, classification, or extraction\n"
            "Natural language query layer over your data\n"
            "Auto-generated summaries, reports, or drafts\n"
            "Connects to your existing tools and databases\n"
            "Full source code and documentation delivered"
        ),
        "who_its_for": (
            "Teams processing high volumes of documents or emails\n"
            "Businesses that want AI in their workflow without a SaaS subscription\n"
            "Founders adding intelligent features to an existing product"
        ),
        "description": (
            "AI tools only pay off when they're wired into how you actually work. "
            "We build custom AI integrations directly into your stack: document processing, intelligent classification, "
            "auto-generated outputs, and natural language interfaces. "
            "No SaaS subscription. No black box. You own the integration and control the model."
        ),
        "price": "4500.00",
        "setup_fee": "1500.00",
        "monthly_price": "350.00",
        "is_price_starting_from": True,
        "display_order": 2,
        "estimated_delivery_days": 21,
    },

    # ── Technical Marketing & Growth ─────────────────────────────
    {
        "name": "Technical SEO Audit & Implementation",
        "slug": "technical-seo-audit-implementation",
        "category_slug": "technical-marketing-growth",
        "short_description": "A full technical SEO audit of your site followed by hands-on implementation covering structured data, Core Web Vitals, crawlability, and on-page foundations.",
        "features": (
            "Full crawl audit with prioritised issue list\n"
            "Core Web Vitals analysis and fixes\n"
            "Structured data (schema.org) implementation\n"
            "Sitemap, robots.txt, and canonical tag review\n"
            "Page speed optimisation\n"
            "Written report with findings and recommendations"
        ),
        "who_its_for": (
            "Businesses whose site isn't ranking despite good content\n"
            "Teams preparing for a site relaunch\n"
            "Founders who want a clean SEO baseline before scaling content"
        ),
        "description": (
            "Most SEO problems are technical before they're content problems. "
            "We audit your site from the ground up, covering crawlability, page speed, structured data, "
            "internal linking, and Core Web Vitals, then implement the fixes ourselves. "
            "You get a written report plus a cleaner, faster, more crawlable site."
        ),
        "price": "2200.00",
        "setup_fee": None,
        "monthly_price": None,
        "is_price_starting_from": False,
        "display_order": 1,
        "estimated_delivery_days": 10,
    },
    {
        "name": "Lead Generation System",
        "slug": "lead-generation-system",
        "category_slug": "technical-marketing-growth",
        "short_description": "A conversion-optimised landing page, lead capture form, and automated email nurture sequence. Built, connected, and live in three weeks.",
        "features": (
            "Conversion-optimised landing page built and deployed\n"
            "Lead capture form with CRM integration\n"
            "Automated email nurture sequence (5–7 emails)\n"
            "Analytics and conversion tracking setup\n"
            "A/B test framework configured\n"
            "Full documentation and handover"
        ),
        "who_its_for": (
            "Businesses running paid ads with no optimised landing page\n"
            "Service providers wanting a systematic follow-up process\n"
            "Founders launching a new product or offer"
        ),
        "description": (
            "Traffic without conversion infrastructure is expensive. "
            "We build the full funnel: a fast, conversion-optimised landing page, "
            "a lead capture form connected to your CRM, and an automated email sequence "
            "that follows up without anyone touching it. "
            "Visitors come in. Leads come out."
        ),
        "price": "3800.00",
        "setup_fee": None,
        "monthly_price": None,
        "is_price_starting_from": False,
        "display_order": 2,
        "estimated_delivery_days": 21,
    },

    # ── Infrastructure & Support ─────────────────────────────────
    {
        "name": "Managed Hosting & Deployment Setup",
        "slug": "managed-hosting-deployment-setup",
        "category_slug": "infrastructure-support",
        "short_description": "Full production deployment of your application: VPS provisioning, CI/CD pipeline, SSL, backups, and uptime monitoring. All on infrastructure you own.",
        "features": (
            "VPS provisioning and server hardening\n"
            "CI/CD pipeline (GitHub Actions or equivalent)\n"
            "SSL certificates and domain configuration\n"
            "Automated daily backups with tested restore process\n"
            "Uptime monitoring with Slack/email alerting\n"
            "Documentation of the full deployment setup"
        ),
        "who_its_for": (
            "Founders deploying their first production application\n"
            "Teams moving off shared hosting or Heroku\n"
            "Businesses that want infrastructure they control and understand"
        ),
        "description": (
            "We provision your server, harden it, deploy your application, "
            "wire up CI/CD so pushes go live automatically, configure SSL and backups, "
            "and set up monitoring that alerts you before users notice a problem. "
            "Everything runs on infrastructure you own. No platform dependency, no surprise bills."
        ),
        "price": "1200.00",
        "setup_fee": None,
        "monthly_price": None,
        "is_price_starting_from": False,
        "display_order": 1,
        "estimated_delivery_days": 7,
    },
    {
        "name": "Monthly Maintenance Retainer",
        "slug": "monthly-maintenance-retainer",
        "category_slug": "infrastructure-support",
        "short_description": "Ongoing security patches, dependency updates, performance monitoring, and priority support. A dedicated retainer that keeps your systems healthy long-term.",
        "features": (
            "Monthly security patches and dependency updates\n"
            "Uptime and performance monitoring\n"
            "Monthly plain-English performance report\n"
            "Priority support with same-business-day response\n"
            "Minor bug fixes included (up to 4 hrs/month)\n"
            "Quarterly review call"
        ),
        "who_its_for": (
            "Businesses running a production application without in-house dev support\n"
            "Founders who want a developer on call without hiring full-time\n"
            "Teams that shipped a project and need someone watching it"
        ),
        "description": (
            "Shipping is the beginning, not the end. "
            "On a monthly retainer we handle security patches, dependency updates, "
            "uptime monitoring, and minor fixes so nothing quietly breaks in the background. "
            "You get a monthly plain-English report and priority access when something needs attention. "
            "Cancel any time. No contracts."
        ),
        "price": "450.00",
        "setup_fee": None,
        "monthly_price": "450.00",
        "is_price_starting_from": False,
        "display_order": 2,
        "estimated_delivery_days": None,
    },
]


def seed_packages(apps, schema_editor):
    ServiceCategory = apps.get_model("services", "ServiceCategory")
    ServicePackage = apps.get_model("services", "ServicePackage")

    for pkg in PACKAGES:
        try:
            category = ServiceCategory.objects.get(slug=pkg["category_slug"])
        except ServiceCategory.DoesNotExist:
            continue

        ServicePackage.objects.update_or_create(
            slug=pkg["slug"],
            defaults={
                "name": pkg["name"],
                "category": category,
                "short_description": pkg["short_description"],
                "features": pkg["features"],
                "who_its_for": pkg["who_its_for"],
                "description": pkg["description"],
                "price": pkg["price"],
                "setup_fee": pkg["setup_fee"],
                "monthly_price": pkg["monthly_price"],
                "is_price_starting_from": pkg["is_price_starting_from"],
                "display_order": pkg["display_order"],
                "estimated_delivery_days": pkg["estimated_delivery_days"],
                "is_active": True,
            },
        )


def unseed_packages(apps, schema_editor):
    ServicePackage = apps.get_model("services", "ServicePackage")
    slugs = [p["slug"] for p in PACKAGES]
    ServicePackage.objects.filter(slug__in=slugs).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0005_update_service_categories"),
    ]

    operations = [
        migrations.RunPython(seed_packages, unseed_packages),
    ]
