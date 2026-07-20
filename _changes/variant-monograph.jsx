// VARIANT B — THE MONOGRAPH
// Coffee-table art book. Huge negative space. Plates I-VI. Italic captions.
// Right-side hero panel = manifesto with figure number footnotes.

function VariantMonograph() {
  const [cycleIdx, setCycleIdx] = React.useState(0);
  const [letterIdx, setLetterIdx] = React.useState(0);
  React.useEffect(() => {
    const id = setInterval(() => {
      setCycleIdx((i) => (i + 1) % CYCLE_PHRASES.length);
      setLetterIdx(0);
    }, 3400);
    return () => clearInterval(id);
  }, []);
  React.useEffect(() => {
    const phrase = CYCLE_PHRASES[cycleIdx];
    if (letterIdx >= phrase.length) return;
    const id = setTimeout(() => setLetterIdx(letterIdx + 1), 38);
    return () => clearTimeout(id);
  }, [letterIdx, cycleIdx]);

  const phrase = CYCLE_PHRASES[cycleIdx];
  const typed = phrase.slice(0, letterIdx);

  return (
    <div style={monoStyles.root}>
      <style>{`
        .mg-roman { font-family:'Fraunces',serif; font-weight:300; font-style:italic; color:rgba(245,242,234,0.6); }
        .mg-folio { font-family:'JetBrains Mono',monospace; font-size:10px; letter-spacing:0.28em; text-transform:uppercase; color:rgba(245,242,234,0.5); }
        .mg-caption { font-family:'Fraunces',serif; font-style:italic; font-size:14px; line-height:1.5; color:rgba(245,242,234,0.7); }
        .mg-plate-num { font-family:'Fraunces',serif; font-weight:300; font-size:18px; letter-spacing:0.35em; color:#83A384; text-transform:uppercase; }
        .mg-display { font-family:'Fraunces',serif; font-weight:300; color:#f5f2ea; letter-spacing:-0.03em; line-height:0.94; }
        .mg-display-bold { font-family:'Fraunces',serif; font-weight:700; color:#f5f2ea; letter-spacing:-0.03em; line-height:0.94; }
        .mg-body { font-family:'Fraunces',serif; font-weight:400; color:rgba(245,242,234,0.78); line-height:1.65; font-size:17px; }
        .mg-cursor { display:inline-block; width:2px; height:0.85em; background:#83A384; margin-left:6px; vertical-align:-2px; animation: mgBlink 1s steps(2) infinite; }
        @keyframes mgBlink { 50% { opacity:0; } }
        .mg-figref { vertical-align:super; font-size:0.6em; color:#83A384; font-family:'JetBrains Mono',monospace; font-style:normal; }
        .mg-link { color:#83A384; text-decoration:none; font-family:'Fraunces',serif; font-style:italic; font-size:18px; border-bottom:1px solid rgba(131,163,132,0.4); padding-bottom:2px; transition:border-color .2s; }
        .mg-link:hover { border-bottom-color:#83A384; }
        .mg-btn { display:inline-flex; align-items:center; gap:14px; padding:20px 40px; background:#f5f2ea; color:#0a0c1a; font-family:'Fraunces',serif; font-size:18px; font-weight:600; letter-spacing:-0.01em; border:none; cursor:pointer; transition:background .2s; }
        .mg-btn:hover { background:#83A384; }
        .mg-btn-out { display:inline-flex; align-items:center; gap:14px; padding:20px 40px; background:transparent; color:#f5f2ea; font-family:'Fraunces',serif; font-size:18px; font-weight:500; font-style:italic; border:1px solid rgba(245,242,234,0.4); cursor:pointer; transition:all .2s; }
        .mg-btn-out:hover { border-color:#83A384; color:#83A384; }
        .mg-stars { position:absolute; inset:0; pointer-events:none; }
        .mg-star { position:absolute; width:1px; height:1px; background:#f5f2ea; border-radius:50%; }
        .mg-moon-mg { position:absolute; top:120px; right:200px; width:160px; height:160px; border-radius:50%; background:radial-gradient(circle at 38% 38%, #fff7e6 0%, #f0e6c8 35%, #c4b896 65%, transparent 100%); box-shadow:0 0 100px 30px rgba(245,234,200,0.2); }
        .mg-moon-crater { position:absolute; width:14px; height:14px; border-radius:50%; background:rgba(120,108,80,0.3); }
        .mg-toc-line { display:flex; justify-content:space-between; padding:18px 0; border-bottom:1px solid rgba(245,242,234,0.15); align-items:baseline; cursor:pointer; transition:padding-left .25s; }
        .mg-toc-line:hover { padding-left:6px; }
        .mg-toc-line:hover .mg-toc-name { color:#83A384; }
        .mg-toc-name { font-family:'Fraunces',serif; font-size:22px; color:#f5f2ea; transition:color .2s; }
        .mg-rule-thin { height:1px; background:rgba(245,242,234,0.2); }
        .mg-tab { font-family:'JetBrains Mono',monospace; font-size:10px; letter-spacing:0.2em; text-transform:uppercase; color:#83A384; }
      `}</style>

      {/* ═══════════ MINIMAL HEADER ═══════════ */}
      <header style={{padding:"32px 80px", display:"flex", justifyContent:"space-between", alignItems:"center", position:"relative", zIndex:10}}>
        <div style={{fontFamily:"'Fraunces',serif", fontWeight:600, fontSize:22, color:"#f5f2ea", letterSpacing:"-0.01em"}}>
          Cactus Cat <span style={{fontStyle:"italic", fontWeight:300, color:"rgba(245,242,234,0.6)"}}>Software</span>
        </div>
        <nav style={{display:"flex", gap:40, fontFamily:"'Fraunces',serif", fontSize:16, color:"rgba(245,242,234,0.85)"}}>
          <span>Catalog</span>
          <span>Work</span>
          <span>Journal</span>
          <span>Contact</span>
        </nav>
        <div className="mg-folio">MMXXVI · Vol. I</div>
      </header>

      {/* ═══════════ HERO ═══════════ */}
      <section style={monoStyles.hero}>
        <div style={monoStyles.heroBg}/>
        <div style={monoStyles.heroOverlay}/>
        <div className="mg-moon-mg">
          <div className="mg-moon-crater" style={{top:35, left:48}}/>
          <div className="mg-moon-crater" style={{top:62, left:84, width:8, height:8}}/>
          <div className="mg-moon-crater" style={{top:98, left:42, width:18, height:18}}/>
        </div>
        <div className="mg-stars">
          {Array.from({length:60}).map((_,i)=>(
            <span key={i} className="mg-star" style={{
              left:`${Math.random()*100}%`, top:`${Math.random()*60}%`,
              opacity: Math.random()*0.8+0.2,
              transform:`scale(${Math.random()*2+0.5})`,
              boxShadow: Math.random()>0.7 ? "0 0 4px #fff" : "none"
            }}/>
          ))}
        </div>

        <div style={monoStyles.heroInner}>
          <div style={{flex:"1 1 58%", padding:"40px 60px 80px 80px"}}>
            <div className="mg-plate-num" style={{marginBottom:24}}>Plate &nbsp;·&nbsp; I</div>
            <h1 className="mg-display" style={{fontSize:152, marginBottom:32}}>
              Software<br/>
              <span className="mg-display-bold">built to</span><br/>
              <span style={{color:"#83A384", fontWeight:600, fontStyle:"italic", display:"inline-block", minHeight:"1em"}}>
                {typed}<span className="mg-cursor"/>
              </span>
            </h1>
            <div style={{maxWidth:620, marginTop:48}}>
              <div className="mg-tab" style={{marginBottom:14}}>· An Introduction</div>
              <p className="mg-body" style={{fontSize:21, lineHeight:1.55, color:"rgba(245,242,234,0.88)"}}>
                Cactus Cat is a small east-coast studio that designs, builds, and operates
                <em style={{color:"#83A384"}}> web software</em><span className="mg-figref">[I]</span> and
                <em style={{color:"#83A384"}}> digital marketing</em><span className="mg-figref">[II]</span> for
                companies who would rather own their tools than rent them.
              </p>
              <p className="mg-body" style={{fontSize:17, marginTop:20, color:"rgba(245,242,234,0.7)"}}>
                Custom applications, subscription products, mobile, SEO, content, security — handed to you with the keys, plainly documented, quiet enough to run on its own.
              </p>
            </div>
            <div style={{display:"flex", gap:16, marginTop:56}}>
              <button className="mg-btn">Start a project <span>→</span></button>
              <button className="mg-btn-out">Read the catalog</button>
            </div>
          </div>

          <aside style={monoStyles.heroAside}>
            <div style={{position:"sticky", top:40}}>
              <div className="mg-plate-num" style={{marginBottom:18}}>Contents</div>
              <div className="mg-rule-thin" style={{marginBottom:4}}/>
              {SERVICES.map((s,i)=>(
                <div key={i} className="mg-toc-line">
                  <div style={{display:"flex", gap:18, alignItems:"baseline"}}>
                    <span className="mg-roman" style={{fontSize:14, minWidth:32}}>
                      {["I","II","III","IV","V"][i]}
                    </span>
                    <div>
                      <div className="mg-toc-name">{s.kicker}</div>
                      <div style={{fontFamily:"'Fraunces',serif", fontStyle:"italic", fontSize:13, color:"rgba(245,242,234,0.55)", marginTop:2}}>
                        {["Web, owned outright", "Recurring revenue products", "Findability & growth", "Hardened systems", "Glass-box delivery"][i]}
                      </div>
                    </div>
                  </div>
                  <span className="mg-folio">p.{String((i+1)*8).padStart(2,'0')}</span>
                </div>
              ))}
              <div className="mg-toc-line">
                <div style={{display:"flex", gap:18, alignItems:"baseline"}}>
                  <span className="mg-roman" style={{fontSize:14, minWidth:32}}>VI</span>
                  <div>
                    <div className="mg-toc-name" style={{fontStyle:"italic"}}>Selected work</div>
                    <div style={{fontFamily:"'Fraunces',serif", fontStyle:"italic", fontSize:13, color:"rgba(245,242,234,0.55)", marginTop:2}}>
                      Four engagements, four briefs
                    </div>
                  </div>
                </div>
                <span className="mg-folio">p.48</span>
              </div>

              <div style={{marginTop:36, padding:"28px 24px", border:"1px solid rgba(245,242,234,0.18)", background:"rgba(10,12,26,0.4)"}}>
                <div className="mg-tab" style={{marginBottom:10}}>Editor's note</div>
                <div style={{fontFamily:"'Fraunces',serif", fontStyle:"italic", fontSize:17, lineHeight:1.55, color:"rgba(245,242,234,0.9)"}}>
                  "We pair every line of code with the marketing that makes it findable. Build and broadcast — one studio, one bill."
                </div>
                <div style={{marginTop:16, fontFamily:"'Fraunces',serif", fontSize:13, color:"#83A384", letterSpacing:"0.05em"}}>
                  — The studio, 2026
                </div>
              </div>
            </div>
          </aside>
        </div>
      </section>

      {/* ═══════════ STAT LINE ═══════════ */}
      <section style={{padding:"80px 80px 40px", background:"#0a0c1a", textAlign:"center"}}>
        <div className="mg-plate-num" style={{marginBottom:32}}>Plate &nbsp;·&nbsp; II</div>
        <h2 className="mg-display" style={{fontSize:88, marginBottom:80}}>
          A studio of <span style={{fontStyle:"italic", color:"#83A384"}}>two halves.</span>
        </h2>
        <div style={{display:"grid", gridTemplateColumns:"1fr 1fr", gap:80, maxWidth:1100, margin:"0 auto", textAlign:"left"}}>
          <div>
            <div className="mg-tab" style={{marginBottom:16}}>I · Build</div>
            <div style={{fontFamily:"'Fraunces',serif", fontSize:40, fontWeight:600, color:"#f5f2ea", lineHeight:1.1, marginBottom:18, letterSpacing:"-0.02em"}}>
              Software designed, engineered, &amp; documented.
            </div>
            <p className="mg-body">Web applications, SaaS, mobile, integrations, automations — all custom, all owned by you, all engineered on stacks that have outlived a dozen frameworks.</p>
          </div>
          <div>
            <div className="mg-tab" style={{marginBottom:16}}>II · Broadcast</div>
            <div style={{fontFamily:"'Fraunces',serif", fontSize:40, fontWeight:600, color:"#f5f2ea", lineHeight:1.1, marginBottom:18, letterSpacing:"-0.02em"}}>
              Marketing that finds, frames, &amp; converts.
            </div>
            <p className="mg-body">SEO foundations, content strategy, social automation, analytics, brand. Half of every project is making sure the thing you built actually gets found.</p>
          </div>
        </div>
        <div style={{display:"flex", justifyContent:"center", gap:0, marginTop:80, padding:"32px 0", borderTop:"1px solid rgba(245,242,234,0.18)", borderBottom:"1px solid rgba(245,242,234,0.18)"}}>
          {STATS_STRIP.map((s,i)=>(
            <div key={i} style={{flex:1, padding:"0 24px", borderLeft: i>0?"1px solid rgba(245,242,234,0.15)":"none"}}>
              <div style={{fontFamily:"'Fraunces',serif", fontSize:48, fontWeight:300, fontStyle:"italic", color:"#83A384", lineHeight:1}}>{s.v}</div>
              <div className="mg-tab" style={{marginTop:8}}>{s.k}</div>
            </div>
          ))}
        </div>
      </section>

      {/* ═══════════ SERVICES AS PLATES ═══════════ */}
      <section style={{padding:"80px 80px", background:"#0a0c1a"}}>
        {SERVICES.map((s,i)=>(
          <article key={i} style={{display:"grid", gridTemplateColumns: i%2===0 ? "1fr 1fr" : "1fr 1fr", gap:80, padding:"80px 0", borderTop:"1px solid rgba(245,242,234,0.18)"}}>
            <div style={{order: i%2===0 ? 1 : 2}}>
              <div className="mg-plate-num" style={{marginBottom:14}}>Plate · {["III","IV","V","VI","VII"][i]}</div>
              <div className="mg-tab" style={{color:"#83A384", marginBottom:18}}>{s.kicker}</div>
              <h3 className="mg-display" style={{fontSize:72, marginBottom:28}}>
                {s.title.split(" — ")[0]}
              </h3>
              <p className="mg-body" style={{fontSize:19, marginBottom:36, maxWidth:520}}>{s.body}</p>
              <a className="mg-link">{s.cta} →</a>
            </div>
            <div style={{order: i%2===0 ? 2 : 1, display:"flex", flexDirection:"column", justifyContent:"center"}}>
              {/* Visual block per service */}
              <div style={{
                aspectRatio:"4/5",
                background: i===0 ? "linear-gradient(165deg, #1a2438 0%, #0a0c1a 100%)"
                          : i===1 ? "linear-gradient(165deg, #2a1f3a 0%, #0a0c1a 100%)"
                          : i===2 ? "linear-gradient(165deg, #1a3328 0%, #0a0c1a 100%)"
                          : i===3 ? "linear-gradient(165deg, #2a1818 0%, #0a0c1a 100%)"
                          :         "linear-gradient(165deg, #1a2a3a 0%, #0a0c1a 100%)",
                position:"relative", overflow:"hidden", border:"1px solid rgba(245,242,234,0.15)"
              }}>
                {/* Decorative content per service */}
                {i===0 && (
                  <div style={{position:"absolute", inset:48, display:"grid", gridTemplateColumns:"repeat(3,1fr)", gap:16}}>
                    {["</>", "API", "DB", "AUTH", "JOBS", "DEPLOY"].map((t,j)=>(
                      <div key={j} style={{border:"1px solid rgba(131,163,132,0.3)", padding:14, fontFamily:"'JetBrains Mono',monospace", fontSize:11, color:"#83A384", display:"flex", alignItems:"center", justifyContent:"center", aspectRatio:1}}>{t}</div>
                    ))}
                  </div>
                )}
                {i===1 && (
                  <div style={{position:"absolute", inset:48}}>
                    <div style={{width:140, height:280, border:"2px solid rgba(245,242,234,0.3)", borderRadius:24, margin:"0 auto", padding:18, position:"relative"}}>
                      <div style={{width:50, height:6, background:"rgba(245,242,234,0.3)", borderRadius:3, margin:"0 auto 18px"}}/>
                      <div style={{height:8, background:"#83A384", borderRadius:2, marginBottom:8, width:"80%"}}/>
                      <div style={{height:8, background:"rgba(131,163,132,0.3)", borderRadius:2, marginBottom:8, width:"60%"}}/>
                      <div style={{height:8, background:"rgba(131,163,132,0.3)", borderRadius:2, marginBottom:24, width:"90%"}}/>
                      <div style={{fontFamily:"'Fraunces',serif", fontSize:28, fontWeight:600, color:"#83A384", textAlign:"center"}}>$24<span style={{fontSize:14}}>/mo</span></div>
                    </div>
                  </div>
                )}
                {i===2 && (
                  <div style={{position:"absolute", inset:48, display:"flex", flexDirection:"column", justifyContent:"center", gap:18}}>
                    {[
                      {l:"organic search", v:78},
                      {l:"content engine", v:62},
                      {l:"social reach", v:45},
                      {l:"conversion rate", v:88},
                    ].map((b,j)=>(
                      <div key={j}>
                        <div style={{display:"flex", justifyContent:"space-between", fontFamily:"'JetBrains Mono',monospace", fontSize:10, color:"rgba(245,242,234,0.7)", marginBottom:6, letterSpacing:"0.1em"}}>
                          <span>{b.l.toUpperCase()}</span><span>{b.v}%</span>
                        </div>
                        <div style={{height:3, background:"rgba(245,242,234,0.1)"}}>
                          <div style={{height:"100%", width:`${b.v}%`, background:"#83A384"}}/>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
                {i===3 && (
                  <div style={{position:"absolute", inset:48, fontFamily:"'JetBrains Mono',monospace", fontSize:11, color:"#83A384", lineHeight:2}}>
                    <div>$ scan --target client.app</div>
                    <div style={{color:"rgba(245,242,234,0.5)"}}># Initializing...</div>
                    <div>✓ Ports — 3 open</div>
                    <div>✓ TLS — A+</div>
                    <div style={{color:"#fdcb6e"}}>⚠ Outdated dep</div>
                    <div>✓ Auth — secure</div>
                    <div>✓ SQLi — 0 found</div>
                    <div>✓ XSS — hardened</div>
                    <div style={{color:"rgba(245,242,234,0.5)"}}># Report ready</div>
                    <div>$ <span style={{display:"inline-block", width:8, height:14, background:"#83A384", verticalAlign:"middle", animation:"mgBlink 1s infinite"}}/></div>
                  </div>
                )}
                {i===4 && (
                  <div style={{position:"absolute", inset:48}}>
                    <div style={{fontFamily:"'JetBrains Mono',monospace", fontSize:10, color:"rgba(245,242,234,0.6)", marginBottom:14, letterSpacing:"0.15em"}}>PROJECT · CCS-2026-042</div>
                    {[
                      {l:"Discovery", v:100, s:"DONE"},
                      {l:"Architecture", v:100, s:"DONE"},
                      {l:"Build", v:65, s:"65%"},
                      {l:"QA", v:0, s:"·"},
                      {l:"Launch", v:0, s:"·"},
                    ].map((m,j)=>(
                      <div key={j} style={{display:"flex", alignItems:"center", gap:12, padding:"10px 0", borderBottom:"1px solid rgba(245,242,234,0.08)"}}>
                        <span style={{fontFamily:"'Fraunces',serif", fontSize:14, color:"#f5f2ea", flex:"0 0 100px"}}>{m.l}</span>
                        <div style={{flex:1, height:2, background:"rgba(245,242,234,0.12)"}}>
                          <div style={{height:"100%", width:`${m.v}%`, background:m.v===100?"#83A384":m.v>0?"#0984e3":"transparent"}}/>
                        </div>
                        <span style={{fontFamily:"'JetBrains Mono',monospace", fontSize:9, color:m.v>0?"#83A384":"rgba(245,242,234,0.4)", letterSpacing:"0.1em", minWidth:30, textAlign:"right"}}>{m.s}</span>
                      </div>
                    ))}
                  </div>
                )}
                <div style={{position:"absolute", bottom:14, left:14, fontFamily:"'JetBrains Mono',monospace", fontSize:9, color:"rgba(245,242,234,0.4)", letterSpacing:"0.18em"}}>FIG · {String(i+1).padStart(2,'0')}</div>
                <div style={{position:"absolute", bottom:14, right:14, fontFamily:"'JetBrains Mono',monospace", fontSize:9, color:"rgba(245,242,234,0.4)", letterSpacing:"0.18em"}}>{["III","IV","V","VI","VII"][i]}</div>
              </div>
              <div className="mg-caption" style={{marginTop:18, textAlign:"center"}}>
                <em>Figure {i+1}.</em> {["Architecture sketch — bespoke stacks, ownership intact.", "Subscription product — $24/mo recurring, single bill.", "Growth dashboard — discovery measured weekly.", "Pentest console — finding cracks before attackers.", "Project board — milestones, owned by the client."][i]}
              </div>
            </div>
          </article>
        ))}
      </section>

      {/* ═══════════ FULL-BLEED PLATE VIII ═══════════ */}
      <section style={monoStyles.fullBleed}>
        <div style={monoStyles.fullBleedBg}/>
        <div style={monoStyles.fullBleedOverlay}/>
        <div style={{position:"relative", zIndex:2, padding:"200px 80px", textAlign:"center"}}>
          <div className="mg-plate-num" style={{marginBottom:32, color:"rgba(245,242,234,0.7)"}}>Plate &nbsp;·&nbsp; VIII</div>
          <h2 className="mg-display" style={{fontSize:120, maxWidth:1200, margin:"0 auto", fontStyle:"italic", fontWeight:300}}>
            Built once. <span style={{fontWeight:700, fontStyle:"normal"}}>Owned</span> forever.
          </h2>
          <p className="mg-body" style={{fontSize:22, maxWidth:680, margin:"40px auto 0", color:"rgba(245,242,234,0.85)"}}>
            Every project ships with its full source, its full documentation, and its full operating instructions. We're a studio — not a landlord.
          </p>
        </div>
      </section>

      {/* ═══════════ PROOF OF WORK · CATALOG ═══════════ */}
      <section style={{padding:"100px 80px", background:"#0a0c1a"}}>
        <div className="mg-plate-num" style={{marginBottom:20}}>Plate &nbsp;·&nbsp; IX</div>
        <h2 className="mg-display" style={{fontSize:96, marginBottom:24, maxWidth:900}}>
          Selected <span style={{fontStyle:"italic", color:"#83A384"}}>work,</span> 2024–2026.
        </h2>
        <p className="mg-body" style={{fontSize:20, maxWidth:620, marginBottom:80, color:"rgba(245,242,234,0.7)"}}>
          A small sample. We work under NDA on most engagements; everything below was released with the client's blessing.
        </p>

        <div style={{display:"grid", gridTemplateColumns:"repeat(2,1fr)", gap:80, rowGap:120}}>
          {PROOF.map((p,i)=>(
            <article key={i}>
              <div style={{display:"flex", justifyContent:"space-between", alignItems:"baseline", marginBottom:14}}>
                <div className="mg-tab">{p.tag}</div>
                <div className="mg-folio">№ {String(i+1).padStart(3,'0')}</div>
              </div>
              <div style={{
                aspectRatio:"4/3",
                background:`linear-gradient(155deg, oklch(0.50 0.14 ${p.hue}) 0%, oklch(0.18 0.06 ${p.hue}) 100%)`,
                marginBottom:24, position:"relative", overflow:"hidden",
                border:"1px solid rgba(245,242,234,0.12)"
              }}>
                <div style={{position:"absolute", inset:0, backgroundImage:"repeating-linear-gradient(0deg, transparent 0 28px, rgba(255,255,255,0.04) 28px 29px)"}}/>
                <div style={{position:"absolute", inset:32, border:"1px solid rgba(245,242,234,0.2)", display:"flex", alignItems:"center", justifyContent:"center"}}>
                  <div style={{fontFamily:"'Fraunces',serif", fontStyle:"italic", fontWeight:300, fontSize:48, color:"rgba(245,242,234,0.6)"}}>{p.name}</div>
                </div>
                <div style={{position:"absolute", top:14, left:14, fontFamily:"'JetBrains Mono',monospace", fontSize:9, letterSpacing:"0.18em", color:"rgba(245,242,234,0.5)"}}>SCREEN GRAB · 01 OF 03</div>
              </div>
              <h3 style={{fontFamily:"'Fraunces',serif", fontSize:44, fontWeight:600, color:"#f5f2ea", margin:"0 0 14px", letterSpacing:"-0.02em"}}>{p.name}</h3>
              <p className="mg-body" style={{fontSize:18, marginBottom:24}}>{p.blurb}</p>
              <div style={{display:"flex", gap:32, padding:"20px 0", borderTop:"1px solid rgba(245,242,234,0.18)", borderBottom:"1px solid rgba(245,242,234,0.18)", marginBottom:18}}>
                {p.metrics.map((m,j)=>(
                  <div key={j}>
                    <div style={{fontFamily:"'Fraunces',serif", fontSize:32, fontWeight:300, fontStyle:"italic", color:"#83A384", lineHeight:1}}>{m.v}</div>
                    <div className="mg-tab" style={{fontSize:9, marginTop:6}}>{m.k}</div>
                  </div>
                ))}
              </div>
              <div className="mg-caption">
                Stack: {p.stack.join(" · ")}
              </div>
            </article>
          ))}
        </div>
      </section>

      {/* ═══════════ CTA · COLOPHON ═══════════ */}
      <section style={{padding:"160px 80px", background:"#0a0c1a", borderTop:"1px solid rgba(245,242,234,0.2)", textAlign:"center"}}>
        <div className="mg-plate-num" style={{marginBottom:24}}>Coda</div>
        <h2 className="mg-display" style={{fontSize:128, marginBottom:36, fontStyle:"italic", fontWeight:300}}>
          <span style={{fontWeight:700, fontStyle:"normal"}}>Have</span> something to build?
        </h2>
        <p className="mg-body" style={{fontSize:22, maxWidth:680, margin:"0 auto 56px"}}>
          A sentence is enough. Reply within a day with scope, price, and a date you can put on the calendar.
        </p>
        <div style={{display:"flex", justifyContent:"center", gap:20}}>
          <button className="mg-btn">Commission a project →</button>
          <button className="mg-btn-out">hello@cactuscatsoftware.com ↗</button>
        </div>
        <div style={{marginTop:120, paddingTop:32, borderTop:"1px solid rgba(245,242,234,0.18)", display:"flex", justifyContent:"space-between", maxWidth:1100, margin:"120px auto 0"}}>
          <div className="mg-folio">© MMXXVI · Cactus Cat Software</div>
          <div className="mg-caption">Set in Fraunces, JetBrains Mono &amp; Space Grotesk · printed on east-coast servers</div>
          <div className="mg-folio">Made in USA</div>
        </div>
      </section>
    </div>
  );
}

const monoStyles = {
  root: { background:"#0a0c1a", color:"#f5f2ea", fontFamily:"'Space Grotesk',system-ui,sans-serif", width:"100%", minHeight:"100%" },
  hero: { position:"relative", overflow:"hidden", minHeight:880 },
  heroBg: { position:"absolute", inset:0, backgroundImage:`url(${HERO_BG})`, backgroundSize:"cover", backgroundPosition:"center top", opacity:0.5 },
  heroOverlay: { position:"absolute", inset:0, background:"linear-gradient(180deg, rgba(10,12,26,0.3) 0%, rgba(10,12,26,0.55) 50%, rgba(10,12,26,1) 100%)" },
  heroInner: { position:"relative", zIndex:3, display:"flex", minHeight:880 },
  heroAside: { flex:"0 0 460px", padding:"40px 80px 40px 40px" },
  fullBleed: { position:"relative", overflow:"hidden", borderTop:"1px solid rgba(245,242,234,0.2)", borderBottom:"1px solid rgba(245,242,234,0.2)" },
  fullBleedBg: { position:"absolute", inset:0, backgroundImage:`url(${HERO_BG})`, backgroundSize:"cover", backgroundPosition:"center 60%", filter:"brightness(0.7) hue-rotate(15deg) saturate(1.2)" },
  fullBleedOverlay: { position:"absolute", inset:0, background:"radial-gradient(ellipse at center, rgba(10,12,26,0.4) 0%, rgba(10,12,26,0.85) 100%)" },
};

window.VariantMonograph = VariantMonograph;
