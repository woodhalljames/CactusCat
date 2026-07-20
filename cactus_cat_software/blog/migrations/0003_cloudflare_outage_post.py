import datetime
from django.db import migrations


CONTENT = """
<p>It was a Tuesday afternoon when thousands of websites simultaneously went offline. Support tickets flooded in. Revenue flatlined. And the companies that had no one on call scrambled to figure out what was even happening, let alone how to fix it.</p>

<p>The culprit: Cloudflare.</p>

<h2>What happened</h2>

<p>Cloudflare operates the infrastructure that sits between millions of websites and their visitors. DNS resolution, DDoS mitigation, caching, and SSL termination. It handles the invisible plumbing that makes the modern web work. When a significant portion of that network went down, entire categories of the internet went with it.</p>

<p>The outage wasn't unique. Cloudflare has had several notable incidents over the years, including BGP routing failures, software bugs that cascaded across their global network, and configuration errors that took down regions. Each time, the same pattern plays out: sites go dark, engineers scramble, and businesses lose money while waiting for a vendor to fix something completely outside their control.</p>

<h2>The two types of clients</h2>

<p>In the aftermath of any major infrastructure event, there are two types of businesses:</p>

<p><strong>Type 1:</strong> They get an alert. Someone who knows the system picks it up. They diagnose whether the issue is upstream (Cloudflare, their host, a third-party API) or something in their own stack. They update their status page, communicate to customers, and implement a workaround or failover if one exists. They're back online, or transparently offline, within minutes.</p>

<p><strong>Type 2:</strong> Their site goes down. Customers email. Someone notices. They post in a Slack channel asking "is the site down?" Someone else checks. Nobody knows what Cloudflare is. They can't tell if it's their hosting, their code, or the internet. They file a support ticket with their hosting provider. They wait. Hours pass.</p>

<p>The difference between these two businesses is not budget. It's whether someone who understands the stack is reachable.</p>

<h2>Why retainers exist</h2>

<p>We build software that's designed to run without us. That's the goal. Full source code transferred on day one, documented clearly enough that your team can operate it, hosted on infrastructure you control.</p>

<p>But infrastructure is a living system. Dependencies get updated. Certificates expire. Vendors change APIs. Servers get overloaded. And sometimes, through no fault of yours or ours, a company the size of Cloudflare takes a portion of the internet offline for an afternoon.</p>

<p>A monthly retainer isn't a lock-in. It's a phone call away. It means that when something goes sideways at 11pm on a Friday, someone who built the system and knows every line of it is the person picking up.</p>

<h2>What you can do right now</h2>

<p>Whether you're a current client or not, here are three things worth having in place before the next outage:</p>

<ol>
  <li><strong>A status page.</strong> Even a simple one. Customers can forgive downtime. They can't forgive silence.</li>
  <li><strong>Monitoring with alerting.</strong> You shouldn't find out your site is down from a customer email. Uptime monitoring with SMS or Slack alerts costs almost nothing and saves enormous amounts of reputational damage.</li>
  <li><strong>A clear escalation path.</strong> Who do you call? Do they know the system? Can they act without waiting for a ticket queue?</li>
</ol>

<p>We set all three up as part of every engagement. And for clients on a retainer, we're the answer to that third question.</p>

<p>The next Cloudflare outage is coming. The next AWS us-east-1 incident. The next DNS propagation failure. The internet is remarkably reliable until it isn't. The gap between businesses that weather those moments and ones that don't is almost always a person, not a product.</p>
"""


def seed_post(apps, schema_editor):
    BlogPost = apps.get_model("blog", "BlogPost")
    if BlogPost.objects.filter(slug="when-cloudflare-goes-down").exists():
        return
    BlogPost.objects.create(
        title="When Cloudflare Goes Down: Why Businesses Need a Dev On Call",
        slug="when-cloudflare-goes-down",
        author="James",
        excerpt="A major CDN outage took thousands of sites offline in an afternoon. The businesses that recovered fast all had the same thing in common: someone who knew the stack was reachable.",
        content=CONTENT.strip(),
        status="published",
        published_date=datetime.datetime(2023, 10, 15, 9, 0, 0, tzinfo=datetime.timezone.utc),
        meta_description="What the Cloudflare outage reveals about infrastructure risk, and why a dev on retainer is the difference between minutes and hours of downtime.",
        featured=False,
    )


def reverse_post(apps, schema_editor):
    BlogPost = apps.get_model("blog", "BlogPost")
    BlogPost.objects.filter(slug="when-cloudflare-goes-down").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0002_alter_blogpost_author"),
    ]

    operations = [
        migrations.RunPython(seed_post, reverse_post),
    ]
