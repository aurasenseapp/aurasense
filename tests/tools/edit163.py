"""Build 163 · the Mirror page (23 Oct 2026). Karl: "The you who has come through this.. on repeat too."
The wiser voice's introduction ("The you who has come through this might say:") is shown the first time it speaks in a
visit; after that, its words come alone, in the same voice and style. What Claude hears of its own earlier replies
still carries the introduction, so the listener can count how often the wiser self has spoken.
Stamps 163 on the map and the Seeking. Always starts from the live 162 pages; re-runnable."""
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

WISER = 'The you who has come through this might say:'
edit('/home/claude/work/mirror-living.162.html', '/home/claude/aurasense/mirror-living.html', [
    ("""  22 Oct 2026 · Build 158: where Claude can listen, only Claude answers; if Claude can't, the words go back in the box.""",
     """  23 Oct 2026 · Build 163: the wiser voice's introduction is shown once a visit, never on repeat.
  22 Oct 2026 · Build 158: where Claude can listen, only Claude answers; if Claude can't, the words go back in the box.""",
     'note at the top'),
    ("""var LS={live:false,choice:null,rest:false,busy:false,heavy:false,aiN:0,by:'',turns:[],lastWords:'',snap:'',gen:0,ctl:null};""",
     """var LS={live:false,choice:null,rest:false,busy:false,heavy:false,aiN:0,wiserN:0,by:'',turns:[],lastWords:'',snap:'',gen:0,ctl:null};""",
     'count the wiser voice'),
    ("""  var txt=parts.map(function(p){return p.text;}).filter(Boolean).join(' ');""",
     """  var txt=parts.map(function(p){return (p.say?p.say+' ':'')+p.text;}).filter(Boolean).join(' ');   /* Build 163 · Claude still hears the introduction it no longer sees on screen */""",
     'what Claude hears'),
    ("""    if(asp){if(refl)parts.push({cls:'line ack',text:lsWhole(refl,300)});parts.push({cls:'line soft',text:'""" + WISER + """'});
      parts.push({cls:'line aspire',text:'“'+lsWhole(asp.replace(/^[“"]+|[”"]+$/g,''),360)+'”'});if(!q)q=LISTEN.aspq;}""",
     """    if(asp){if(refl)parts.push({cls:'line ack',text:lsWhole(refl,300)});
      if(!LS.wiserN)parts.push({cls:'line soft',text:'""" + WISER + """'});   /* 23 Oct 2026 · Build 163 · Karl: "on repeat too". Introduced once a visit */
      parts.push({cls:'line aspire',text:'“'+lsWhole(asp.replace(/^[“"]+|[”"]+$/g,''),360)+'”',say:LS.wiserN?'""" + WISER + """':''});LS.wiserN++;if(!q)q=LISTEN.aspq;}""",
     'the introduction, once'),
])
edit('/home/claude/work/index-mapbox.162.html', '/home/claude/aurasense/index-mapbox.html', [
    ('Build <span class="bs-l">22 Oct 2026 · </span>162<span class="bs-l"> · tap to refresh</span>',
     'Build <span class="bs-l">23 Oct 2026 · </span>163<span class="bs-l"> · tap to refresh</span>', 'map stamp')])
edit('/home/claude/work/seeking.162.html', '/home/claude/aurasense/seeking.html', [
    ('>Build 22 Oct 2026 &middot; 162', '>Build 23 Oct 2026 &middot; 163', 'seeking stamp')])
