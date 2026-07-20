// VARIANT C — THE DISPATCH
// Field-explorer's atlas / dispatch log. Coordinates, timestamps, marginalia.
// Right-side hero panel = live dispatch log with telemetry, observations, route.

function VariantDispatch() {
  const [cycleIdx, setCycleIdx] = React.useState(0);
  React.useEffect(() => {
    const id = setInterval(() => setCycleIdx((i) => (i + 1) % CYCLE_PHRASES.length), 3000);
    return () => clearInterval(id);
  }, []);

  const [tick, setTick] = React.useState(0);
  React.useEffect(() => {
    const id = setInterval(() => setTick((t) => t + 1), 1000);
    return () => clearInterval(id);
  }, []);

  const now = new Date(2026, 4, 12, 21, 4 + Math.floor(tick/60), tick%60);
  const ts = `${String(now.getHours()).padStart(2,'0')}:${String(now.getMinutes()).padStart(2,'0')}:${String(now.getSeconds()).padStart(2,'0')}`;

  return (
    <div style={dispStyles.root}>
      <style>{`
        .ds-mono { font-family:'JetBrains Mono',monospace; }
        .ds-eyebrow { font-family:'JetBrains Mono',monospace; font-size:10px; letter-spacing:0.28em; text-transform:uppercase; color:#83A384; }
        .ds-coord { font-family:'JetBrains Mono',monospace; font-size:11px; letter-spacing:0.1em; color:rgba(245,242,234,0.55); }
        .ds-display { font-family:'Fraunces',serif; font-weight:700; color:#f5f2ea; letter-spacing:-0.03em; line-height:0.94; }
        .ds-body { font-family:'Fraunces',serif; font-weight:400; color:rgba(245,242,234,0.78); line-height:1.6; font-size:17px; }
        .ds-cycle-out { transform:translateY(-100%); opacity:0; }
        .ds-cycle-in { animation: dsRoll .6s cubic-bezier(.65,.04,.3,1) both; }
        @keyframes dsRoll { from { transform:translateY(100%); opacity:0; } to { transform:translateY(0); opacity:1; } }
        .ds-cycle-mask { display:inline-block; overflow:hidden; height:1em; vertical-align:bottom; position:relative; }
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
        .ds-topo { position:absolute; inset:0; opacity:0.08; pointer-events:none;
          background-image:
            radial-gradient(ellipse 600px 200px at 20% 30%, transparent 0%, transparent 30%, rgba(131,163,132,0.5) 31%, rgba(131,163,132,0.5) 32%, transparent 33%),
            radial-gradient(ellipse 600px 200px at 20% 30%, transparent 0%, transparent 45%, rgba(131,163,132,0.5) 46%, rgba(131,163,132,0.5) 47%, transparent 48%),
            radial-gradient(ellipse 600px 200px at 20% 30%, transparent 0%, transparent 60%, rgba(131,163,132,0.5) 61%, rgba(131,163,132,0.5) 62%, transparent 63%),
            radial-gradient(ellipse 800px 250px at 80% 70%, transparent 0%, transparent 30%, rgba(131,163,132,0.5) 31%, rgba(131,163,132,0.5) 32%, transparent 33%),
            radial-gradient(ellipse 800px 250px at 80% 70%, transparent 0%, transparent 50%, rgba(131,163,132,0.5) 51%, rgba(131,163,132,0.5) 52%, transparent 53%);
        }
        .ds-stars { position:absolute; inset:0; pointer-events:none; }
        .ds-star { position:absolute; background:#fff; border-radius:50%; }
        @keyframes dsTw { 0%,100% { opacity:0.3; } 50% { opacity:1; } }
        .ds-moon-c { position:absolute; top:90px; right:120px; width:140px; height:140px; border-radius:50%; background:radial-gradient(circle at 35% 35%, #fef6e0 0%, #ede2bf 35%, #c5b88a 70%, transparent 100%); box-shadow:0 0 90px 30px rgba(254,246,224,0.18); }
        .ds-tick { font-family:'JetBrains Mono',monospace; font-size:11px; color:#83A384; }
        .ds-compass { width:80px; height:80px; border:1px solid rgba(131,163,132,0.4); border-radius:50%; position:relative; }
        .ds-compass::before { content:'N'; position:absolute; top:4px; left:50%; transform:translateX(-50%); font-family:'JetBrains Mono',monospace; font-size:10px; color:#83A384; }
        .ds-compass::after { content:''; position:absolute; top:10%; left:50%; width:1px; height:40%; background:linear-gradient(to bottom, #83A384, transparent); transform:translateX(-50%); }
        .ds-log-line { display:grid; grid-template-columns:80px 14px 1fr; gap:10px; padding:9px 0; border-bottom:1px dotted rgba(245,242,234,0.12); font-family:'JetBrains Mono',monospace; font-size:11px; color:rgba(245,242,234,0.78); }
        .ds-log-line .ts { color:#83A384; }
        .ds-log-line .lvl { color:rgba(245,242,234,0.5); }
      `}</style>

      {/* ═══════════ HEADER ═══════════ */}
      <header style={{padding:"24px 56px", display:"flex", justifyContent:"space-between", alignItems:"center", borderBottom:"1px solid rgba(245,242,234,0.18)", position:"relative", zIndex:10, background:"rgba(10,12,26,0.85)", backdropFilter:"blur(8px)"}}>
        <div style={{display:"flex", alignItems:"center", gap:16}}>
          <div style={{width:24, height:24, border:"1px solid #83A384", borderRadius:"50%", position:"relative"}}>
            <div style={{position:"absolute", top:"50%", left:"50%", width:6, height:6, background:"#83A384", borderRadius:"50%", transform:"translate(-50%,-50%)"}}/>
          </div>
          <div style={{fontFamily:"'JetBrains Mono',monospace", fontSize:13, color:"#f5f2ea", letterSpacing:"0.12em"}}>CACTUS_CAT // DISPATCH</div>
        </div>
        <nav style={{display:"flex", gap:32, fontFamily:"'JetBrains Mono',monospace", fontSize:11, letterSpacing:"0.18em", textTransform:"uppercase", color:"rgba(245,242,234,0.7)"}}>
          <span>~/services</span><span>~/work</span><span>~/journal</span><span>~/contact</span>
        </nav>
        <div style={{display:"flex", alignItems:"center", gap:12}}>
          <span style={{width:6, height:6, background:"#83A384", borderRadius:"50%", boxShadow:"0 0 8px #83A384", animation:"dsTw 1.5s infinite"}}/>
          <span className="ds-mono" style={{fontSize:11, color:"#83A384"}}>LIVE · {ts} ET</span>
        </div>
      </header>

      {/* ═══════════ HERO ═══════════ */}
      <section style={dispStyles.hero}>
        <div style={dispStyles.heroBg}/>
        <div style={dispStyles.heroOverlay}/>
        <div className="ds-moon-c"/>
        <div className="ds-stars">
          {Array.from({length:80}).map((_,i)=>{
            const s = Math.random()*2.5+0.5;
            return <span key={i} className="ds-star" style={{
              left:`${Math.random()*100}%`, top:`${Math.random()*65}%`,
              width:s, height:s, opacity:Math.random()*0.7+0.3,
              boxShadow: s>2 ? `0 0 ${s*3}px #fff` : "none",
              animation: `dsTw ${1.5+Math.random()*3}s ease-in-out ${Math.random()*3}s infinite`
            }}/>
          })}
        </div>

        <div style={dispStyles.heroInner}>
          {/* Left */}
          <div style={{flex:"1 1 60%", padding:"60px 40px 80px 56px"}}>
            <div style={{display:"flex", alignItems:"center", gap:24, marginBottom:32}}>
              <span className="ds-eyebrow">·· Dispatch №042</span>
              <span style={{width:40, height:1, background:"#83A384"}}/>
              <span className="ds-coord">41°N · 73°W · ELEV 64m</span>
              <span className="ds-coord">/ FIELD ENTRY · 2026.05.12 / 21:04 ET</span>
            </div>

            <h1 className="ds-display" style={{fontSize:124, marginBottom:24}}>
              Software<br/>
              built to
            </h1>
            <div style={{fontSize:124, fontFamily:"'Fraunces',serif", fontWeight:700, lineHeight:0.94, letterSpacing:"-0.03em", color:"#83A384", overflow:"hidden", height:"1em", position:"relative", display:"inline-block"}}>
              <div key={cycleIdx} className="ds-cycle-in" style={{display:"inline-block"}}>
                {CYCLE_PHRASES[cycleIdx]}
              </div>
            </div>

            <div style={{display:"grid", gridTemplateColumns:"1fr 1fr", gap:40, marginTop:56, maxWidth:760}}>
              <div>
                <div className="ds-eyebrow" style={{marginBottom:10}}>· Brief</div>
                <p className="ds-body" style={{margin:0}}>
                  A small east-coast studio that ships <strong style={{color:"#f5f2ea", fontWeight:600}}>custom web software</strong> and the <strong style={{color:"#f5f2ea", fontWeight:600}}>digital marketing</strong> that makes it findable. Owned by you, documented in plain English, quiet enough to run on its own.
                </p>
              </div>
              <div>
                <div className="ds-eyebrow" style={{marginBottom:10}}>· Operational scope</div>
                <div style={{display:"grid", gap:6}}>
                  {["Web apps · SaaS · mobile","SEO · content · social","Cybersecurity & audits","Live project dashboards"].map((s,i)=>(
                    <div key={i} className="ds-mono" style={{fontSize:12, color:"rgba(245,242,234,0.78)", display:"flex", alignItems:"center", gap:10}}>
                      <span style={{color:"#83A384"}}>▸</span> {s}
                    </div>
                  ))}
                </div>
              </div>
            </div>

            <div style={{display:"flex", gap:16, marginTop:56}}>
              <button className="ds-btn-solid">Open a commission →</button>
              <button className="ds-btn">View the catalog</button>
            </div>
          </div>

          {/* Right: live dispatch panel */}
          <aside style={dispStyles.heroAside}>
            <div style={{position:"relative", border:"1px solid rgba(131,163,132,0.3)", padding:"24px 22px", background:"rgba(10,12,26,0.7)", backdropFilter:"blur(6px)"}}>
              <span className="ds-corner ds-corner-tl"/>
              <span className="ds-corner ds-corner-tr"/>
              <span className="ds-corner ds-corner-bl"/>
              <span className="ds-corner ds-corner-br"/>

              <div style={{display:"flex", justifyContent:"space-between", alignItems:"flex-start", marginBottom:18}}>
                <div>
                  <div className="ds-eyebrow">Live · Studio Status</div>
                  <div style={{fontFamily:"'Fraunces',serif", fontSize:24, fontWeight:600, color:"#f5f2ea", marginTop:6, letterSpacing:"-0.01em"}}>Tonight in the studio</div>
                </div>
                <div className="ds-compass"/>
              </div>

              <div style={{display:"grid", gridTemplateColumns:"1fr 1fr", gap:14, marginBottom:18, padding:"14px 0", borderTop:"1px solid rgba(245,242,234,0.12)", borderBottom:"1px solid rgba(245,242,234,0.12)"}}>
                <div>
                  <div className="ds-eyebrow" style={{fontSize:9}}>Open slots</div>
                  <div style={{fontFamily:"'Fraunces',serif", fontSize:32, fontWeight:600, color:"#83A384", lineHeight:1}}>4 / 5</div>
                </div>
                <div>
                  <div className="ds-eyebrow" style={{fontSize:9}}>Next start</div>
                  <div style={{fontFamily:"'Fraunces',serif", fontSize:32, fontWeight:600, color:"#83A384", lineHeight:1}}>Jun 03</div>
                </div>
                <div>
                  <div className="ds-eyebrow" style={{fontSize:9}}>Avg. build</div>
                  <div style={{fontFamily:"'Fraunces',serif", fontSize:22, fontWeight:600, color:"#f5f2ea", lineHeight:1}}>8 wk</div>
                </div>
                <div>
                  <div className="ds-eyebrow" style={{fontSize:9}}>Reply window</div>
                  <div style={{fontFamily:"'Fraunces',serif", fontSize:22, fontWeight:600, color:"#f5f2ea", lineHeight:1}}>≤ 24 h</div>
                </div>
              </div>

              <div className="ds-eyebrow" style={{marginBottom:8}}>· Recent log</div>
              <div className="ds-log-line"><span className="ts">21:04</span><span className="lvl">✓</span><span>Deploy <em style={{color:"#83A384",fontStyle:"normal"}}>routesentry</em> · build #214 passed</span></div>
              <div className="ds-log-line"><span className="ts">20:47</span><span className="lvl">✓</span><span>Preview URL refreshed for <em style={{color:"#83A384",fontStyle:"normal"}}>mesaverde</em></span></div>
              <div className="ds-log-line"><span className="ts">19:18</span><span className="lvl">★</span><span>New brief · landing page + SEO migration</span></div>
              <div className="ds-log-line"><span className="ts">18:02</span><span className="lvl">✓</span><span>Pentest report delivered · client.app · grade A+</span></div>
              <div className="ds-log-line"><span className="ts">17:30</span><span className="lvl">⚑</span><span>Milestone 02 signed off by <em style={{color:"#83A384",fontStyle:"normal"}}>dreamwed</em></span></div>

              <div style={{marginTop:18, padding:"14px 12px", background:"rgba(131,163,132,0.06)", border:"1px dashed rgba(131,163,132,0.3)"}}>
                <div className="ds-eyebrow" style={{marginBottom:6}}>· Tonight's note</div>
                <div style={{fontFamily:"'Fraunces',serif", fontStyle:"italic", fontSize:14, color:"rgba(245,242,234,0.85)", lineHeight:1.5}}>
                  Build twice, sleep once. The desert sky is what we work toward.
                </div>
              </div>
            </div>

            <div style={{marginTop:24, fontFamily:"'JetBrains Mono',monospace", fontSize:10, color:"rgba(245,242,234,0.45)", letterSpacing:"0.18em", textAlign:"right"}}>
              CCS // FIELD STATION 01 — END TRANSMISSION
            </div>
          </aside>
        </div>
      </section>

      {/* ═══════════ MARQUEE STATS ═══════════ */}
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
        <style>{`@keyframes dsMarquee { from { transform:translateX(0); } to { transform:translateX(-33.33%); } }`}</style>
      </section>

      {/* ═══════════ SERVICES · ATLAS PAGES ═══════════ */}
      <section style={{padding:"96px 56px 56px", background:"#0a0c1a", position:"relative"}}>
        <div className="ds-topo"/>
        <div style={{position:"relative", zIndex:1}}>
          <div style={{display:"flex", justifyContent:"space-between", alignItems:"flex-end", marginBottom:56}}>
            <div>
              <div className="ds-eyebrow" style={{marginBottom:14}}>· II / The Catalog</div>
              <h2 className="ds-display" style={{fontSize:96, maxWidth:1000}}>
                Five disciplines.<br/>One studio.
              </h2>
            </div>
            <div style={{maxWidth:340}}>
              <div className="ds-coord" style={{marginBottom:8}}>· 41.1°N · 73.2°W</div>
              <p className="ds-body" style={{fontSize:17}}>Each discipline is sold as a fixed-fee, fixed-timeline engagement. Take one; take the whole stack.</p>
            </div>
          </div>

          <div style={{display:"grid", gridTemplateColumns:"repeat(6,1fr)", gap:0, border:"1px solid rgba(131,163,132,0.25)"}}>
            {SERVICES.map((s,i)=>(
              <article key={i} style={{
                gridColumn: i<2 ? "span 3" : i<4 ? "span 2" : "span 6",
                padding:"40px 32px",
                borderRight: (i===0 || i===2 || i===3) ? "1px solid rgba(131,163,132,0.25)" : "none",
                borderBottom: i<4 ? "1px solid rgba(131,163,132,0.25)" : "none",
                position:"relative",
                background: i===4 ? "linear-gradient(90deg, rgba(131,163,132,0.06) 0%, transparent 60%)" : "transparent",
              }}>
                <div style={{display:"flex", justifyContent:"space-between", alignItems:"flex-start", marginBottom:18}}>
                  <div className="ds-eyebrow">{s.kicker}</div>
                  <div className="ds-coord">§ {s.n}</div>
                </div>
                <h3 style={{fontFamily:"'Fraunces',serif", fontSize: i===4 ? 48 : 34, fontWeight:600, color:"#f5f2ea", letterSpacing:"-0.02em", lineHeight:1.05, margin:"0 0 18px", maxWidth: i===4 ? 720 : "auto"}}>
                  {s.title}
                </h3>
                <p className="ds-body" style={{fontSize:15, maxWidth: i===4 ? 760 : "auto", margin:"0 0 22px"}}>{s.body}</p>
                <div style={{display:"flex", flexWrap:"wrap", gap:8, marginBottom:24}}>
                  {s.bullets.map((b,j)=>(
                    <span key={j} className="ds-mono" style={{fontSize:10, padding:"4px 10px", border:"1px solid rgba(131,163,132,0.3)", color:"rgba(245,242,234,0.8)", letterSpacing:"0.12em", textTransform:"uppercase"}}>{b}</span>
                  ))}
                </div>
                <a className="ds-link">{s.cta} →</a>
              </article>
            ))}
          </div>
        </div>
      </section>

      {/* Star-chart interlude moved → about-header-snippet.jsx (lifted to About page header). */}

      {/* ═══════════ PROOF · EXPEDITION LOG ═══════════ */}
      <section style={{padding:"96px 56px", background:"#0a0c1a"}}>
        <div style={{display:"flex", justifyContent:"space-between", alignItems:"flex-end", marginBottom:48}}>
          <div>
            <div className="ds-eyebrow" style={{marginBottom:14}}>· IV / Expedition Log</div>
            <h2 className="ds-display" style={{fontSize:88}}>Selected work, on the record.</h2>
          </div>
          <div className="ds-coord" style={{maxWidth:280}}>· Four engagements, four briefs. All shipped, all owned by their clients.</div>
        </div>

        <div style={{display:"grid", gridTemplateColumns:"100px 1fr", gap:24}}>
          {PROOF.map((p,i)=>(
            <React.Fragment key={i}>
              <div style={{padding:"32px 0", borderTop:"1px solid rgba(131,163,132,0.3)", display:"flex", flexDirection:"column", alignItems:"flex-start"}}>
                <div className="ds-eyebrow" style={{marginBottom:8}}>№ {String(i+1).padStart(3,'0')}</div>
                <div className="ds-coord">2026.0{i+1}</div>
                <div style={{width:1, height:32, background:"rgba(131,163,132,0.3)", margin:"16px 0"}}/>
                <div className="ds-coord" style={{fontSize:9}}>STATUS</div>
                <div className="ds-mono" style={{fontSize:11, color:"#83A384", marginTop:4, letterSpacing:"0.15em"}}>SHIPPED ✓</div>
              </div>
              <article style={{padding:"32px 0", borderTop:"1px solid rgba(131,163,132,0.3)", display:"grid", gridTemplateColumns:"320px 1fr", gap:40, alignItems:"start"}}>
                <div style={{
                  aspectRatio:"4/3",
                  background:`linear-gradient(155deg, oklch(0.52 0.13 ${p.hue}) 0%, oklch(0.20 0.06 ${p.hue}) 100%)`,
                  position:"relative", overflow:"hidden",
                }}>
                  <div style={{position:"absolute", inset:0, backgroundImage:"linear-gradient(90deg, transparent 24px, rgba(0,0,0,0.1) 24px, rgba(0,0,0,0.1) 25px, transparent 25px), linear-gradient(0deg, transparent 24px, rgba(0,0,0,0.1) 24px, rgba(0,0,0,0.1) 25px, transparent 25px)", backgroundSize:"25px 25px"}}/>
                  <div style={{position:"absolute", top:12, left:12, fontFamily:"'JetBrains Mono',monospace", fontSize:9, color:"rgba(245,242,234,0.5)", letterSpacing:"0.18em"}}>FIELD CAPTURE</div>
                  <div style={{position:"absolute", bottom:12, right:12, fontFamily:"'JetBrains Mono',monospace", fontSize:9, color:"rgba(245,242,234,0.5)", letterSpacing:"0.18em"}}>{String(i+1).padStart(2,'0')} / {String(PROOF.length).padStart(2,'0')}</div>
                </div>
                <div>
                  <div style={{display:"flex", alignItems:"center", gap:12, marginBottom:14}}>
                    <span className="ds-eyebrow">{p.tag}</span>
                    <span style={{width:24, height:1, background:"rgba(131,163,132,0.4)"}}/>
                    <span className="ds-coord">est. read · 90s</span>
                  </div>
                  <h3 style={{fontFamily:"'Fraunces',serif", fontSize:44, fontWeight:700, color:"#f5f2ea", margin:"0 0 12px", letterSpacing:"-0.02em"}}>{p.name}</h3>
                  <p className="ds-body" style={{fontSize:17, marginBottom:24, maxWidth:520}}>{p.blurb}</p>
                  <div style={{display:"flex", gap:28, padding:"16px 0", borderTop:"1px solid rgba(131,163,132,0.2)", borderBottom:"1px solid rgba(131,163,132,0.2)"}}>
                    {p.metrics.map((m,j)=>(
                      <div key={j}>
                        <div style={{fontFamily:"'Fraunces',serif", fontSize:28, fontWeight:600, color:"#83A384", lineHeight:1}}>{m.v}</div>
                        <div className="ds-eyebrow" style={{fontSize:9, marginTop:6}}>{m.k}</div>
                      </div>
                    ))}
                    <div style={{flex:1, textAlign:"right", alignSelf:"end"}}>
                      <div className="ds-coord" style={{marginBottom:6}}>· stack</div>
                      <div style={{display:"flex", gap:6, flexWrap:"wrap", justifyContent:"flex-end"}}>
                        {p.stack.map((t,j)=>(
                          <span key={j} className="ds-mono" style={{fontSize:9, padding:"2px 8px", border:"1px solid rgba(245,242,234,0.18)", color:"rgba(245,242,234,0.7)", letterSpacing:"0.12em"}}>{t}</span>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              </article>
            </React.Fragment>
          ))}
        </div>
      </section>

      {/* ═══════════ FAQ + CTA ═══════════ */}
      <section style={{padding:"96px 56px", background:"#0a0c1a", borderTop:"1px solid rgba(245,242,234,0.18)"}}>
        <div style={{display:"grid", gridTemplateColumns:"1fr 1fr", gap:80}}>
          <div>
            <div className="ds-eyebrow" style={{marginBottom:14}}>· V / FAQ</div>
            <h2 className="ds-display" style={{fontSize:56, marginBottom:32}}>Common questions.</h2>
            {FAQ.map((f,i)=>(
              <div key={i} style={{padding:"22px 0", borderTop:"1px solid rgba(245,242,234,0.18)"}}>
                <div style={{display:"flex", alignItems:"baseline", gap:14, marginBottom:8}}>
                  <span className="ds-eyebrow">Q.{String(i+1).padStart(2,'0')}</span>
                  <div style={{fontFamily:"'Fraunces',serif", fontSize:22, fontWeight:600, color:"#f5f2ea"}}>{f.q}</div>
                </div>
                <div className="ds-body" style={{fontSize:16, paddingLeft:48}}>{f.a}</div>
              </div>
            ))}
          </div>
          <div style={{position:"relative", border:"1px solid rgba(131,163,132,0.4)", padding:48}}>
            <span className="ds-corner ds-corner-tl"/>
            <span className="ds-corner ds-corner-tr"/>
            <span className="ds-corner ds-corner-bl"/>
            <span className="ds-corner ds-corner-br"/>
            <div className="ds-eyebrow" style={{marginBottom:16}}>· VI / Start a dispatch</div>
            <h2 className="ds-display" style={{fontSize:72, marginBottom:24}}>
              Send us<br/>a brief.
            </h2>
            <p className="ds-body" style={{fontSize:18, marginBottom:36}}>
              A sentence is enough. We'll reply within a day with fixed scope, fixed price, and a date you can put on the calendar.
            </p>
            <div style={{display:"flex", flexDirection:"column", gap:14, marginBottom:32}}>
              <button className="ds-btn-solid" style={{justifyContent:"space-between"}}>Open a commission <span>→</span></button>
              <button className="ds-btn" style={{justifyContent:"space-between"}}>hello@cactuscatsoftware.com <span>↗</span></button>
            </div>
            <div className="ds-coord" style={{paddingTop:24, borderTop:"1px solid rgba(245,242,234,0.18)"}}>
              · Office hours · Mon–Fri · 09:00–18:00 ET · Reply ≤ 24h · USA based
            </div>
          </div>
        </div>
      </section>

      <footer style={{padding:"32px 56px", background:"#0a0c1a", borderTop:"1px solid rgba(245,242,234,0.18)", display:"flex", justifyContent:"space-between", fontFamily:"'JetBrains Mono',monospace", fontSize:10, letterSpacing:"0.18em", color:"rgba(245,242,234,0.5)", textTransform:"uppercase"}}>
        <span>© MMXXVI · CACTUS CAT SOFTWARE</span>
        <span>END OF DISPATCH №042 · {ts} ET</span>
        <span>MADE IN USA</span>
      </footer>
    </div>
  );
}

const dispStyles = {
  root: { background:"#0a0c1a", color:"#f5f2ea", fontFamily:"'Space Grotesk',system-ui,sans-serif", width:"100%", minHeight:"100%" },
  hero: { position:"relative", overflow:"hidden", minHeight:820 },
  heroBg: { position:"absolute", inset:0, backgroundImage:`url(${HERO_BG})`, backgroundSize:"cover", backgroundPosition:"center top", opacity:0.55 },
  heroOverlay: { position:"absolute", inset:0, background:"linear-gradient(180deg, rgba(10,12,26,0.25) 0%, rgba(10,12,26,0.55) 55%, rgba(10,12,26,1) 100%)" },
  heroInner: { position:"relative", zIndex:3, display:"flex", minHeight:820 },
  heroAside: { flex:"0 0 420px", padding:"56px 40px 56px 24px" },
  fullBleed: { position:"relative", overflow:"hidden", borderTop:"1px solid rgba(245,242,234,0.18)", borderBottom:"1px solid rgba(245,242,234,0.18)", minHeight:600 },
  fullBleedBg: { position:"absolute", inset:0, backgroundImage:`url(${HERO_BG})`, backgroundSize:"cover", backgroundPosition:"center 45%", filter:"brightness(0.6) saturate(1.1)" },
  fullBleedOverlay: { position:"absolute", inset:0, background:"radial-gradient(ellipse at 30% 50%, rgba(10,12,26,0.55) 0%, rgba(10,12,26,0.85) 100%)", zIndex:1 },
};

window.VariantDispatch = VariantDispatch;
