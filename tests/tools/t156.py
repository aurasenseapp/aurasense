"""Build 156 · Claude listening live in the Mirror: whole walks in a real browser, with a pretend helper (22 Oct 2026).
Test-only: never part of the real site."""
import sys, io, os, json, shutil
sys.path.insert(0, '/home/claude/scripts')
from harness import *

os.makedirs(TEST, exist_ok=True)
shutil.copy('/home/claude/aurasense/mirror-living.html', TEST + '/mirror-living.html')
shutil.copy('/home/claude/work/mirror-living.155.html', TEST + '/mirror155.html')
io.open(TEST + '/privacy.html', 'w').write('<!doctype html><title>privacy</title>')
io.open(TEST + '/test-host.html', 'w', encoding='utf-8').write("""<!doctype html><meta charset=utf-8><body style="margin:0">
<div id="as-living-mirror"><iframe id="f" src="/mirror-living.html?in=site" sandbox="allow-scripts allow-same-origin allow-popups allow-popups-to-escape-sandbox" style="width:390px;height:664px;border:0"></iframe></div>
<script>var f=document.getElementById('f');f.addEventListener('load',function(){setTimeout(function(){f.contentWindow.postMessage({as:'mirror-host',act:'begin',q:'What is the light showing you?',a:'I feel restless tonight, and I can\\u2019t settle',kind:''},location.origin);},300);},{once:true});
addEventListener('message',function(e){window.__got=(window.__got||[]).concat([e.data]);});</script></body>""")

fails = []
def check(name, ok, detail=''):
    print(('PASS ' if ok else 'FAIL ') + name + ('' if ok else '  -> ' + str(detail)[:400]), flush=True)
    if not ok: fails.append(name)

CL = lambda refl, q, asp='': {'ok': True, 'by': 'claude', 'reflect': refl, 'question': q, 'aspire': asp, 'care': False, 'ground': False}

# ── A · no helper (as on Vercel today): exactly as before, and nothing is ever sent ───────────────────────
said = ['I keep going round in circles about work', 'in my chest', 'yes, many times', 'goodbye']
outs = {}
for f in ['mirror155.html', 'mirror-living.html']:
    api = Api('absent'); w = Walk(390, 664, mobile=True, api=api); w.open(f)
    first = w.speak(); doors = w.visible('doors')
    w.click_text('#doors button', 'Something else'); w.page.wait_for_timeout(3000)
    turns = [first]
    for t in said: w.say(t); turns.append(w.speak())
    outs[f] = dict(turns=turns, doors=doors, who=w.visible('who'), ask=w.visible('lsAsk'), note=w.js("document.getElementById('note').textContent"),
                   posts=len(api.posts), errors=w.errors[:3])
    if f == 'mirror-living.html': w.shot('a_absent_end_phone')
    w.close()
o5, o6 = outs['mirror155.html'], outs['mirror-living.html']
check('A: with no helper, the opening is the same as 155', o5['turns'][0] == o6['turns'][0], (o5['turns'][0], o6['turns'][0]))
check('A: with no helper, the doors show', o6['doors'])
check('A: with no helper, no "who answered" line and no choice of listener', not o6['who'] and not o6['ask'])
check('A: with no helper, the note is unchanged', o6['note'] == o5['note'], o6['note'])
check('A: with no helper, nothing is ever sent', o6['posts'] == 0)
same = sum(1 for a, b in zip(o5['turns'], o6['turns']) if a == b)
check('A: the written rules answer the same as 155 (%d of %d turns identical)' % (same, len(o5['turns'])), same == len(o5['turns']), list(zip(o5['turns'], o6['turns'])))
check('A: no page errors', not o6['errors'], o6['errors'])

# ── B · helper live, first visit: who listens is asked first; Claude listens; heavy words never go ──────────
api = Api('live', [CL('You said “round in circles about work”, as if the same road keeps coming back.', 'What happens just before the circle starts again?'),
                   CL('“A tightness” — so your body knows the circle before your thoughts do.', 'If you let that tightness be there, just for a moment, what happens?')])
