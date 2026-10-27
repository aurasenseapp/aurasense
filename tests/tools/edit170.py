"""Build 170 · launch readiness (27 Oct 2026). Karl: "a big effort ... to help take us a step closer to launch and
helping people AI mutual benefit works." From the launch-gate walk and the fortnightly research check:
- ONE list of heavy words for all of Aurasense: the Mirror's page, its helper, and the map's two rule-based Mirrors
  (which missed 16 and 25 of 38 test sentences, and could not read an iPhone's curly apostrophe). The classic Mirror
  answered "I wish I was dead" with "What is the first hour of that, and could it happen this week?".
- The Mirror is for people 18 and over: said, and confirmed once, at the moment Claude is chosen (one answer for all
  of Aurasense, kept on this device only). The Mirror's note (AI, not a therapist) is now easy to read.
- A second heavy reading within a fortnight is never met with silence: the way to a person is always shown.
- Small step-lights answer a fingertip (WCAG 2.2, 2.5.8); the readings' answer words are larger; the guide's close
  button and "the one before" are easy to tap.
- The guiding light's first hint steps aside if a page opens while it is showing.
- The sign-up's hidden "coming soon" card tells the truth; terms and privacy name the registered trade name and say
  plainly what happens when things are heavy.
Always starts from the live build-169 files saved in /home/claude/work. Re-runnable."""
import io, re
W = '/home/claude/work/'; A = '/home/claude/aurasense/'
ONE = io.open(W + 'heavy-one-list.txt', encoding='utf-8').read().strip()
assert ONE.startswith('/\\b(?:kill') and ONE.endswith(')\\b/i') and 'wish i\'?d never been born' in ONE

def edit(src, dst, pairs):
    t = io.open(src, encoding='utf-8').read()
    for old, new, label in pairs:
        c = t.count(old); assert c == 1, (dst, label, c)
        t = t.replace(old, new); print('ok', dst.split('/')[-1], label)
    io.open(dst, 'w', encoding='utf-8').write(t)
    return t

def regex_line(text, prefix):
    """the whole regex literal that follows prefix, up to and including /i"""
    i = text.index(prefix) + len(prefix); j = text.index(')\\b/i', i) + len(')\\b/i')
    return text[i:j]

# ── the Mirror's page ─────────────────────────────────────────────────────────────────────────────────────────────
m = io.open(W + 'mirror-living.169.html', encoding='utf-8').read()
OLD_M = regex_line(m, 'var HEAVY=')
edit(W + 'mirror-living.169.html', A + 'mirror-living.html', [
  ("""  the words glow, char and fall away. Listen Forward opens Stripe, where the person chooses the amount.
""", """  the words glow, char and fall away. Listen Forward opens Stripe, where the person chooses the amount.
  27 Oct 2026 · Build 170: one list of heavy words for all of Aurasense (wider, and read the same with an iPhone's
  curly apostrophe); the Mirror is for people 18 and over, said and confirmed once when Claude is chosen; the note
  that Claude is an AI and not a therapist is easy to read.
""", 'header note'),
  ('var HEAVY=' + OLD_M + ';   /* 22 Oct 2026', 'var HEAVY=' + ONE + ';   /* 27 Oct 2026 · Build 170 · ONE LIST for all of Aurasense (the map\'s Mirrors and the helper carry this same line): also "I want to end it", "I wish I was dead", "better off without me", "I don\'t want to wake up again" · 22 Oct 2026', 'the one list'),
  (""".note{font-size:.85rem;color:var(--faint);margin-top:10px;text-align:center}""",
   """.note{font-size:.85rem;color:var(--soft);margin-top:10px;text-align:center}   /* 27 Oct 2026 · Build 170 · AI, not a therapist: said where it can be read (it was 2.7 to 1 against its ground; WCAG asks 4.5) */""", 'the note, readable'),
  ("""/* ══ TP CSS END ══ */""", """/* ══ TP CSS END ══ */
.line.small{color:var(--soft)}   /* 27 Oct 2026 · Build 170 · small words that carry meaning stay readable */""", 'small lines, readable'),
  ("""  var yes=el('button','door','Begin with Claude');yes.type='button';
  var no=el('button','door','Not now');no.type='button';
  yes.addEventListener('click',function(){lsChoose('claude');lsAskHide();if(after)after();});""",
   """  var adult=lsAdult();   /* 27 Oct 2026 · Build 170 · the Mirror is for people 18 and over: one answer for all of Aurasense, kept on this device only */
  var yes=el('button','door',adult?'Begin with Claude':'I’m 18 or over · Begin with Claude');yes.type='button';
  var no=el('button','door','Not now');no.type='button';
  yes.addEventListener('click',function(){lsAdultYes();lsChoose('claude');lsAskHide();if(after)after();});""", 'consent: 18 and over'),
  ("""  var why=el('p','ask-why','Claude reads your words only to shape each reply.""",
   """  var why=el('p','ask-why',(adult?'':'The Mirror is for people 18 and over. ')+'Claude reads your words only to shape each reply.""", 'consent: said plainly'),
  ("""function lsAskHide(){var a=$('lsAsk');""",
   """function lsAdult(){try{return localStorage.getItem('as_age18')==='1';}catch(e){return false;}}
function lsAdultYes(){try{localStorage.setItem('as_age18','1');}catch(e){}}
function lsAskHide(){var a=$('lsAsk');""", 'the one age answer'),
  ("""  var b=el('button','door','Begin with Claude after all');b.type='button';
  b.addEventListener('click',function(){lsAskHide();var w=$('words').value.trim();lsChoose('claude');""",
   """  var b=el('button','door',lsAdult()?'Begin with Claude after all':'I’m 18 or over · Begin with Claude');b.type='button';
  b.addEventListener('click',function(){lsAdultYes();lsAskHide();var w=$('words').value.trim();lsChoose('claude');""", 'after all: 18 and over'),
])

