"""Tests draft 4 of the Mirror's two places (slow crumple, the breath ring, the burning words; fold, seal) in a real
browser. Test-only. Usage: python3 t_twoplaces3.py [path-to-page] [quick]"""
import os, sys, json
from playwright.sync_api import sync_playwright

SRC = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1].endswith('.html') else '/home/claude/work/out/two-places/the-two-places.html'
OUT = '/tmp/claude-0/-home-claude/89e7564b-fd6e-5cd5-8cd5-5383c8af45f8/scratchpad/twoplaces4'
os.makedirs(OUT, exist_ok=True)
page_html = ('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
             '<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top);padding-bottom:env(safe-area-inset-bottom)}body{margin:0;font:14px system-ui}[hidden]{display:none!important}</style></head><body>'
             + open(SRC, encoding='utf-8').read() + '</body></html>')
H = os.path.join(OUT, 'harness.html'); open(H, 'w', encoding='utf-8').write(page_html)
fails = []
def check(name, ok, detail=''):
    print(('PASS ' if ok else 'FAIL ') + name + ('' if ok else '  -> ' + str(detail)[:300]), flush=True)
    if not ok: fails.append(name)

def speak(p): return p.eval_on_selector('#speak', 'e => e.innerText')
def guide(p): return p.eval_on_selector('#tpGuide', 'e => e.innerText')
def who(p): return p.eval_on_selector('#who', 'e => e.textContent')
def doors(p): return p.eval_on_selector_all('#tpDoors .door', 'es => es.map(e => e.innerText.replace(/\\s+/g," ").trim())')
def kept(p): return p.evaluate("() => JSON.parse(localStorage.getItem('as_reminding') || '[]')")
def click_door(p, label): p.locator('#tpDoors .door', has_text=label).first.click()
def settle(p, ms=700): p.wait_for_timeout(ms)
def until(p, js, ms=9000):
    try: p.wait_for_function(js, timeout=ms); return True
    except Exception: return False
def speak_has(p, text, ms=12000): return until(p, "() => document.getElementById('speak').innerText.includes(%s)" % json.dumps(text), ms)
def guide_has(p, text, ms=9000): return until(p, "() => document.getElementById('tpGuide').innerText.includes(%s)" % json.dumps(text), ms)
INK = """() => { const c=document.querySelector('.tpfx'), g=c.getContext('2d'), d=g.getImageData(0,0,c.width,c.height).data;
  let n=0, x0=1e9, x1=-1, y0=1e9, y1=-1; const w=c.width;
  for(let i=3;i<d.length;i+=16){ if(d[i]>40){ n++; const k=(i-3)/4, x=k%w, y=(k-x)/w; if(x<x0)x0=x; if(x>x1)x1=x; if(y<y0)y0=y; if(y>y1)y1=y; } }
  const dpr=c.width/c.offsetWidth; return {n:n, w:(x1-x0)/dpr, h:(y1-y0)/dpr, cx:(x0+x1)/2/dpr, cy:(y0+y1)/2/dpr}; }"""
def ink(p): return p.evaluate(INK)
def stage(p): return p.get_attribute('.tpfx', 'data-stage') or ''
def paper(p): return [float(x) for x in (p.get_attribute('.tpfx', 'data-paper') or '0,0,0,0').split(',')]
def dark_middle(p): return p.evaluate("() => { const c=document.querySelector('.tpfx'), g=c.getContext('2d'), d=g.getImageData(Math.round(c.width*0.5), Math.round(c.height*0.25), 1, 1).data; return d[3] > 140 && d[0] < 110; }")
def circle(p): return p.eval_on_selector('#mirror', 'e => { const r=e.getBoundingClientRect(); return {x:r.left+r.width/2, y:r.top+r.height/2, R:r.width/2}; }')