w = Walk(390, 664, mobile=True, api=api); w.open()
check('B: the opening asks who listens', 'Who would you like to listen to you?' in w.speak(), w.speak())
check('B: two equal choices, and the doors wait', w.visible('lsAsk') and not w.visible('doors'), (w.visible('lsAsk'), w.visible('doors')))
check('B: the choices name Claude as an AI, and the written rules', w.js("[...document.querySelectorAll('#lsAsk button')].map(b=>b.textContent).join('|')") == 'Claude, an AI|The written rules')
check('B: what each choice means is said, with a privacy link', 'Aurasense keeps nothing' in w.js("document.getElementById('lsAsk').textContent") and w.js("document.querySelector('#lsAsk a').getAttribute('href')") == 'privacy.html#mirror')
w.shot('b_consent_phone')
w.click_text('#lsAsk button', 'Claude, an AI'); w.page.wait_for_timeout(2600)
check('B: after choosing, the usual opening and the doors', 'What would you like to see more clearly?' in w.speak() and w.visible('doors') and not w.visible('lsAsk'), w.speak())
check('B: the note says Claude is listening, with the way to change it', w.js("document.getElementById('note').textContent").startswith('Claude, an AI, is listening; Aurasense keeps nothing.'), w.js("document.getElementById('note').textContent"))
check('B: the choice is remembered on this device', w.js("localStorage.getItem('as_mirror_listener')") == 'claude')
check('B: nothing sent yet', len(api.posts) == 0)
w.click_text('#doors button', 'Something else'); w.page.wait_for_timeout(3000)
w.say('I keep going round in circles about work')
check('B: their words go to the helper', len(api.posts) == 1 and api.posts[0]['words'] == 'I keep going round in circles about work', api.posts)
check('B: the conversation so far travels with them (the door question, marked as the written rules)', api.posts[0]['turns'] and api.posts[0]['turns'][-1]['role'] == 'assistant' and 'written rules' in api.posts[0]['turns'][-1]['content'], api.posts[0]['turns'])
check('B: Claude’s reply is shown, their own words in it', 'round in circles about work' in w.speak() and 'What happens just before the circle starts again?' in w.speak(), w.speak())
check('B: beside it, who answered', w.who() == 'Answered by Claude, an AI, listening.', w.who())
w.shot('b_claude_reply_phone')
w.say('I want to die some days')
check('B: heavy words are never sent', len(api.posts) == 1, len(api.posts))
check('B: heavy words go straight to real help', '988' in w.speak(), w.speak())
w.say('I have been feeling suicidal lately')
check('B: "suicidal" is never sent either (the review found the old list missed it)', len(api.posts) == 1 and '988' in w.speak(), (len(api.posts), w.speak()))
w.say('a tightness in my chest')
check('B: the next words go again', len(api.posts) == 2, len(api.posts))
check('B: the heavy words are not in what was sent', 'die' not in json.dumps(api.posts[1]), api.posts[1])
check('B: Claude’s earlier reply is in the thread, unmarked', any(t['role'] == 'assistant' and t['content'].startswith('You said') for t in api.posts[1]['turns']), api.posts[1]['turns'])
check('B: no page errors', not w.errors, w.errors[:3])
w.close()

