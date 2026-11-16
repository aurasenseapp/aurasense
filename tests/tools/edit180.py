"""Build 180 · join the new Mirror to the map. Run once from the repo root. Every replacement is asserted."""
import io
def sub(s, a, b, n=1):
    assert s.count(a) == n, (s.count(a), a[:70])
    return s.replace(a, b)

# ───────── the Mirror page ─────────
p = 'mirror.html'; s = io.open(p, encoding='utf-8').read()
s = sub(s, """<button id="back" class="lnk hide" type="button">Back to the map</button></header>""",
"""<span><button id="older" class="lnk hide" type="button">Your balance of light</button> <button id="back" class="lnk hide" type="button">Back to the map</button></span></header>""")
s = sub(s, """  card.appendChild(el('p','','This is what would be offered, for other people, and AI, to learn from. It carries no name. Change any word you like.'));""",
"""  card.appendChild(el('p','','This is what would be offered, for other people, and AI, to learn from. It carries no name. Change any word you like.'));
  if(inSite)card.appendChild(el('p','small soft','The map will place it in the area where you are now, never at your door.'));""")
s = sub(s, """  row.appendChild(btn('btn','Hold it ready for the map',function(){""", """  row.appendChild(btn('btn',inSite?'Offer it to the map':'Hold it ready for the map',function(){""")
s = sub(s, """    var a=list('as_mirror_offers');a.push({at:new Date().toISOString().slice(0,10),text:t,words:p.words,fresh:p.fresh,word:p.word,working:p.working});
    if(put""", """    /* Build 180 · inside the map, the sense goes to the map itself, which places it in the area the person is in.
       Only the offered sentence and its symbols go: never the conversation. This conversation waits here meanwhile. */
    if(inSite){M.sent=true;waitMap();
      try{window.parent.postMessage({as:'mirror',act:'offer',text:t,words:(p.words||[]).slice(0,4),fresh:!!p.fresh,working:str(p.working,60)},location.origin);}
      catch(e){M.sent=false;notOffered();}
      return;}
    var a=list('as_mirror_offers');a.push({at:new Date().toISOString().slice(0,10),text:t,words:p.words,fresh:p.fresh,word:p.word,working:p.working});
    if(put""")
s = sub(s, """function keptShow(){""", """function waitMap(){
  var b=$('close');b.textContent='';var card=el('div','card');card.appendChild(el('h2','','Going to the map'));
  card.appendChild(el('p','','The map is finding the area you are in. This conversation waits here.'));b.appendChild(card);
}
function notOffered(){
  if(!M.close){$('close').classList.add('hide');$('close').textContent='';$('say').classList.remove('hide');return;}
  closeShow();var n=el('p','small','It was not offered. Your sense is still here.');n.setAttribute('role','status');$('close').insertBefore(n,$('close').firstChild);
}
function landed(area){
  var b=$('close');b.textContent='';var card=el('div','card');card.appendChild(el('h2','','Offered to the map'));
  card.appendChild(el('p','','It rests '+(area?'in the area of '+area:'in the area where you are')+', with no name. Other people, and AI, can learn from it.'));b.appendChild(card);
  var row=el('div','row');
  row.appendChild(btn('btn','Carry on with this conversation',function(){b.classList.add('hide');b.textContent='';$('say').classList.remove('hide');try{$('words').focus();}catch(e){}}));
  row.appendChild(btn('btn quiet','Begin a new one',again));b.appendChild(row);
  M.close=null;refreshNote();
}
function keptShow(){""")
# the open place for the third: kept beside a meeting of inner and outer, on this device only
s = sub(s, """  a.push({at:new Date().toISOString().slice(0,10),sensed:c.sensed,words:p.words,fresh:p.fresh,word:p.word,working:p.working,learned:c.learned});
  if(put('as_mirror_senses',JSON.stringify(a.slice(-60))))ended('Kept','It is kept on this device only. No one else can see it, and you can let it go whenever you like.');""",
"""  var rec={at:new Date().toISOString().slice(0,10),sensed:c.sensed,words:p.words,fresh:p.fresh,word:p.word,working:p.working,learned:c.learned};
  /* Build 180 · Karl, 16 Nov: the third meaning is left for the person to discover. So a kept meeting of inner and
     outer holds an open place beside it, to fill whenever that arrives. On this device only. */
  var meet=(p.words||[]).indexOf('Synchronicity')>-1;if(meet)rec.third='';
  a.push(rec);
  if(put('as_mirror_senses',JSON.stringify(a.slice(-60))))ended('Kept','It is kept on this device only. No one else can see it, and you can let it go whenever you like.'+(meet?' An open place is kept beside it, for what the two say together, whenever that arrives.':''));""")
