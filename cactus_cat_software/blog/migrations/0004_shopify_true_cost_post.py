import datetime
from django.db import migrations


CONTENT = """
<p>The pitch is simple: $29 a month for Wix, $39 a month for Shopify. Launch your store this weekend. No developers, no complexity, no upfront cost.</p>

<p>That pitch is true for about six months. After that, the math changes and keeps changing, in one direction, for as long as you stay on the platform.</p>

<h2>What you actually pay in year one</h2>

<p>The base plan gets you a storefront and a checkout. It does not get you a business. Everything a real operation needs sits behind additional fees:</p>

<ul>
  <li><strong>Apps &amp; plugins.</strong> Email marketing, subscriptions, loyalty programs, reviews, shipping automation, advanced reporting, upsells, and SMS. None of it is included. The average Shopify store at real volume runs 6–12 paid apps at $20–$150 each per month. That's $120–$1,800/month on top of the plan fee.</li>
  <li><strong>Transaction fees.</strong> Use any payment processor other than Shopify Payments and they charge 0.5%–2% of every transaction. On $500k in annual revenue, that's up to $10,000/year paid to Shopify as a toll for processing your own money.</li>
  <li><strong>Tier paywalls.</strong> Advanced reporting? Shopify Advanced at $399/month. Custom checkout logic, B2B pricing, automation workflows? Shopify Plus at $2,300/month. The plan you start on is not the plan you need at scale.</li>
  <li><strong>Wix adds its own layer.</strong> Wix Business plans range from $36–$159/month, but real functionality such as removing transaction fees, multiple currencies, and advanced analytics requires constant upgrades. Third-party app costs mirror Shopify's ecosystem exactly.</li>
</ul>

<p>By the end of year one, a business with any meaningful volume is typically spending $1,200–$4,000/month across platform fees, apps, and transaction costs. That's $14,400–$48,000 per year, and rising.</p>

<h2>The hidden cost: manual labor</h2>

<p>The more insidious expense is the one that doesn't show up in any invoice. Both Shopify and Wix are designed, at tiers below Plus, to be operated manually. Inventory updates, wholesale order processing, export-to-spreadsheet reporting, return reconciliation, and multi-location stock management. These are human tasks on these platforms because automation is either unavailable or costs extra.</p>

<p>Staff hours spent on work that a properly built system would do automatically are a real cost. At $25/hour, 10 hours of manual process per week is $13,000/year in labor doing nothing but keeping the platform functional. That number compounds every year headcount touches the problem.</p>

<h2>You don't own any of it</h2>

<p>Every customer record, every order, every behavioral signal lives in Shopify's or Wix's database, not yours. You have export access, not ownership. When they change their API, you adapt. When they raise prices, you pay. When they deprecate a feature, you rebuild your workflow. When they decide your use case no longer fits their product direction, you migrate at enormous cost to wherever fits next.</p>

<p>Switching after three years means migrating product data, customer records, URLs, integrations, and staff workflows. It is a multi-month project. That switching cost is not an accident. It is the business model.</p>

<h2>The ten-year number</h2>

<p>A business spending $2,000/month on a mid-tier Shopify stack, covering plan costs, apps, and transaction fees, will spend $240,000 over ten years. And own nothing. No code. No data infrastructure. No competitive moat. Nothing that couldn't be replicated by a competitor signing up for the same plan tomorrow.</p>

<p>A Wix business at the equivalent tier is not meaningfully different. The platform names change; the extraction model is the same.</p>

<h2>What working with Cactus Cat looks like instead</h2>

<p>We build custom software on a fixed-price, fixed-timeline model. A full e-commerce platform covering product catalog, checkout, customer accounts, order management, inventory, and integrations with the tools you already use typically runs $12,000–$28,000 to build, depending on scope. You own 100% of the code and data from day one.</p>

<p>After delivery, your ongoing costs are:</p>

<ul>
  <li><strong>Hosting:</strong> $40–$120/month on infrastructure you control (no per-transaction fees, no tier restrictions)</li>
  <li><strong>Optional support:</strong> Monthly maintenance if you want us actively managing it, or nothing, because it's your system and you can hand it to any developer</li>
  <li><strong>Integrations:</strong> One-time build cost per integration, not a perpetual monthly subscription to a third-party app</li>
</ul>

<p>At $80/month in hosting costs, year-one total cost is your build fee plus ~$960 in hosting. Year two is $960. Year three is $960. The system compounds in value as you build on it, rather than depleting margin as a landlord raises rent.</p>

<h2>The break-even math</h2>

<p>If you're spending $1,500/month on Shopify or Wix, a conservative figure for a growing business, custom software breaks even in 12–18 months. After that, every month is money you're keeping instead of paying for a platform you don't own.</p>

<p>The upfront cost is real. The long-term math is not close.</p>
"""


def seed_post(apps, schema_editor):
    BlogPost = apps.get_model("blog", "BlogPost")
    if BlogPost.objects.filter(slug="the-real-cost-of-shopify-and-wix").exists():
        return
    BlogPost.objects.create(
        title="The Real Lifetime Cost of Shopify and Wix (And What You Own at the End)",
        slug="the-real-cost-of-shopify-and-wix",
        author="James",
        excerpt="Shopify says $39/month. Wix says $29. Ten years later, you've spent over $200,000 and own nothing. Here's the actual math and what a custom-built alternative costs instead.",
        content=CONTENT.strip(),
        status="published",
        published_date=datetime.datetime(2024, 2, 12, 9, 0, 0, tzinfo=datetime.timezone.utc),
        meta_description="Full breakdown of Shopify and Wix lifetime costs including app fees, transaction tolls, manual labor, and lock-in, versus custom software you actually own.",
        featured=False,
    )


def reverse_post(apps, schema_editor):
    BlogPost = apps.get_model("blog", "BlogPost")
    BlogPost.objects.filter(slug="the-real-cost-of-shopify-and-wix").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0003_cloudflare_outage_post"),
    ]

    operations = [
        migrations.RunPython(seed_post, reverse_post),
    ]