# ── C · the written rules chosen: nothing is sent, until they choose otherwise ─────────────────────────────
api = Api('live', [CL('Heard you.', 'What else is here?')])
w = Walk(1440, 900, api=api); w.open()
w.click_text('#lsAsk button', 'The written rules'); w.page.wait_for_timeout(2600)
w.click_text('#doors button', 'A feeling I can’t place'); w.page.wait_for_timeout(3000)
w.say('a kind of grey sadness')
check('C: the written rules answer, and nothing is sent', len(api.posts) == 0 and w.who() == 'Answered by the written rules. Nothing left this page.', (len(api.posts), w.who()))
check('C: the note offers Claude, and promises nothing leaves', w.js("document.getElementById('note').textContent") == 'Nothing you write leaves this page. The Mirror is not a person, and not a therapist. Let Claude listen', w.js("document.getElementById('note').textContent"))
w.click_text('#note button', 'Let Claude listen'); w.page.wait_for_timeout(400)
check('C: switching is said plainly', w.who() == 'Claude will listen from your next words.', w.who())
w.say('since my dad died')
check('C: after switching, Claude listens', len(api.posts) == 1 and w.who() == 'Answered by Claude, an AI, listening.', (len(api.posts), w.who()))
w.shot('c_laptop_switched')
check('C: no page errors', not w.errors, w.errors[:3])
w.close()

# ── D · Claude resting (credit used): the written rules answer, say so, and nothing more is sent ──────────
api = Api('live', [{'ok': False, 'code': 'resting', '_status': 503}])
w = Walk(390, 664, mobile=True, api=api, init="try{localStorage.setItem('as_mirror_listener','claude')}catch(e){}"); w.open()
check('D: a remembered choice is not asked again', not w.visible('lsAsk') and w.visible('doors'))
w.click_text('#doors button', 'Something else'); w.page.wait_for_timeout(3000)
w.say('I feel stuck between two jobs')
check('D: the written rules answered', len(w.speak()) > 10 and 'stuck between two jobs' in w.speak(), w.speak())
check('D: the line says Claude is resting', w.who() == 'Claude is resting for now, so the written rules answered.', w.who())
w.say('the new one pays more')
check('D: nothing more is sent this visit', len(api.posts) == 1, len(api.posts))
check('D: and that is said, truthfully', w.who() == 'Claude is resting for now, so the written rules are answering. Nothing leaves this page.', w.who())
check('D: the note no longer says Claude is listening', w.js("document.getElementById('note').textContent").startswith('Nothing you write leaves this page.'), w.js("document.getElementById('note').textContent"))
w.say('are you an AI?')
check('D: "are you an AI?" is answered truthfully while Claude rests', 'Claude, an AI, usually answers here; it is resting for now' in w.speak() and len(api.posts) == 1, w.speak())
check('D: no page errors', not w.errors, w.errors[:3])
w.close()

# ── E · a hiccup: the written rules answer this one, and Claude is asked again next time ───────────────────
api = Api('live', [{'ok': False, 'code': 'upstream', '_status': 503}, CL('You said “quieter now”.', 'What made it quieter?')])
w = Walk(390, 664, mobile=True, api=api, init="try{localStorage.setItem('as_mirror_listener','claude')}catch(e){}"); w.open()
w.click_text('#doors button', 'Something else'); w.page.wait_for_timeout(3000)
w.say('I have felt this for a while, and it is getting heavier')
check('E: the written rules answer this one, as themselves', 'getting heavier' in w.speak() and w.who() == 'Claude couldn’t answer just then, so the written rules did.', (w.speak(), w.who()))
w.say('quieter now')
check('E: Claude is asked again, and answers', len(api.posts) == 2 and w.who() == 'Answered by Claude, an AI, listening.', (len(api.posts), w.who()))
check('E: the written rules’ answer is in the thread, marked as theirs', any('written rules' in t['content'] for t in api.posts[1]['turns'] if t['role'] == 'assistant'), api.posts[1]['turns'])
check('E: no page errors', not w.errors, w.errors[:3])
w.close()
api = Api('live', [{'ok': False, 'code': 'upstream', '_status': 503}])
w = Walk(390, 664, mobile=True, api=api, init="try{localStorage.setItem('as_mirror_listener','claude')}catch(e){}"); w.open()
w.click_text('#doors button', 'Something else'); w.page.wait_for_timeout(3000)
w.say('I feel lost'); w.say('are you an AI?')
check('E2: after a hiccup, "are you an AI?" never claims nothing left the page', 'just now the Mirror’s written rules answered instead' in w.speak() and 'nothing you write here leaves it' not in w.speak(), w.speak())
w.close()

