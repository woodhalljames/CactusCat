// VARIANT A — THE BROADSHEET
// Newspaper / manifesto. Masthead, hairline rules, drop caps, plate numbers.
// Right-side hero panel = "Edition no. / Table of contents / From the desk of"

function VariantBroadsheet() {
  const [cycleIdx, setCycleIdx] = React.useState(0);
  React.useEffect(() => {
    const id = setInterval(() => setCycleIdx((i) => (i + 1) % CYCLE_PHRASES.length), 3200);
    return () => clearInterval(id);
  }, []);

  const today = "May · MMXXVI";

  return (
    <div style={broadsheetStyles.root}>
      <style>{`
        .bs-rule { height:1px; background:rgba(245,242,234,0.25); width:100%; }
        .bs-rule-thick { height:3px; background:#f5f2ea; width:100%; }
        .bs-rule-double { height:6px; border-top:1px solid #f5f2ea; border-bottom:1px solid #f5f2ea; width:100%; }
        .bs-eyebrow { font-family:'JetBrains Mono',monospace; font-size:11px; letter-spacing:0.22em; text-transform:uppercase; color:#83A384; }
        .bs-display { font-family:'Fraunces',serif; font-weight:700; color:#f5f2ea; letter-spacing:-0.025em; line-height:0.92; }
        .bs-body { font-family:'Fraunces',serif; font-weight:400; color:rgba(245,242,234,0.78); line-height:1.55; font-size:16px; }
        .bs-dropcap::first-letter { font-family:'Fraunces',serif; font-weight:700; font-size:5.2em; line-height:0.85; float:left; padding:8px 12px 0 0; color:#83A384; }
        .bs-cycle-word { display:inline-block; transition:transform .55s cubic-bezier(.65,.04,.3,1), opacity .35s; }
        .bs-cycle-out { transform:translateY(-1.05em) skewY(-3deg); opacity:0; }
        .bs-cycle-in { animation: bsIn .55s cubic-bezier(.65,.04,.3,1) both; }
        @keyframes bsIn { from { transform:translateY(1.05em) skewY(3deg); opacity:0; } to { transform:translateY(0) skewY(0); opacity:1; } }
        .bs-toc-item { display:flex; align-items:baseline; gap:8px; padding:14px 0; border-bottom:1px solid rgba(245,242,234,0.12); cursor:pointer; transition:padding-left .25s, color .2s; }
        .bs-toc-item:hover { padding-left:8px; }
        .bs-toc-item:hover .bs-toc-title { color:#83A384; }
        .bs-toc-num { font-family:'JetBrains Mono',monospace; font-size:11px; color:#83A384; min-width:24px; }
        .bs-toc-title { font-family:'Fraunces',serif; font-size:17px; color:#f5f2ea; flex:1; transition:color .2s; }
        .bs-toc-page { font-family:'JetBrains Mono',monospace; font-size:11px; color:rgba(245,242,234,0.5); }
        .bs-toc-dots { flex:1; border-bottom:1px dotted rgba(245,242,234,0.3); margin:0 8px; transform:translateY(-3px); }
        .bs-plate { border:1px solid rgba(245,242,234,0.18); position:relative; }
        .bs-plate::before { content:attr(data-plate); position:absolute; top:-9px; left:16px; padding:0 8px; background:#0a0c1a; font-family:'JetBrains Mono',monospace; font-size:10px; letter-spacing:0.2em; color:#83A384; }
        .bs-pull { font-family:'Fraunces',serif; font-style:italic; font-weight:300; font-size:32px; line-height:1.25; color:#f5f2ea; border-left:2px solid #83A384; padding:8px 0 8px 24px; }
        .bs-tag { font-family:'JetBrains Mono',monospace; font-size:10px; letter-spacing:0.18em; text-transform:uppercase; padding:3px 8px; border:1px solid rgba(131,163,132,0.4); color:#83A384; display:inline-block; }
        .bs-link { color:#f5f2ea; text-decoration:none; border-bottom:1px solid #83A384; padding-bottom:2px; font-family:'JetBrains Mono',monospace; font-size:11px; letter-spacing:0.18em; text-transform:uppercase; transition:color .2s; }
        .bs-link:hover { color:#83A384; }
        .bs-btn-primary { display:inline-flex; align-items:center; gap:12px; background:#83A384; color:#0a0c1a; padding:18px 28px; font-family:'JetBrains Mono',monospace; font-size:12px; letter-spacing:0.22em; text-transform:uppercase; font-weight:600; border:none; cursor:pointer; transition:background .2s; }
        .bs-btn-primary:hover { background:#a4c4a5; }
        .bs-btn-ghost { display:inline-flex; align-items:center; gap:12px; background:transparent; color:#f5f2ea; padding:18px 28px; font-family:'JetBrains Mono',monospace; font-size:12px; letter-spacing:0.22em; text-transform:uppercase; border:1px solid rgba(245,242,234,0.4); cursor:pointer; transition:border-color .2s, color .2s; }
        .bs-btn-ghost:hover { border-color:#83A384; color:#83A384; }
        .bs-stars { position:absolute; inset:0; pointer-events:none; opacity:0.6; }
        .bs-twinkle { position:absolute; width:2px; height:2px; background:#fff; border-radius:50%; box-shadow:0 0 6px #fff; animation: bsTw 3s ease-in-out infinite; }
        @keyframes bsTw { 0%,100% { opacity:0.2; transform:scale(0.8); } 50% { opacity:1; transform:scale(1.2); } }
        .bs-moon { position:absolute; top:80px; right:140px; width:120px; height:120px; border-radius:50%; background:radial-gradient(circle at 35% 35%, #f5f2ea 0%, #e8e4d6 40%, #c9c1ad 70%, transparent 100%); box-shadow:0 0 80px 20px rgba(245,242,234,0.15); }
      `}</style>

      {/* ═══════════ MASTHEAD ═══════════ */}
      <header style={{padding:"24px 56px 0", position:"relative", zIndex:5}}>
        <div style={{display:"flex", justifyContent:"space-between", alignItems:"flex-end", paddingBottom:16}}>
          <div style={{fontFamily:"'JetBrains Mono',monospace", fontSize:11, letterSpacing:"0.18em", color:"rgba(245,242,234,0.7)"}}>
            VOL. XI · NO. 042 · {today}
          </div>
          <div style={{display:"flex", gap:32, fontFamily:"'JetBrains Mono',monospace", fontSize:11, letterSpacing:"0.18em", textTransform:"uppercase", color:"rgba(245,242,234,0.8)"}}>
            <span>Services</span><span>Work</span><span>Process</span><span>Journal</span><span>Contact</span>
          </div>
        </div>
        <div className="bs-rule-double" />
        <div style={{display:"flex", justifyContent:"space-between", alignItems:"baseline", padding:"22px 0 8px"}}>
          <div className="bs-eyebrow">East Coast U.S. — Delivered Worldwide</div>
          <div style={{fontFamily:"'Fraunces',serif", fontStyle:"italic", fontSize:42, fontWeight:300, color:"#f5f2ea", letterSpacing:"-0.02em"}}>
            The Cactus Cat Broadsheet
          </div>
          <div className="bs-eyebrow">Edition price · A handshake</div>
        </div>
        <div className="bs-rule-thick" />
      </header>

      {/* ═══════════ HERO ═══════════ */}
      <section style={broadsheetStyles.hero}>
        <div style={broadsheetStyles.heroBg} />
        <div style={broadsheetStyles.heroGradient} />
        <div className="bs-moon" />
        <div className="bs-stars">
          {Array.from({length:40}).map((_,i)=>(
            <span key={i} className="bs-twinkle" style={{
              left:`${Math.random()*100}%`, top:`${Math.random()*55}%`,
              animationDelay:`${Math.random()*3}s`,
              opacity: Math.random()*0.6+0.2
            }}/>
          ))}
        </div>

        <div style={broadsheetStyles.heroInner}>
          {/* Left: massive headline + cycling */}
          <div style={{flex:"1 1 60%", padding:"56px 40px 56px 56px"}}>
            <div style={{display:"flex", gap:16, alignItems:"center", marginBottom:24}}>
              <span className="bs-tag">Feature</span>
              <span style={{fontFamily:"'JetBrains Mono',monospace", fontSize:10, color:"rgba(245,242,234,0.55)", letterSpacing:"0.15em"}}>
                FILED · 5/12/2026 · 21:04 LOCAL
              </span>
            </div>
            <h1 className="bs-display" style={{fontSize:128, marginBottom:36}}>
              Software<br/>built to<br/>
              <span style={{display:"inline-block", position:"relative", color:"#83A384"}}>
                <span key={cycleIdx} className="bs-cycle-in bs-cycle-word">
                  {CYCLE_PHRASES[cycleIdx]}
                </span>
              </span>
            </h1>
            <div style={{display:"flex", gap:48, maxWidth:680}}>
              <div className="bs-body bs-dropcap" style={{flex:1, fontSize:17}}>
                Custom web applications, SaaS platforms, and digital marketing — engineered from a quiet office on the east coast and shipped to clients on six continents. Lean, sharp, handed to you to own. No subscriptions. No black boxes.
              </div>
              <div style={{flex:"0 0 240px", borderLeft:"1px solid rgba(245,242,234,0.25)", paddingLeft:24}}>
                <div className="bs-eyebrow" style={{marginBottom:10}}>The Thesis</div>
                <div style={{fontFamily:"'Fraunces',serif", fontStyle:"italic", fontSize:18, lineHeight:1.45, color:"rgba(245,242,234,0.9)"}}>
                  "We build software the way it ought to be built — fully owned, plainly understood, and quiet enough to run without us."
                </div>
              </div>
            </div>
            <div style={{display:"flex", gap:16, marginTop:48}}>
              <a className="bs-btn-primary">Commission a project →</a>
              <a className="bs-btn-ghost">Browse the catalog</a>
            </div>
          </div>

          {/* Right: edition panel */}
          <aside style={broadsheetStyles.heroAside}>
            <div className="bs-eyebrow" style={{marginBottom:6}}>In This Edition</div>
            <div style={{fontFamily:"'Fraunces',serif", fontSize:28, color:"#f5f2ea", lineHeight:1.15, marginBottom:24, fontWeight:600}}>
              A working catalog of every service, every method, every receipt.
            </div>
            <div className="bs-rule" style={{marginBottom:8}} />
            {SERVICES.map((s, i) => (
              <div key={i} className="bs-toc-item">
                <span className="bs-toc-num">{s.n}</span>
                <span className="bs-toc-title">{s.kicker}</span>
                <span className="bs-toc-dots" />
                <span className="bs-toc-page">p. {String((i+1)*4).padStart(2,'0')}</span>
              </div>
            ))}
            <div className="bs-toc-item">
              <span className="bs-toc-num">★</span>
              <span className="bs-toc-title" style={{fontStyle:"italic"}}>Selected receipts</span>
              <span className="bs-toc-dots" />
              <span className="bs-toc-page">p. 24</span>
            </div>

            <div style={{marginTop:32, padding:"20px 0", borderTop:"1px solid rgba(245,242,234,0.18)", borderBottom:"1px solid rgba(245,242,234,0.18)"}}>
              <div className="bs-eyebrow" style={{marginBottom:14}}>Tonight's Conditions</div>
              <div style={{display:"grid", gridTemplateColumns:"1fr 1fr", gap:14, fontFamily:"'JetBrains Mono',monospace", fontSize:11, color:"rgba(245,242,234,0.75)"}}>
                <div><div style={{color:"#83A384", fontSize:18, fontFamily:"'Fraunces',serif"}}>4 / 5</div>open commissions</div>
                <div><div style={{color:"#83A384", fontSize:18, fontFamily:"'Fraunces',serif"}}>8 wk</div>avg. turnaround</div>
                <div><div style={{color:"#83A384", fontSize:18, fontFamily:"'Fraunces',serif"}}>94%</div>retention</div>
                <div><div style={{color:"#83A384", fontSize:18, fontFamily:"'Fraunces',serif"}}>$0</div>kept hostage</div>
              </div>
            </div>

            <div style={{marginTop:24}}>
              <div className="bs-eyebrow" style={{marginBottom:10}}>From the Desk Of</div>
              <div style={{fontFamily:"'Fraunces',serif", fontSize:14, lineHeight:1.55, color:"rgba(245,242,234,0.85)", fontStyle:"italic"}}>
                Most software is rented; we believe it should be owned. The catalog inside is a fixed-price, fixed-timeline answer to that idea. Read it as a menu — or as a manifesto.
              </div>
              <div style={{marginTop:14, fontFamily:"'Fraunces',serif", fontStyle:"italic", fontSize:18, color:"#83A384"}}>
                — The editors
              </div>
            </div>
          </aside>
        </div>
      </section>

      {/* ═══════════ STATS STRIP ═══════════ */}
      <section style={{padding:"0 56px", background:"#0a0c1a", position:"relative", zIndex:2}}>
        <div className="bs-rule-thick"/>
        <div style={{display:"grid", gridTemplateColumns:"repeat(4,1fr)", padding:"36px 0"}}>
          {STATS_STRIP.map((s,i)=>(
            <div key={i} style={{padding:"0 24px", borderLeft: i>0 ? "1px solid rgba(245,242,234,0.18)":"none"}}>
              <div className="bs-eyebrow" style={{marginBottom:8}}>{s.k}</div>
              <div style={{fontFamily:"'Fraunces',serif", fontWeight:700, fontSize:48, color:"#f5f2ea", lineHeight:1}}>{s.v}</div>
            </div>
          ))}
        </div>
        <div className="bs-rule"/>
      </section>

      {/* ═══════════ SERVICE COLUMNS ═══════════ */}
      <section style={{padding:"96px 56px", background:"#0a0c1a"}}>
        <div style={{display:"flex", justifyContent:"space-between", alignItems:"flex-end", marginBottom:48}}>
          <div>
            <div className="bs-eyebrow" style={{marginBottom:12}}>Section · The Catalog</div>
            <h2 className="bs-display" style={{fontSize:84}}>The five disciplines.</h2>
          </div>
          <div style={{maxWidth:380, fontFamily:"'Fraunces',serif", fontSize:18, lineHeight:1.55, color:"rgba(245,242,234,0.75)", fontStyle:"italic"}}>
            Each discipline below is sold as a fixed-fee engagement. Mix and match — or hand us the whole stack.
          </div>
        </div>
        <div className="bs-rule-thick" style={{marginBottom:48}}/>

        {SERVICES.slice(0,3).map((s, i) => (
          <article key={i} style={{display:"grid", gridTemplateColumns:"120px 1fr 1fr 280px", gap:40, padding:"40px 0", borderBottom:"1px solid rgba(245,242,234,0.18)"}}>
            <div>
              <div style={{fontFamily:"'Fraunces',serif", fontSize:84, fontWeight:300, color:"#83A384", lineHeight:0.9}}>{s.n}</div>
              <div className="bs-eyebrow" style={{marginTop:8, color:"rgba(245,242,234,0.55)"}}>plate · {String(i+1).padStart(2,'0')}</div>
            </div>
            <div>
              <div className="bs-eyebrow" style={{marginBottom:10}}>{s.kicker}</div>
              <h3 style={{fontFamily:"'Fraunces',serif", fontSize:36, fontWeight:600, color:"#f5f2ea", lineHeight:1.05, letterSpacing:"-0.015em", marginBottom:16}}>{s.title}</h3>
              <p className="bs-body" style={{margin:0, columnCount: i===0?2:1, columnGap:24}}>{s.body}</p>
            </div>
            <div>
              <div className="bs-eyebrow" style={{marginBottom:14}}>Included</div>
              <ul style={{listStyle:"none", padding:0, margin:0}}>
                {s.bullets.map((b, j) => (
                  <li key={j} style={{padding:"10px 0", borderBottom:"1px dotted rgba(245,242,234,0.18)", fontFamily:"'Fraunces',serif", fontSize:16, color:"rgba(245,242,234,0.85)", display:"flex", justifyContent:"space-between"}}>
                    <span>{b}</span>
                    <span style={{color:"#83A384", fontFamily:"'JetBrains Mono',monospace", fontSize:11}}>✓</span>
                  </li>
                ))}
              </ul>
            </div>
            <div style={{display:"flex", flexDirection:"column", justifyContent:"space-between"}}>
              <div className="bs-pull" style={{fontSize:22, padding:"4px 0 4px 20px"}}>
                {i===0 ? "Built once. Owned forever." : i===1 ? "Recurring revenue, single-bill simplicity." : "Found, ranked, converted."}
              </div>
              <a className="bs-link" style={{alignSelf:"flex-start", marginTop:24}}>{s.cta} →</a>
            </div>
          </article>
        ))}
      </section>

      {/* ═══════════ FULL-BLEED DESERT II — Pull Quote ═══════════ */}
      <section style={broadsheetStyles.feature}>
        <div style={broadsheetStyles.featureBg}/>
        <div style={broadsheetStyles.featureOverlay}/>
        <div style={{position:"relative", zIndex:2, padding:"160px 56px", maxWidth:1200}}>
          <div className="bs-eyebrow" style={{marginBottom:24}}>Interlude · Plate VI</div>
          <div style={{fontFamily:"'Fraunces',serif", fontWeight:300, fontStyle:"italic", fontSize:96, lineHeight:1.02, color:"#f5f2ea", letterSpacing:"-0.025em"}}>
            "The desert teaches you to build for the night, and for the wind, and for the people who'll be here long after you've left."
          </div>
          <div style={{display:"flex", alignItems:"center", gap:16, marginTop:48}}>
            <div style={{width:64, height:1, background:"#83A384"}}/>
            <div style={{fontFamily:"'JetBrains Mono',monospace", fontSize:12, letterSpacing:"0.2em", textTransform:"uppercase", color:"#83A384"}}>
              Our design ethos, abbreviated.
            </div>
          </div>
        </div>
      </section>

      {/* ═══════════ REMAINING SERVICES ═══════════ */}
      <section style={{padding:"96px 56px", background:"#0a0c1a"}}>
        {SERVICES.slice(3).map((s, i) => (
          <article key={i} style={{display:"grid", gridTemplateColumns:"120px 1fr 1fr 280px", gap:40, padding:"40px 0", borderBottom:"1px solid rgba(245,242,234,0.18)"}}>
            <div>
              <div style={{fontFamily:"'Fraunces',serif", fontSize:84, fontWeight:300, color:"#83A384", lineHeight:0.9}}>{s.n}</div>
              <div className="bs-eyebrow" style={{marginTop:8, color:"rgba(245,242,234,0.55)"}}>plate · {String(i+4).padStart(2,'0')}</div>
            </div>
            <div>
              <div className="bs-eyebrow" style={{marginBottom:10}}>{s.kicker}</div>
              <h3 style={{fontFamily:"'Fraunces',serif", fontSize:36, fontWeight:600, color:"#f5f2ea", lineHeight:1.05, letterSpacing:"-0.015em", marginBottom:16}}>{s.title}</h3>
              <p className="bs-body" style={{margin:0}}>{s.body}</p>
            </div>
            <div>
              <div className="bs-eyebrow" style={{marginBottom:14}}>Included</div>
              <ul style={{listStyle:"none", padding:0, margin:0}}>
                {s.bullets.map((b, j) => (
                  <li key={j} style={{padding:"10px 0", borderBottom:"1px dotted rgba(245,242,234,0.18)", fontFamily:"'Fraunces',serif", fontSize:16, color:"rgba(245,242,234,0.85)", display:"flex", justifyContent:"space-between"}}>
                    <span>{b}</span>
                    <span style={{color:"#83A384", fontFamily:"'JetBrains Mono',monospace", fontSize:11}}>✓</span>
                  </li>
                ))}
              </ul>
            </div>
            <div style={{display:"flex", flexDirection:"column", justifyContent:"space-between"}}>
              <div className="bs-pull" style={{fontSize:22, padding:"4px 0 4px 20px"}}>
                {i===0 ? "Hardened before they find the cracks." : "No black boxes. No surprise invoices."}
              </div>
              <a className="bs-link" style={{alignSelf:"flex-start", marginTop:24}}>{s.cta} →</a>
            </div>
          </article>
        ))}
      </section>

      {/* ═══════════ PROOF OF WORK · RECEIPTS ═══════════ */}
      <section style={{padding:"96px 56px 80px", background:"#0a0c1a", borderTop:"3px solid #f5f2ea"}}>
        <div style={{display:"flex", justifyContent:"space-between", alignItems:"flex-end", marginBottom:48}}>
          <div>
            <div className="bs-eyebrow" style={{marginBottom:12}}>Section · Selected Receipts</div>
            <h2 className="bs-display" style={{fontSize:84}}>The work, on the record.</h2>
          </div>
          <div style={{maxWidth:340, fontFamily:"'Fraunces',serif", fontSize:18, lineHeight:1.55, color:"rgba(245,242,234,0.75)", fontStyle:"italic"}}>
            Four engagements, four very different briefs. All shipped, all owned by their clients.
          </div>
        </div>

        <div style={{display:"grid", gridTemplateColumns:"repeat(2,1fr)", gap:32}}>
          {PROOF.map((p, i) => (
            <article key={i} className="bs-plate" data-plate={`PLATE · ${String(i+1).padStart(2,'0')}`} style={{padding:"40px 32px 32px", background:"rgba(245,242,234,0.02)"}}>
              {/* Image placeholder */}
              <div style={{
                aspectRatio:"16/9",
                background:`linear-gradient(135deg, oklch(0.55 0.12 ${p.hue}) 0%, oklch(0.25 0.08 ${p.hue}) 100%)`,
                marginBottom:24, position:"relative", overflow:"hidden"
              }}>
                <div style={{position:"absolute", inset:0, backgroundImage:"repeating-linear-gradient(90deg, transparent 0 22px, rgba(0,0,0,0.08) 22px 23px)"}}/>
                <div style={{position:"absolute", bottom:16, left:16, fontFamily:"'JetBrains Mono',monospace", fontSize:10, letterSpacing:"0.2em", color:"rgba(245,242,234,0.7)"}}>
                  {p.name.toUpperCase()} · SCREEN GRAB · 01/03
                </div>
              </div>
              <div style={{display:"flex", justifyContent:"space-between", alignItems:"baseline", marginBottom:8}}>
                <span className="bs-tag">{p.tag}</span>
                <span style={{fontFamily:"'JetBrains Mono',monospace", fontSize:10, color:"rgba(245,242,234,0.5)", letterSpacing:"0.15em"}}>RECEIPT №{String(i+1).padStart(3,'0')}</span>
              </div>
              <h3 style={{fontFamily:"'Fraunces',serif", fontSize:32, fontWeight:700, color:"#f5f2ea", margin:"6px 0 10px", letterSpacing:"-0.015em"}}>{p.name}</h3>
              <p className="bs-body" style={{fontSize:15, margin:"0 0 20px"}}>{p.blurb}</p>
              <div style={{display:"flex", gap:24, padding:"16px 0", borderTop:"1px solid rgba(245,242,234,0.15)", borderBottom:"1px solid rgba(245,242,234,0.15)"}}>
                {p.metrics.map((m,j)=>(
                  <div key={j}>
                    <div style={{fontFamily:"'Fraunces',serif", fontSize:24, fontWeight:600, color:"#83A384", lineHeight:1}}>{m.v}</div>
                    <div className="bs-eyebrow" style={{fontSize:9, marginTop:4}}>{m.k}</div>
                  </div>
                ))}
              </div>
              <div style={{display:"flex", gap:8, flexWrap:"wrap", marginTop:16}}>
                {p.stack.map((t,j)=>(
                  <span key={j} style={{fontFamily:"'JetBrains Mono',monospace", fontSize:10, padding:"3px 8px", border:"1px solid rgba(245,242,234,0.2)", color:"rgba(245,242,234,0.7)", letterSpacing:"0.1em"}}>{t}</span>
                ))}
              </div>
            </article>
          ))}
        </div>
      </section>

      {/* ═══════════ FAQ + CTA · CLASSIFIEDS ═══════════ */}
      <section style={{padding:"80px 56px 96px", background:"#0a0c1a"}}>
        <div className="bs-rule-thick" style={{marginBottom:48}}/>
        <div style={{display:"grid", gridTemplateColumns:"1fr 1fr", gap:80}}>
          <div>
            <div className="bs-eyebrow" style={{marginBottom:14}}>Letters · F.A.Q.</div>
            <h2 className="bs-display" style={{fontSize:56, marginBottom:32}}>Common questions, plainly answered.</h2>
            {FAQ.map((f,i)=>(
              <div key={i} style={{padding:"24px 0", borderTop:"1px solid rgba(245,242,234,0.18)"}}>
                <div style={{fontFamily:"'Fraunces',serif", fontSize:22, fontWeight:600, color:"#f5f2ea", marginBottom:8}}>{f.q}</div>
                <div className="bs-body" style={{margin:0}}>{f.a}</div>
              </div>
            ))}
          </div>
          <div>
            <div className="bs-eyebrow" style={{marginBottom:14}}>Classifieds · For Hire</div>
            <h2 className="bs-display" style={{fontSize:56, marginBottom:24, fontStyle:"italic", fontWeight:300}}>
              Have something to build?
            </h2>
            <p className="bs-body" style={{fontSize:18, marginBottom:36}}>
              Tell us what you need in a sentence. We'll reply within a day with a fixed scope, fixed price, and a fixed date you can put on the calendar.
            </p>
            <div style={{display:"flex", flexDirection:"column", gap:16, marginBottom:36}}>
              <a className="bs-btn-primary" style={{justifyContent:"space-between"}}>Start a project<span>→</span></a>
              <a className="bs-btn-ghost" style={{justifyContent:"space-between"}}>hello@cactuscatsoftware.com<span>↗</span></a>
            </div>
            <div style={{padding:"24px 0", borderTop:"1px solid rgba(245,242,234,0.18)", borderBottom:"1px solid rgba(245,242,234,0.18)", display:"grid", gridTemplateColumns:"1fr 1fr 1fr", gap:24, fontFamily:"'JetBrains Mono',monospace", fontSize:11, color:"rgba(245,242,234,0.7)"}}>
              <div><div style={{color:"#83A384", fontFamily:"'Fraunces',serif", fontSize:24}}>Mon–Fri</div>9–6 ET</div>
              <div><div style={{color:"#83A384", fontFamily:"'Fraunces',serif", fontSize:24}}>24h</div>reply time</div>
              <div><div style={{color:"#83A384", fontFamily:"'Fraunces',serif", fontSize:24}}>USA</div>made &amp; based</div>
            </div>
          </div>
        </div>
      </section>

      {/* ═══════════ COLOPHON ═══════════ */}
      <footer style={{padding:"40px 56px", background:"#0a0c1a", borderTop:"6px double rgba(245,242,234,0.3)"}}>
        <div style={{display:"flex", justifyContent:"space-between", alignItems:"center", fontFamily:"'JetBrains Mono',monospace", fontSize:10, letterSpacing:"0.18em", textTransform:"uppercase", color:"rgba(245,242,234,0.55)"}}>
          <span>© MMXXVI Cactus Cat Software · Made in USA</span>
          <span style={{fontFamily:"'Fraunces',serif", fontStyle:"italic", fontSize:18, textTransform:"none", letterSpacing:0, color:"rgba(245,242,234,0.7)"}}>Go-to people for all things web.</span>
          <span>Set in Fraunces &amp; JetBrains Mono</span>
        </div>
      </footer>

    </div>
  );
}

