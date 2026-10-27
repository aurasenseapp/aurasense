"""Build 168 · the Mirror (27 Oct 2026): the Mirror's two places, Let it go and The Re-minding, inside the Mirror.
Karl, 25 Oct: "Where we 'bin' useless recurring thoughts and place those we want re-minding of ..." On draft 2:
"real slower motion crumpling ... slower more detailed burn to see the words going up in flame and disintegrating"
and "Build 168 with the paper line, yes." The shared code (TP CSS and TP MODULE) is copied, unchanged, from the
study page that was walked in a real browser (draft 3), so what Karl felt is exactly what goes live.
- From the Mirror's opening: a quiet "A thought that keeps coming back?" opens both places.
- At a conversation's end: only the one that fits is offered (a circling thought: Let a thought go; otherwise, when
  there was a real conversation: Keep something for when it's needed). Never after heavy words.
- After "Keep what I found": "Seal it for when it's needed".
- In a conversation, when the person's words match a moment something was kept for: a quiet offer, once.
Always starts from the live 167 page; re-runnable."""
import io, re

STUDY = '/home/claude/work/out/two-places/the-two-places.html'
SRC = '/home/claude/work/mirror-living.167.html'
DST = '/home/claude/aurasense/mirror-living.html'
st = io.open(STUDY, encoding='utf-8').read()
s = io.open(SRC, encoding='utf-8').read()

def between(text, a, b):
    i = text.index(a); j = text.index(b, i) + len(b); return text[i:j]
TP_CSS = between(st, '/* ══ TP CSS BEGIN', '/* ══ TP CSS END ══ */')
TP_MODULE = between(st, '/* ══ TP MODULE BEGIN', '/* ══ TP MODULE END ══ */')
assert 'function TwoPlaces(env)' in TP_MODULE and '.tpfx{' in TP_CSS

def rep(old, new, label, count=1):
    global s
    c = s.count(old)
    assert c == count, (label, c)
    s = s.replace(old, new)
    print('ok', label)

rep("""  23 Oct 2026 · Build 165: once, a quiet line under the little lights: "Tap a light to see that moment again."
""", """  23 Oct 2026 · Build 165: once, a quiet line under the little lights: "Tap a light to see that moment again."
  27 Oct 2026 · Build 168: the Mirror's two places. Let it go: the thought on paper, crumpled slowly, a deep breath,
  then into the fire, where the words char and fall away as ash and light. The Re-minding: folded, sealed, kept on
  this device for the moment it is needed. Nothing written in either ever leaves the device.
""", 'header note')
rep("""</style>""", TP_CSS + """
/* Build 168 · the quiet way in, and the quiet offer in a conversation */
#tpRow .btn{font-size:.92rem}
#tpPeek .quote{font-size:clamp(.98rem,3.4vw,1.12rem)}
</style>""", 'styles')
rep("""    <div class="speak" id="speak" aria-live="polite"></div>
  </div>
""", """    <div class="speak" id="speak" aria-live="polite"></div>
  </div>
  <p class="tpguide dim hide" id="tpGuide" aria-live="polite"></p>
  <div class="tpsay hide" id="tpSay"><textarea id="tpWords" rows="2" maxlength="280" aria-label="Your words"></textarea></div>
  <div class="tpdoors hide" id="tpDoors" role="group" aria-label="Let it go, or keep it"></div>
  <p class="who hide" id="tpWho" role="status"></p>
  <div class="tplist hide" id="tpList"></div>
  <p class="note hide" id="tpNote">Nothing you write here leaves this device. Aurasense never sees it.</p>
""", 'the two places, beneath the circle')
rep("""  <div class="doors" id="doors" role="group" aria-label="Ways to begin"></div>
""", """  <div class="doors" id="doors" role="group" aria-label="Ways to begin"></div>
  <p class="note hide" id="tpRow"></p>
""", 'the quiet way in')
rep("""    <button class="btn lead" id="send" type="button">Offer it</button>
  </div>
""", """    <button class="btn lead" id="send" type="button">Offer it</button>
  </div>
  <div class="gift tplist hide" id="tpPeek" role="note"></div>
""", 'the quiet offer')

