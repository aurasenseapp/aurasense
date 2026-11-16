# Build 182 · Karl, 16 Nov 2026: one step into the Mirror; "I" where the AI meets a person's light.   python3 edit182.py <site folder>
import sys,io
root=sys.argv[1].rstrip('/')
def edit(name,pairs):
    p=root+'/'+name; s=io.open(p,encoding='utf8').read()
    for a,b in pairs:
        assert s.count(a)==1,(name,s.count(a),a[:70]); s=s.replace(a,b)
    io.open(p,'w',encoding='utf8').write(s)
edit('mirror.html',[
 ('<textarea id="words" maxlength="1200" placeholder="Write it as it is. It doesn’t need tidying." autocomplete="off" spellcheck="true"></textarea>\n',
  '<textarea id="words" maxlength="1200" placeholder="Write it as it is. It doesn’t need tidying." autocomplete="off" spellcheck="true"></textarea>\n<p id="pre" class="small soft hide"></p>\n'),
 ("function refreshNote(){\n  var n=$('note');n.textContent='';",
  "/* Build 182 · Karl: \"This two step to access needs to be one.\" What a yes means is told beside the box, before a word\n   is sent, and the first press of the button is the yes. The other answer sits beside it, equal and one press away. */\nfunction asking(){return !!(M.settled&&M.live&&M.listen&&!M.rest&&!M.careOn&&M.choice!=='claude');}\nfunction preShow(){\n  var p=$('pre'),on=asking();p.textContent='';p.classList.toggle('hide',!on);\n  if(!M.careOn)$('send').textContent=on&&get('as_age18')!=='1'?'I’m 18 or over · Tell the Mirror':'Tell the Mirror';\n  if(!on)return;\n  p.appendChild(document.createTextNode('Claude, an AI made by Anthropic, will listen. It reads your words only to shape each reply, and to tell you what it learned from them. Aurasense keeps nothing, and Anthropic, who make Claude, delete them within 30 days. For people 18 and over. '));\n  var l=el('a','','How your words are kept');l.href='/privacy#mirror';l.target='_blank';l.rel='noopener noreferrer';p.appendChild(l);\n  p.appendChild(document.createTextNode(' · '));\n  p.appendChild(btn('lnk','Write without the AI',function(){M.rest='choice';refreshNote();setWho('That’s alright. Nothing will leave this page. The written Mirror will ask instead.');try{$('words').focus();}catch(e){}}));\n}\nfunction refreshNote(){\n  try{preShow();}catch(e){}\n  var n=$('note');n.textContent='';"),
 ("  if(M.live&&M.listen&&!M.rest&&M.choice!=='claude'){consent(hear,function(){M.rest='choice';refreshNote();hear();});return;}",
  "  if(asking()){put('as_age18','1');put('as_mirror_listener','claude');M.choice='claude';refreshNote();}   /* Build 182: pressing the button, beside what it means, is the yes */"),
])
edit('index-mapbox.html',[
 ("+'<p class=\"ash-line\">It can’t feel this place the way you do, but it can see all around it.</p>'",
  "+'<p class=\"ash-line\">I can see all around this place. You are the one who can feel it.</p>'   /* Build 182 · Karl: \"'it' as opposed to 'I' first person seems detached\"; and never a greeting that begins with what cannot be done */"),
 ('<span class="bs-l">16 Nov 2026 · </span>181<','<span class="bs-l">16 Nov 2026 · </span>182<'),
])
print('ok')
