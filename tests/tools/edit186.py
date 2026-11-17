# Build 186 · Karl, 17 Nov 2026: "The animation needs to pop in a similar way"; the quiet line of honesty at the
# moment of offering ("third way. Ok."). Both run through the Usability Law's six questions first.   python3 edit186.py <site folder>
import sys,io
p=sys.argv[1].rstrip('/')+'/seeking.html'
s=io.open(p,encoding='utf8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:70]); s=s.replace(a,b)
# 1 · THE WAKING LIGHT POPS. By day a small dusk now falls inside the circle as the hold begins, and the sense wakes in it
#     as light, the way it already does at night. (25 Aug: "Additive light does nothing on a white ground". The answer
#     parked that day was to give the light its own ground; the countdown's dark halo is the same idea.)
rep("var qNight=false, qT1=[196,181,253], qT2=[232,220,255], qAB=1;",
    "var qNight=false, qDusk=false, qT1=[196,181,253], qT2=[232,220,255], qAB=1;")
rep("  qNight=document.body.classList.contains('night');\n  qAB=qNight?1.25:2.7;                    /* ink needs more weight than glow */",
    "  /* Build 186 · Karl, 17 Nov 2026: \"The animation needs to pop in a similar way\" (as the countdown: light, with its\n     own dark ground). By day a small dusk falls inside the circle and the sense wakes in it as light, exactly as it\n     already does at night. qDusk remembers that the page itself is in daylight, so the dusk is plum, never black. */\n  qDusk=!document.body.classList.contains('night');\n  qNight=true;\n  qAB=qDusk?1.7:1.25;                     /* a little more light by day: the sky around it is bright */")
rep("  var bedRGB=qNight?'10,7,14':'255,251,246';\n  var bedA=(qNight?0.60:0.30)*v*(0.82+br*0.18);",
    "  var bedRGB=qDusk?'38,24,74':(qNight?'10,7,14':'255,251,246');          /* Build 186: plum dusk by day */\n  var bedA=(qDusk?0.78:(qNight?0.60:0.30))*v*(0.82+br*0.18);")
# 2 · THE LINE OF HONESTY, at the moment of offering. Two sentences before, two sentences after (the word budget, §3.7):
#     the second now says who learns from it and why. The deep copy stays one deliberate tap away (About).
rep('<div class="tiny">The place is shown on the map. Who left it is not.</div>\n  </div>\n</section>\n\n<!-- ══ 4 · THE MAP',
    '<div class="tiny" id="honest">The place is shown on the map; who left it is not. People and AI both learn from it, for mutual benefit. <a href="/about" target="_blank" rel="noopener">About</a></div>\n  </div>\n</section>\n\n<!-- ══ 4 · THE MAP')
rep("body.night #typed .pHead{text-shadow:0 1px 11px rgba(10,7,13,.92)}",
    "body.night #typed .pHead{text-shadow:0 1px 11px rgba(10,7,13,.92)}\n/* Build 186 · the line of honesty is read, not squinted at: the Usability Law's floor is 5.5 to 1, and this line is on\n   the first-ninety-seconds path. It was 12px italic at about 4.9 to 1. */\n#typed #honest{font-size:15px;line-height:1.6;font-style:normal;color:#463b60;max-width:340px}\nbody.night #typed #honest{color:#d6ccf2}\n#typed #honest a{color:inherit;text-decoration:underline;text-underline-offset:3px;white-space:nowrap}\n#typed #honest a:focus-visible{outline:2px solid currentColor;outline-offset:3px;border-radius:4px}")
# 1b · the light itself: a little more colour, a soft glow of its own, and strokes that can be seen past a thumb
rep("  qT1=qTriple(qCol,qNight);\n  qT2=qTriple(qSig.c2||qCol,qNight);",
    "  qT1=qTriple(qCol,qNight);\n  qT2=qTriple(qSig.c2||qCol,qNight);\n  if(qDusk){ qT1=qVivid(qT1); qT2=qVivid(qT2); }      /* Build 186: hue kept, colour pushed up, never darkened */")
rep("function qA(t,a){",
    "/* Build 186 · light on dusk can afford more colour than light on true night: hue kept, saturation up, and\n   nothing else. Nothing is ever darkened, and nothing is whitened (25 Aug: one darkness made every sense mud). */\nfunction qVivid(t){\n  var mx=Math.max(t[0],t[1],t[2]), mn=Math.min(t[0],t[1],t[2]), mid=(mx+mn)/2, o=[];\n  for(var i=0;i<3;i++){ var c=mid+(t[i]-mid)*1.6; o.push(Math.round(Math.min(255,Math.max(0,c)))); }\n  return o;\n}\nfunction qA(t,a){")
rep("  if(!qNight){\n    qCtx.shadowColor='rgba(255,252,247,0.95)';\n    qCtx.shadowBlur=Math.max(3,r*0.030);\n  }",
    "  if(!qNight){\n    qCtx.shadowColor='rgba(255,252,247,0.95)';\n    qCtx.shadowBlur=Math.max(3,r*0.030);\n  }else if(qDusk){                                  /* Build 186: each stroke carries a glow of the sense's own colour */\n    qCtx.shadowColor='rgba('+qT2[0]+','+qT2[1]+','+qT2[2]+',0.85)';\n    qCtx.shadowBlur=Math.max(4,r*0.050);\n  }")
rep("    qCtx.lineWidth=Math.max(0.6,r*0.010*(1-k*0.6));",
    "    qCtx.lineWidth=Math.max(0.6,r*0.010*(1-k*0.6))*(qDusk?1.7:1);")
rep("  qCtx.lineWidth=Math.max(0.8,r*0.030*(0.5+th*0.7));",
    "  qCtx.lineWidth=Math.max(0.8,r*0.030*(0.5+th*0.7))*(qDusk?1.35:1);")
rep("  qAB=qDusk?1.7:1.25;","  qAB=qDusk?1.55:1.25;")
rep("#qNum{z-index:9;font-size:clamp(34px,10vmin,56px);font-weight:500;letter-spacing:.04em;color:#fff;\n  text-shadow:0 0 3px rgba(44,28,92,.98),0 0 9px rgba(44,28,92,.9),0 0 22px rgba(44,28,92,.7),0 0 44px rgba(44,28,92,.45)}",
    "#qNum{z-index:9;font-size:clamp(34px,10vmin,56px);font-weight:600;letter-spacing:.04em;color:#fff;\n  text-shadow:0 0 2px rgba(34,20,78,1),0 0 4px rgba(34,20,78,1),0 0 7px rgba(34,20,78,.95),0 0 12px rgba(34,20,78,.9),0 0 24px rgba(34,20,78,.75),0 0 44px rgba(34,20,78,.5)}   /* Build 186: a denser edge, now that the light behind it is bright */")
rep("        if(e.type!=='pointerdown'&&!n.classList.contains('on'))return;\n",
    "        /* Build 186: it follows the finger from the first touch, so it is already beside the finger when the count begins */\n")
# the Seeking's own stamp, so a glance says which Seeking this is
rep("Build 27 Oct 2026 &middot; 170","Build 17 Nov 2026 &middot; 186")
io.open(p,'w',encoding='utf8').write(s)
print('ok')