s = sub(s, """  a.slice().reverse().forEach(function(k){if(!k||typeof k!=='object')return;var card=el('div','card');""",
"""  a.slice().reverse().forEach(function(k,ri){if(!k||typeof k!=='object')return;var at=a.length-1-ri,card=el('div','card');""")
s = sub(s, """    card.appendChild(el('p','',str(k.sensed,320)));b.appendChild(card);});""",
"""    card.appendChild(el('p','',str(k.sensed,320)));
    if(typeof k.third==='string'){var t3=el('div','side third');t3.appendChild(el('span','tag','What the two say together'));
      var lb=el('label','sr','What the two say together');lb.htmlFor='third'+at;t3.appendChild(lb);
      var ti=el('input','');ti.type='text';ti.id='third'+at;ti.maxLength=200;ti.value=str(k.third,200);ti.placeholder='An open place, for whenever it arrives';t3.appendChild(ti);
      var ts=el('p','small soft','');ts.setAttribute('role','status');
      t3.appendChild(btn('btn quiet','Keep',function(){var v=str(ti.value,200);if(HEAVY.test(norm(v))){care('');return;}
        var all=list('as_mirror_senses');if(!all[at]||typeof all[at]!=='object'||typeof all[at].third!=='string'){ts.textContent='This device would not keep it.';return;}
        all[at].third=v;ts.textContent=put('as_mirror_senses',JSON.stringify(all))?(v?'Kept on this device only.':'The place is open again.'):'This device would not keep it.';}));
      t3.appendChild(ts);card.appendChild(t3);}
    b.appendChild(card);});""")
s = sub(s, """if(inSite){$('back').classList.remove('hide');$('back').addEventListener('click',function(){tell('close');});
  document.addEventListener('keydown',function(e){if(e.key==='Escape')tell('close');});}""",
"""if(inSite){$('back').classList.remove('hide');$('back').addEventListener('click',function(){tell('close');});
  $('older').classList.remove('hide');$('older').addEventListener('click',function(){tell('classic');});
  document.addEventListener('keydown',function(e){if(e.key==='Escape')tell('close');});
  /* Build 180 · the map answers: only Aurasense's own page is listened to, and only these four plain messages. */
  addEventListener('message',function(e){try{
    if(e.origin!==location.origin||e.source!==window.parent)return;var m=e.data||{};if(m.as!=='mirror-host')return;
    if(m.act==='landed'){if(M.sent){M.sent=false;landed(str(m.area,80));}}
    else if(m.act==='held'){if(M.sent){M.sent=false;notOffered();}}
    else if(m.act==='fresh'){M.sent=false;again();}
    else if(m.act==='begin'){if(!$('thread').children.length&&!$('words').value)$('words').value=str(m.a,600);}
  }catch(x){}});}""")
io.open(p, 'w', encoding='utf-8').write(s)

# ───────── the map ─────────
p = 'index-mapbox.html'; s = io.open(p, encoding='utf-8').read()
s = sub(s, """async function reverseAddress(lat,lng){
  try{""", """async function reverseAddress(lat,lng){
  try{var _ma=mirrorAreaFor(lat,lng);if(_ma)return _ma.name||'this area';}catch(e){}   /* Build 180: a sense from the Mirror is named by its area, never a door */
  try{""")
s = sub(s, """async function lookupPlace(lat,lng){
  try{""", """async function lookupPlace(lat,lng){
  try{var _ma=mirrorAreaFor(lat,lng);if(_ma)return _ma.name||null;}catch(e){}           /* Build 180: the same, for the place that is stored */
  try{""")
s = sub(s, """  const loc=placeLabel||'this spot';
  const sym=SENSE_SYMBOLS[senseId]||'';
  const safeText=(text||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');""",
"""  /* Build 180 · a sense that came from the Mirror shows its Alphasense symbols when its aura is tapped (Karl: "Only
     when an aura is tapped does a symbol show"), and its place is told as the street it is near, never a door. */
  let _mp=null;try{_mp=mirrorParse(text);}catch(e){_mp=null;}
  const loc=_mp?mirrorNear(placeLabel):(placeLabel||'this spot');
  const sym=SENSE_SYMBOLS[senseId]||'';
  const safeText=(_mp?_mp.text:(text||'')).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');""")
