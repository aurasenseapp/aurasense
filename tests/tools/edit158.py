"""Build 158 · the Mirror page (22 Oct 2026).
Karl: "It's worse than the written rules. And that's unusable and i was going to ask you to remove that option."
Where Claude can listen, the written rules are no longer offered, and never answer in Claude's place: the Mirror asks
"Would you like Claude to listen?" (Begin with Claude / Not now), and if Claude can't answer, the person's words go
back in the box with the reason. The written rules still answer only where no listener exists at all (a preview).
A remembered "rules" choice from before is asked again. "Stop sharing my words" withdraws the yes at any moment.
Always starts from the live 157 file; re-runnable."""
import io, re

SRC = '/home/claude/work/mirror-living.157.html'
DST = '/home/claude/aurasense/mirror-living.html'
s = io.open(SRC, encoding='utf-8').read()

def rep(old, new, label, count=1):
    global s
    c = s.count(old)
    assert c == count, (label, c)
    s = s.replace(old, new)
    print('ok', label)

# 1 · the opening question and its two answers
rep("""    if(LS.live&&!LS.choice){show(openParts('Who would you like to listen to you?'),'');
      lsAsk(function(){if(S.turns.length){setWho('');lsHint();return;}show(openParts(),'');d.classList.remove('hide');});return;}""",
    """    if(LS.live&&!LS.choice){show(openParts('Would you like Claude, an AI, to listen to you here?'),'');
      lsAsk(function(){if(S.turns.length){setWho('');lsHint();return;}show(openParts(),'');d.classList.remove('hide');},lsNotNow);return;}""",
    '1 the opening asks one plain question')

# 2 · hearing: where Claude can listen, only Claude answers
rep("""  if(LS.live&&LS.choice==='claude'&&!LS.rest){listen(raw,t);return;}
  if(LS.live)setWho(LS.rest?WHY.restnote:'Answered by the written rules. Nothing left this page.');
  rulesHear(raw,t);
}""",
    """  if(LS.live){if(LS.rest){$('words').value=raw;LS.lastWords='';setWho(WHY.restnote);return;}listen(raw,t);return;}   /* 22 Oct 2026 · Build 158 · where Claude can listen, only Claude answers */
  rulesHear(raw,t);   /* only where no listener exists at all (a preview) */
}""", '2 only Claude answers where Claude can listen')

# 3 · when Claude can't answer: their words go back in the box, with the reason, and nothing answers in Claude's place
rep("""var WHY={
  resting:'Claude is resting for now, so the written rules answered.',
  key:'Claude is resting for now, so the written rules answered.',
  off:'Claude is resting for now, so the written rules answered.',
  elsewhere:'Claude is resting for now, so the written rules answered.',
  busy:'Claude has listened a lot just now, so the written rules answered this one.',
  slow:'Claude took too long, so the written rules answered this one.',
  refused:'Claude didn’t answer those words, so the written rules did.',
  upstream:'Claude couldn’t answer just then, so the written rules did.',
  restnote:'Claude is resting for now, so the written rules are answering. Nothing leaves this page.'
};""",
    """var WHY={   /* 22 Oct 2026 · Build 158 · nothing answers in Claude's place: the words go back in the box, with the reason */
  resting:'The Mirror is resting for now. Your words are back in the box; please come back a little later.',
  key:'The Mirror is resting for now. Your words are back in the box; please come back a little later.',
  off:'The Mirror is resting for now. Your words are back in the box; please come back a little later.',
  elsewhere:'The Mirror is resting for now. Your words are back in the box; please come back a little later.',
  busy:'Claude has listened a lot just now. Your words are back in the box; try again in a minute.',
  slow:'Claude took too long to answer. Your words are back in the box; send them again when you’re ready.',
  refused:'Claude didn’t answer those words. They are back in the box, if you’d like to say them another way.',
  upstream:'Claude couldn’t answer just then. Your words are back in the box; send them again when you’re ready.',
  restnote:'The Mirror is resting for now. Your words are still in the box; please come back a little later.'
};""", '3a the reasons, plainly')
rep("""    if(/^(resting|key|off|elsewhere)$/.test(c)){LS.rest=true;refreshNote();}   /* for the rest of this visit, nothing more is sent */
    restoreS();
    rulesHear(raw,t);
    setWho(WHY[c]||WHY.upstream);""",
    """    if(/^(resting|key|off|elsewhere)$/.test(c)){LS.rest=true;refreshNote();}   /* for the rest of this visit, nothing more is sent */
    restoreS();LS.lastWords='';
    if(!$('words').value.trim())$('words').value=raw;   /* their words go back in the box, exactly as written */
    setWho(WHY[c]||WHY.upstream);""", '3b their words go back in the box')

# 4 · the note beneath: what is happening to their words, and the way to stop
rep("""  var sw=function(label,to){var b=el('button','lnk',label);b.type='button';
    b.addEventListener('click',function(){if(LS.busy)return;lsChoose(to);
      setWho(to==='claude'?'Claude will listen from your next words.':'The written rules will answer from your next words. Nothing leaves this page.');});
    n.appendChild(b);};
  if(LS.choice==='claude'&&!LS.rest){n.appendChild(document.createTextNode('Claude, an AI, is listening; Aurasense keeps nothing. Not a person, and not a therapist. '));sw('Use the written rules instead','rules');}
  else if(LS.choice){n.appendChild(document.createTextNode('Nothing you write leaves this page. The Mirror is not a person, and not a therapist. '));if(!LS.rest)sw('Let Claude listen','claude');}
  else n.appendChild(document.createTextNode('The Mirror is not a person, and not a therapist.'));""",
    """  if(LS.choice==='claude'&&!LS.rest){n.appendChild(document.createTextNode('Claude, an AI, is listening; Aurasense keeps nothing. Not a person, and not a therapist. '));
    var b=el('button','lnk','Stop sharing my words');b.type='button';b.addEventListener('click',function(){lsForget();});n.appendChild(b);}
  else if(LS.rest)n.appendChild(document.createTextNode('The Mirror is resting for now. Not a person, and not a therapist.'));
  else n.appendChild(document.createTextNode('The Mirror is not a person, and not a therapist.'));""", '4 the note beneath')