# ── F · Claude hears something heavy: real help, and no gift line afterwards ────────────────────────────────
api = Api('live', [{'ok': True, 'by': 'claude', 'care': True, 'reflect': 'That sounds very heavy.', 'question': '', 'aspire': ''}, CL('Heard.', 'What else?')])
w = Walk(390, 664, mobile=True, api=api, init="try{localStorage.setItem('as_mirror_listener','claude')}catch(e){}"); w.open()
w.click_text('#doors button', 'Something else'); w.page.wait_for_timeout(3000)
w.say('I don’t see the point of anything any more')
check('F: Claude’s care signal shows real help', '988' in w.speak() and w.who() == 'Claude heard something heavy, so the Mirror points to real help.', (w.speak(), w.who()))
w.say('ok'); w.say('thank you')
w.js("document.getElementById('rest').click()"); w.page.wait_for_timeout(3000)
w.click_text('#doors button', 'Just the feeling of being met'); w.page.wait_for_timeout(3500)
check('F: after heavy words, no gift line', not w.visible('gift'))
w.close()

# ── G · a good ending after Claude listened: the Listen Forward door, once a week ────────────────────────────
api = Api('live', [CL('You said “restless”.', 'Where does the restlessness want to go?'), CL('“Outside, walking” — your feet already know.', 'What would one walk tomorrow feel like?'),
                   CL('“Lighter”.', 'What would you like to keep from this?')])
w = Walk(390, 664, mobile=True, api=api, init="try{localStorage.setItem('as_mirror_listener','claude')}catch(e){}"); w.open()
w.click_text('#doors button', 'Something else'); w.page.wait_for_timeout(3000)
w.say('restless'); w.say('outside, walking'); w.say('lighter')
w.js("document.getElementById('rest').click()"); w.page.wait_for_timeout(3000)
w.click_text('#doors button', 'Just the feeling of being met'); w.page.wait_for_timeout(3600)
check('G: after a good ending, the gift line shows', w.visible('gift'))
g = w.js("({t:document.getElementById('gift').innerText,h:document.querySelector('#gift a').href,tg:document.querySelector('#gift a').target,rel:document.querySelector('#gift a').rel})")
check('G: its words', 'Someone you’ll never meet kept this listening open for you.' in g['t'] and 'listen forward' in g['t'] and 'Nothing changes if you don’t.' in g['t'], g['t'])
check('G: it says plainly that it opens Stripe, that the person chooses, and that it pays for the listening just had', 'Listen forward opens a secure Stripe page where you choose the amount.' in g['t'] and 'It pays for the listening you’ve just had' in g['t'] and 'If it helped, you can pay what feels right for it' in g['t'] and 'Gifts' not in g['t'], g['t'])
check('G: it opens Stripe in a new window, safely', g['h'] == 'https://buy.stripe.com/aFacN7aoI9Eo6Ahale87K00' and g['tg'] == '_blank' and 'noopener' in g['rel'], g)
w.shot('g_gift_phone')
w.click_text('#gift button', 'or simply go well'); w.page.wait_for_timeout(300)
check('G: "or simply go well" lets it go', not w.visible('gift'))
w.page.reload(); w.page.wait_for_timeout(2600)
w.click_text('#doors button', 'Something else'); w.page.wait_for_timeout(3000)
w.say('restless'); w.say('outside, walking')
w.js("document.getElementById('rest').click()"); w.page.wait_for_timeout(3000)
w.click_text('#doors button', 'Just the feeling of being met'); w.page.wait_for_timeout(3600)
check('G: not again within the week', not w.visible('gift'))
check('G: no page errors', not w.errors, w.errors[:3])
w.close()

