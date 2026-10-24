"""Build 165 · the one-time hint under the little lights, walked in a real browser with a pretend helper. Test-only."""
import sys, io, os, shutil, json
sys.path.insert(0, '/home/claude/scripts')
from harness import *
shutil.copy('/home/claude/aurasense/mirror-living.html', TEST + '/mirror-living.html')
shutil.copy('/home/claude/work/mirror-living.164.html', TEST + '/mirror164.html')
fails = []
def check(name, ok, detail=''):
    print(('PASS ' if ok else 'FAIL ') + name + ('' if ok else '  -> ' + str(detail)[:400]), flush=True)
    if not ok: fails.append(name)
YES = "try{localStorage.setItem('as_mirror_listener','claude')}catch(e){}"
def helper():
    n = {'i': 0}
    def r(body):
        if body.get('keep'):
            return {'ok': True, 'by': 'claude', 'keep': {'found': 'You found “slow”.', 'wiser': 'Slow is allowed.'}}
        n['i'] += 1
        return {'ok': True, 'by': 'claude', 'reflect': '“Turn %d”, you said.' % n['i'], 'question': 'What else is here, %d?' % n['i'], 'aspire': '', 'care': False, 'ground': False}
    return r
HINT = """(()=>{const h=document.getElementById('trailHint');if(!h)return null;const r=h.getBoundingClientRect(),cs=getComputedStyle(h);
  return {hidden:h.hidden,on:h.classList.contains('on'),op:+cs.opacity,text:h.textContent,top:r.top|0,bottom:r.bottom|0,vh:innerHeight,
  lights:document.querySelectorAll('#trail button').length,flag:localStorage.getItem('as_trail_hint'),aria:h.getAttribute('aria-hidden'),
  seen:!h.hidden&&h.classList.contains('on')};})()"""
def lights(w): return w.js("document.querySelectorAll('#trail button').length")
def begin(w): w.click_text('#doors button', 'Something else'); w.page.wait_for_timeout(3000)
def live(W_=390, H_=664):
    api = Api('live', [helper()]); api.replies = [helper()] * 20
    w = Walk(W_, H_, mobile=True, api=api, init=YES); w.open(); return w

# A · it appears once there is something to look back at, and a touch on a light lets it go
w = live(); begin(w)
w.say('the hills feel alive'); h1 = w.js(HINT)
check('A: after one reply (two lights), no hint yet (its line quietly kept)', h1['lights'] == 2 and not h1['seen'] and h1['op'] < 0.05 and h1['aria'] == 'true', h1)
w.say('they ask me to slow down'); w.page.wait_for_timeout(900); h2 = w.js(HINT)
check('A: after two replies (three lights), the hint shows, in Karl\'s approved words', h2['lights'] == 3 and not h2['hidden'] and h2['on'] and h2['op'] > 0.9 and h2['text'] == 'Tap a light to see that moment again.', h2)
check('A: it sits on screen, beneath the lights', 0 < h2['top'] < h2['vh'] and h2['bottom'] <= h2['vh'], h2)
check('A: it is remembered on this device, so it shows only once', h2['flag'] == '1', h2)
w.shot('165_hint_phone')
w.js("document.querySelectorAll('#trail button')[1].click()"); w.page.wait_for_timeout(1100); h3 = w.js(HINT)
check('A: touching a light shows that moment again', '“Turn 1”, you said.' in w.speak(), w.speak())
w.page.wait_for_timeout(600); h3 = w.js(HINT)
check('A: and the hint goes, gently, and is silent to screen readers again', not h3['on'] and h3['op'] < 0.05 and h3['aria'] == 'true', h3)
check('A: no page errors', not w.errors, w.errors[:3])
# the same device, another visit: never again
w.page.reload(); w.page.wait_for_timeout(2600); begin(w)
for t in ['one', 'two', 'three']: w.say(t)
h4 = w.js(HINT)
check('A: another visit on the same device: no hint again, and no line kept for it', h4['hidden'] and h4['lights'] >= 4, h4)
w.close()