with sync_playwright() as pw:
    br = pw.chromium.launch()
    for (w, h, tag) in [(390, 844, 'phone'), (1280, 800, 'laptop')]:
        ctx = br.new_context(viewport={'width': w, 'height': h}, device_scale_factor=2 if tag == 'phone' else 1, has_touch=(tag == 'phone'))
        p = ctx.new_page(); errs = []
        p.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
        p.on('pageerror', lambda e: errs.append(str(e)))
        p.goto('file://' + H); settle(p, 900)
        T = tag + ': '
        check(T + 'opens with the two places, apart and unalike',
              'A thought that keeps coming back?' in speak(p) and p.is_visible('#tpLet') and p.is_visible('#tpKeep') and p.is_visible('#tpDoors .or'), doors(p))
        p.screenshot(path=os.path.join(OUT, tag + '-01-home.png'))

        # LET IT GO
        p.click('#tpLet'); settle(p)
        check(T + 'before writing, it says what will happen and what it can mean', 'It will leave your hand, and it can leave your mind too.' in speak(p), speak(p))
        check(T + 'letting go turns the circle warm', p.evaluate("() => document.body.classList.contains('tp-warm')"), '')
        p.fill('#tpWords', 'I always mess everything up'); click_door(p, 'It’s written'); settle(p, 1300)
        check(T + 'dusk falls in the circle, and the words write themselves onto the paper', stage(p) == 'writing' and dark_middle(p), [stage(p), dark_middle(p)])
        ok = until(p, "() => !!document.getElementById('tpCrumple')", 6000)
        check(T + 'the thought on paper, with a moment to be with it', ok and stage(p) == 'paper' and 'Here it is. Take a moment with it.' in guide(p) and 'breathe in slowly as you crumple it' in guide(p), guide(p))
        check(T + 'the words are only drawn, never in the page as text', 'mess everything up' not in p.content(), '')
        p.screenshot(path=os.path.join(OUT, tag + '-02-paper.png'))
        pr = paper(p); c = circle(p); cvb = p.eval_on_selector('.tpfx', 'e => { const r=e.getBoundingClientRect(); return {x:r.left, y:r.top}; }')
        p.mouse.click(cvb['x'] + pr[0] + pr[2] / 2, cvb['y'] + pr[1] + pr[3] / 2)
        settle(p, 1700); p.screenshot(path=os.path.join(OUT, tag + '-03-crumple.png'))
        pv = float(p.get_attribute('.tpfx', 'data-p') or 0)
        check(T + 'the crumple is slow and goes with the breath in', 0.15 < pv < 0.7 and 'Breathe in slowly' in guide(p), [pv, guide(p)])
        check(T + '... a little more ... as the last squeeze comes', guide_has(p, 'a little more', 4500), guide(p))
        check(T + 'no throw yet while still breathing in', not p.is_visible('#tpThrow'), '')
        ok = guide_has(p, 'Now throw it into the fire, and breathe out.', 3500)
        bb = p.eval_on_selector('#tpThrow', 'e => { const r=e.getBoundingClientRect(); return {top:r.top, bottom:r.bottom, w:r.width, h:r.height}; }') if p.is_visible('#tpThrow') else None
        check(T + 'the moment the crumple ends, Throw it in appears, big and in view', ok and bb is not None and bb['bottom'] <= h and bb['h'] >= 44, [guide(p), bb])
        check(T + 'it is a ball now', stage(p) == 'ball', stage(p))
        settle(p, 600); p.screenshot(path=os.path.join(OUT, tag + '-04-ready.png'))
        c = circle(p); bx, by = c['x'], c['y'] - c['R'] * 0.1
        p.mouse.move(bx, by); p.mouse.down(); p.mouse.up()
        check(T + 'a tap on the paper throws it, with the breath out', guide_has(p, 'Breathe out slowly', 2000) and not p.is_visible('#tpThrow'), guide(p))
        settle(p, 1500); p.screenshot(path=os.path.join(OUT, tag + '-05-catch.png'))
        check(T + 'it burns in the fire', stage(p) == 'burning', stage(p))
        settle(p, 1500); p.screenshot(path=os.path.join(OUT, tag + '-06-burning.png'))
        settle(p, 1500); p.screenshot(path=os.path.join(OUT, tag + '-07-burning.png'))
        check(T + 'the breath out lasts as long as the burning: still burning five seconds on', 'Gone.' not in speak(p) and stage(p) == 'burning', [speak(p), stage(p)])
        check(T + '... all the way out', guide_has(p, 'all the way out', 3000), guide(p))
        settle(p, 900); p.screenshot(path=os.path.join(OUT, tag + '-08-burning.png'))
        ok = speak_has(p, 'Gone.', 9000)
        check(T + 'then gone, and the words that follow', ok and 'It has left your hand. Let it leave your mind too.' in speak(p), speak(p))
        check(T + 'and dusk lifts again', until(p, "() => { const c=document.querySelector('.tpfx'), g=c.getContext('2d'); return g.getImageData(c.width>>1, c.height>>1, 1, 1).data[3] < 30; }", 3000), '')
        check(T + 'the real-paper line follows', guide_has(p, 'If you have paper nearby', 4000), guide(p))
        check(T + 'nothing let go is kept anywhere', kept(p) == [] and 'mess' not in json.dumps(p.evaluate('() => Object.assign({}, localStorage)')), '')
        p.screenshot(path=os.path.join(OUT, tag + '-10-gone.png'))

        # waiting at the top of the breath: no pressure
        click_door(p, 'Let another go'); settle(p); p.fill('#tpWords', 'Nobody listens to me'); p.keyboard.press('Enter')
        until(p, "() => !!document.getElementById('tpCrumple')", 6000); p.click('#tpCrumple'); until(p, "() => !!document.getElementById('tpThrow')", 9000)
        check(T + 'if they wait, it says to breathe however feels easy', guide_has(p, 'Breathe however feels easy', 6000) and p.is_visible('#tpThrow'), guide(p))
        p.click('#tpThrow')
        check(T + 'and it still goes into the fire', speak_has(p, 'Gone.', 14000), speak(p))

        # by the buttons alone
        click_door(p, 'Let another go'); settle(p); p.fill('#tpWords', 'They all think I am boring'); p.keyboard.press('Enter')
        until(p, "() => !!document.getElementById('tpCrumple')", 6000); p.click('#tpCrumple')
        check(T + 'the Crumple it button works too; Throw it in comes as the crumple ends', until(p, "() => !!document.getElementById('tpThrow')", 9000), doors(p))
        p.click('#tpThrow')
        check(T + 'and Throw it in', speak_has(p, 'Gone.', 14000), speak(p))

        # heavy words
        click_door(p, 'Let another go'); settle(p); p.fill('#tpWords', 'some days I want to die'); click_door(p, 'It’s written'); settle(p)
        check(T + 'heavy words: real help first, never the fire', '988' in speak(p) and not p.is_visible('#tpCrumple') and ink(p)['n'] < 50, speak(p))
        click_door(p, 'Back'); settle(p)

        # THE RE-MINDING
        p.click('#tpKeep'); settle(p)
        check(T + 'keeping turns the circle cool', p.evaluate("() => document.body.classList.contains('tp-cool')"), '')
        p.fill('#tpWords', 'Don’t decide anything big when you’re exhausted. Sleep on it first.'); click_door(p, 'It’s written'); settle(p)
        check(T + 'it asks when it should come back', 'When should it come back to you?' in speak(p) and 'A big choice' in doors(p), doors(p))
        click_door(p, 'A big choice'); settle(p, 2000); p.screenshot(path=os.path.join(OUT, tag + '-11-folding.png'))
        check(T + 'it folds into an envelope, and waits to be sealed', until(p, "() => !!document.getElementById('tpSeal')", 6000) and 'Seal it.' in guide(p), guide(p))
        p.screenshot(path=os.path.join(OUT, tag + '-12-envelope.png'))
        check(T + 'it is kept, on this device only', len(kept(p)) == 1 and kept(p)[0]['moment'] == 'choice', kept(p))
        p.click('#tpSeal'); settle(p, 1100); p.screenshot(path=os.path.join(OUT, tag + '-13-sealing.png'))
        check(T + 'sealed, for a big choice', speak_has(p, 'Sealed, for a big choice.', 8000) and 'Your mind can put it down now.' in speak(p), speak(p))
        click_door(p, 'Keep another'); settle(p); p.fill('#tpWords', 'Breathe before you answer.'); click_door(p, 'It’s written'); settle(p)
        click_door(p, 'Something else…'); settle(p)
        check(T + 'something else: a short box', p.eval_on_selector('#tpWords', 'e => e.maxLength') == 60, '')
        p.fill('#tpWords', 'before a job interview'); click_door(p, 'Keep it for then')
        until(p, "() => !!document.getElementById('tpSeal')", 8000); p.click('#tpSeal')
        check(T + 'sealed for a moment in their own words', speak_has(p, 'Sealed, for before a job interview.', 8000) and len(kept(p)) == 2, speak(p))
        click_door(p, 'Done'); settle(p)
        check(T + 'home offers what was kept; boxes back to full length', 'What I’ve kept (2)' in doors(p) and p.eval_on_selector('#tpWords', 'e => e.maxLength') == 280, doors(p))

        # WHEN A MOMENT COMES
        click_door(p, 'Something is happening now'); settle(p); p.fill('#tpWords', 'I have to decide whether to take the offer'); click_door(p, 'That’s it'); settle(p)
        check(T + 'a matching moment: offered, never pushed', 'You kept something for moments like this.' in speak(p) and 'Sleep on it' not in p.content(), speak(p))
        click_door(p, 'Show me')
        check(T + 'its envelope comes back, still sealed', until(p, "() => !!document.getElementById('tpOpen')", 4000) and 'for a big choice' in guide(p), guide(p))
        p.click('#tpOpen')
        check(T + 'opened: the words, as they were kept', speak_has(p, 'Sleep on it first.', 5000) and 'You kept this for a big choice.' in speak(p), speak(p))
        click_door(p, 'Keep it'); settle(p)
        check(T + 'keep it: still kept', len(kept(p)) == 2 and p.is_visible('#tpList') and 'Still kept.' in who(p), who(p))
        click_door(p, 'Back'); settle(p)
        click_door(p, 'Something is happening now'); settle(p); p.fill('#tpWords', 'I felt this way before about the weather'); click_door(p, 'That’s it'); settle(p)
        check(T + 'no match: says so plainly', 'Nothing you’ve kept is for a moment like this.' in speak(p), speak(p))

        # THE LIST, and letting a kept thought go
        click_door(p, 'Open what I’ve kept'); settle(p)
        items = p.eval_on_selector_all('#tpList .tpmoment', 'es => es.map(e => e.innerText.replace(/\\s+/g, " "))')
        check(T + 'the list shows only the moments, never the words', items == ['For a big choice 1', 'For before a job interview 1'] and 'Breathe before' not in p.content(), items)
        p.locator('#tpList .tpmoment').nth(1).click(); until(p, "() => !!document.getElementById('tpOpen')", 4000); p.click('#tpOpen')
        speak_has(p, 'Breathe before you answer', 5000)
        click_door(p, 'Let it go now')
        check(T + 'a kept thought whose moment has passed can go into the fire', guide_has(p, 'Its moment has passed', 4000) and len(kept(p)) == 1, guide(p))
        until(p, "() => !!document.getElementById('tpCrumple')", 6000); p.click('#tpCrumple'); until(p, "() => !!document.getElementById('tpThrow')", 14000); p.click('#tpThrow')
        check(T + '... and it is gone from the device', speak_has(p, 'Gone.', 14000) and 'Breathe' not in json.dumps(kept(p)), kept(p))
        click_door(p, 'Done'); settle(p); click_door(p, 'What I’ve kept (1)'); settle(p)
        p.locator('#tpList .door', has_text='Forget all of it').click(); settle(p, 200)
        p.locator('#tpList .door', has_text='Tap again').click(); settle(p)
        check(T + 'forget all: nothing kept, back home', kept(p) == [] and p.is_visible('#tpLet') and 'Forgotten' in who(p), who(p))

        # the longest thought stays inside the circle; nothing scrolls sideways
        p.click('#tpLet'); settle(p); p.fill('#tpWords', ('I keep thinking that if I had only said something different that day then none of this would have happened and everyone would still be talking to me and ' * 3)[:280]); click_door(p, 'It’s written'); settle(p, 300)
        until(p, "() => !!document.getElementById('tpCrumple')", 8000)
        pr = paper(p); c = circle(p); cv = p.eval_on_selector('.tpfx', 'e => { const r=e.getBoundingClientRect(); return {x:r.left, y:r.top}; }')
        top = cv['y'] + pr[1]; bottom = cv['y'] + pr[1] + pr[3]
        check(T + 'the longest thought fits on paper inside the circle', top > c['y'] - c['R'] and bottom < c['y'] + c['R'], [top, bottom, c])
        p.screenshot(path=os.path.join(OUT, tag + '-14-long.png'))
        sw = p.evaluate('() => [document.documentElement.scrollWidth, innerWidth]')
        check(T + 'nothing scrolls sideways', sw[0] <= sw[1], sw)
        check(T + 'no errors', not errs, errs)
        ctx.close()

    # stillness
    ctx = br.new_context(viewport={'width': 390, 'height': 844}, reduced_motion='reduce'); p = ctx.new_page(); errs = []
    p.on('pageerror', lambda e: errs.append(str(e)))
    p.goto('file://' + H); settle(p, 300)
    p.click('#tpLet'); settle(p, 200); p.fill('#tpWords', 'not good enough'); click_door(p, 'It’s written'); until(p, "() => !!document.getElementById('tpCrumple')", 3000)
    p.click('#tpCrumple'); settle(p, 1200)
    check('still: one plain instruction for the breath, and the throw is ready', 'Now throw it into the fire as you breathe out.' in guide(p) and p.is_visible('#tpThrow'), guide(p))
    p.click('#tpThrow')
    check('still: let go quickly and quietly', speak_has(p, 'Gone.', 3000), speak(p))
    click_door(p, 'Done'); settle(p, 300); p.click('#tpKeep'); settle(p, 200); p.fill('#tpWords', 'Ask for help sooner.'); click_door(p, 'It’s written'); settle(p, 300)
    click_door(p, 'When I’m worn out'); until(p, "() => !!document.getElementById('tpSeal')", 3000); p.click('#tpSeal')
    check('still: sealed quickly too', speak_has(p, 'Sealed, for when you’re worn out.', 3000), speak(p))
    check('still: no errors', not errs, errs)
    ctx.close(); br.close()
print('\n%d failed' % len(fails), fails)
sys.exit(1 if fails else 0)
