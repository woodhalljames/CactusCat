// Shared content across all three variants. Single source of truth so
// copy stays consistent and we can A/B layout treatments only.

const HERO_BG = "assets/hero_navbar.png";

const CYCLE_PHRASES = [
  "delivers results.",
  "scales with you.",
  "lasts a lifetime.",
  "runs without you.",
];

const SERVICES = [
  {
    n: "01",
    kicker: "Custom Development",
    title: "Web apps, built from scratch — owned by you.",
    body: "Bespoke web applications and marketing sites engineered for your workflow. Same stack the giants run on, handed over with the keys so your team operates it without a developer on retainer.",
    bullets: ["Web applications", "Marketing websites", "Business automations", "API & data integrations"],
    cta: "Development services",
  },
  {
    n: "02",
    kicker: "SaaS & Mobile",
    title: "Subscription products and native apps.",
    body: "From recurring-revenue SaaS to iOS and Android — secure payments, user management, and a marketing suite built in from day one.",
    bullets: ["Subscription SaaS", "iOS / Android", "Stripe & billing", "Auth & permissions"],
    cta: "SaaS & mobile",
  },
  {
    n: "03",
    kicker: "Digital Marketing",
    title: "Broadcast the signal further.",
    body: "Software needs to be found. We pair every build with SEO foundations, social automation, content strategy, and analytics — discovery to conversion in one motion.",
    bullets: ["SEO foundations", "Social automation", "Content strategy", "Conversion analytics"],
    cta: "Marketing services",
  },
  {
    n: "04",
    kicker: "Cybersecurity",
    title: "Protected at every layer.",
    body: "Security is the foundation, not a feature. Penetration testing, compliance consulting, and vulnerability management — we harden your systems before attackers find the cracks.",
    bullets: ["Penetration testing", "HIPAA · PCI · SOC 2", "Vulnerability management", "Awareness training"],
    cta: "Security services",
  },
  {
    n: "05",
    kicker: "Transparency",
    title: "Your personal control room.",
    body: "Real-time status, milestone tracking, live preview access, and direct comms through a dashboard built for you. No black boxes, no surprise invoices.",
    bullets: ["Live preview URLs", "Milestone approvals", "Document repository", "Direct messaging"],
    cta: "Our process",
  },
];

// Proof of work — real-ish projects mocked as placeholders.
const PROOF = [
  {
    tag: "Wedding · SaaS",
    name: "DreamWed AI",
    blurb: "AI-assisted vendor matchmaking and timeline builder for couples planning weddings.",
    metrics: [{ k: "MRR", v: "$24k" }, { k: "Users", v: "8,400" }, { k: "Uptime", v: "99.97%" }],
    stack: ["Django", "Next.js", "Postgres", "Stripe"],
    hue: 24,
  },
  {
    tag: "E-commerce · Web",
    name: "Saguaro Outfitters",
    blurb: "Independent outdoor retailer storefront with custom inventory + Square POS sync.",
    metrics: [{ k: "Orders/mo", v: "1,240" }, { k: "Conv.", v: "3.8%" }, { k: "TTI", v: "0.9s" }],
    stack: ["Django", "Shopify API", "Cloudflare"],
    hue: 162,
  },
  {
    tag: "Hospitality · Marketing",
    name: "Mesa Verde Inn",
    blurb: "Boutique hotel marketing site with direct-booking engine and SEO content engine.",
    metrics: [{ k: "Organic", v: "+312%" }, { k: "DR", v: "C → AA" }, { k: "Bookings", v: "+47%" }],
    stack: ["Webflow", "Cloudbeds", "GA4"],
    hue: 200,
  },
  {
    tag: "Logistics · Internal",
    name: "RouteSentry",
    blurb: "Dispatch & route-optimization dashboard for a regional last-mile fleet operator.",
    metrics: [{ k: "Fleet", v: "84 vans" }, { k: "Saved", v: "11hrs/wk" }, { k: "ROI", v: "6.2×" }],
    stack: ["Django", "Mapbox", "Celery"],
    hue: 280,
  },
];

const STATS_STRIP = [
  { k: "Projects delivered", v: "120+" },
  { k: "Avg. timeline", v: "8 wks" },
  { k: "Code shipped", v: "1.2M lines" },
  { k: "Client retention", v: "94%" },
];

const FAQ = [
  { q: "Who owns the code?", a: "You do — every line, from day one. Repo is yours, hosting is yours, the keys are yours." },
  { q: "What does a typical engagement look like?", a: "Two-week discovery, a fixed-fee build (usually 6–12 weeks), and a fixed monthly retainer if you want us to keep operating it." },
  { q: "Do you only work East Coast?", a: "We're East Coast based but ship globally. Most clients we never meet in person." },
];

Object.assign(window, {
  HERO_BG, CYCLE_PHRASES, SERVICES, PROOF, STATS_STRIP, FAQ,
});
