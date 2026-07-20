<!--
  ABOUT-PAGE HEADER SNIPPET — pulled from the Dispatch home variant.

  The "Felis Cactus" star-chart interlude was lifted off the home page so
  the splash flows uninterrupted from services → expedition log. Drop it
  in as the hero/header section of the eventual About page; it carries
  the design-ethos statement that used to anchor the home midpoint.

  Dependencies:
    - dispStyles.fullBleed / .fullBleedBg / .fullBleedOverlay
    - .ds-eyebrow / .ds-display utility classes
    - HERO_BG asset (assets/hero_navbar.png)

  JSX form below — paste inside the About-page React component.
-->

{/* ═══════════ ABOUT · STAR-CHART HEADER ═══════════ */}
<section style={dispStyles.fullBleed}>
  <div style={dispStyles.fullBleedBg}/>
  <div style={dispStyles.fullBleedOverlay}/>
  {/* constellation overlay — Felis Cactus, our patron constellation */}
  <svg viewBox="0 0 1200 600" preserveAspectRatio="xMidYMid slice"
       style={{position:"absolute", inset:0, width:"100%", height:"100%", zIndex:2, opacity:0.7}}>
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
  <div style={{position:"relative", zIndex:3, padding:"180px 56px"}}>
    <div className="ds-eyebrow" style={{marginBottom:20}}>· About · Studio Ethos</div>
    <h2 className="ds-display" style={{fontSize:108, maxWidth:1100, fontWeight:300, fontStyle:"italic"}}>
      <span style={{fontWeight:700, fontStyle:"normal"}}>Built</span> for the night,<br/>
      and the wind, and<br/>
      the long road ahead.
    </h2>
    <div style={{display:"flex", alignItems:"center", gap:18, marginTop:48}}>
      <span style={{width:64, height:1, background:"#83A384"}}/>
      <span className="ds-eyebrow">· Design ethos · printed on every receipt</span>
    </div>
  </div>
</section>
