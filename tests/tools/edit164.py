"""Build 164 · the Mirror page: Keep what you found (23 Oct 2026).
Karl: "Already I feel like I wish I had those words I gave the mirror." Of the idea: "Love it."
When a conversation Claude listened to rests, "What I found, in my own words" becomes "Keep what I found": Claude
gathers what they found (mostly their own words), the step they chose, and their wiser self's last word. They may keep
it on this device only (a growing thread of their own light), copy it, or simply leave. "Your thread" beneath the
Mirror shows what was kept, with "Forget all of it". Aurasense keeps nothing. If Claude can't gather it, their own
words are shown, as before. Privacy page made true; stamps 164. Always starts from the live 163 pages; re-runnable."""
import io

def edit(src, dst, pairs):
    s = io.open(src, encoding='utf-8').read()
    for old, new, label in pairs:
        c = s.count(old)
        assert c == 1, (label, c)
        s = s.replace(old, new)
        print('ok', label)
    io.open(dst, 'w', encoding='utf-8').write(s)
    print('written', dst, len(s))

edit('/home/claude/work/mirror-living.163.html', '/home/claude/aurasense/mirror-living.html', [
    ("""  23 Oct 2026 · Build 163: the wiser voice's introduction is shown once a visit, never on repeat.""",
     """  23 Oct 2026 · Build 164: Keep what you found. A few lines, gathered by Claude when a conversation rests, kept on
  this device only if the person chooses ("Your thread"), with "Forget all of it". Aurasense keeps nothing.
  23 Oct 2026 · Build 163: the wiser voice's introduction is shown once a visit, never on repeat.""",
     'note at the top'),
    (""".gift .gift-s{font-size:.8rem;color:var(--faint);margin-top:8px}""",
     """.gift .gift-s{font-size:.8rem;color:var(--faint);margin-top:8px}
/* 23 Oct 2026 · Build 164 · Keep what you found, and the thread of what was kept */
.keepnote{font-size:.8rem;color:var(--faint);text-align:center;max-width:min(520px,92vw);margin:6px auto 0;line-height:1.45}
.thread .t-title{font-size:1.02rem;color:var(--ink)}
.thread .t-list{max-height:46vh;overflow-y:auto;-webkit-overflow-scrolling:touch;text-align:left;margin-top:6px}
.thread .t-item{margin:10px 0 0;padding-top:8px;border-top:1px solid rgba(233,181,106,.28);color:var(--ink)}
.thread .t-item p{margin:2px 0}
.thread .t-date{font-size:.78rem;color:var(--faint)}
.thread .t-wiser{font-style:italic}""",
     'styles'),
    ("""  <div class="gift hide" id="gift" role="note"></div>""",
     """  <div class="gift hide" id="gift" role="note"></div>
  <div class="gift thread hide" id="thread" role="region" aria-label="Your thread of light"></div>""",
     'the thread panel'),
    ("""   ['What I found, in my own words',function(){var w=S.turns.map(function(x){return x.rim;}).filter(Boolean);
      fin([{cls:'line soft',text:'In your own words:'}].concat(w.slice(-3).map(function(x){return {cls:'quote',text:x};})).concat([{cls:'line soft',text:'Only you wrote these. Keep them if they help.'}]));}],""",
     """   [canKeep()?'Keep what I found':'What I found, in my own words',function(){if(canKeep())keepFound();else ownWords();}],   /* 23 Oct 2026 · Build 164 */""",
     'the ending: keep what I found'),
    ("""function fin(parts){""",
     """/* their own words, as before (and whenever Claude can't gather a keepsake) */
function ownWords(){var w=S.turns.map(function(x){return x.rim;}).filter(Boolean);
  fin([{cls:'line soft',text:'In your own words:'}].concat(w.slice(-3).map(function(x){return {cls:'quote',text:x};})).concat([{cls:'line soft',text:'Only you wrote these. Keep them if they help.'}]));}
function fin(parts){""",
     'own words'),
    ("""/* is a listener switched on here? Asked once; the answer never takes longer than a second and a half */""",
     """/* ═══ 23 Oct 2026 · BUILD 164 · KEEP WHAT YOU FOUND ═══════════════════════════════════════════════════════
   Karl: "Already I feel like I wish I had those words I gave the mirror." When a conversation Claude listened to rests,
   Claude gathers a few lines: what they found (mostly their own words), the step they chose, their wiser self's last
   word. Kept on this device only, and only if they choose; each one adds to "Your thread". Aurasense keeps nothing.
   The Mutual Pause (philosophy record, 23 Oct): nothing here is for the AI; someone else using the device could read
   it, so it is offered, never automatic, said plainly, and one tap (then a second) forgets all of it. */
var THREAD_KEY='as_mirror_thread';
function canKeep(){return LS.live&&LS.choice==='claude'&&!LS.rest&&!LS.heavy&&LS.aiN>=2&&LS.turns.some(function(t){return t.role==='user';});}
function threadGet(){try{var a=JSON.parse(localStorage.getItem(THREAD_KEY)||'[]');
  return Array.isArray(a)?a.filter(function(x){return x&&typeof x.found==='string'&&x.found;}):[];}catch(e){return [];}}
function threadPut(k){try{var a=threadGet();
  a.push({at:new Date().toISOString().slice(0,10),found:String(k.found||'').slice(0,600),step:String(k.step||'').slice(0,300),wiser:String(k.wiser||'').slice(0,400)});
  if(a.length>60)a=a.slice(-60);localStorage.setItem(THREAD_KEY,JSON.stringify(a));return threadGet().length;}catch(e){return 0;}}
function threadForget(){try{localStorage.removeItem(THREAD_KEY);}catch(e){}}
function niceDate(d){try{var t=new Date(String(d)+'T12:00:00');if(isNaN(t))return String(d||'');return t.toLocaleDateString(undefined,{day:'numeric',month:'long',year:'numeric'});}catch(e){return String(d||'');}}
function plainWiser(w){return String(w||'').replace(/^[“"]+|[”"]+$/g,'');}
function keepText(k){var d=new Date();
  return 'What I found: '+k.found+(k.step?'\\nMy step: '+k.step:'')+(k.wiser?'\\nMy wiser self’s last word: “'+plainWiser(k.wiser)+'”':'')+
    '\\n— The Mirror, Aurasense · '+d.toISOString().slice(0,10);}
function copyText(t,done){
  var fallback=function(){try{var a=document.createElement('textarea');a.value=t;a.setAttribute('readonly','');a.style.position='fixed';a.style.top='0';a.style.opacity='0';
    document.body.appendChild(a);a.select();var ok=document.execCommand('copy');document.body.removeChild(a);return !!ok;}catch(e){return false;}};
  try{if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t).then(function(){done(true);},function(){done(fallback());});return;}}catch(e){}
  done(fallback());}
function keepFound(){
  $('doors').classList.add('hide');
  show([{cls:'line soft',text:'Gathering what you found…'}],S.first||'');
  setWho('Claude, an AI, is gathering a few lines for you to keep.');document.body.classList.add('listening');
  var ctl=null;try{ctl=new AbortController();}catch(e){}
  var timer=setTimeout(function(){try{if(ctl)ctl.abort();}catch(e){}},50000);
  var done=function(){clearTimeout(timer);document.body.classList.remove('listening');};
  fetch('/api/mirror',{method:'POST',headers:{'Content-Type':'application/json'},cache:'no-store',credentials:'same-origin',
    body:JSON.stringify({keep:true,turns:LS.turns.slice(-24)}),signal:ctl?ctl.signal:undefined})
  .then(function(r){return r.json().then(function(j){return j||{};},function(){return {ok:false};});})
  .then(function(v){done();
    var k=v&&v.keep;
    if(v.ok!==true||v.care===true||!k||typeof k.found!=='string'||!k.found.trim())throw {code:v.code||'upstream'};
    keepShow({found:String(k.found).trim(),step:typeof k.step==='string'?k.step.trim():'',wiser:typeof k.wiser==='string'?k.wiser.trim():''});})
  .catch(function(){done();setWho('Claude couldn’t gather it just then, so here are your own words.');ownWords();});
}
function keepShow(k){
  var parts=[{cls:'line soft',text:'What you found:'},{cls:'line',text:lsWhole(k.found,320)}];
  if(k.step)parts.push({cls:'line soft',text:'Your step:'},{cls:'line',text:lsWhole(k.step,160)});
  if(k.wiser)parts.push({cls:'line soft',text:'Your wiser self’s last word:'},{cls:'line aspire',text:'“'+lsWhole(plainWiser(k.wiser),240)+'”'});
  fin(parts);
  setWho('Gathered by Claude, an AI, from your conversation.');
  var r=$('after');
  var kb=el('button','btn lead','Keep it on this device');kb.type='button';
  var cb=el('button','btn quiet','Copy it');cb.type='button';
  kb.addEventListener('click',function(){if(kb.disabled)return;var n=threadPut(k);kb.disabled=true;kb.textContent=n?'Kept':'Not kept';
    setWho(n?('Kept on this device only. Your thread now holds '+n+(n===1?' line.':' lines.')):'This browser wouldn’t keep it. You can copy it instead.');refreshNote();});
  cb.addEventListener('click',function(){copyText(keepText(k),function(ok){setWho(ok?'Copied. Paste it wherever you keep things.':'Your browser didn’t allow copying. You can select the words in the circle instead.');});});
  r.insertBefore(cb,r.firstChild);r.insertBefore(kb,r.firstChild);
  var old=document.getElementById('keepnote');if(old)old.parentNode.removeChild(old);
  var nt=el('p','keepnote','Kept only on this device, and only if you choose. Aurasense keeps nothing. Anyone using this device could see it.');nt.id='keepnote';
  r.parentNode.insertBefore(nt,r.nextSibling);
}
/* Your thread: what was kept, newest first, with a way to forget all of it */
function threadShow(){
  var t=$('thread');if(!t)return;var a=threadGet();t.textContent='';
  t.appendChild(el('p','t-title','Your thread of light'));
  t.appendChild(el('p','gift-s','Kept on this device only. Aurasense keeps nothing.'));
  var list=el('div','t-list');
  a.slice().reverse().forEach(function(x){var it=el('div','t-item');
    it.appendChild(el('p','t-date',niceDate(x.at)));it.appendChild(el('p','',x.found));
    if(x.step)it.appendChild(el('p','','Your step: '+x.step));
    if(x.wiser)it.appendChild(el('p','t-wiser','“'+plainWiser(x.wiser)+'”'));
    list.appendChild(it);});
  if(!a.length)list.appendChild(el('p','','Nothing is kept on this device.'));
  t.appendChild(list);
  var row=el('div','row');
  var close=el('button','btn quiet','Close');close.type='button';close.addEventListener('click',function(){t.classList.add('hide');});
  row.appendChild(close);
  if(a.length){var forget=el('button','btn quiet','Forget all of it');forget.type='button';var armed=false;
    forget.addEventListener('click',function(){if(!armed){armed=true;forget.textContent='Tap again to forget all '+a.length;return;}
      threadForget();t.classList.add('hide');setWho('Forgotten. Nothing from the Mirror is kept on this device now.');refreshNote();});
    row.appendChild(forget);}
  t.appendChild(row);t.classList.remove('hide');
  try{t.scrollIntoView({block:'nearest',behavior:asStill()?'auto':'smooth'});}catch(e){}
}

/* is a listener switched on here? Asked once; the answer never takes longer than a second and a half */""",
     'keep what you found'),
    ("""  else n.appendChild(document.createTextNode('The Mirror is not a person, and not a therapist.'));
}""",
     """  else n.appendChild(document.createTextNode('The Mirror is not a person, and not a therapist.'));
  var tn=threadGet().length;   /* 23 Oct 2026 · Build 164 · what was kept, on this device */
  if(tn){n.appendChild(document.createTextNode(' '));var tb=el('button','lnk','Your thread ('+tn+')');tb.type='button';tb.addEventListener('click',threadShow);n.appendChild(tb);}
}""",
     'your thread, beneath'),
])

