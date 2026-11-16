# Build 181 · three repairs from Karl's first real offering from the Mirror (16 Nov 2026).   python3 edit181.py <site folder>
import sys,io
p=sys.argv[1].rstrip('/')+'/index-mapbox.html'
s=io.open(p,encoding='utf8').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(s.count(a),a[:70])
    s=s.replace(a,b)
# 1 · the held moment rests everything else on the page. It must never rest the Mirror's own card.
rep("if(!el||el===root||el===dim||el===deep||el===cv||el.id==='as-reach-svg'||/^(SCRIPT|STYLE|LINK)$/.test(el.tagName))return;",
    "if(!el||el===root||el===dim||el===deep||el===cv||el.id==='as-reach-svg'||el.id==='as-mirror-land'||/^(SCRIPT|STYLE|LINK)$/.test(el.tagName))return;   /* Build 181: the way back to the Mirror is never put to rest */")
rep("window.asHeldOn=function(){return on;};",
    "window.asHeldOn=function(){return on;};\n/* Build 181 · going back to the Mirror ends the held moment, so nothing is left resting underneath it. */\nwindow.asHeldStop=function(){try{gen++;if(on)stop();}catch(e){}};")
# 2 · back to the Mirror: end the held moment and wake the Mirror (Karl: \"the final button was unresponsive\")
rep("var back=function(){try{mirrorLandCard(null);}catch(e){}if(gone)return;ov.classList.remove('away');",
    "var back=function(){try{mirrorLandCard(null);}catch(e){}if(gone)return;\n      /* Build 181 · Karl: \"the final button was unresponsive\". The held moment after a landing puts the rest of the page to\n         rest, and the Mirror was left resting when the person came back to it. Coming back ends that moment and wakes it. */\n      try{if(typeof window.asHeldStop==='function')window.asHeldStop();}catch(e){}\n      try{ov.removeAttribute('inert');}catch(e){}\n      ov.classList.remove('away');")
# 3 · the landing is seen first: the card waits for the held moment (at most twelve seconds), and is smaller
rep("""          setTimeout(function(){if(!h.alive())return;
            mirrorLandCard({text:""","""          var _t0=Date.now();
          setTimeout(function show(){if(!h.alive())return;
            /* Build 181 · Karl: "The view of the landing was somewhat blocked." The landing is seen first. */
            try{if(typeof window.asHeldOn==='function'&&window.asHeldOn()&&Date.now()-_t0<12000){setTimeout(show,600);return;}}catch(e){}
            mirrorLandCard({text:""")
rep("padding:13px 15px 12px;border-radius:16px;background:rgba(20,16,38,.94);","padding:10px 13px 10px;border-radius:16px;background:rgba(20,16,38,.9);")
rep("font:15px/1.45 system-ui,-apple-system,'Segoe UI',sans-serif;opacity:0;transition:opacity .5s ease,transform .5s ease}","font:14px/1.4 system-ui,-apple-system,'Segoe UI',sans-serif;opacity:0;transition:opacity .5s ease,transform .5s ease}")
rep("#as-mirror-land .ml-row{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}","#as-mirror-land .ml-row{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}")
rep("#as-mirror-land button{min-height:44px;padding:9px 14px;","#as-mirror-land button{min-height:44px;padding:8px 12px;")
# 4 · My Aura: a sense's story and a list are never open on top of each other (Karl: "the my aura text is overlapping again")
rep("  window._macListOpen=true;\n  box.innerHTML='';",
    "  window._macListOpen=true;\n  /* Build 181 · Karl: \"the my aura text is overlapping again\". A sense's story closes when a list opens. */\n  try{window._macCardOpen=false;var _sc181=document.getElementById('ma-sense-card');if(_sc181)_sc181.classList.remove('on');}catch(e){}\n  box.innerHTML='';")
rep("    var c=document.getElementById('ma-sense-card'); if(!c)return;\n    window._macCardOpen=true;",
    "    var c=document.getElementById('ma-sense-card'); if(!c)return;\n    try{if(window._macListOpen)macOpenDoor(-1);}catch(e){}   /* Build 181: and a list closes when a sense's story opens */\n    window._macCardOpen=true;")
# the stamp
rep('<span class="bs-l">16 Nov 2026 · </span>180<','<span class="bs-l">16 Nov 2026 · </span>181<')
io.open(p,'w',encoding='utf8').write(s)
print('ok')