# ── H · the written rules only: no gift line (it is Claude's listening that was kept open) ──────────────────
api = Api('live', [])
w = Walk(390, 664, mobile=True, api=api, init="try{localStorage.setItem('as_mirror_listener','rules')}catch(e){}"); w.open()
w.click_text('#doors button', 'Something else'); w.page.wait_for_timeout(3000)
w.say('restless'); w.say('outside, walking'); w.say('goodbye')
w.click_text('#doors button', 'Just the feeling of being met'); w.page.wait_for_timeout(3600)
check('H: written rules only, no gift line', not w.visible('gift') and len(api.posts) == 0)
w.close()

# ── I · the wiser voice from Claude ─────────────────────────────────────────────────────────────────────────
api = Api('live', [CL('“Torn between urgency and the moment” — both want your life to be lived.', '', 'You don’t have to choose between acting and breathing. Breathe first, then take the one step that still feels like you tomorrow.')])
w = Walk(360, 640, mobile=True, api=api, init="try{localStorage.setItem('as_mirror_listener','claude')}catch(e){}"); w.open()
w.click_text('#doors button', 'Something else'); w.page.wait_for_timeout(3000)
w.say('Torn between urgency and living for the moment')
sp = w.speak()
check('I: the wiser voice is introduced, and the written rules’ closing question follows', 'The you who has come through this might say:' in sp and 'Which part of that feels true for you — and which doesn’t?' in sp, sp)
far = w.js("""(()=>{const m=document.getElementById('mirror').getBoundingClientRect(),cx=m.left+m.width/2,cy=m.top+m.height/2,R=m.width/2;
  let far=0;const tw=document.createTreeWalker(document.getElementById('speak'),NodeFilter.SHOW_TEXT,null);let n;const rg=document.createRange();
  while((n=tw.nextNode())){if(!n.nodeValue.trim()||n.parentNode.offsetParent===null)continue;rg.selectNodeContents(n);
    for(const b of rg.getClientRects()){const dx=Math.max(Math.abs(b.left-cx),Math.abs(b.right-cx)),dy=Math.max(Math.abs(b.top-cy),Math.abs(b.bottom-cy));far=Math.max(far,Math.hypot(dx,dy)/R);}}
  return +far.toFixed(3);})()""")
check('I: the whole of it sits inside the circle on a small phone (%.3f of the radius)' % far, far <= 0.9, far)
w.shot('i_wiser_smallphone')
w.close()

# ── J · begun from the light on the map, inside the map's frame: asked mid-way, words wait, then go ─────────
api = Api('live', [CL('“Restless tonight, and I can’t settle”.', 'What is the restlessness asking for?')])
w = Walk(390, 664, mobile=True, api=api); w.open('test-host.html', wait=3600)
fr = w.page.frame_locator('#f')
frm = [f for f in w.page.frames if f.url.endswith('mirror-living.html?in=site')][0]
check('J: inside the map, the way back shows', frm.evaluate("!document.getElementById('home').classList.contains('hide')"))
check('J: the light’s question opens it, the words wait in the box', 'What is the light showing you?' in frm.evaluate("document.getElementById('speak').innerText") and 'restless tonight' in frm.evaluate("document.getElementById('words').value"))
frm.evaluate("document.getElementById('send').click()"); w.page.wait_for_timeout(800)
check('J: before anything is sent, who listens is asked, and the words stay', len(api.posts) == 0 and frm.evaluate("!document.getElementById('lsAsk').classList.contains('hide')") and 'restless tonight' in frm.evaluate("document.getElementById('words').value"))
check('J: the line says why', frm.evaluate("document.getElementById('who').textContent") == 'First, choose who listens. Your words wait in the box.')
w.shot('j_mid_consent_in_map')
frm.evaluate("[...document.querySelectorAll('#lsAsk button')].find(b=>b.textContent==='Claude, an AI').click()"); w.page.wait_for_timeout(4200)
check('J: once chosen, the words go by themselves', len(api.posts) == 1 and 'restless tonight' in api.posts[0]['words'], api.posts)
check('J: and Claude answers', 'What is the restlessness asking for?' in frm.evaluate("document.getElementById('speak').innerText"))
n0 = len(w.popups)
frm.evaluate("(()=>{const a=document.createElement('a');a.href='https://buy.stripe.com/aFacN7aoI9Eo6Ahale87K00';a.target='_blank';a.rel='noopener noreferrer';a.textContent='x';document.body.appendChild(a);a.click();})()"); w.page.wait_for_timeout(800)
check('J: from inside the map, the gift link can open its window', len(w.popups) > n0, len(w.popups))
check('J: no page errors', not w.errors, w.errors[:3])
w.close()