edit('/home/claude/work/privacy.163.html', '/home/claude/aurasense/privacy.html', [
    ("""<strong>Aurasense keeps none of it</strong>: not in our database, not in logs, and not on your device.</li>""",
     """<strong>Aurasense keeps none of it</strong>: not in our database, not in logs, and not on your device.</li>
<li id="keep"><strong>Keep what you found (optional).</strong> When you let a conversation rest, Claude can gather a few lines from it: what you found, the step you chose, and your wiser self's last word. Gathering them sends the conversation to Claude once more, in the same way. <strong>If you choose to keep them, they are kept in your browser on this device only</strong>, as "Your thread", until you choose <em>Forget all of it</em> (or clear your browser's data). <strong>Aurasense never receives them.</strong> Anyone who uses this device could see them.</li>""",
     'privacy: keep what you found'),
    ("""and what you notice after an offering (whether a sense changed, and any words you write about it) all live in your browser's storage on your own device.""",
     """what you notice after an offering (whether a sense changed, and any words you write about it), and any lines you choose to keep from the Mirror all live in your browser's storage on your own device.""",
     'privacy: on your device'),
    ('<div class="sub">Plain language on purpose. Last updated: 22 October 2026.</div>',
     '<div class="sub">Plain language on purpose. Last updated: 23 October 2026.</div>', 'privacy: date'),
])

edit('/home/claude/work/index-mapbox.163.html', '/home/claude/aurasense/index-mapbox.html', [
    ('Build <span class="bs-l">23 Oct 2026 · </span>163<span class="bs-l"> · tap to refresh</span>',
     'Build <span class="bs-l">23 Oct 2026 · </span>164<span class="bs-l"> · tap to refresh</span>', 'map stamp')])
edit('/home/claude/work/seeking.163.html', '/home/claude/aurasense/seeking.html', [
    ('>Build 23 Oct 2026 &middot; 163', '>Build 23 Oct 2026 &middot; 164', 'seeking stamp')])
