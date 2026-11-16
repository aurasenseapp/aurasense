"""Build 177 · the new Mirror's naming: one symbol, symbols together, or a new symbol formed in the moment.
python3 edit177page.py   (test-only tool: never part of the real site)"""
import io
P = '/home/claude/aurasense/mirror.html'
s = io.open(P, encoding='utf-8').read()
assert 'Build 177' not in s
def once(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:70]); s = s.replace(a, b)
def between(a, b, new):
    global s
    assert s.count(a) == 1 and s.count(b) == 1, (s.count(a), s.count(b), a[:40])
    i = s.index(a); j = s.index(b); assert i < j
    s = s[:i] + new + s[j:]

once("  Build 176, from Karl's first use:", "  Build 177 · Karl, 15 November: a sense is shown \"According to whether the sense offered is unique enough to justify\n  the formation of a new symbol in the moment or a combination of existing symbols.\" So a sense carries one symbol,\n  up to four symbols together, or a new symbol formed just then by fusing the nearest ones, the way the map already\n  shows two symbols becoming a third. Claude suggests which; the person always decides.\n  Build 176, from Karl's first use:")
once(".word .sym{flex:0 0 64px;width:64px;height:64px;border-radius:50%;display:flex;align-items:center;justify-content:center}",
     ".sym{width:64px;height:64px;border-radius:50%;display:flex;align-items:center;justify-content:center}\n.word .sym{flex:0 0 64px}\n"
     ".fuse{flex:0 0 auto;display:flex;align-items:center;justify-content:center;border-radius:46%;padding:.15rem .5rem;max-width:100%}\n.fuse svg{max-width:100%;height:auto}\n"
     ".bond{display:flex;flex-wrap:wrap;gap:.4rem .5rem;align-items:flex-start;justify-content:center;margin:0 0 .8rem}\n"
     ".bw{flex:1 1 6.4rem;min-width:6rem;max-width:11rem;text-align:center}\n.bw .sym{margin:0 auto .3rem}\n.bw b{display:block;font-weight:600;font-size:1.06rem;line-height:1.2}\n.bw span{display:block;color:var(--soft);font-size:.9rem;line-height:1.3}\n"
     ".plus{align-self:center;font-size:1.5rem;color:var(--soft);line-height:1}\n"
     ".grid button[aria-pressed=\"true\"]{border-color:var(--plum);background:rgba(91,58,122,.13)}")
once("    M.alpha={by:by,words:words,chapters:j.chapters.filter(function(c){return c&&typeof c.id==='string'&&typeof c.name==='string';})};",
     "    var jn={};(Array.isArray(j.junctions)?j.junctions:[]).forEach(function(x){if(Array.isArray(x)&&by[x[0]]&&by[x[1]]&&typeof x[2]==='string'){jn[x[0]+'|'+x[1]]=jn[x[1]+'|'+x[0]]=x[2].slice(0,160);}});\n"
     "    M.alpha={by:by,words:words,jn:jn,chapters:j.chapters.filter(function(c){return c&&typeof c.id==='string'&&typeof c.name==='string';})};")
