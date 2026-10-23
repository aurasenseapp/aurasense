"""Build 158 · the Mirror page with a pretend helper: one plain question (Begin with Claude / Not now), only Claude
answers where Claude can listen, words go back in the box when Claude can't, Stop sharing my words, an older
"rules" choice asked again, the light on the map, the gift line, and nothing sent without a yes. Test-only."""
import sys, io, os, json, shutil
sys.path.insert(0, '/home/claude/scripts')
from harness import *
shutil.copy('/home/claude/aurasense/mirror-living.html', TEST + '/mirror-living.html')
shutil.copy('/home/claude/work/mirror-living.157.html', TEST + '/mirror157.html')
fails = []
def check(name, ok, detail=''):
    print(('PASS ' if ok else 'FAIL ') + name + ('' if ok else '  -> ' + str(detail)[:400]), flush=True)
    if not ok: fails.append(name)
CL = lambda refl, q, asp='': {'ok': True, 'by': 'claude', 'reflect': refl, 'question': q, 'aspire': asp, 'care': False, 'ground': False}
YES = "try{localStorage.setItem('as_mirror_listener','claude')}catch(e){}"
note = lambda w: w.js("document.getElementById('note').textContent")

# A · no helper (a preview): the written rules answer exactly as in 157, nothing is sent
outs = {}
for f in ['mirror157.html', 'mirror-living.html']:
    api = Api('absent'); w = Walk(390, 664, mobile=True, api=api); w.open(f)
    w.click_text('#doors button', 'Something else'); w.page.wait_for_timeout(3000)
    t = [w.speak()]
    for s in ['I keep going round in circles about work', 'in my chest', 'yes, many times']: w.say(s); t.append(w.speak())
    outs[f] = (t, len(api.posts), w.visible('lsAsk'), w.errors[:2]); w.close()
check('A: no helper: the written rules answer exactly as before', outs['mirror157.html'][0] == outs['mirror-living.html'][0], outs)
check('A: no helper: nothing sent, nothing asked', outs['mirror-living.html'][1] == 0 and not outs['mirror-living.html'][2] and not outs['mirror-living.html'][3], outs['mirror-living.html'][1:])

# B · first visit with Claude switched on: one plain question, two equal answers
api = Api('live', [CL('You said “round in circles”.', 'What starts the circle?')])
w = Walk(390, 664, mobile=True, api=api); w.open()
check('B: the opening asks one plain question', 'Would you like Claude, an AI, to listen to you here?' in w.speak(), w.speak())
check('B: Begin with Claude, or Not now', w.js("[...document.querySelectorAll('#lsAsk button')].map(b=>b.textContent).join('|')") == 'Begin with Claude|Not now')
check('B: no mention of the written rules anywhere on screen', 'written rules' not in w.js("document.body.innerText"), '')
check('B: what a yes means, with the privacy link', 'Aurasense keeps nothing' in w.js("document.getElementById('lsAsk').textContent") and '30 days' in w.js("document.getElementById('lsAsk').textContent"))
w.shot('158_ask')
w.click_text('#lsAsk button', 'Not now'); w.page.wait_for_timeout(2600)
check('B: Not now: nothing sent, and said so', 'Nothing has left this page.' in w.speak() and len(api.posts) == 0, w.speak())
check('B: Not now: the way back in stays open', w.js("[...document.querySelectorAll('#lsAsk button')].map(b=>b.textContent).join('|')") == 'Begin with Claude after all')
check('B: Not now remembers nothing', w.js("localStorage.getItem('as_mirror_listener')") is None)
w.shot('158_not_now')
w.click_text('#lsAsk button', 'Begin with Claude after all'); w.page.wait_for_timeout(2600)
check('B: after all: the usual opening and the doors', 'What would you like to see more clearly?' in w.speak() and w.visible('doors'), w.speak())
w.click_text('#doors button', 'Something else'); w.page.wait_for_timeout(3000)
w.say('I keep going round in circles about work')
check('B: Claude answers, and says so', len(api.posts) == 1 and w.who() == 'Answered by Claude, an AI, listening.' and 'What starts the circle?' in w.speak(), (len(api.posts), w.who()))
check('B: the note says Claude is listening, with the way to stop', note(w).startswith('Claude, an AI, is listening; Aurasense keeps nothing.') and 'Stop sharing my words' in note(w), note(w))
w.say('I have been feeling suicidal lately')
check('B: heavy words never sent; real help shows', len(api.posts) == 1 and '988' in w.speak(), (len(api.posts), w.speak()[:80]))
check('B: no page errors', not w.errors, w.errors[:3])
w.close()

# C · Claude can't answer: the words go back in the box, with the reason; nothing answers in Claude's place
api = Api('live', [{'ok': False, 'code': 'upstream', '_status': 503}, CL('“Quieter now”.', 'What made it quieter?')])
w = Walk(390, 664, mobile=True, api=api, init=YES); w.open()
w.click_text('#doors button', 'Something else'); w.page.wait_for_timeout(3000)
before = w.speak()
w.say('I have felt this for a while, and it is getting heavier')
check('C: nothing answers in Claude’s place', w.speak() == before, w.speak())
check('C: the words are back in the box, exactly as written', w.js("document.getElementById('words').value") == 'I have felt this for a while, and it is getting heavier')
check('C: and the reason is said plainly', w.who() == 'Claude couldn’t answer just then. Your words are back in the box; send them again when you’re ready.', w.who())
w.js("document.getElementById('send').click()"); w.page.wait_for_timeout(4200)
check('C: sent again, Claude answers', len(api.posts) == 2 and 'What made it quieter?' in w.speak(), (len(api.posts), w.speak()))
check('C: the failed try left nothing behind in the thread', sum(1 for t in api.posts[1]['turns'] if t['role'] == 'user') == 0, api.posts[1]['turns'])
check('C: no page errors', not w.errors, w.errors[:3])
w.close()