# ── J2 · the review's race: the question of who listens is showing when the light on the map begins it ───────
io.open(TEST + '/test-host2.html', 'w', encoding='utf-8').write(io.open(TEST + '/test-host.html', encoding='utf-8').read().replace('},300);', '},1800);'))
api = Api('live', [CL('“Restless”.', 'What is it asking for?')])
w = Walk(390, 664, mobile=True, api=api); w.open('test-host2.html', wait=1200)
frm = [f for f in w.page.frames if f.url.endswith('mirror-living.html?in=site')][0]
shown_first = frm.evaluate("!document.getElementById('lsAsk').classList.contains('hide')")
w.page.wait_for_timeout(2400)
check('J2: the opening asked who listens, then the light began it, and the question stepped aside', shown_first and frm.evaluate("document.getElementById('lsAsk').classList.contains('hide')") and 'What is the light showing you?' in frm.evaluate("document.getElementById('speak').innerText"),
      (shown_first, frm.evaluate("document.getElementById('speak').innerText")))
frm.evaluate("document.getElementById('send').click()"); w.page.wait_for_timeout(700)
frm.evaluate("[...document.querySelectorAll('#lsAsk button')].find(b=>b.textContent==='Claude, an AI').click()"); w.page.wait_for_timeout(4200)
check('J2: asked again when they offer, then sent; the doors never come back over it', len(api.posts) == 1 and frm.evaluate("document.getElementById('doors').classList.contains('hide')") and 'What is it asking for?' in frm.evaluate("document.getElementById('speak').innerText"))
w.close()
api = Api('live', [CL('“Restless”.', 'What is it asking for?')])
w = Walk(390, 664, mobile=True, api=api, init="try{localStorage.setItem('as_mirror_listener','claude')}catch(e){}"); w.open('test-host.html', wait=3600)
frm = [f for f in w.page.frames if f.url.endswith('mirror-living.html?in=site')][0]
check('J3: words waiting from the light, with Claude chosen before: the page says Claude will read them', frm.evaluate("document.getElementById('who').textContent") == 'If you offer these words, Claude, an AI, will read them to answer.' and len(api.posts) == 0,
      frm.evaluate("document.getElementById('who').textContent"))
w.close()

# ── A2 · no helper: the fuller list of heavy words now reaches real help with the written rules too ────────────
api = Api('absent'); w = Walk(390, 664, mobile=True, api=api); w.open()
w.click_text('#doors button', 'Something else'); w.page.wait_for_timeout(3000)
w.say('I have been feeling suicidal lately')
check('A2: with the written rules, "suicidal" now reaches real help (it did not before)', '988' in w.speak() and len(api.posts) == 0, w.speak())
w.close()

# ── K · a preview without the key ('off'): the same as no helper ─────────────────────────────────────────────
api = Api('off'); w = Walk(390, 664, mobile=True, api=api); w.open()
check('K: a helper that is switched off is the same as none', w.visible('doors') and not w.visible('lsAsk') and not w.visible('who') and api.gets == 1)
w.close()

# ── L · reduced motion, laptop, consent screen ───────────────────────────────────────────────────────────────
api = Api('live'); w = Walk(1440, 900, reduce=True, api=api); w.open()
w.shot('l_consent_laptop_reduced')
check('L: reduced motion, no page errors', not w.errors, w.errors[:3])
w.close()

print('\n%d failed' % len(fails), fails)
