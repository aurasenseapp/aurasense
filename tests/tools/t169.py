"""Build 169 · Let it go draft 4 inside the Mirror, and Listen Forward through Stripe; privacy and terms. Test-only."""
import sys, os, io, json, shutil
sys.path.insert(0, '/home/claude/scripts')
from harness import *
shutil.copy('/home/claude/aurasense/mirror-living.html', TEST + '/mirror-living.html')
io.open(TEST + '/privacy.html', 'w').write('<!doctype html><title>privacy</title>')
STRIPE = 'https://buy.stripe.com/aFacN7aoI9Eo6Ahale87K00'
fails = []
def check(name, ok, detail=''):
    print(('PASS ' if ok else 'FAIL ') + name + ('' if ok else '  -> ' + str(detail)[:400]), flush=True)
    if not ok: fails.append(name)
YES = "try{localStorage.setItem('as_mirror_listener','claude')}catch(e){}"
def helper():
    n = {'i': 0}
    def r(body):
        if body.get('keep'): return {'ok': True, 'by': 'claude', 'keep': {'found': 'You found “slow”.', 'step': 'A walk.', 'wiser': 'Slow is allowed.'}}
        n['i'] += 1
        return {'ok': True, 'by': 'claude', 'reflect': '“Turn %d”, you said.' % n['i'], 'question': 'What else is here, %d?' % n['i'], 'aspire': '', 'care': False, 'ground': False}
    return r
def until(w, js, ms=12000):
    try: w.page.wait_for_function(js, timeout=ms); return True
    except Exception: return False

# A · the Listen Forward door now opens Stripe, worded as payment for the listening just had
api = Api('live', [helper()]); api.replies = [helper()] * 30
w = Walk(390, 664, mobile=True, api=api, init=YES); w.open()
w.click_text('#doors button', 'Something else'); w.page.wait_for_timeout(3000)
w.say('restless'); w.say('outside, walking'); w.say('lighter')
w.js("document.getElementById('rest').click()"); w.page.wait_for_timeout(2600)
w.click_text('#doors button', 'Just the feeling of being met'); w.page.wait_for_timeout(3600)
check('A: after a good ending, Listen Forward shows', w.visible('gift'))
g = w.js("({t:document.getElementById('gift').innerText,h:document.querySelector('#gift a').href,tg:document.querySelector('#gift a').target,rel:document.querySelector('#gift a').rel,l:document.querySelector('#gift a').innerText})")
check('A: it asks only if it helped, for the listening just had', 'If it helped, you can pay what feels right for it, and keep it open for the next person.' in g['t'] and 'It pays for the listening you’ve just had' in g['t'], g['t'])
check('A: it says plainly it opens Stripe and the person chooses the amount; never Ko-fi, never gifts', 'Listen forward opens a secure Stripe page where you choose the amount.' in g['t'] and 'Ko-fi' not in g['t'] and 'Gift' not in g['t'], g['t'])
check('A: it opens the Stripe page in a new window, safely', g['h'] == STRIPE and g['tg'] == '_blank' and 'noopener' in g['rel'] and g['l'] == 'Listen forward', g)
check('A: "or simply go well" is right beside it', 'or simply go well' in g['t'], g['t'])
w.shot('169_A_gift')
check('A: no page errors', not w.errors, w.errors[:3])
w.close()

# B · Let it go, draft 4, inside the Mirror on a small phone: the throw button is big and in view, and dusk lifts after
api = Api('live', [helper()]); api.replies = [helper()] * 30
w = Walk(375, 667, mobile=True, api=api, init=YES); w.open()
w.js("document.getElementById('tpEnter').click()"); w.page.wait_for_timeout(1600); w.js("document.getElementById('tpLet').click()"); w.page.wait_for_timeout(1500)
w.js("t=>{document.getElementById('tpWords').value=t;}", 'I always mess everything up'); w.click_text('#tpDoors button', 'It’s written')
check('B: the words write themselves, then Crumple it', until(w, "() => document.querySelector('.tpfx').getAttribute('data-stage')==='writing'", 3000) and until(w, "() => !!document.getElementById('tpCrumple')", 7000))
w.shot('169_B_paper')
w.js("document.getElementById('tpCrumple').click()")
check('B: breathe in as it crumples', until(w, "() => document.getElementById('tpGuide').innerText.includes('Breathe in slowly')", 2000))
check('B: the throw comes as the crumple ends', until(w, "() => !!document.getElementById('tpThrow')", 9000))
bb = w.js("(() => { const r=document.getElementById('tpThrow').getBoundingClientRect(); return {bottom:r.bottom, h:r.height, vh:innerHeight}; })()")
check('B: Throw it in is big, and in view without scrolling', bb['bottom'] <= bb['vh'] and bb['h'] >= 44, bb)
w.shot('169_B_ready', full=False)
w.js("document.getElementById('tpThrow').click()")
check('B: breathe out as it burns', until(w, "() => document.getElementById('tpGuide').innerText.includes('Breathe out slowly')", 2000))
check('B: gone, and dusk lifts', until(w, "() => document.getElementById('speak').innerText.includes('Gone.')", 15000) and until(w, "() => { const c=document.querySelector('.tpfx'), g=c.getContext('2d'); return g.getImageData(c.width>>1, c.height>>1, 1, 1).data[3] < 30; }", 3000))
sw = w.js('[document.documentElement.scrollWidth, innerWidth]')
check('B: nothing scrolls sideways', sw[0] <= sw[1], sw)
check('B: no page errors', not w.errors, w.errors[:3])
w.close()

# C · privacy and terms tell the truth about Stripe
pv = io.open('/home/claude/aurasense/privacy.html', encoding='utf-8').read(); tm = io.open('/home/claude/aurasense/terms.html', encoding='utf-8').read()
check('C: privacy names Stripe, and Ko-fi is gone', '<strong>Stripe</strong> — only if you choose to pay for the listening you' in pv and 'Ko-fi' not in pv and 'Last updated: 27 October 2026.' in pv)
check('C: terms: pay what feels right, through Stripe, a thank-you that unlocks nothing; no Ko-fi', 'pay what feels right' in tm and STRIPE in tm and 'unlocks nothing' in tm and 'Ko-fi' not in tm and 'Last updated: 27 October 2026.' in tm)
for f in ['mirror-living.html', 'privacy.html', 'terms.html', 'index-mapbox.html', 'seeking.html']:
    t = io.open('/home/claude/aurasense/' + f, encoding='utf-8').read()
    check('C: no test hooks or private words in ' + f, '__T=' not in t and 'Harvey' not in t)
print('\n%d failed' % len(fails), fails)
sys.exit(1 if fails else 0)
