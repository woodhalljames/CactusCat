// ABOUT PAGE — dispatch theming applied.
// Star-chart hero, same nav/footer, same marquee + atlas-grid + log layouts.

function AboutPage() {
  const [tick, setTick] = React.useState(0);
  React.useEffect(() => {
    const id = setInterval(() => setTick((t) => t + 1), 1000);
    return () => clearInterval(id);
  }, []);
  const now = new Date(2026, 4, 12, 21, 4 + Math.floor(tick/60), tick%60);
  const ts = `${String(now.getHours()).padStart(2,'0')}:${String(now.getMinutes()).padStart(2,'0')}:${String(now.getSeconds()).padStart(2,'0')}`;

  // Mirror the styles object used in variant-dispatch.jsx — kept inline so
  // this file can be imported independently of the home variant.
  const styles = {
    root: { background:"#0a0c1a", color:"#f5f2ea", fontFamily:"'Space Grotesk',system-ui,sans-serif", width:"100%", minHeight:"100%" },
    fullBleed: { position:"relative", overflow:"hidden", borderBottom:"1px solid rgba(245,242,234,0.18)", minHeight:680 },
    fullBleedBg: { position:"absolute", inset:0, backgroundImage:`url(${HERO_BG})`, backgroundSize:"cover", backgroundPosition:"center 40%", filter:"brightness(0.6) saturate(1.1)" },
    fullBleedOverlay: { position:"absolute", inset:0, background:"radial-gradient(ellipse at 30% 50%, rgba(10,12,26,0.55) 0%, rgba(10,12,26,0.9) 100%)", zIndex:1 },
  };

  const STORY = [
    { yr: "2019", title: "Founded · one laptop, one desk.", body: "Started as a freelance practice taking on overflow work from agencies who couldn't ship. First client still on retainer." },
    { yr: "2021", title: "Studio of two.", body: "Brought on a second engineer + a marketer. Stopped doing overflow work; started running engagements end-to-end." },
    { yr: "2023", title: "Marketing arm formalized.", body: "Built our own SEO + content stack. Every project now ships with the broadcast layer included." },
    { yr: "2025", title: "Security practice added.", body: "Pentest, compliance, vulnerability management. We harden what we build — and what other people built." },
    { yr: "2026", title: "120+ projects shipped.", body: "Still small on purpose. Still owned by the client. Still answering email within 24 hours." },
  ];

  const PRINCIPLES = [
    { n: "01", t: "You own everything we build.",  b: "Source, hosting, accounts, documentation. We deliver the keys; we don't hold a copy." },
    { n: "02", t: "Fixed scope, fixed price, fixed date.", b: "We quote in plain English and stick to it. Surprises are our problem, not yours." },
    { n: "03", t: "Build and broadcast together.", b: "Engineering and marketing as one motion. The thing you build has to be found." },
    { n: "04", t: "Quiet enough to run on its own.", b: "Boring stacks. Plain documentation. Software that does not need us standing over it." },
    { n: "05", t: "Small, on purpose.", b: "Three to five engagements at a time. The same hands that quote it ship it." },
  ];

  const TEAM = [
    { name: "M. Reyes",    role: "Founder · Engineering", bio: "15 yrs building boring, durable web software. Reformed agency dev.", hue: 210 },
    { name: "S. Okafor",   role: "Lead Engineer · Mobile", bio: "iOS / Android since the original SDK. Likes Stripe webhooks more than anyone should.", hue: 280 },
    { name: "J. Halloran", role: "Marketing & Growth", bio: "SEO, content, analytics. Treats a content calendar like a deployment pipeline.", hue: 24 },
    { name: "A. Gupta",    role: "Engineering & Cybersecurity", bio: "MS Information Security, Carnegie Mellon · BS CS, Penn State. 6+ yrs in Zero Trust, post-quantum cryptography, and cloud security. CISSP · AWS SAA · eJPT · CMMC · vCISO.", hue: 340 },
    { name: "P. Linde",    role: "Security & Compliance", bio: "OSCP. Has broken more software than most engineers have shipped.", hue: 162 },
  ];

  return (
    <div style={styles.root}>
      <style>{`
        .ds-mono { font-family:'JetBrains Mono',monospace; }
        .ds-eyebrow { font-family:'JetBrains Mono',monospace; font-size:10px; letter-spacing:0.28em; text-transform:uppercase; color:#83A384; }
        .ds-coord { font-family:'JetBrains Mono',monospace; font-size:11px; letter-spacing:0.1em; color:rgba(245,242,234,0.55); }
        .ds-display { font-family:'Fraunces',serif; font-weight:700; color:#f5f2ea; letter-spacing:-0.03em; line-height:0.94; }
        .ds-body { font-family:'Fraunces',serif; font-weight:400; color:rgba(245,242,234,0.78); line-height:1.6; font-size:17px; }
        .ds-link { color:#83A384; text-decoration:none; font-family:'JetBrains Mono',monospace; font-size:11px; letter-spacing:0.22em; text-transform:uppercase; border-bottom:1px solid currentColor; padding-bottom:3px; transition:color .2s; }
        .ds-link:hover { color:#a4c4a5; }
        .ds-btn { display:inline-flex; align-items:center; gap:14px; padding:18px 28px; background:transparent; color:#83A384; border:1px solid #83A384; font-family:'JetBrains Mono',monospace; font-size:11px; letter-spacing:0.24em; text-transform:uppercase; font-weight:500; cursor:pointer; transition:all .2s; }
        .ds-btn:hover { background:#83A384; color:#0a0c1a; }
        .ds-btn-solid { display:inline-flex; align-items:center; gap:14px; padding:18px 28px; background:#83A384; color:#0a0c1a; border:1px solid #83A384; font-family:'JetBrains Mono',monospace; font-size:11px; letter-spacing:0.24em; text-transform:uppercase; font-weight:600; cursor:pointer; transition:background .2s; }
        .ds-btn-solid:hover { background:#a4c4a5; }
        .ds-corner { position:absolute; width:12px; height:12px; border-color:#83A384; }
        .ds-corner-tl { top:-1px; left:-1px; border-top:1px solid; border-left:1px solid; }
        .ds-corner-tr { top:-1px; right:-1px; border-top:1px solid; border-right:1px solid; }
        .ds-corner-bl { bottom:-1px; left:-1px; border-bottom:1px solid; border-left:1px solid; }
        .ds-corner-br { bottom:-1px; right:-1px; border-bottom:1px solid; border-right:1px solid; }
        @keyframes dsTw { 0%,100% { opacity:0.3; } 50% { opacity:1; } }
        @keyframes dsMarquee { from { transform:translateX(0); } to { transform:translateX(-33.33%); } }
      `}</style>

      {/* ═══════════ HEADER — identical to home ═══════════ */}
      <header style={{padding:"24px 56px", display:"flex", justifyContent:"space-between", alignItems:"center", borderBottom:"1px solid rgba(245,242,234,0.18)", position:"relative", zIndex:10, background:"rgba(10,12,26,0.85)", backdropFilter:"blur(8px)"}}>
        <div style={{display:"flex", alignItems:"center", gap:16}}>
          <div style={{width:24, height:24, border:"1px solid #83A384", borderRadius:"50%", position:"relative"}}>
            <div style={{position:"absolute", top:"50%", left:"50%", width:6, height:6, background:"#83A384", borderRadius:"50%", transform:"translate(-50%,-50%)"}}/>
          </div>
          <div style={{fontFamily:"'JetBrains Mono',monospace", fontSize:13, color:"#f5f2ea", letterSpacing:"0.12em"}}>CACTUS_CAT // ABOUT</div>
        </div>
        <nav style={{display:"flex", gap:32, fontFamily:"'JetBrains Mono',monospace", fontSize:11, letterSpacing:"0.18em", textTransform:"uppercase", color:"rgba(245,242,234,0.7)"}}>
          <a href="Home.html" style={{color:"inherit", textDecoration:"none"}}>~/services</a>
          <span>~/work</span>
          <a href="About.html" style={{color:"#83A384", textDecoration:"none"}}>~/about</a>
          <span>~/contact</span>
        </nav>
        <div style={{display:"flex", alignItems:"center", gap:12}}>
          <span style={{width:6, height:6, background:"#83A384", borderRadius:"50%", boxShadow:"0 0 8px #83A384", animation:"dsTw 1.5s infinite"}}/>
          <span className="ds-mono" style={{fontSize:11, color:"#83A384"}}>LIVE · {ts} ET</span>
        </div>
      </header>

      {/* ═══════════ STAR-CHART HERO (lifted from home interlude) ═══════════ */}
      <section style={styles.fullBleed}>
        <div style={styles.fullBleedBg}/>
        <div style={styles.fullBleedOverlay}/>
        <svg viewBox="0 0 1200 600" preserveAspectRatio="xMidYMid slice" style={{position:"absolute", inset:0, width:"100%", height:"100%", zIndex:2, opacity:0.7}}>
          <g stroke="#83A384" strokeWidth="0.5" fill="none">
            <line x1="180" y1="120" x2="280" y2="180"/>
            <line x1="280" y1="180" x2="360" y2="140"/>
            <line x1="360" y1="140" x2="440" y2="220"/>
            <line x1="440" y1="220" x2="520" y2="190"/>
            <line x1="520" y1="190" x2="620" y2="260"/>
            <line x1="780" y1="140" x2="880" y2="180"/>
            <line x1="880" y1="180" x2="960" y2="120"/>
            <line x1="960" y1="120" x2="1040" y2="200"/>
          </g>
          <g fill="#fef6e0">
            {[[180,120],[280,180],[360,140],[440,220],[520,190],[620,260],[780,140],[880,180],[960,120],[1040,200]].map(([x,y],i)=>(
              <circle key={i} cx={x} cy={y} r="3" style={{filter:"drop-shadow(0 0 6px #fff)"}}/>
            ))}
          </g>
          <text x="370" y="100" fill="#83A384" fontFamily="JetBrains Mono" fontSize="10" letterSpacing="3">FELIS CACTUS</text>
        </svg>
        <div style={{position:"relative", zIndex:3, padding:"140px 56px 100px"}}>
          <div style={{display:"flex", alignItems:"center", gap:24, marginBottom:24}}>
            <span className="ds-eyebrow">·· About the studio</span>
            <span style={{width:40, height:1, background:"#83A384"}}/>
            <span className="ds-coord">41°N · 73°W · ELEV 64m</span>
          </div>
          <h1 className="ds-display" style={{fontSize:108, maxWidth:1100, fontWeight:300, fontStyle:"italic"}}>
            <span style={{fontWeight:700, fontStyle:"normal"}}>Built</span> for the night,<br/>
            and the wind, and<br/>
            the long road ahead.
          </h1>
          <div style={{display:"flex", alignItems:"center", gap:18, marginTop:48}}>
            <span style={{width:64, height:1, background:"#83A384"}}/>
            <span className="ds-eyebrow">· Design ethos · printed on every receipt</span>
          </div>
        </div>
      </section>

      {/* ═══════════ MARQUEE (home-matched) ═══════════ */}
      <section style={{padding:"24px 0", background:"#83A384", color:"#0a0c1a", overflow:"hidden", borderTop:"1px solid rgba(245,242,234,0.18)", borderBottom:"1px solid rgba(245,242,234,0.18)"}}>
        <div style={{display:"flex", gap:64, whiteSpace:"nowrap", animation:"dsMarquee 40s linear infinite", fontFamily:"'JetBrains Mono',monospace", fontSize:14, letterSpacing:"0.15em", textTransform:"uppercase", fontWeight:600}}>
          {Array.from({length:3}).flatMap((_,k)=>STATS_STRIP.map((s,i)=>(
            <span key={`${k}-${i}`} style={{display:"inline-flex", alignItems:"center", gap:18}}>
              <span style={{fontFamily:"'Fraunces',serif", fontWeight:700, fontSize:28, letterSpacing:"-0.01em", textTransform:"none"}}>{s.v}</span>
              <span>{s.k}</span>
              <span style={{color:"rgba(10,12,26,0.4)"}}>◆</span>
            </span>
          )))}
        </div>
      </section>

      {/* ═══════════ THE THESIS ═══════════ */}
      <section style={{padding:"112px 56px", background:"#0a0c1a"}}>
        <div style={{display:"grid", gridTemplateColumns:"320px 1fr", gap:80}}>
          <div>
            <div className="ds-eyebrow" style={{marginBottom:14}}>· I / The Thesis</div>
            <div className="ds-coord">2019–present · East Coast, USA</div>
          </div>
          <div style={{maxWidth:880}}>
            <h2 className="ds-display" style={{fontSize:72, marginBottom:36}}>
              We're a small studio that <span style={{fontStyle:"italic", color:"#83A384"}}>builds</span> custom web software and the <span style={{fontStyle:"italic", color:"#83A384"}}>marketing</span> that makes it findable.
            </h2>
            <div style={{display:"grid", gridTemplateColumns:"1fr 1fr", gap:48}}>
              <p className="ds-body" style={{fontSize:19, margin:0}}>
                Most software is rented. Subscriptions, lock-in, black boxes. We don't do that. Every project we ship is owned outright by the client — source, hosting, accounts, the lot. We deliver the keys and step back.
              </p>
              <p className="ds-body" style={{fontSize:19, margin:0}}>
                And we don't stop at the codebase. Half of every engagement is making sure the thing we built can actually be found by the people it's for. Build, then broadcast — one studio, one bill.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* ═══════════ PRINCIPLES — atlas grid (home-matched) ═══════════ */}
      <section style={{padding:"0 56px 112px", background:"#0a0c1a"}}>
        <div style={{display:"flex", justifyContent:"space-between", alignItems:"flex-end", marginBottom:40}}>
          <div>
            <div className="ds-eyebrow" style={{marginBottom:14}}>· II / Operating Principles</div>
            <h2 className="ds-display" style={{fontSize:64}}>Five things we don't compromise on.</h2>
          </div>
          <div className="ds-coord" style={{maxWidth:280}}>· The shortest list we could make it. Each one is a habit, not a hope.</div>
        </div>
        <div style={{display:"grid", gridTemplateColumns:"repeat(6,1fr)", gap:0, border:"1px solid rgba(131,163,132,0.25)"}}>
          {PRINCIPLES.map((p,i)=>(
            <article key={i} style={{
              gridColumn: i<2 ? "span 3" : i<4 ? "span 2" : "span 6",
              padding:"40px 32px",
              borderRight: (i===0 || i===2 || i===3) ? "1px solid rgba(131,163,132,0.25)" : "none",
              borderBottom: i<4 ? "1px solid rgba(131,163,132,0.25)" : "none",
              background: i===4 ? "linear-gradient(90deg, rgba(131,163,132,0.06) 0%, transparent 60%)" : "transparent",
            }}>
              <div style={{display:"flex", justifyContent:"space-between", alignItems:"flex-start", marginBottom:18}}>
                <div className="ds-eyebrow">Principle · {p.n}</div>
                <div className="ds-coord">§ {p.n}</div>
              </div>
              <h3 style={{fontFamily:"'Fraunces',serif", fontSize: i===4 ? 44 : 30, fontWeight:600, color:"#f5f2ea", letterSpacing:"-0.02em", lineHeight:1.05, margin:"0 0 16px", maxWidth: i===4 ? 720 : "auto"}}>
                {p.t}
              </h3>
              <p className="ds-body" style={{fontSize:15, maxWidth: i===4 ? 760 : "auto", margin:0}}>{p.b}</p>
            </article>
          ))}
        </div>
      </section>

      {/* ═══════════ TIMELINE — expedition log shape (home-matched) ═══════════ */}
      <section style={{padding:"112px 56px", background:"#0a0c1a", borderTop:"1px solid rgba(245,242,234,0.18)"}}>
        <div style={{display:"flex", justifyContent:"space-between", alignItems:"flex-end", marginBottom:48}}>
          <div>
            <div className="ds-eyebrow" style={{marginBottom:14}}>· III / Field Log · 2019→</div>
            <h2 className="ds-display" style={{fontSize:72}}>How we got here.</h2>
          </div>
          <div className="ds-coord" style={{maxWidth:280}}>· Five waypoints, seven years.</div>
        </div>
        <div style={{display:"grid", gridTemplateColumns:"100px 1fr", gap:24}}>
          {STORY.map((p,i)=>(
            <React.Fragment key={i}>
              <div style={{padding:"32px 0", borderTop:"1px solid rgba(131,163,132,0.3)", display:"flex", flexDirection:"column", alignItems:"flex-start"}}>
                <div className="ds-eyebrow" style={{marginBottom:8}}>WP {String(i+1).padStart(2,'0')}</div>
                <div style={{fontFamily:"'Fraunces',serif", fontSize:40, fontWeight:300, color:"#83A384", lineHeight:1}}>{p.yr}</div>
                <div style={{width:1, height:24, background:"rgba(131,163,132,0.3)", margin:"12px 0"}}/>
                <div className="ds-mono" style={{fontSize:11, color:"#83A384", letterSpacing:"0.15em"}}>{i === STORY.length-1 ? "PRESENT" : "LOGGED"}</div>
              </div>
              <article style={{padding:"32px 0 40px", borderTop:"1px solid rgba(131,163,132,0.3)"}}>
                <h3 style={{fontFamily:"'Fraunces',serif", fontSize:36, fontWeight:600, color:"#f5f2ea", margin:"0 0 14px", letterSpacing:"-0.015em"}}>{p.title}</h3>
                <p className="ds-body" style={{fontSize:17, margin:0, maxWidth:780}}>{p.body}</p>
              </article>
            </React.Fragment>
          ))}
        </div>
      </section>

      {/* ═══════════ TEAM ═══════════ */}
      <section style={{padding:"112px 56px", background:"#0a0c1a", borderTop:"1px solid rgba(245,242,234,0.18)"}}>
        <div style={{display:"flex", justifyContent:"space-between", alignItems:"flex-end", marginBottom:48}}>
          <div>
            <div className="ds-eyebrow" style={{marginBottom:14}}>· IV / Field Station 01 · Roster</div>
            <h2 className="ds-display" style={{fontSize:72}}>Four hands. <span style={{fontStyle:"italic", color:"#83A384"}}>Same hands</span> that quote it and ship it.</h2>
          </div>
          <div className="ds-coord" style={{maxWidth:280}}>· The same engineer who scopes your project writes the code. No handoffs.</div>
        </div>
        <div style={{display:"grid", gridTemplateColumns:"repeat(4,1fr)", gap:24}}>
          {TEAM.map((m,i)=>(
            <article key={i} style={{position:"relative", border:"1px solid rgba(131,163,132,0.3)", padding:"28px 24px", background:"rgba(245,242,234,0.02)"}}>
              <span className="ds-corner ds-corner-tl"/>
              <span className="ds-corner ds-corner-tr"/>
              <span className="ds-corner ds-corner-bl"/>
              <span className="ds-corner ds-corner-br"/>
              <div style={{
                aspectRatio:"1/1",
                background:`linear-gradient(155deg, oklch(0.50 0.13 ${m.hue}) 0%, oklch(0.20 0.06 ${m.hue}) 100%)`,
                position:"relative", overflow:"hidden", marginBottom:18,
              }}>
                <div style={{position:"absolute", inset:0, backgroundImage:"linear-gradient(90deg, transparent 24px, rgba(0,0,0,0.1) 24px, rgba(0,0,0,0.1) 25px, transparent 25px), linear-gradient(0deg, transparent 24px, rgba(0,0,0,0.1) 24px, rgba(0,0,0,0.1) 25px, transparent 25px)", backgroundSize:"25px 25px"}}/>
                <div style={{position:"absolute", inset:0, display:"flex", alignItems:"center", justifyContent:"center", fontFamily:"'Fraunces',serif", fontStyle:"italic", fontWeight:300, fontSize:64, color:"rgba(245,242,234,0.55)"}}>
                  {m.name.split(" ").map(s=>s[0]).join("")}
                </div>
                <div style={{position:"absolute", top:10, left:10, fontFamily:"'JetBrains Mono',monospace", fontSize:9, letterSpacing:"0.18em", color:"rgba(245,242,234,0.55)"}}>ID · {String(i+1).padStart(3,'0')}</div>
              </div>
              <div className="ds-eyebrow" style={{marginBottom:6}}>{m.role}</div>
              <h3 style={{fontFamily:"'Fraunces',serif", fontSize:26, fontWeight:600, color:"#f5f2ea", margin:"0 0 10px", letterSpacing:"-0.015em"}}>{m.name}</h3>
              <p className="ds-body" style={{fontSize:14, margin:0, color:"rgba(245,242,234,0.7)"}}>{m.bio}</p>
            </article>
          ))}
        </div>
      </section>

      {/* ═══════════ STUDIO / PLACE ═══════════ */}
      <section style={{padding:"112px 56px", background:"#0a0c1a", borderTop:"1px solid rgba(245,242,234,0.18)"}}>
        <div style={{display:"grid", gridTemplateColumns:"1fr 1fr", gap:80, alignItems:"start"}}>
          <div>
            <div className="ds-eyebrow" style={{marginBottom:14}}>· V / The Studio</div>
            <h2 className="ds-display" style={{fontSize:72, marginBottom:32}}>A quiet office on the east coast. Clients on six continents.</h2>
            <p className="ds-body" style={{fontSize:19, marginBottom:24, maxWidth:560}}>
              We work from a small studio in Connecticut. Most clients we never meet in person — we ship through dashboards, weekly preview URLs, and the occasional video call.
            </p>
            <p className="ds-body" style={{fontSize:17, color:"rgba(245,242,234,0.65)", maxWidth:560}}>
              That keeps overhead low and lets us pass the savings through as fixed fees instead of hourly rates that balloon. It also means we can be picky about projects — we take four to five engagements a year and put real care into each one.
            </p>
            <div style={{display:"flex", gap:16, marginTop:40}}>
              <button className="ds-btn-solid">Start a project →</button>
              <a className="ds-btn" href="Home.html">See the work</a>
            </div>
          </div>
          <div style={{position:"relative", border:"1px solid rgba(131,163,132,0.3)", padding:32, background:"rgba(10,12,26,0.5)"}}>
            <span className="ds-corner ds-corner-tl"/>
            <span className="ds-corner ds-corner-tr"/>
            <span className="ds-corner ds-corner-bl"/>
            <span className="ds-corner ds-corner-br"/>
            <div className="ds-eyebrow" style={{marginBottom:18}}>· Field station coordinates</div>
            <div style={{display:"grid", gridTemplateColumns:"1fr 1fr", gap:20, marginBottom:24}}>
              <div>
                <div className="ds-coord" style={{marginBottom:6}}>· Location</div>
                <div style={{fontFamily:"'Fraunces',serif", fontSize:24, color:"#f5f2ea", lineHeight:1.15}}>Connecticut, USA</div>
              </div>
              <div>
                <div className="ds-coord" style={{marginBottom:6}}>· Coordinates</div>
                <div style={{fontFamily:"'JetBrains Mono',monospace", fontSize:18, color:"#83A384"}}>41.05°N<br/>73.54°W</div>
              </div>
              <div>
                <div className="ds-coord" style={{marginBottom:6}}>· Founded</div>
                <div style={{fontFamily:"'Fraunces',serif", fontSize:24, color:"#f5f2ea"}}>2019</div>
              </div>
              <div>
                <div className="ds-coord" style={{marginBottom:6}}>· Headcount</div>
                <div style={{fontFamily:"'Fraunces',serif", fontSize:24, color:"#f5f2ea"}}>4 humans, 1 cat</div>
              </div>
              <div>
                <div className="ds-coord" style={{marginBottom:6}}>· Hours</div>
                <div style={{fontFamily:"'JetBrains Mono',monospace", fontSize:14, color:"#f5f2ea"}}>Mon–Fri · 09:00–18:00 ET</div>
              </div>
              <div>
                <div className="ds-coord" style={{marginBottom:6}}>· Reply window</div>
                <div style={{fontFamily:"'JetBrains Mono',monospace", fontSize:14, color:"#f5f2ea"}}>≤ 24 hours</div>
              </div>
            </div>
            <div style={{padding:"18px 14px", background:"rgba(131,163,132,0.06)", border:"1px dashed rgba(131,163,132,0.3)"}}>
              <div className="ds-eyebrow" style={{marginBottom:6}}>· Tonight's status</div>
              <div style={{fontFamily:"'Fraunces',serif", fontStyle:"italic", fontSize:15, color:"rgba(245,242,234,0.85)", lineHeight:1.5}}>
                Open for 1 new engagement starting June. Two slots reserved for existing clients. Reach out by end of month for a Q3 build.
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ═══════════ FOOTER — identical to home ═══════════ */}
      <footer style={{padding:"32px 56px", background:"#0a0c1a", borderTop:"1px solid rgba(245,242,234,0.18)", display:"flex", justifyContent:"space-between", fontFamily:"'JetBrains Mono',monospace", fontSize:10, letterSpacing:"0.18em", color:"rgba(245,242,234,0.5)", textTransform:"uppercase"}}>
        <span>© MMXXVI · CACTUS CAT SOFTWARE</span>
        <span>END OF DISPATCH · ABOUT PAGE · {ts} ET</span>
        <span>MADE IN USA</span>
      </footer>
    </div>
  );
}

window.AboutPage = AboutPage;
