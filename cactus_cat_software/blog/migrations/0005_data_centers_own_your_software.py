import datetime
from django.db import migrations


CONTENT = """
<p>Between 2024 and 2028, Microsoft, Amazon, Google, and Meta will collectively spend over a trillion dollars building data centers. Nvidia is shipping GPUs faster than the industry can install them. Electricity infrastructure is being renegotiated at a national level to feed the demand. The raw cost of compute, the fundamental unit of all software, is falling, measurably, at scale.</p>

<p>So why is your Shopify bill going up?</p>

<h2>What data center investment actually means</h2>

<p>When hyperscalers invest at this scale, the cost of running workloads decreases over time. More supply, more efficiency, better hardware. AWS spot instance prices have fallen. Storage costs per gigabyte have dropped by roughly 80% over the last decade. The infrastructure layer of software is cheaper than it has ever been to operate.</p>

<p>This deflationary pressure should flow downstream. If the cost to run a server goes down, the cost to run your business's software should follow. And for software you own, specifically software running on infrastructure you control, it does.</p>

<h2>For rented software, the math runs the other way</h2>

<p>Shopify raised their plan prices 20–33% in 2023. Wix has increased pricing on every plan tier over the past three years. Salesforce, HubSpot, and QuickBooks Online. Every major SaaS business has increased prices over the same period that underlying infrastructure costs fell.</p>

<p>This isn't a contradiction. It's the business model. The falling cost of compute doesn't benefit you as a tenant. It benefits the landlord. When Shopify's infrastructure costs fall, that delta becomes additional margin, not a discount passed to merchants. You are not their customer in any meaningful sense. You are inventory on a revenue line.</p>

<p>The companies that captured the benefit of falling infrastructure costs are the ones that own their systems. They pay for compute directly. When AWS drops spot prices, their monthly bill goes down. When storage gets cheaper, their database costs less. The efficiency gain belongs to them.</p>

<h2>Owning versus leasing: the structural difference</h2>

<p>Leasing software, whether SaaS, platforms, or subscription tools, transfers operational simplicity to you and financial upside to the vendor. You don't manage servers. You don't handle updates. You don't think about infrastructure. In exchange, you pay a monthly fee that the vendor sets, can increase at any time, and controls entirely. The fact that their underlying costs are falling is irrelevant to your contract.</p>

<p>Owning software means paying once (or in phases) to build something, then paying the market rate for the compute it runs on. The market rate for compute is falling. Your system gets cheaper to operate every year, not more expensive. And because you own the code, you can move it to cheaper infrastructure whenever better options emerge, without asking permission or triggering migration penalties.</p>

<h2>The ten-year comparison</h2>

<p>A custom-built platform for a growing e-commerce or service business might cost $18,000 to build and $80/month to host. Over ten years: $18,000 + $9,600 = $27,600. Total.</p>

<p>An equivalent Shopify stack at $2,000/month over ten years: $240,000. And those costs will be higher by year ten, not lower, because Shopify's pricing trajectory is upward regardless of infrastructure economics.</p>

<p>The trillion-dollar data center buildout is the best argument for owning your software that has ever existed. Compute is abundant. Infrastructure is cheap. The only reason software costs should be rising is if someone else is extracting margin between you and the infrastructure.</p>

<h2>What this means practically</h2>

<p>The economics of software ownership have never been better. Building on top of open-source frameworks like Django, PostgreSQL, Redis, and Linux means you're not paying licensing fees on the stack itself. Hosting on AWS, DigitalOcean, or Hetzner means you pay market rates that are being driven down by the largest capital investment in computing history. Your cost of ownership is bounded by how efficiently you can run commodity infrastructure.</p>

<p>That's the deal. Pay once to build. Pay the market to run. Watch the market get cheaper.</p>

<p>Or pay Shopify $2,300/month for Plus, watch them raise it, and own nothing at the end.</p>
"""


def seed_post(apps, schema_editor):
    BlogPost = apps.get_model("blog", "BlogPost")
    if BlogPost.objects.filter(slug="data-centers-own-your-software").exists():
        return
    BlogPost.objects.create(
        title="Data Centers Are Getting Cheaper. Your Software Bill Shouldn't Be Going Up.",
        slug="data-centers-own-your-software",
        author="James",
        excerpt="Microsoft, Amazon, and Google are spending a trillion dollars on infrastructure. Compute costs are falling. So why does your Shopify bill keep going up? Because you're renting, not owning.",
        content=CONTENT.strip(),
        status="published",
        published_date=datetime.datetime(2024, 6, 10, 9, 0, 0, tzinfo=datetime.timezone.utc),
        meta_description="Hyperscaler investment drives compute costs down. Software you own gets cheaper every year. Software you rent gets more expensive. Here's the difference.",
        featured=False,
    )


def reverse_post(apps, schema_editor):
    BlogPost = apps.get_model("blog", "BlogPost")
    BlogPost.objects.filter(slug="data-centers-own-your-software").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0004_shopify_true_cost_post"),
    ]

    operations = [
        migrations.RunPython(seed_post, reverse_post),
    ]