between("function sym(w,size){", "\n/* ── naming the sense, then three doors ── */", r'''/* the one place markup is ever placed: a symbol built only from shapes that passed the check above */
function draw(box,markup){box.innerHTML=markup;}
function sym(w,size){
  var s=el('span','sym');s.style.background='radial-gradient(circle, '+w.c+'cc 0%, '+w.c+'55 60%, '+w.c+'00 100%)';
  if(size){s.style.width=size+'px';s.style.height=size+'px';s.style.flexBasis=size+'px';}
  if(w.g)draw(s,'<svg width="'+Math.round((size||64)*.72)+'" height="'+Math.round((size||64)*.72)+'" viewBox="0 0 48 48" fill="none" stroke="#5b3a7a" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+w.g.replace(/class="f"/g,'fill="#5b3a7a" stroke="none"')+'</svg>');
  return s;
}
function joined(ws){return ws.length>2?ws.slice(0,-1).join(', ')+' and '+ws[ws.length-1]:ws.join(' and ');}
/* a new symbol, formed in the moment: the nearest symbols fused into one form, each still visible within it, sharing
   one core, as the map's own language does. With no relatives yet, an open ring: a new sense waiting for its form. */
function fused(ws,H){
  var a=M.alpha,n=ws.length,s=el('span','fuse');s.setAttribute('role','img');
  if(!n){s.setAttribute('aria-label','An open ring: a new sense, waiting for its form');
    draw(s,'<svg width="'+H+'" height="'+H+'" viewBox="0 0 48 48" fill="none" stroke="#5b3a7a" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M24 8 A16 16 0 1 1 12.7 12.7"/><circle cx="24" cy="24" r="2.2" fill="#5b3a7a" stroke="none"/></svg>');
    s.style.background='radial-gradient(circle, #e9b56a66 0%, #e9b56a22 60%, #e9b56a00 100%)';return s;}
  var step=30,vw=48+step*(n-1),W=Math.round(H*(vw+16)/64),g='',i;
  g+='<ellipse cx="'+(vw/2)+'" cy="24" rx="'+(vw/2+6)+'" ry="29" stroke-width="1" opacity="0.3"/>';
  for(i=0;i<n;i++)g+='<g transform="translate('+(i*step)+' 0)">'+a.by[ws[i]].g.replace(/<[^>]*class="f"[^>]*\/>/g,'')+'</g>';
  for(i=1;i<n;i++)g+='<circle cx="'+(i*step+9)+'" cy="24" r="4.2" fill="#e9b56a" stroke="none" opacity="0.85"/><circle cx="'+(i*step+9)+'" cy="24" r="1.6" fill="#5b3a7a" stroke="none"/>';
  if(n===1)g+='<circle cx="24" cy="24" r="4.2" fill="#e9b56a" stroke="none" opacity="0.85"/><circle cx="24" cy="24" r="1.6" fill="#5b3a7a" stroke="none"/>';
  draw(s,'<svg width="'+W+'" height="'+H+'" viewBox="-8 -8 '+(vw+16)+' 64" fill="none" stroke="#5b3a7a" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+g+'</svg>');
  s.setAttribute('aria-label','A new symbol, formed from '+joined(ws));
  s.style.background='radial-gradient(ellipse, '+a.by[ws[0]].c+'aa 0%, '+a.by[ws[n-1]].c+'55 62%, '+a.by[ws[n-1]].c+'00 100%)';
  return s;
}
/* what two symbols mean where they meet, when the language already says */
function meet(ws){var a=M.alpha,i,j;if(!a)return null;for(i=0;i<ws.length;i++)for(j=i+1;j<ws.length;j++)if(a.jn[ws[i]+'|'+ws[j]])return [ws[i],ws[j],a.jn[ws[i]+'|'+ws[j]]];return null;}
''')
once("name:str(k.name,60),also:str(k.also,60),working:str(k.working,60),", "name:str(k.name,60),also:str(k.also,60),working:str(k.working,60),words:Array.isArray(k.words)?k.words.slice(0,4).map(function(x){return str(x,60);}):[],fits:str(k.fits,10),")
once("name:'',also:'',working:'',learned:'',clear:'',offer:'',by:'rules'};", "name:'',also:'',working:'',words:[],fits:'',learned:'',clear:'',offer:'',by:'rules'};")
once("    M.pick=(a&&c.name&&a.by[c.name])?{word:c.name}:(c.name==='new'&&c.working?{working:c.working}:null);",
     "    var ws=a?c.words.filter(function(x,i){return a.by[x]&&c.words.indexOf(x)===i;}).slice(0,4):[];\n"
     "    if(a&&!ws.length&&a.by[c.name])ws=[c.name].concat(c.also&&c.also!==c.name&&a.by[c.also]?[c.also]:[]);   /* an answer in the older form */\n"
     "    if(c.fits==='one')ws=ws.slice(0,1);\n"
     "    M.pick={words:ws,fresh:c.fits==='new'||(!c.fits&&c.name==='new'),working:c.working||''};\n"
     "    M.offered={words:ws.slice(),fresh:M.pick.fresh};")
