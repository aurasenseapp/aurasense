"""Tests draft 2 of the Mirror's two places (crumple, breathe, fire; fold, seal) in a real browser. Test-only."""
import os, sys, json
from playwright.sync_api import sync_playwright

SRC = '/home/claude/work/out/two-places/the-two-places.html'
OUT = '/tmp/claude-0/-home-claude/89e7564b-fd6e-5cd5-8cd5-5383c8af45f8/scratchpad/twoplaces2'
os.makedirs(OUT, exist_ok=True)
page_html = ('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
             '<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top);padding-bottom:env(safe-area-inset-bottom)}body{margin:0;font:14px system-ui}[hidden]{display:none!important}</style></head><body>'
             + open(SRC, encoding='utf-8').read() + '</body></html>')
H = os.path.join(OUT, 'harness.html'); open(H, 'w', encoding='utf-8').write(page_html)
fails = []
def check(name, ok, detail=''):
    print(('PASS ' if ok else 'FAIL ') + name + ('' if ok else '  -> ' + str(detail)[:300]))
    if not ok: fails.append(name)

def speak(p): return p.eval_on_selector('#speak', 'e => e.innerText')
def guide(p): return p.eval_on_selector('#guide', 'e => e.innerText')
def who(p): return p.eval_on_selector('#who', 'e => e.textContent')
def doors(p): return p.eval_on_selector_all('#doors .door', 'es => es.map(e => e.innerText.replace(/\\s+/g," ").trim())')
def kept(p): return p.evaluate("() => JSON.parse(localStorage.getItem('as_reminding') || '[]')")
def click_door(p, label): p.locator('#doors .door', has_text=label).first.click()
def settle(p, ms=700): p.wait_for_timeout(ms)
INK = """() => { const c=document.getElementById('fx'), g=c.getContext('2d'), d=g.getImageData(0,0,c.width,c.height).data;
  let n=0, x0=1e9, x1=-1, y0=1e9, y1=-1; const w=c.width;
  for(let i=3;i<d.length;i+=16){ if(d[i]>40){ n++; const k=(i-3)/4, x=k%w, y=(k-x)/w; if(x<x0)x0=x; if(x>x1)x1=x; if(y<y0)y0=y; if(y>y1)y1=y; } }
  const dpr=c.width/c.offsetWidth; return {n:n, w:(x1-x0)/dpr, h:(y1-y0)/dpr, cx:(x0+x1)/2/dpr, cy:(y0+y1)/2/dpr}; }"""