# 5 · the question and its two answers: Begin with Claude, or Not now
rep("""/* who listens: two equal choices, and what each means, in plain words */
function lsAsk(after){
  var a=$('lsAsk');if(!a)return;a.textContent='';
  var row=el('div','doors');
  var yes=el('button','door','Claude, an AI');yes.type='button';
  var no=el('button','door','The written rules');no.type='button';
  var pick=function(c){lsChoose(c);lsAskHide();if(after)after();};
  yes.addEventListener('click',function(){pick('claude');});no.addEventListener('click',function(){pick('rules');});
  row.appendChild(yes);row.appendChild(no);a.appendChild(row);
  var why=el('p','ask-why','Claude reads your words only to shape each reply. Aurasense keeps nothing, and Anthropic, who make Claude, delete them within 30 days. With the written rules, nothing leaves this page. Either way, if you may be in danger, the Mirror shows you how to reach a real person. ');""",
    """/* 22 Oct 2026 · Build 158 · one plain question: may Claude listen? Two equal answers, and what a yes means */
function lsAsk(after,onNo){
  var a=$('lsAsk');if(!a)return;a.textContent='';
  var row=el('div','doors');
  var yes=el('button','door','Begin with Claude');yes.type='button';
  var no=el('button','door','Not now');no.type='button';
  yes.addEventListener('click',function(){lsChoose('claude');lsAskHide();if(after)after();});
  no.addEventListener('click',function(){lsAskHide();(onNo||lsNotNow)();});
  row.appendChild(yes);row.appendChild(no);a.appendChild(row);
  var why=el('p','ask-why','Claude reads your words only to shape each reply. Aurasense keeps nothing, and Anthropic, who make Claude, delete them within 30 days. If you may be in danger, the Mirror shows you how to reach a real person. ');""",
    '5 Begin with Claude, or Not now')

# 6 · Not now, and Stop sharing my words
rep("""function lsAskHide(){var a=$('lsAsk');if(a){a.classList.add('hide');a.textContent='';}}""",
    """function lsAskHide(){var a=$('lsAsk');if(a){a.classList.add('hide');a.textContent='';}}
/* Not now: nothing is sent, nothing is kept, and the way back in stays open */
function lsNotNow(){
  $('doors').classList.add('hide');$('say').classList.add('hide');setWho('');
  show([{cls:'line',text:'That’s alright. Nothing has left this page.'},{cls:'line soft',text:'The Mirror will be here whenever you’d like.'}],'');
  var a=$('lsAsk');a.textContent='';var row=el('div','doors');
  var b=el('button','door','Begin with Claude after all');b.type='button';
  b.addEventListener('click',function(){lsAskHide();var w=$('words').value.trim();lsChoose('claude');
    if(S.turns.length){$('say').classList.remove('hide');if(w)hear();}else{show(openParts(),'');$('doors').classList.remove('hide');}});
  row.appendChild(b);a.appendChild(row);a.classList.remove('hide');}
/* Stop sharing my words: the yes is forgotten on this device, and the conversation is let rest */
function lsForget(){LS.choice=null;try{localStorage.removeItem('as_mirror_listener');}catch(e){}refreshNote();rest();setWho('Nothing more will be shared. The Mirror will ask again next time.');}""",
    '6 Not now, and Stop sharing')

# 7 · asked mid-way (the light on the map began it)
rep("""function lsConsentMid(){setWho('First, choose who listens. Your words wait in the box.');lsAsk(function(){setWho('');hear();});}""",
    """function lsConsentMid(){setWho('First, a question. Your words wait in the box.');lsAsk(function(){setWho('');hear();},lsNotNow);}""",
    '7 asked mid-way')

# 8 · a "rules" choice remembered from before is asked again
rep("""LS.choice=(c==='claude'||c==='rules')?c:null;""", """LS.choice=(c==='claude')?c:null;   /* 22 Oct 2026 · Build 158 · an older "rules" choice is asked again */""",
    '8 an older choice is asked again')

# 9 · a larger Claude can take a little longer
rep("""  var timer=setTimeout(function(){try{if(ctl)ctl.abort();}catch(e){}},30000);""",
    """  var timer=setTimeout(function(){try{if(ctl)ctl.abort();}catch(e){}},50000);   /* Build 158 · a larger Claude may take a little longer */""",
    '9 waiting a little longer')

# 10 · the page's own top note
rep("""  22 Oct 2026 · Build 156: words leave this page only when the person has chosen to let Claude listen, and then""",
    """  22 Oct 2026 · Build 158: where Claude can listen, only Claude answers; if Claude can't, the words go back in the box.
  22 Oct 2026 · Build 156: words leave this page only when the person has chosen to let Claude listen, and then""",
    '10 the note at the top')

io.open(DST, 'w', encoding='utf-8').write(s)
print('written', DST, len(s))