const broadsheetStyles = {
  root: { background:"#0a0c1a", color:"#f5f2ea", fontFamily:"'Space Grotesk',system-ui,sans-serif", width:"100%", minHeight:"100%" },
  hero: { position:"relative", overflow:"hidden", borderTop:"1px solid rgba(245,242,234,0.25)" },
  heroBg: { position:"absolute", inset:0, backgroundImage:`url(${HERO_BG})`, backgroundSize:"cover", backgroundPosition:"center top", opacity:0.55 },
  heroGradient: { position:"absolute", inset:0, background:"linear-gradient(180deg, rgba(10,12,26,0.2) 0%, rgba(10,12,26,0.5) 50%, rgba(10,12,26,0.95) 100%)" },
  heroInner: { position:"relative", zIndex:3, display:"flex", minHeight:760 },
  heroAside: { flex:"0 0 380px", padding:"56px 56px 56px 40px", borderLeft:"1px solid rgba(245,242,234,0.25)", background:"rgba(10,12,26,0.55)", backdropFilter:"blur(2px)" },
  feature: { position:"relative", overflow:"hidden", borderTop:"1px solid rgba(245,242,234,0.25)", borderBottom:"1px solid rgba(245,242,234,0.25)" },
  featureBg: { position:"absolute", inset:0, backgroundImage:`url(${HERO_BG})`, backgroundSize:"cover", backgroundPosition:"center 35%", opacity:0.65, filter:"hue-rotate(-15deg) saturate(1.1)" },
  featureOverlay: { position:"absolute", inset:0, background:"linear-gradient(90deg, rgba(10,12,26,0.85) 0%, rgba(10,12,26,0.4) 70%, rgba(10,12,26,0.2) 100%)" },
};

window.VariantBroadsheet = VariantBroadsheet;