def ink(p): return p.evaluate(INK)
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
        check(T + 'opens with the question and the two places, apart and unalike',
              'A thought that keeps coming back?' in speak(p) and p.is_visible('#goLet') and p.is_visible('#goKeep') and p.is_visible('#doors .or')
              and 'ember' in p.get_attribute('#goLet', 'class') and 'seal' in p.get_attribute('#goKeep', 'class'), doors(p))
        p.screenshot(path=os.path.join(OUT, tag + '-01-home.png'))

        # LET IT GO: tap the paper, breathe, flick it into the fire
        p.click('#goLet'); settle(p)
        check(T + 'letting go turns the circle warm', p.evaluate("() => document.body.classList.contains('warm')"), '')
        p.fill('#words', 'I always mess everything up'); click_door(p, 'It’s written'); settle(p, 1400)
        a = ink(p)
        check(T + 'the thought appears on paper, with a moment to be with it', a['n'] > 500 and 'Here it is. Take a moment with it.' in guide(p) and p.is_visible('#crumple'), [a, guide(p)])
        check(T + 'the words are not in the page as text (only drawn)', 'mess everything up' not in p.content(), '')
        p.screenshot(path=os.path.join(OUT, tag + '-02-paper.png'))
        c = circle(p); p.mouse.click(c['x'], c['y'] - c['R'] * 0.06)
        p.wait_for_timeout(700); p.screenshot(path=os.path.join(OUT, tag + '-03-crumpling.png'))
        settle(p, 1100)
        b = ink(p)
        check(T + 'a tap on the paper crumples it into a small ball', b['w'] < a['w'] * 0.62, [a['w'], b['w']])
        check(T + 'then a deep breath in', 'Take a deep breath in' in guide(p) and p.is_visible('#throw'), guide(p))
        p.screenshot(path=os.path.join(OUT, tag + '-04-breathe.png'))
        try: p.wait_for_function("() => document.getElementById('guide').innerText.includes('a little more')", timeout=6000); more = True
        except Exception: more = False
        check(T + '... a little more ...', more, guide(p))
        p.wait_for_function("() => document.getElementById('guide').innerText.includes('breathe out')", timeout=4000)
        check(T + '... and as you breathe out, throw it into the fire', 'breathe out, throw it into the fire' in guide(p) and 'Feel it leave your hand' in guide(p), guide(p))
        p.screenshot(path=os.path.join(OUT, tag + '-05-breathe-out.png'))
        c = circle(p); bx, by = c['x'], c['y'] - c['R'] * 0.06
        p.mouse.move(bx, by); p.mouse.down(); p.mouse.move(bx, by + 30, steps=4); p.mouse.move(bx + 5, by + 70, steps=4); p.mouse.up()
        p.wait_for_timeout(1000); p.screenshot(path=os.path.join(OUT, tag + '-06-fire.png'))
        p.wait_for_timeout(500); p.screenshot(path=os.path.join(OUT, tag + '-07-sparks.png'))
        p.wait_for_function("() => document.getElementById('speak').innerText.includes('Gone.')", timeout=7000)
        check(T + 'flicked into the fire: gone, never read back', 'Gone.' in speak(p) and 'It has left your hand. Let it leave your mind too.' in speak(p), speak(p))
        check(T + 'nothing let go is kept anywhere', kept(p) == [] and 'mess' not in json.dumps(p.evaluate('() => Object.assign({}, localStorage)')), '')
        check(T + 'the breath has ended', 'guided' not in p.get_attribute('#mirror', 'class'), p.get_attribute('#mirror', 'class'))
        settle(p, 1600); p.screenshot(path=os.path.join(OUT, tag + '-08-gone.png'))

        # LET IT GO by the buttons alone
        click_door(p, 'Let another go'); settle(p); p.fill('#words', 'They all think I am boring'); p.keyboard.press('Enter'); settle(p, 1300)
        p.click('#crumple'); settle(p, 1700)
        check(T + 'the Crumple it button works too', p.is_visible('#throw'), doors(p))
        p.click('#throw'); p.wait_for_function("() => document.getElementById('speak').innerText.includes('Gone.')", timeout=7000)
        check(T + 'and Throw it in, without waiting for the breath', 'Gone.' in speak(p), speak(p))

        # heavy words are never thrown away
        click_door(p, 'Let another go'); settle(p); p.fill('#words', 'some days I want to die'); click_door(p, 'It’s written'); settle(p)
        check(T + 'heavy words: real help first, never the fire', '988' in speak(p) and not p.is_visible('#crumple') and ink(p)['n'] < 50, speak(p))
        click_door(p, 'Back'); settle(p)

        # THE RE-MINDING: choose the moment, watch it fold, seal it
        p.click('#goKeep'); settle(p)
        check(T + 'keeping turns the circle cool', p.evaluate("() => document.body.classList.contains('cool')"), '')
        p.fill('#words', 'Don’t decide anything big when you’re exhausted. Sleep on it first.'); click_door(p, 'It’s written'); settle(p)
        check(T + 'it asks when it should come back', 'When should it come back to you?' in speak(p) and 'A big choice' in doors(p), doors(p))
        click_door(p, 'A big choice'); p.wait_for_timeout(1500); p.screenshot(path=os.path.join(OUT, tag + '-09-folding.png'))
        settle(p, 2300)
        check(T + 'it folds into an envelope, and waits to be sealed', p.is_visible('#seal') and 'Seal it.' in guide(p) and ink(p)['n'] > 300, guide(p))
        p.screenshot(path=os.path.join(OUT, tag + '-10-envelope.png'))
        check(T + 'it is kept already, on this device only', len(kept(p)) == 1 and kept(p)[0]['moment'] == 'choice', kept(p))
        p.click('#seal'); p.wait_for_timeout(1100); p.screenshot(path=os.path.join(OUT, tag + '-11-sealed.png'))
        settle(p, 2600)
        check(T + 'sealed, for a big choice; the mind can put it down', 'Sealed, for a big choice.' in speak(p) and 'Your mind can put it down now.' in speak(p), speak(p))
        click_door(p, 'Keep another'); settle(p); p.fill('#words', 'Breathe before you answer.'); click_door(p, 'It’s written'); settle(p)
        click_door(p, 'Something else…'); settle(p)
        check(T + 'something else: a short box', p.eval_on_selector('#words', 'e => e.maxLength') == 60, '')
        p.fill('#words', 'before a job interview'); click_door(p, 'Keep it for then'); settle(p, 3800)
        p.click('#seal'); settle(p, 3500)
        check(T + 'sealed for a moment in their own words', 'Sealed, for before a job interview.' in speak(p) and len(kept(p)) == 2, speak(p))
        click_door(p, 'Done'); settle(p)
        check(T + 'home offers what was kept, and boxes are back to full length', 'What I’ve kept (2)' in doors(p) and p.eval_on_selector('#words', 'e => e.maxLength') == 280, doors(p))

        # WHEN A MOMENT COMES
        click_door(p, 'Something is happening now'); settle(p); p.fill('#words', 'I have to decide whether to take the offer'); click_door(p, 'That’s it'); settle(p)
        check(T + 'a matching moment: offered, never pushed', 'You kept something for moments like this.' in speak(p) and 'Sleep on it' not in p.content(), speak(p))
        click_door(p, 'Show me'); settle(p, 1300)
        check(T + 'its envelope comes back, still sealed, to open if wanted', p.is_visible('#open') and 'for a big choice' in guide(p) and 'Sleep on it' not in p.content(), guide(p))
        p.screenshot(path=os.path.join(OUT, tag + '-12-returned.png'))
        p.click('#open'); settle(p, 2400)
        check(T + 'opened: the words, as they were kept', 'Sleep on it first.' in speak(p) and 'You kept this for a big choice.' in speak(p), speak(p))
        p.screenshot(path=os.path.join(OUT, tag + '-13-opened.png'))
        click_door(p, 'Keep it'); settle(p)
        check(T + 'keep it: still kept', len(kept(p)) == 2 and p.is_visible('#list') and 'Still kept.' in who(p), who(p))
        click_door(p, 'Back'); settle(p)
        click_door(p, 'Something is happening now'); settle(p); p.fill('#words', 'I felt this way before about the weather'); click_door(p, 'That’s it'); settle(p)
        check(T + 'no match: says so plainly', 'Nothing you’ve kept is for a moment like this.' in speak(p), speak(p))

        # THE LIST, and letting a kept thought go
        click_door(p, 'Open what I’ve kept'); settle(p)
        items = p.eval_on_selector_all('#list .moment', 'es => es.map(e => e.innerText.replace(/\\s+/g, " "))')
        check(T + 'the list shows only the moments, never the words', items == ['For a big choice 1', 'For before a job interview 1'] and 'Breathe before' not in p.content(), items)
        p.screenshot(path=os.path.join(OUT, tag + '-14-list.png'), full_page=True)
        p.locator('#list .moment').nth(1).click(); settle(p, 1100); p.click('#open'); settle(p, 2300)
        click_door(p, 'Let it go now'); settle(p, 1400)
        check(T + 'a kept thought whose moment has passed can go into the fire', 'Its moment has passed' in guide(p) and p.is_visible('#crumple') and len(kept(p)) == 1, guide(p))
        p.click('#crumple'); settle(p, 1700); p.click('#throw'); p.wait_for_function("() => document.getElementById('speak').innerText.includes('Gone.')", timeout=7000)
        check(T + '... and it is gone from the device', 'Gone.' in speak(p) and 'Breathe' not in json.dumps(kept(p)), kept(p))
        click_door(p, 'Done'); settle(p); click_door(p, 'What I’ve kept (1)'); settle(p)
        p.locator('#list .door', has_text='Forget all of it').click(); settle(p, 200)
        p.locator('#list .door', has_text='Tap again').click(); settle(p)
        check(T + 'forget all: nothing kept, back home', kept(p) == [] and p.is_visible('#goLet') and 'Forgotten' in who(p), who(p))

        # the longest thought stays inside the circle; nothing scrolls sideways
        p.click('#goLet'); settle(p); p.fill('#words', ('I keep thinking that if I had only said something different that day then none of this would have happened and everyone would still be talking to me and ' * 3)[:280]); click_door(p, 'It’s written'); settle(p, 1400)
        a = ink(p); c = circle(p); cv = p.eval_on_selector('#fx', 'e => { const r=e.getBoundingClientRect(); return {x:r.left, y:r.top}; }')
        top = cv['y'] + a['cy'] - a['h'] / 2; bottom = cv['y'] + a['cy'] + a['h'] / 2
        check(T + 'the longest thought fits on paper inside the circle', top > c['y'] - c['R'] and bottom < c['y'] + c['R'], [top, bottom, c])
        p.screenshot(path=os.path.join(OUT, tag + '-15-long.png'))
        sw = p.evaluate('() => [document.documentElement.scrollWidth, innerWidth]')
        check(T + 'nothing scrolls sideways', sw[0] <= sw[1], sw)
        check(T + 'no errors', not errs, errs)
        ctx.close()

    # stillness: with motion reduced, every step is quick and calm
    ctx = br.new_context(viewport={'width': 390, 'height': 844}, reduced_motion='reduce'); p = ctx.new_page(); errs = []
    p.on('pageerror', lambda e: errs.append(str(e)))
    p.goto('file://' + H); settle(p, 300)
    p.click('#goLet'); settle(p, 200); p.fill('#words', 'not good enough'); click_door(p, 'It’s written'); settle(p, 500)
    p.click('#crumple'); settle(p, 500)
    check('still: no guided breathing, the words say it instead', 'Take a deep breath.' in guide(p) and 'guided' not in p.get_attribute('#mirror', 'class'), guide(p))
    p.click('#throw'); p.wait_for_function("() => document.getElementById('speak').innerText.includes('Gone.')", timeout=7000)
    check('still: let go quickly and quietly', 'Gone.' in speak(p), speak(p))
    p.click('#doors .door >> text=Done'); settle(p, 300); p.click('#goKeep'); settle(p, 200); p.fill('#words', 'Ask for help sooner.'); click_door(p, 'It’s written'); settle(p, 300)
    click_door(p, 'When I’m worn out'); settle(p, 1500); p.click('#seal'); settle(p, 1500)
    check('still: sealed quickly too', 'Sealed, for when you’re worn out.' in speak(p), speak(p))
    check('still: no errors', not errs, errs)
    ctx.close(); br.close()
print('\n%d failed' % len(fails), fails)
sys.exit(1 if fails else 0)