# D · Claude resting (credit used): the words stay, nothing more is sent this visit
api = Api('live', [{'ok': False, 'code': 'resting', '_status': 503}])
w = Walk(390, 664, mobile=True, api=api, init=YES); w.open()
w.click_text('#doors button', 'Something else'); w.page.wait_for_timeout(3000)
w.say('I feel stuck between two jobs')
check('D: resting: said plainly, words back in the box', w.who().startswith('The Mirror is resting for now.') and w.js("document.getElementById('words').value") == 'I feel stuck between two jobs', w.who())
w.js("document.getElementById('send').click()"); w.page.wait_for_timeout(1500)
check('D: nothing more is sent this visit', len(api.posts) == 1, len(api.posts))
check('D: the note says the Mirror is resting', note(w).startswith('The Mirror is resting for now.'), note(w))
check('D: no page errors', not w.errors, w.errors[:3])
w.close()

# E · an older "rules" choice is asked again
api = Api('live', [])
w = Walk(390, 664, mobile=True, api=api, init="try{localStorage.setItem('as_mirror_listener','rules')}catch(e){}"); w.open()
check('E: an older “rules” choice is asked again', w.visible('lsAsk') and not w.visible('doors'), (w.visible('lsAsk'), w.visible('doors')))
w.close()

# F · Stop sharing my words
api = Api('live', [CL('“Restless”.', 'Where does it want to go?')])
w = Walk(390, 664, mobile=True, api=api, init=YES); w.open()
w.click_text('#doors button', 'Something else'); w.page.wait_for_timeout(3000)
w.say('restless')
w.js("[...document.querySelectorAll('#note button')].find(b=>b.textContent==='Stop sharing my words').click()"); w.page.wait_for_timeout(2600)
check('F: Stop sharing: the yes is forgotten', w.js("localStorage.getItem('as_mirror_listener')") is None)
check('F: and the conversation rests, said plainly', w.who() == 'Nothing more will be shared. The Mirror will ask again next time.' and 'What would you like to leave with?' in w.speak(), (w.who(), w.speak()))
check('F: no page errors', not w.errors, w.errors[:3])
w.close()

# G · begun from the light on the map, inside the map's frame: asked first, words wait, then go
api = Api('live', [CL('“Restless tonight”.', 'What is the restlessness asking for?')])
w = Walk(390, 664, mobile=True, api=api); w.open('test-host.html', wait=3600)
frm = [f for f in w.page.frames if f.url.endswith('mirror-living.html?in=site')][0]
frm.evaluate("document.getElementById('send').click()"); w.page.wait_for_timeout(800)
check('G: asked first; the words wait; nothing sent', len(api.posts) == 0 and frm.evaluate("!document.getElementById('lsAsk').classList.contains('hide')") and 'restless tonight' in frm.evaluate("document.getElementById('words').value"))
check('G: the line says why', frm.evaluate("document.getElementById('who').textContent") == 'First, a question. Your words wait in the box.')
frm.evaluate("[...document.querySelectorAll('#lsAsk button')].find(b=>b.textContent==='Begin with Claude').click()"); w.page.wait_for_timeout(4200)
check('G: once begun, the words go by themselves, and Claude answers', len(api.posts) == 1 and 'What is the restlessness asking for?' in frm.evaluate("document.getElementById('speak').innerText"))
check('G: no page errors', not w.errors, w.errors[:3])
w.close()
api = Api('live', [])
w = Walk(390, 664, mobile=True, api=api); w.open('test-host.html', wait=3600)
frm = [f for f in w.page.frames if f.url.endswith('mirror-living.html?in=site')][0]
frm.evaluate("document.getElementById('send').click()"); w.page.wait_for_timeout(800)
frm.evaluate("[...document.querySelectorAll('#lsAsk button')].find(b=>b.textContent==='Not now').click()"); w.page.wait_for_timeout(2600)
check('G: Not now from the map: nothing sent, and said so', len(api.posts) == 0 and 'Nothing has left this page.' in frm.evaluate("document.getElementById('speak').innerText"))
w.close()

# H · the gift line after a good ending with Claude
api = Api('live', [CL('“Restless”.', 'Where does it want to go?'), CL('“Outside”.', 'What would one walk be like?'), CL('“Lighter”.', 'What will you keep?')])
w = Walk(390, 664, mobile=True, api=api, init=YES); w.open()
w.click_text('#doors button', 'Something else'); w.page.wait_for_timeout(3000)
w.say('restless'); w.say('outside'); w.say('lighter')
w.js("document.getElementById('rest').click()"); w.page.wait_for_timeout(3000)
w.click_text('#doors button', 'Just the feeling of being met'); w.page.wait_for_timeout(3600)
check('H: after a good ending, the gift line', w.visible('gift'))
check('H: no page errors', not w.errors, w.errors[:3])
w.close()

# K · a helper switched off (a preview): the written rules, nothing asked
api = Api('off'); w = Walk(390, 664, mobile=True, api=api); w.open()
check('K: switched off: no question, the doors at once', w.visible('doors') and not w.visible('lsAsk'))
w.close()

print('\n%d failed' % len(fails), fails)