s = sub(s, """    <div class="pop-aura" style="color:${s.color}">${sym} ${s.label}</div>
    <div class="pop-sense-list">${listInner}</div>
    <div class="pop-action pop-link pop-seeaura\"""", """    ${_mp?mirrorPopLine(_mp):`<div class="pop-aura" style="color:${s.color}">${sym} ${s.label}</div>`}
    <div class="pop-sense-list">${listInner}</div>
    <div class="pop-action pop-link pop-seeaura\"""")
old_open = s[s.index("function mirrorOpen(opts){"):s.index("function mirrorOpenClassic(){")]
assert "fr.src='/mirror-living.html?in=site'" in old_open
new_open = r"""function mirrorOpen(opts){
  try{
    /* Build 180 · the Mirror may be waiting underneath while a sense lands on the map: opening it again brings
       back the same conversation. */
    var old=document.getElementById('as-living-mirror');
    if(old){if(old.classList.contains('away')&&typeof old._back==='function')old._back();return;}
    var ov=document.createElement('div');ov.id='as-living-mirror';ov.setAttribute('role','dialog');ov.setAttribute('aria-label','The Mirror');
    /* Build 180 · Karl's go-ahead, 16 Nov: the new Mirror ("What are you sensing?") is the Mirror of the map. */
    var fr=document.createElement('iframe');fr.src='/mirror.html?in=site';fr.title='The Mirror';
    fr.setAttribute('referrerpolicy','no-referrer');fr.setAttribute('sandbox','allow-scripts allow-same-origin allow-popups allow-popups-to-escape-sandbox');
    /* 6 Oct 2026 · from the guiding light: the Mirror begins with the same question, and their own words wait, unsent */
    if(opts&&opts.q){fr.addEventListener('load',function(){try{fr.contentWindow.postMessage({as:'mirror-host',act:'begin',q:String(opts.q).slice(0,300),a:String(opts.a||'').slice(0,600),kind:String(opts.kind||'')},location.origin);}catch(e){}},{once:true});}
    ov.appendChild(fr);document.body.appendChild(ov);
    requestAnimationFrame(function(){ov.classList.add('on');});
    var gone=false;
    var shut=function(then){gone=true;try{mirrorLandCard(null);}catch(e){}try{ov.classList.remove('on');setTimeout(function(){try{ov.remove();}catch(e){}if(then)then();},450);}catch(e){}};
    var post=function(m){try{m.as='mirror-host';fr.contentWindow.postMessage(m,location.origin);}catch(e){}};
    var away=function(){ov.classList.remove('on');ov.classList.add('away');};
    var back=function(){try{mirrorLandCard(null);}catch(e){}if(gone)return;ov.classList.remove('away');requestAnimationFrame(function(){ov.classList.add('on');});};
    ov._back=back;
    var onMsg=function(e){
      try{if(e.origin!==location.origin||e.source!==fr.contentWindow)return;
        var m=e.data||{};if(m.as!=='mirror')return;
        if(m.act==='close'){removeEventListener('message',onMsg);shut();}
        else if(m.act==='classic'){removeEventListener('message',onMsg);shut(function(){try{mirrorOpenClassic();}catch(x){}});}
        else if(m.act==='offer'){away();mirrorOffer(m,{post:post,back:back,alive:function(){return !gone;}});}
      }catch(x){}};
    addEventListener('message',onMsg);
    var esc=function(e){if(e.key==='Escape'){if(ov.classList.contains('away'))return;removeEventListener('keydown',esc);removeEventListener('message',onMsg);shut();}};
    addEventListener('keydown',esc);
  }catch(e){try{mirrorOpenClassic();}catch(x){}}
}
/* ════════════════════════════════════════════════════════════════════════
   A SENSE FROM THE MIRROR REACHES THE MAP · Build 180 · 16 Nov 2026
   Karl: once the symbol is chosen, the person offers it to the map where they are now; "Soften the place: yes".
   · Only the one offered sentence and its symbols travel. Never the conversation.
   · The place is softened to the area (a cell about a kilometre across), so a sense never rests on a doorstep,
     and it is named by its area, never an address.
   · The symbols travel inside the words themselves, after a small star, so nothing new is stored and every
     older page still reads the offering as plain words. Only Alphasense's own words are ever drawn.
   · The Mirror waits underneath, so the person can go back to the same conversation or begin a new one.
   ════════════════════════════════════════════════════════════════════════ */
var AS_MIRROR_AREAS=[];
function mirrorAreaFor(lat,lng){
  for(var i=AS_MIRROR_AREAS.length-1;i>=0;i--){var a=AS_MIRROR_AREAS[i];if(haversine(a.lat,a.lng,lat,lng)<90)return a;}
  return null;
}
function mirrorSoftPoint(lat,lng){
  var STEP=0.009;                                             /* about a kilometre */
  var c=Math.max(0.2,Math.cos(lat*Math.PI/180)),stepLng=STEP/c;
  var gl=Math.round(lat/STEP)*STEP,gn=Math.round(lng/stepLng)*stepLng;
  /* a random drift inside the cell: it carries nothing about where the person stood */
  gl+=(Math.random()-0.5)*STEP*0.6; gn+=(Math.random()-0.5)*stepLng*0.6;
  return {lat:+gl.toFixed(6),lng:+gn.toFixed(6)};
}
function mirrorArea(lat,lng){
  var ask=(async function(){
    try{
      var r=await fetch('https://api.mapbox.com/geocoding/v5/mapbox.places/'+lng+','+lat+'.json?access_token='+MAPBOX_TOKEN+'&types=neighborhood,locality,place&limit=1');
      var d=await r.json(),f=d&&d.features&&d.features[0];if(!f)return '';
      var name=String(f.text||'').slice(0,60),town='';
      (f.context||[]).forEach(function(cx){if(String(cx.id||'').indexOf('place')===0)town=String(cx.text||'').slice(0,60);});
      return (town&&town!==name)?(name+', '+town):name;
    }catch(e){return '';}
  })();
  return Promise.race([ask,new Promise(function(res){setTimeout(function(){res('');},5000);})]);
}
function mirrorKind(words){
  for(var i=0;i<words.length;i++){var w=String(words[i]).toLowerCase();
    var s=SENSES.find(function(x){return String(x.id).indexOf('ns-')!==0&&String(x.label).toLowerCase()===w;});if(s)return s.id;}
  return 'intuition';
}
function mirrorSuffix(words,fresh,working){
  if(!words.length)return '';
  var j=words.join(' + ');
  return ' ✧ '+(fresh?('new sense: '+(working||'not yet named')+' ('+j+')'):j);
}
function mirrorParse(text){
  var t=String(text||''),i=t.lastIndexOf(' ✧ ');if(i<0)return null;
  var tail=t.slice(i+3),fresh=false,working='',m=/^new sense: ([^()]{1,60}) \(([^()]{1,120})\)$/.exec(tail);
  if(m){fresh=true;working=m[1];tail=m[2];}
  var ws=tail.split(' + ');if(!ws.length||ws.length>4)return null;
  var out=[];
  for(var k=0;k<ws.length;k++){var a=null;for(var q=0;q<ALPHA_WORDS.length;q++){if(ALPHA_WORDS[q].w===ws[k]){a=ALPHA_WORDS[q];break;}}if(!a)return null;out.push(a);}
  return {text:t.slice(0,i),words:out,fresh:fresh,working:working};
}
function mirrorNear(place){
  var p=String(place||'').split(',')[0].replace(/^\s*\d+[A-Za-z]?\s*[-–]?\s*\d*\s+/,'').trim();
  if(!p||/^-?\d/.test(p))return 'this area';
  for(var i=0;i<AS_MIRROR_AREAS.length;i++){if(AS_MIRROR_AREAS[i].name===place)return String(place);}
  return 'near '+p;
}
function mirrorPopLine(mp){
  var names=mp.words.map(function(a){return a.w;}).join(' + '),col=mp.words[0].c,g;
  if(mp.fresh)g=fuseGlyphs(mp.words,30);
  else g=mp.words.map(function(a){return alphaGlyph(a,26);}).join('');
  var line=mp.fresh?('“'+escT(mp.working)+'” · a new sense, near '+escT(names)):escT(names);
  return '<div class="pop-aura pop-mirror" style="color:'+col+'"><span style="display:inline-flex;vertical-align:middle;gap:2px;margin-right:6px">'+g+'</span>'+line+'</div>';
}
function mirrorLandCard(o){
  var old=document.getElementById('as-mirror-land');if(old)old.remove();
  if(!o)return;
  var d=document.createElement('div');d.id='as-mirror-land';d.setAttribute('role','status');
  var t=document.createElement('div');t.className='ml-t';t.textContent=o.text;d.appendChild(t);
  var row=document.createElement('div');row.className='ml-row';
  (o.buttons||[]).forEach(function(b){var x=document.createElement('button');x.type='button';x.textContent=b[0];if(b[2])x.className='ml-quiet';
    x.addEventListener('click',function(){try{b[1]();}catch(e){}});row.appendChild(x);});
  d.appendChild(row);document.body.appendChild(d);
  requestAnimationFrame(function(){d.classList.add('on');});
}
function mirrorOffer(m,h){
  var held=function(why,stay){try{h.post({act:'held'});}catch(e){}if(!stay)h.back();if(why)setTimeout(function(){try{showMsg(why,7000);}catch(e){}},700);};
  try{
    var text=String(m.text||'').replace(/\s+/g,' ').trim().slice(0,220);
    var words=(Array.isArray(m.words)?m.words:[]).map(function(x){return String(x);}).filter(function(x){return ALPHA_WORDS.some(function(a){return a.w===x;});}).slice(0,4);
    var fresh=!!m.fresh&&words.length>0;
    var working=String(m.working||'').replace(/[()✧]/g,' ').replace(/\s+/g,' ').trim().slice(0,60);
    if(!text||text.indexOf(' ✧ ')>-1){held('');return;}
    if(typeof guardOK==='function'&&!guardOK(text)){held('',true);return;}
    var full=text+mirrorSuffix(words,fresh,working),kind=mirrorKind(words);
    var land=function(lat,lng){
      var p=mirrorSoftPoint(lat,lng);
      mirrorArea(p.lat,p.lng).then(function(name){
        if(!h.alive())return;
        try{
          AS_MIRROR_AREAS.push({lat:p.lat,lng:p.lng,name:name||''});
          try{map.jumpTo({center:[p.lng,p.lat],zoom:Math.max(14.6,Math.min(16,map.getZoom()))});}catch(e){}
          var was=selSense;selSense=kind;
          try{submit(p.lat,p.lng,full);}finally{selSense=was;}
          h.post({act:'landed',area:name||''});
          setTimeout(function(){if(!h.alive())return;
            mirrorLandCard({text:'✧ Your sense rests '+(name?'in the area of '+name:'in the area where you are')+'.',
              buttons:[['Back to the Mirror',h.back],['Begin a new one',function(){h.post({act:'fresh'});h.back();}],['Stay on the map',function(){mirrorLandCard(null);},1]]});},4200);
        }catch(e){held('The map could not take it just now. Your sense is still in the Mirror.');}
      });
    };
    var ask=function(){
      mirrorLandCard({text:'Your device keeps its place to itself. Your sense can rest in the area the map is showing, or wait in the Mirror.',
        buttons:[['Offer it where the map is looking',function(){mirrorLandCard(null);var c=map.getCenter();land(c.lat,c.lng);}],['Back to the Mirror',function(){held('');},1]]});
    };
    try{showMsg('Finding the area you are in…',5000);}catch(e){}
    if(!navigator.geolocation){ask();return;}
    var done=false,tm=setTimeout(function(){if(!done){done=true;ask();}},15000);
    navigator.geolocation.getCurrentPosition(function(pos){if(done)return;done=true;clearTimeout(tm);land(pos.coords.latitude,pos.coords.longitude);},
      function(){if(done)return;done=true;clearTimeout(tm);ask();},{enableHighAccuracy:false,maximumAge:600000,timeout:12000});
  }catch(e){held('The map could not take it just now. Your sense is still in the Mirror.');}
}
"""
s = s.replace(old_open, new_open)
s = sub(s, """#as-living-mirror.on{opacity:1}""", """#as-living-mirror.on{opacity:1}
#as-living-mirror.away{opacity:0;visibility:hidden;pointer-events:none;transition:opacity .45s ease,visibility 0s .45s}
#as-mirror-land{position:fixed;left:50%;top:max(14px,env(safe-area-inset-top));transform:translate(-50%,-12px);z-index:2600;width:min(92vw,430px);box-sizing:border-box;padding:13px 15px 12px;border-radius:16px;background:rgba(20,16,38,.94);border:1px solid rgba(196,181,253,.45);box-shadow:0 10px 34px rgba(0,0,0,.45);color:#f3eeff;font:15px/1.45 system-ui,-apple-system,'Segoe UI',sans-serif;opacity:0;transition:opacity .5s ease,transform .5s ease}
#as-mirror-land.on{opacity:1;transform:translate(-50%,0)}
#as-mirror-land .ml-row{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}
#as-mirror-land button{min-height:44px;padding:9px 14px;border-radius:999px;border:1px solid rgba(196,181,253,.7);background:rgba(196,181,253,.2);color:#fff;font:inherit;font-size:14px;cursor:pointer}
#as-mirror-land button.ml-quiet{background:transparent;border-color:rgba(196,181,253,.3);color:#d9cffb}
#as-mirror-land button:focus-visible{outline:2px solid #fff;outline-offset:2px}
@media (prefers-reduced-motion: reduce){#as-mirror-land{transition:none}}""")
io.open(p, 'w', encoding='utf-8').write(s)
print('ok')