# the opening: the quiet way in appears with the doors
rep("""show(openParts(),'');d.classList.remove('hide');""", """show(openParts(),'');d.classList.remove('hide');tpRowShow();""", 'opening shows the way in', 2)
rep("""else{show(openParts(),'');$('doors').classList.remove('hide');}""", """else{show(openParts(),'');$('doors').classList.remove('hide');tpRowShow();}""", 'not now shows the way in')
rep("""function begin(i){
  S.door=i; $('doors').classList.add('hide');""", """function begin(i){
  S.door=i; $('doors').classList.add('hide'); tpRowHide();""", 'a conversation hides the way in')
rep("""  S.door=-1; $('doors').classList.add('hide'); $('say').classList.remove('hide');
  ask({q:q,plain:q,kind:kind||'guide'});""", """  S.door=-1; $('doors').classList.add('hide'); tpRowHide(); $('say').classList.remove('hide');
  ask({q:q,plain:q,kind:kind||'guide'});""", 'a conversation from the map hides it too')
# the ending: only the place that fits
rep("""  ].forEach(function(o){var b=el('button','door',o[0]);b.type='button';b.addEventListener('click',o[1]);d.appendChild(b);});
}""", """  ].forEach(function(o){var b=el('button','door',o[0]);b.type='button';b.addEventListener('click',o[1]);d.appendChild(b);});
  tpRestDoor(d);   /* 27 Oct 2026 · Build 168 */
}""", 'the ending offers the place that fits')
# after Keep what I found: seal it for when it's needed
rep("""  r.insertBefore(cb,r.firstChild);r.insertBefore(kb,r.firstChild);""", """  r.insertBefore(cb,r.firstChild);r.insertBefore(kb,r.firstChild);
  var sb=el('button','door seal','Seal it for when it’s needed');sb.type='button';   /* 27 Oct 2026 · Build 168 */
  sb.addEventListener('click',function(){tpEnter('rest');TP.keepStart(tpKeepText(k));});
  r.appendChild(sb);""", 'a keepsake can be sealed for its moment')
# in a conversation: the quiet offer, once
rep("""  $('words').value='';dwHide();LS.lastWords=raw;""", """  $('words').value='';dwHide();LS.lastWords=raw;tpPeekMaybe(raw);""", 'a matching moment is offered quietly')