# B · it goes by itself once two more moments have come (counted in moments, never on a clock)
w = live(); begin(w)
w.say('one'); w.say('two'); w.page.wait_for_timeout(800)
b1 = w.js(HINT); w.say('three'); b2 = w.js(HINT); w.say('four'); w.page.wait_for_timeout(900); b3 = w.js(HINT)
check('B: shown at three lights, still there at four, gone at five', b1['seen'] and b2['seen'] and not b3['seen'], [b1, b2, b3])
w.close()

# C · letting it rest lets the hint rest too
w = live(); begin(w)
w.say('one'); w.say('two'); w.page.wait_for_timeout(800)
w.js("document.getElementById('rest').click()"); w.page.wait_for_timeout(1400); c1 = w.js(HINT)
check('C: "Let it rest here" lets the hint go too', not c1['seen'], c1)
check('C: the ending still offers Keep what I found', 'Keep what I found' in w.js("[...document.querySelectorAll('#doors button')].map(b=>b.textContent).join('|')"))
w.close()

# D · with the written rules (no helper), the same
w = Walk(390, 664, mobile=True); w.open(); begin(w)
w.say('I feel heavy today'); w.say('it is like a weight'); w.page.wait_for_timeout(900); d1 = w.js(HINT)
check('D: the written rules too: the hint shows at three lights', d1['lights'] >= 3 and d1['seen'], d1)
check('D: no page errors', not w.errors, w.errors[:3])
w.close()

# E · heavy words: care first, and no hint
w = live(); begin(w)
w.say('some days I want to die'); w.say('yes'); w.page.wait_for_timeout(900); e1 = w.js(HINT)
check('E: after heavy words, no hint appears', not e1['seen'], e1)
w.close()

# F · nothing moves out of reach: the words box and its button stay where they were in 164, on a small phone
def box(file):
    api = Api('live', [helper()]); api.replies = [helper()] * 20
    w = Walk(360, 640, mobile=True, api=api, init=YES); w.open(file); begin(w)
    w.say('one'); w.say('two'); w.page.wait_for_timeout(900)
    m = w.js("(()=>{const s=document.getElementById('send').getBoundingClientRect(),m=document.getElementById('mirror').getBoundingClientRect();return {send:s.bottom|0,mirror:m.top|0,vh:innerHeight,sh:document.documentElement.scrollHeight};})()")
    if file == 'mirror-living.html': w.shot('165_hint_smallphone')
    w.close(); return m
f164, f165 = box('mirror164.html'), box('mirror-living.html')
def moves(file):
    api = Api('live', [helper()]); api.replies = [helper()] * 20
    w = Walk(360, 640, mobile=True, api=api, init=YES); w.open(file); begin(w)
    pos = lambda: w.js("Math.round(document.getElementById('mirror').getBoundingClientRect().top)")
    out = [pos()]
    for t in ['one', 'two', 'three', 'four']:
        w.say(t); w.page.wait_for_timeout(900); out.append(pos())
    w.close(); return [b - a for a, b in zip(out, out[1:])]
m164, m165 = moves('mirror164.html'), moves('mirror-living.html')
check('F: small phone: the hint adds no movement of its own (each turn moves the circle exactly as in 164: %s)' % m165, m164 == m165, [m164, m165])
check('F: small phone: the "Offer it" button moves down by no more than one short line (%d px)' % (f165['send'] - f164['send']), 0 <= f165['send'] - f164['send'] <= 30, [f164, f165])

# G · the laptop
api = Api('live', [helper()]); api.replies = [helper()] * 20
w = Walk(1440, 900, api=api, init=YES); w.open(); begin(w); w.say('one'); w.say('two'); w.page.wait_for_timeout(900)
g = w.js(HINT); w.shot('165_hint_laptop')
check('G: laptop: the hint shows, on screen', g['seen'] and 0 < g['top'] < g['vh'], g)
w.close()
print('\n%d failed' % len(fails), fails)