between("function wordBlock(box){", "function closeShow(){", r'''function wordBlock(box){
  var a=M.alpha,p=M.pick||(M.pick={words:[],fresh:false,working:''});
  var ws=p.words.filter(function(x){return a&&a.by[x];}),row,t,i,w;
  if(p.fresh){
    box.appendChild(el('span','tag','A new symbol, formed just now'));
    row=el('div','word');row.appendChild(fused(ws,ws.length>2?72:84));t=el('div','');
    t.appendChild(el('span','',ws.length>1?'Formed from '+joined(ws)+'. Each remains within it, sharing one core.':ws.length?'Formed from '+ws[0]+', its nearest relative.':'An open ring: a new sense, waiting for its form.'));
    row.appendChild(t);box.appendChild(row);
    var lab=el('label','small soft','Your name for this sense, in your own words');lab.htmlFor='working';box.appendChild(lab);
    var inp=el('input','');inp.type='text';inp.id='working';inp.maxLength=60;inp.value=p.working||'';inp.autocomplete='off';
    inp.addEventListener('input',function(){M.pick.working=inp.value.slice(0,60);});box.appendChild(inp);
    box.appendChild(el('p','small soft','A new sense is yours to name. Nothing is invented for you: its symbol grows only from symbols people already share.'));
  }else if(ws.length>1){
    box.appendChild(el('span','tag','Symbols together, for your sense'));
    row=el('div','bond');
    for(i=0;i<ws.length;i++){w=a.by[ws[i]];if(i)row.appendChild(el('span','plus','+'));
      t=el('div','bw');t.appendChild(sym(w,56));t.appendChild(el('b','',w.w));t.appendChild(el('span','',w.d));row.appendChild(t);}
    box.appendChild(row);
    var m=meet(ws);if(m)box.appendChild(el('p','small soft','In Alphasense, '+m[0]+' and '+m[1]+' meet as: “'+m[2]+'”.'));
    box.appendChild(el('p','small soft','These are only an offer. You are the one who knows.'));
  }else if(ws.length===1){w=a.by[ws[0]];
    box.appendChild(el('span','tag','A symbol for it, if it fits'));
    row=el('div','word');row.appendChild(sym(w));t=el('div','');t.appendChild(el('b','',w.w));t.appendChild(el('span','',w.d));row.appendChild(t);box.appendChild(row);
    if(w.door&&a.by[w.door])box.appendChild(el('p','small soft','In Alphasense, '+w.w+' carries a doorway: '+w.door+', “'+a.by[w.door].d+'”.'));
    box.appendChild(el('p','small soft','An Alphasense word is only an offer. You are the one who knows.'));
  }else{
    box.appendChild(el('span','tag','A symbol for it, if one fits'));
    box.appendChild(el('p','','No symbol has been chosen. That is welcome too: a sense does not need a name.'));}
  var chips=el('div','chips'),o=M.offered;
  function set(words,fresh){M.pick.words=words;M.pick.fresh=fresh;closeShow();if(fresh){try{$('working').focus({preventScroll:true});}catch(e){}}}
  if(a)chips.appendChild(btn('',ws.length?'Add or change symbols':'Look through the symbols',browse));
  if(!p.fresh&&ws.length>1)chips.appendChild(btn('','Only '+ws[0],function(){set([ws[0]],false);}));
  if(!p.fresh)chips.appendChild(btn('','This is a new sense',function(){set(ws,true);}));
  else chips.appendChild(btn('',ws.length>1?'Not new: the symbols together':ws.length?'Not new: '+ws[0]:'Not new',function(){set(ws,false);}));
  if(o&&o.words.length&&(o.words.join('|')!==ws.join('|')||o.fresh!==p.fresh))chips.appendChild(btn('','Back to what was offered',function(){set(o.words.slice(),o.fresh);}));
  if(ws.length||p.fresh)chips.appendChild(btn('','No symbol',function(){set([],false);}));
  box.appendChild(chips);
}
''')
between("function browse(){", "function picked(){", r'''function browse(){
  var a=M.alpha,b=$('close');if(!a)return;b.textContent='';
  var p=M.pick||(M.pick={words:[],fresh:false,working:''});
  b.appendChild(el('h2','','The Alphasense symbols'));
  b.appendChild(el('p','soft','Tap a symbol to choose it, and again to let it go. Up to four can join.'));
  var chosen=el('p','small','');chosen.setAttribute('role','status');
  var chips=el('div','chips'),note=el('p','small soft',''),grid=el('div','grid');
  function say(){chosen.textContent=p.words.length?'Chosen: '+p.words.join(' + '):'None chosen yet.';}
  function open(ch){
    for(var i=0;i<chips.children.length;i++)chips.children[i].setAttribute('aria-pressed',chips.children[i].dataset.id===ch.id?'true':'false');
    note.textContent=ch.note||'';grid.textContent='';
    a.words.forEach(function(w){if(w.fam!==ch.id)return;
      var x=btn('','',function(){var ix=p.words.indexOf(w.w);
        if(ix>=0)p.words.splice(ix,1);else if(p.words.length>=4){chosen.textContent='Up to four symbols can join. Let one go to choose another.';return;}else p.words.push(w.w);
        x.setAttribute('aria-pressed',p.words.indexOf(w.w)>=0?'true':'false');say();});
      x.title=w.d;x.setAttribute('aria-pressed',p.words.indexOf(w.w)>=0?'true':'false');x.appendChild(sym(w,44));x.appendChild(el('span','',w.w));grid.appendChild(x);});
  }
  a.chapters.forEach(function(ch){var x=btn('',ch.name,function(){open(ch);});x.dataset.id=ch.id;x.setAttribute('aria-pressed','false');chips.appendChild(x);});
  b.appendChild(chips);b.appendChild(note);b.appendChild(chosen);b.appendChild(grid);
  var row=el('div','row');row.appendChild(btn('btn','Done',closeShow));b.appendChild(row);
  var start=a.chapters[0];if(p.words.length&&a.by[p.words[0]])a.chapters.forEach(function(ch){if(ch.id===a.by[p.words[0]].fam)start=ch;});
  if(start)open(start);say();
  try{b.scrollIntoView({block:'start'});}catch(e){}
}
''')
once("function picked(){var p=M.pick;return {word:p&&p.word?p.word:'',working:p&&p.working?str(p.working,60):''};}",
     "function picked(){var a=M.alpha,p=M.pick||{words:[],fresh:false,working:''};\n"
     "  var ws=(p.words||[]).filter(function(x){return a&&a.by[x];}).slice(0,4),nm=p.fresh?str(p.working,60):'';\n"
     "  return {words:ws,fresh:!!p.fresh,working:nm,word:p.fresh?'':(ws[0]||''),\n"
     "    label:p.fresh?('A new sense: '+(nm||'not yet named')+(ws.length?', formed from '+joined(ws):'')):ws.length>1?'Its symbols: '+ws.join(' + '):ws.length?'Its symbol: '+ws[0]:''};}")
