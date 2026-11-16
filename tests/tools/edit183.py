# Build 183 · the opening, made ready but not yet opened (Karl opens on his word).   python3 edit183.py <site folder>
import sys,io
root=sys.argv[1].rstrip('/')
def rd(n): return io.open(root+'/'+n,encoding='utf8').read()
def wr(n,s): io.open(root+'/'+n,'w',encoding='utf8').write(s)
def rep(s,a,b):
    assert s.count(a)==1,(s.count(a),a[:70]); return s.replace(a,b)
# 1 · the real front door, kept beside the holding page until the day (seen at /front)
s=rd('index.html')
s=rep(s,'<title>Aurasense</title>','<title>Aurasense</title>\n<meta name="robots" content="noindex">')
s=rep(s,'content="Aurasense, a map of how places feel, is coming soon. Open now: a free checklist for choosing a quiet home, the Mutual Benefit Pledge, and the open ledger."',
        'content="Aurasense is a living map of how places feel, made from what people sense there. Free to wander, with no account needed."')
s=rep(s,'  /* 14 Nov 2026 · Build 171 · what is open now, while the map is made ready */',
"""  /* 17 Nov 2026 · Build 183 · the front door: one plain sentence, one way in */
  body{overflow:auto}
  .say{position:relative;z-index:1;margin-top:1.9em;max-width:26em;font-family:Georgia,"Iowan Old Style","Times New Roman",serif;font-size:clamp(1.05rem,4vw,1.22rem);line-height:1.55;color:#e9e2ff}
  .enter{position:relative;z-index:1;margin-top:1.7em;display:inline-flex;align-items:center;justify-content:center;min-height:52px;padding:0 2.1em;border-radius:999px;
    background:linear-gradient(135deg,#c4b5fd,#ffb7cf);color:#1a1230;font-weight:600;font-size:1.05rem;letter-spacing:.04em;text-decoration:none;box-shadow:0 8px 34px rgba(196,181,253,.32)}
  .enter:focus-visible{outline:3px solid #fff;outline-offset:3px}
  .free{position:relative;z-index:1;margin-top:1.1em;font-size:.86rem;line-height:1.5;color:#a79dcb;max-width:24em}
  /* 14 Nov 2026 · Build 171 · what is open now, while the map is made ready */""")
s=rep(s,'      <div class="soon">coming soon</div>\n    </div>',
"""    </div>
    <p class="say">A living map of how places feel, made from what people sense there.</p>
    <a class="enter" href="/m">Enter the map</a>
    <p class="free">Free to wander. No account needed. For people 18 and over.</p>""")
s=rep(s,'<nav class="open" aria-label="Open now">\n      <p>open now</p>','<nav class="open" aria-label="Also here">\n      <p>also here</p>')
s=rep(s,'      <a href="/door">The Answering Door</a>','      <a href="/door">The Answering Door</a>\n      <a href="/privacy">The privacy promise</a>')
wr('front.html',s)
# 2 · the curtain learns one word: OPEN
m=rd('index-mapbox.html')
m=rep(m,"(function(){\n  var WORDS = ['Atest',","(function(){\n  /* Build 183 · THE OPENING SWITCH. While this says false, the curtain stays as it is. On the day Karl says so,\n     it becomes true (the tool open_doors.py does it, together with the front door), and everyone may come in. */\n  var OPEN = false;\n  if(OPEN) return;\n  var WORDS = ['Atest',")
# 3 · a kind word if sign-in codes are slow or many are being asked for
a="if(r&&r.error){if(note)note.textContent='The Gate is not keeping lights just yet \\u2014 soon \\u2727';return false;}if(note)note.textContent='\\u2713 Sent. Six digits are on their way to '+email+' \\u2014 they open below.';return true;}"
b="if(r&&r.error){var _busy=(r.error.status===429)||/rate|limit|too many|seconds/i.test(String(r.error.message||''));if(note)note.textContent=_busy?'Many codes are being asked for just now, so the next one may take a little while. Your aura is safe on this device meanwhile, and nothing is lost by trying again later \\u2727':'The Gate is not keeping lights just yet \\u2014 soon \\u2727';return false;}if(note){var _sent='\\u2713 Sent. Six digits are on their way to '+email+' \\u2014 they open below.';note.textContent=_sent;/* Build 183: a kind word if the code is slow */setTimeout(function(){try{if(note.textContent===_sent)note.textContent=_sent+' Not arrived yet? Codes can take a few minutes, and sometimes land in spam or junk. Your aura is safe on this device meanwhile.';}catch(e){}},45000);}return true;}"
m=rep(m,a,b)
m=rep(m,'<span class="bs-l">16 Nov 2026 · </span>182<','<span class="bs-l">17 Nov 2026 · </span>183<')
wr('index-mapbox.html',m)
print('ok')