GLUE = TP_MODULE + r"""

/* ═══ 27 Oct 2026 · BUILD 168 · THE MIRROR'S TWO PLACES, INSIDE THE MIRROR ══════════════════════════════════
   The shared code above is the study Karl felt (draft 3). Here it is given the Mirror's own circle and words.
   While it is open, the Mirror's own choices step aside; leaving puts back exactly what was there. */
var TP_UI=['doors','say','after','trail','who','gift','thread','lsAsk','note','classicRow','tpRow','tpPeek'];
var TPE={from:'',hidden:[],peeked:false,said:[]};
var TP_LOOP=/\b(?:keeps? (?:thinking|going back|coming back|replaying|telling myself|wondering)|i keep|can'?t stop (?:thinking|worrying)|over and over|again and again|round and round|on repeat|replay\w*|loop\w*|spiral\w*|won'?t leave me alone|stuck in my head|ruminat\w*|same thoughts?|cycl\w*|circl\w*)\b/i;
var TPENV={mirror:$('mirror'), guide:$('tpGuide'), doors:$('tpDoors'), say:$('tpSay'), words:$('tpWords'), list:$('tpList'), HEAVY:HEAVY, fadeMs:1150,
  show:function(parts){show(parts,'');},
  setWho:function(t){var w=$('tpWho');w.textContent=t||'';w.classList.toggle('hide',!t);},
  care:function(){var from=TPE.from;tpLeave();care();if(from==='rest')tpAfter();},
  home:function(){if(TPE.from==='rest')tpExit('back');else TP.home();},
  exit:function(kind){tpExit(kind);}};
var TP=TwoPlaces(TPENV);
function tpEnter(from){
  if(TP.isActive())return;
  TPE.from=from;TPE.hidden=[];
  try{dwHide();}catch(e){}
  TP_UI.forEach(function(id){var e=$(id);if(e&&!e.classList.contains('hide')){e.classList.add('hide');TPE.hidden.push(id);}});
  var h=$('trailHint');if(h&&!h.hidden){TPE.hint=true;h.classList.add('hide');}
  $('tpGuide').classList.remove('hide');$('tpNote').classList.remove('hide');
  TPENV.backLabel=from==='open'?'Back to the Mirror':'';
}
function tpLeave(){
  TP.stop();$('tpGuide').classList.add('hide');$('tpNote').classList.add('hide');TPENV.setWho('');
  TPE.hidden.forEach(function(id){var e=$(id);if(e)e.classList.remove('hide');});TPE.hidden=[];
  var h=$('trailHint');if(h)h.classList.remove('hide');
}
function tpExit(kind){
  var from=TPE.from;tpLeave();TPE.from='';
  if(from==='open'){show(openParts(),'');tpRowShow();return;}
  if(kind==='back'){rest();return;}
  fin([{cls:'line',text:kind==='let-done'?'You let a thought go.':kind==='keep-done'?'You sealed something for when it’s needed.':'You were listened to, just as you are.'}]);
}
/* after heavy words, from the ending: a way to begin again, and nothing else */
function tpAfter(){var r=$('after');r.textContent='';r.classList.remove('hide');var b=el('button','btn quiet','Begin again');b.type='button';
  b.addEventListener('click',function(){location.reload();});r.appendChild(b);
  if(inSite){var hb=el('button','btn quiet','← Back to the map');hb.type='button';hb.addEventListener('click',function(){tell('close');});r.appendChild(hb);}}
function tpRowShow(){
  var r=$('tpRow');if(!r||S.turns.length)return;r.textContent='';
  var b=el('button','btn quiet','A thought that keeps coming back? →');b.type='button';b.id='tpEnter';
  b.addEventListener('click',function(){tpEnter('open');TP.home();});r.appendChild(b);
  var n=TP.count();
  if(n){var k=el('button','btn quiet','What I’ve kept ('+n+')');k.type='button';k.id='tpKept';k.addEventListener('click',function(){tpEnter('open');TP.list();});r.appendChild(k);}
  r.classList.remove('hide');
}
function tpRowHide(){var r=$('tpRow');if(r)r.classList.add('hide');}
/* the ending: offer only the place that fits this conversation */
function tpUserWords(){return (TPE.said.join(' ')+' '+String(S.first||'')).replace(/[‘’ʼ]/g,"'");}
function tpRestDoor(d){
  if(LS.heavy||!S.turns.length)return;
  var circling=S.door===2||S.theme==='cycle'||TP_LOOP.test(tpUserWords()), b;
  if(circling){b=el('button','door ember','Let a thought go');b.addEventListener('click',function(){tpEnter('rest');TP.letStart();});}
  else if(!canKeep()&&(LS.aiN>=2||S.turns.length>=3)){b=el('button','door seal','Keep something for when it’s needed');b.addEventListener('click',function(){tpEnter('rest');TP.keepStart();});}
  if(b){b.type='button';d.appendChild(b);}
}
function tpKeepText(k){
  var t=String(k.found||'').trim()+(k.step?' My step: '+String(k.step).trim():'');
  if(t.length<=280)return t;
  t=t.slice(0,279);var sp=t.lastIndexOf(' ');return (sp>200?t.slice(0,sp):t)+'…';
}
function tpPeekMaybe(raw){
  TPE.said.push(String(raw||'').slice(0,1200));if(TPE.said.length>40)TPE.said.shift();
  if(TPE.peeked||!TP.count())return;
  var ids=TP.matches(raw);
  if(ids.length&&TP.peek(ids,$('tpPeek')))TPE.peeked=true;
}
"""
rep("""$('send').addEventListener('click',hear);""", GLUE + """$('send').addEventListener('click',hear);""", 'the two places, given the Mirror')

assert s.count('function TwoPlaces(env)') == 1
io.open(DST, 'w', encoding='utf-8').write(s)
print('written', DST, len(s))

def edit(src, dst, old, new, label):
    t = io.open(src, encoding='utf-8').read()
    assert t.count(old) == 1, (label, t.count(old))
    io.open(dst, 'w', encoding='utf-8').write(t.replace(old, new)); print('ok', label)
edit('/home/claude/work/index-mapbox.167.html', '/home/claude/aurasense/index-mapbox.html',
     'Build <span class="bs-l">25 Oct 2026 · </span>167<span class="bs-l"> · tap to refresh</span>',
     'Build <span class="bs-l">27 Oct 2026 · </span>168<span class="bs-l"> · tap to refresh</span>', 'map stamp')
edit('/home/claude/work/seeking.167.html', '/home/claude/aurasense/seeking.html',
     '>Build 25 Oct 2026 &middot; 167', '>Build 27 Oct 2026 &middot; 168', 'seeking stamp')