once("  a.push({at:new Date().toISOString().slice(0,10),sensed:c.sensed,word:p.word,working:p.working,learned:c.learned});",
     "  a.push({at:new Date().toISOString().slice(0,10),sensed:c.sensed,words:p.words,fresh:p.fresh,word:p.word,working:p.working,learned:c.learned});")
once("  if(p.word||p.working)card.appendChild(el('p','small soft','Its word: '+(p.word||p.working)+'.'));",
     "  if(p.label)card.appendChild(el('p','small soft',p.label+'.'));")
once("a.push({at:new Date().toISOString().slice(0,10),text:t,word:p.word,working:p.working});",
     "a.push({at:new Date().toISOString().slice(0,10),text:t,words:p.words,fresh:p.fresh,word:p.word,working:p.working});")
once("    card.appendChild(el('span','tag',str(k.at,10)+(k.word||k.working?' · '+str(k.word||k.working,60):'')));",
     "    var nm=k.fresh?str(k.working,60)||'a new sense':(Array.isArray(k.words)&&k.words.length?k.words.slice(0,4).map(function(x){return str(x,60);}).join(' + '):str(k.word||k.working,60));\n"
     "    card.appendChild(el('span','tag',str(k.at,10)+(nm?' · '+nm:'')));")
once("function fresh(){M.turns=[{role:'assistant',content:RULES_MARK+DOOR}];M.first='';M.replies=0;M.wstep=0;M.pick=null;M.close=null;M.lastReady=false;}",
     "function fresh(){M.turns=[{role:'assistant',content:RULES_MARK+DOOR}];M.first='';M.replies=0;M.wstep=0;M.pick=null;M.offered=null;M.close=null;M.lastReady=false;}")
once("THE MIRROR · the new way of listening · Build 176 ·", "THE MIRROR · the new way of listening · Build 177 ·")
io.open(P, 'w', encoding='utf-8').write(s)
print('ok')