# ── the helper ────────────────────────────────────────────────────────────────────────────────────────────────────
f = io.open(W + 'mirror-fn.169.js', encoding='utf-8').read()
OLD_F = regex_line(f, 'const HEAVY = ')
edit(W + 'mirror-fn.169.js', A + 'functions/api/mirror.js', [
  ('const HEAVY = ' + OLD_F + ';', '/* 27 Oct 2026 · Build 170 · ONE LIST for all of Aurasense: the Mirror page and the map carry this same line */\nconst HEAVY = ' + ONE + ';', 'the one list'),
])

# ── the map page ──────────────────────────────────────────────────────────────────────────────────────────────────
p = io.open(W + 'index-mapbox.169.html', encoding='utf-8').read()
OLD_MV = regex_line(p, 'const MV_HEAVY=')
OLD_MR = regex_line(p, 'const MR_HEAVY=')
TEST_FN = "{test:function(t){try{return AS_ONE.test(String(t||'').replace(/[\\u2018\\u2019\\u02bc]/g,\"'\"));}catch(e){return false;}}}"
edit(W + 'index-mapbox.169.html', A + 'index-mapbox.html', [
  ('const MV_HEAVY=' + OLD_MV + ';   /* 22 Oct 2026 · “suicide”, “suicidal”, “self-harming” and “hurting myself” were missed */',
   """/* ═══ 27 Oct 2026 · BUILD 170 · ONE LIST OF HEAVY WORDS ═══════════════════════════════════════════════════════
   The same line as the Mirror's page and its helper. Of 38 test sentences, this Mirror's own list missed 16 and the
   held moment's missed 25; neither could read an iPhone's curly apostrophe, so "I don’t want to live" passed.
   Each list here is now that one line, read with plain apostrophes. Despair is always met with a way to a person. */
const MV_HEAVY=(function(){const AS_ONE=""" + ONE + """;return """ + TEST_FN + """;})();""", 'Mirror\'s Voice: the one list'),
  ('const MR_HEAVY=' + OLD_MR + ';   /* 22 Oct 2026 · the same mend */',
   """const MR_HEAVY=(function(){const AS_ONE=""" + ONE + """;return """ + TEST_FN + """;})();   /* 27 Oct 2026 · Build 170 · the one list (it answered "I wish I was dead" with a question about the first hour) */""", 'held moment and classic Mirror: the one list'),
  ("""/* Shown at most once a fortnight, and never as a verdict. */
function qzHeavy(q,negA,negN){
  if(!negN||negA<4.2)return;                        /* only the far end of the scale */
  if(['phq','gad','dass'].indexOf(q.id)<0)return;   /* only the readings that warrant it */
  try{
    const k='as_heavy_seen', last=parseInt(localStorage.getItem(k)||'0',10)||0;
    if(Date.now()-last < 12*24*3600*1000)return;
    localStorage.setItem(k,String(Date.now()));
  }catch(e){}""",
   """/* Never as a verdict. 27 Oct 2026 · Build 170: a second heavy reading within a fortnight is never met with silence.
   Karl: "we can't ignore someone in need." The way to a person is always shown; the second time, in fewer words. */
function qzHeavy(q,negA,negN){
  if(!negN||negA<4.2)return;                        /* only the far end of the scale */
  if(['phq','gad','dass'].indexOf(q.id)<0)return;   /* only the readings that warrant it */
  let again=false;
  try{
    const k='as_heavy_seen', last=parseInt(localStorage.getItem(k)||'0',10)||0;
    if(Date.now()-last < 12*24*3600*1000)again=true;
    localStorage.setItem(k,String(Date.now()));
  }catch(e){}""", 'heavy reading: never silence'),
  ("""        +'<div class="ah-t">That reading came back heavy.</div>'
        +'<div class="ah-b">Aurasense is not able to tell you what that means, and it will not try.<br><br>'
        +'But a reading like that is worth saying out loud to somebody \\u2014 someone you trust, or a doctor, '
        +'or a helpline if that is easier tonight.<br><br>'
        +'<b>It costs nothing to say it to one person.</b></div>'""",
   """        +(again
          ?'<div class="ah-t">That reading came back heavy again.</div>'
           +'<div class="ah-b">You do not have to carry it on your own. Please say it out loud to somebody \\u2014 someone you trust, '
           +'a doctor, or a helpline if that is easier tonight.</div>'
          :'<div class="ah-t">That reading came back heavy.</div>'
           +'<div class="ah-b">Aurasense is not able to tell you what that means, and it will not try.<br><br>'
           +'But a reading like that is worth saying out loud to somebody \\u2014 someone you trust, or a doctor, '
           +'or a helpline if that is easier tonight.<br><br>'
           +'<b>It costs nothing to say it to one person.</b></div>')""", 'heavy reading: the second time'),
  ("""color:#6f5a6c;font-size:11.5px;display:flex;flex-direction:column;align-items:center;gap:6px;cursor:pointer;box-shadow:none}""",
   """color:#5d4a5b;font-size:13px;line-height:1.2;display:flex;flex-direction:column;align-items:center;gap:6px;cursor:pointer;box-shadow:none}""", 'answer words, larger'),
  ("""#quest-page .qzc-answers{gap:3px}#quest-page .qzc-answers .qz-dot{width:60px;font-size:10.5px}}""",
   """#quest-page .qzc-answers{gap:3px}#quest-page .qzc-answers .qz-dot{width:60px;font-size:12.5px}}""", 'answer words, larger on small phones too'),
  ("""#quest-page .qzc-back{display:block;margin:26px auto 0;background:none;border:0;color:#7a6577;font-family:inherit;font-size:14px;cursor:pointer}""",
   """#quest-page .qzc-back{display:block;margin:16px auto 0;padding:10px 18px;min-height:44px;background:none;border:0;color:#6f5a6c;font-family:inherit;font-size:14px;cursor:pointer}""", 'the one before: easy to tap'),
  ("""#ra-modal #ra-body>*{flex:0 0 auto}""",
   """#ra-modal #ra-body>*{flex:0 0 auto}
#ra-modal #ra-body{justify-content:safe center;overflow-y:auto}   /* 27 Oct 2026 · Build 170 · a tall page no longer loses its first line under the heading: it starts at the top, and can be scrolled */""", 'the guide: no first line lost'),
  ("""#ra-modal .ra-x{display:block;width:100%;margin-top:10px;background:none;border:none;color:var(--mute);font-size:13px;cursor:pointer;font-family:var(--serif)}""",
   """#ra-modal .ra-x{display:block;width:100%;margin-top:2px;padding:8px 0;min-height:32px;background:none;border:none;color:var(--mute);font-size:13px;cursor:pointer;font-family:var(--serif)}""", 'close the guide: easy to tap'),
  (""".as-onenav .as-onetrail button.fresh{animation:asFresh 1.6s ease-in-out 2}""",
   """.as-onenav .as-onetrail button.fresh{animation:asFresh 1.6s ease-in-out 2}
/* 27 Oct 2026 · Build 170 · every little step-light keeps its look and answers a fingertip: a 26px touch area (WCAG 2.2 · 2.5.8) */
#quest-page .qzc-trail,#register-page .rg-trail,#trajectory-page .tj-trail,#op-nav .op-trail,.as-onenav .as-onetrail,.asp-trail{position:relative;z-index:3}   /* above the breathing circle's glow, which covered them so a touch never reached them */
#quest-page .qzc-trail button,#register-page .rg-trail button,#trajectory-page .tj-trail button,#op-nav .op-trail button,.as-onenav .as-onetrail button,.asp-trail button{position:relative}
#quest-page .qzc-trail button::after,#register-page .rg-trail button::after,#trajectory-page .tj-trail button::after,#op-nav .op-trail button::after,.as-onenav .as-onetrail button::after,.asp-trail button::after{content:"";position:absolute;left:50%;top:50%;width:26px;height:26px;margin:-13px 0 0 -13px;border-radius:50%}""", 'step-lights: a fingertip'),
  ("""      <div class="rg-h">Shape your aura <span class="rg-opt">optional · coming</span></div>
      <div class="rg-sub">Soon you will be able to take gentle, private questionnaires that open your aura further — revealing its colours, its energy, and the areas most alive in you. A space held here for when you are ready. We will always be clear about what each one is for.</div>""",
   """      <div class="rg-h">Shape your aura <span class="rg-opt">optional</span></div>
      <div class="rg-sub">Gentle, private readings that open your aura further — its colours, its energy, and the areas most alive in you. They wait in My Aura, under Add to your aura, for whenever you are ready. Each one says plainly what it is for.</div>""", 'the sign-up tells the truth'),
  ("""h.classList.add('show');setTimeout(go,11000);""",
   """h.classList.add('show');setTimeout(go,11000);
      /* 27 Oct 2026 · Build 170 · if a page opens while it is speaking, it steps aside (and will speak another day) */
      const aside=setInterval(()=>{try{if(!document.body.contains(h)||!h.classList.contains('show')){clearInterval(aside);return;}
        if(document.querySelector('[id$="-page"].show,#mv-panel.show,#explore-panel.open,#gv.show,#ra-modal,#as-age,#as-heavy,#as-living-mirror,#mr-modal')){clearInterval(aside);h.classList.remove('show');setTimeout(()=>{try{h.remove();}catch(e){}},700);}}catch(e){clearInterval(aside);}},500);""", 'the guiding light steps aside'),
  ('Build <span class="bs-l">27 Oct 2026 · </span>169<span class="bs-l"> · tap to refresh</span>',
   'Build <span class="bs-l">27 Oct 2026 · </span>170<span class="bs-l"> · tap to refresh</span>', 'map stamp'),
])
edit(W + 'seeking.169.html', A + 'seeking.html', [('>Build 27 Oct 2026 &middot; 169', '>Build 27 Oct 2026 &middot; 170', 'seeking stamp')])

