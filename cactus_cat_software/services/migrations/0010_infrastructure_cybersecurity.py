from django.db import migrations


def upgrade(apps, schema_editor):
    ServiceCategory = apps.get_model("services", "ServiceCategory")
    ServicePackage = apps.get_model("services", "ServicePackage")

    # Rename category
    ServiceCategory.objects.filter(slug="infrastructure-support").update(
        name="Infrastructure & Cybersecurity",
        slug="infrastructure-cybersecurity",
    )

    try:
        category = ServiceCategory.objects.get(slug="infrastructure-cybersecurity")
    except ServiceCategory.DoesNotExist:
        return

    ServicePackage.objects.update_or_create(
        slug="security-audit-penetration-test",
        defaults={
            "name": "Security Audit & Penetration Test",
            "category": category,
            "short_description": (
                "A hands-on assessment of your application and infrastructure: "
                "vulnerability scanning, exploitation testing, and a plain-English "
                "remediation report ranked by business risk."
            ),
            "features": (
                "External and internal network vulnerability scan\n"
                "Web application penetration test (OWASP Top 10)\n"
                "Authentication and access control review\n"
                "Cloud configuration audit (AWS or Azure)\n"
                "Detailed findings report with severity rankings\n"
                "Remediation roadmap prioritised by business impact\n"
                "Follow-up verification scan after fixes are applied"
            ),
            "who_its_for": (
                "Businesses preparing for a compliance audit or enterprise sales process\n"
                "Founders who have never had a third-party security review\n"
                "Teams that recently launched a customer-facing application\n"
                "Companies handling sensitive data or financial transactions"
            ),
            "description": (
                "Most vulnerabilities are found by attackers, not owners. "
                "We approach your systems the way an adversary would: scanning for exposure, "
                "testing authentication flows, probing cloud configuration, and attempting controlled "
                "exploitation to find what actually matters. "
                "You receive a plain-English report that ranks findings by real business risk, "
                "not CVSS scores, along with a prioritised remediation roadmap. "
                "Once fixes are in place we run a verification scan to confirm they hold."
            ),
            "price": "2800.00",
            "setup_fee": None,
            "monthly_price": None,
            "is_price_starting_from": True,
            "display_order": 3,
            "estimated_delivery_days": 14,
        },
    )

    ServicePackage.objects.update_or_create(
        slug="compliance-readiness-assessment",
        defaults={
            "name": "Compliance Readiness Assessment",
            "category": category,
            "short_description": (
                "A structured gap analysis and remediation roadmap for HIPAA, "
                "PCI-DSS, SOC 2, or CMMC. Know exactly where you stand and what it takes to get compliant."
            ),
            "features": (
                "Framework selection and scoping (HIPAA, PCI-DSS, SOC 2, or CMMC)\n"
                "Current-state gap analysis against chosen framework controls\n"
                "Policy and procedure review\n"
                "Data flow and access control mapping\n"
                "Risk register with likelihood and impact scoring\n"
                "Prioritised remediation roadmap with effort estimates\n"
                "Executive summary suitable for board or investor review"
            ),
            "who_its_for": (
                "Healthcare and fintech companies approaching their first audit\n"
                "SaaS businesses entering enterprise or government sales cycles\n"
                "Defense contractors preparing for CMMC certification\n"
                "Founders who need to answer 'are you compliant?' in a deal room"
            ),
            "description": (
                "Compliance frameworks are not checklists; they are risk management programs. "
                "We map your current controls against the requirements of your chosen framework, "
                "identify the gaps that carry the most risk, and hand you a remediation roadmap "
                "with realistic effort estimates so you can plan the work and budget it accurately. "
                "The deliverable is a board-ready summary and a working risk register, "
                "not a stack of boilerplate PDFs."
            ),
            "price": "3500.00",
            "setup_fee": None,
            "monthly_price": None,
            "is_price_starting_from": True,
            "display_order": 4,
            "estimated_delivery_days": 21,
        },
    )


def downgrade(apps, schema_editor):
    ServiceCategory = apps.get_model("services", "ServiceCategory")
    ServicePackage = apps.get_model("services", "ServicePackage")

    ServicePackage.objects.filter(
        slug__in=["security-audit-penetration-test", "compliance-readiness-assessment"]
    ).delete()

    ServiceCategory.objects.filter(slug="infrastructure-cybersecurity").update(
        name="Infrastructure & Support",
        slug="infrastructure-support",
    )


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0009_managed_content_dashboard_service"),
    ]

    operations = [
        migrations.RunPython(upgrade, downgrade),
    ]