# ── terms and privacy ─────────────────────────────────────────────────────────────────────────────────────────────
edit(W + 'terms.169.html', A + 'terms.html', [
  ("""<p>Aurasense is operated by its founder — an independent sole operator based in Alberta, Canada ("Aurasense", "we", "us").""",
   """<p>Aurasense is a trade name registered in Alberta, Canada, operated by its founder as a sole proprietorship ("Aurasense", "we", "us").""", 'who we are'),
  ("""anywhere else, <a href="https://findahelpline.com">findahelpline.com</a> lists helplines.</p>

<h2>3 · Who can use it</h2>""",
   """anywhere else, <a href="https://findahelpline.com">findahelpline.com</a> lists helplines.</p>
<p id="heavy"><strong>When things are heavy, this is what Aurasense does.</strong></p>
<ul>
<li>Words that clearly say someone may be in danger (such as wanting to end their life, or to hurt themselves) are recognised on your own device, by one list used everywhere in Aurasense. In the Mirror they are <strong>never sent to the AI</strong>: the Mirror stops and shows how to reach a real person.</li>
<li>When Claude listens, it is also asked to watch for danger in other words, and when it hears it, the Mirror shows the same way to a real person.</li>
<li>If a reading about mood or worry comes back at its heaviest, Aurasense says so once, gently, without any label, and shows the same way to a real person. It never diagnoses.</li>
<li>Aurasense cannot see who you are or where you are, so <strong>it cannot call anyone for you</strong>. If you are in danger, please call 911 (or your local emergency number) yourself, or ask someone near you to.</li>
</ul>

<h2>3 · Who can use it</h2>""", 'when things are heavy'),
])
edit(W + 'privacy.169.html', A + 'privacy.html', [
  ("""<p>Aurasense is operated by its founder — an independent sole operator based in Alberta, Canada.""",
   """<p>Aurasense is a trade name registered in Alberta, Canada, operated by its founder as a sole proprietorship.""", 'who is responsible'),
])
print('done')
