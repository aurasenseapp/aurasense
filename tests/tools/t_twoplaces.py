"""Tests the draft of the Mirror's two places (Let it go, The Re-minding) in a real browser. Test-only."""
import os, sys, json
from playwright.sync_api import sync_playwright

SRC = '/home/claude/work/out/two-places/the-two-places.html'
OUT = '/tmp/claude-0/-home-claude/89e7564b-fd6e-5cd5-8cd5-5383c8af45f8/scratchpad/twoplaces'
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
def who(p): return p.eval_on_selector('#who', 'e => e.textContent')
def doors(p): return p.eval_on_selector_all('#doors .door', 'es => es.map(e => e.textContent)')
def kept(p): return p.evaluate("() => JSON.parse(localStorage.getItem('as_reminding') || '[]')")
def click_door(p, label): p.locator('#doors .door', has_text=label).first.click()
def settle(p, ms=700): p.wait_for_timeout(ms)
def hold(p, ms):
    b = p.locator('#hold'); box = b.bounding_box()
    p.mouse.move(box['x'] + box['width'] / 2, box['y'] + box['height'] / 2); p.mouse.down(); p.wait_for_timeout(ms); p.mouse.up()

with sync_playwright() as pw:
    br = pw.chromium.launch()
    for (w, h, tag) in [(390, 844, 'phone'), (1280, 800, 'laptop')]:
        ctx = br.new_context(viewport={'width': w, 'height': h}, device_scale_factor=2 if tag == 'phone' else 1, has_touch=(tag == 'phone'))
        p = ctx.new_page(); errs = []
        p.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
        p.on('pageerror', lambda e: errs.append(str(e)))
        p.goto('file://' + H); settle(p, 900)
        T = tag + ': '
        check(T + 'opens with the question and two doors', 'A thought that keeps coming back?' in speak(p) and doors(p) == ['Let it go', 'Keep it for when it’s needed'], [speak(p), doors(p)])
        p.screenshot(path=os.path.join(OUT, tag + '-1-home.png'))

        # LET IT GO, by holding
        click_door(p, 'Let it go'); settle(p)
        check(T + 'let it go asks for the thought', 'What’s the thought?' in speak(p) and p.is_visible('#words'), speak(p))
        click_door(p, 'It’s written'); settle(p, 200)
        check(T + 'nothing written: a gentle word, no step forward', who(p) == 'Write the thought first, in any words.' and p.is_visible('#words'), who(p))
        p.fill('#words', 'I always mess everything up'); click_door(p, 'It’s written'); settle(p)
        check(T + 'the thought is shown in the circle, ready to hold', '“I always mess everything up”' in speak(p) and p.is_visible('#hold') and not p.is_visible('#words'), speak(p))
        p.screenshot(path=os.path.join(OUT, tag + '-2-hold.png'))
        hold(p, 400); settle(p, 300)
        check(T + 'let go too soon: asked to hold a little longer, the thought still there', who(p) == 'Hold a little longer, then let go.' and 'mess everything up' in speak(p), [who(p), speak(p)])
        b = p.locator('#hold'); box = b.bounding_box()
        p.mouse.move(box['x'] + box['width'] / 2, box['y'] + box['height'] / 2); p.mouse.down(); p.wait_for_timeout(1300)
        check(T + 'held long enough: "Now let go", the ring full', p.eval_on_selector('#hold', 'e => e.textContent') == 'Now let go' and 'full' in p.eval_on_selector('#mirror', 'e => e.className'), p.eval_on_selector('#hold', 'e => e.textContent'))
        p.screenshot(path=os.path.join(OUT, tag + '-3-held.png'))
        p.mouse.up(); p.wait_for_timeout(500)
        p.screenshot(path=os.path.join(OUT, tag + '-4-falling.png'))
        settle(p, 2600)
        check(T + 'released: "Let go", gone from the page, never read back', 'Let go.' in speak(p) and 'mess everything up' not in p.content(), speak(p))
        check(T + 'nothing let go is kept on the device', kept(p) == [] and 'mess' not in json.dumps(p.evaluate('() => Object.assign({}, localStorage)')), kept(p))
        p.screenshot(path=os.path.join(OUT, tag + '-5-letgo.png'))

        # LET IT GO, by keyboard
        click_door(p, 'Let another go'); settle(p); p.fill('#words', 'They all think I am boring'); p.keyboard.press('Enter'); settle(p)
        check(T + 'Enter in the box moves on', p.is_visible('#hold'), doors(p))
        p.focus('#hold'); p.keyboard.down(' '); p.wait_for_timeout(1300); p.keyboard.up(' '); settle(p, 2600)
        check(T + 'keyboard: hold Space, then let go', 'Let go.' in speak(p) and 'boring' not in p.content(), speak(p))

        # LET IT GO, without holding
        click_door(p, 'Let another go'); settle(p); p.fill('#words', 'Why did I say that'); click_door(p, 'It’s written'); settle(p)
        click_door(p, 'Let it go without holding'); settle(p, 2600)
        check(T + 'there is a way that needs no holding', 'Let go.' in speak(p) and 'Why did I say that' not in p.content(), speak(p))

        # HEAVY words are never binned
        click_door(p, 'Let another go'); settle(p); p.fill('#words', 'some days I want to die'); click_door(p, 'It’s written'); settle(p)
        check(T + 'heavy words: real help first, never the bin', '988' in speak(p) and not p.is_visible('#hold') and 'want to die' not in p.content(), speak(p))
        click_door(p, 'Back'); settle(p)

        # THE RE-MINDING
        click_door(p, 'Keep it for when it’s needed'); settle(p)
        p.fill('#words', 'Don’t decide anything big when you’re exhausted. Sleep on it first.'); click_door(p, 'It’s written'); settle(p)
        check(T + 'keep: it asks when it should come back', 'When should it come back to you?' in speak(p) and 'A big choice' in doors(p) and 'Something else…' in doors(p), doors(p))
        p.screenshot(path=os.path.join(OUT, tag + '-6-moments.png'))
        click_door(p, 'A big choice'); settle(p)
        k = kept(p)
        check(T + 'kept, for a big choice, on this device only', 'Kept, for a big choice.' in speak(p) and len(k) == 1 and k[0]['moment'] == 'choice' and 'Sleep on it' in k[0]['text'], [speak(p), k])
        click_door(p, 'Keep another'); settle(p); p.fill('#words', 'Breathe before you answer.'); click_door(p, 'It’s written'); settle(p)
        click_door(p, 'Something else…'); settle(p)
        check(T + 'something else: a short box for the moment', p.eval_on_selector('#words', 'e => e.maxLength') == 60, '')
        click_door(p, 'Back'); settle(p)
        check(T + 'back returns to the moments, the thought still held', 'Breathe before you answer.' in speak(p) and 'A big choice' in doors(p), speak(p))
        click_door(p, 'Something else…'); settle(p); p.fill('#words', 'before a job interview'); click_door(p, 'Keep it for then'); settle(p)
        check(T + 'kept for a moment in their own words', 'Kept, for before a job interview.' in speak(p) and len(kept(p)) == 2, speak(p))
        click_door(p, 'Done'); settle(p)
        check(T + 'home now offers what was kept', 'What I’ve kept (2)' in doors(p) and 'Something is happening now' in doors(p), doors(p))
        check(T + 'every box is back to its usual length', p.eval_on_selector('#words', 'e => e.maxLength') == 280, '')

        # WHEN A MOMENT COMES
        click_door(p, 'Something is happening now'); settle(p); p.fill('#words', 'I have to decide whether to take the offer'); click_door(p, 'That’s it'); settle(p)
        check(T + 'a matching moment: offered, never pushed', 'You kept something for moments like this.' in speak(p) and 'Would you like to see it?' in speak(p) and 'Sleep on it' not in speak(p), speak(p))
        click_door(p, 'Show me'); settle(p)
        check(T + 'shown only when asked', 'Sleep on it first.' in speak(p) and 'You kept this for a big choice.' in speak(p), speak(p))
        p.screenshot(path=os.path.join(OUT, tag + '-7-returned.png'))
        click_door(p, 'Keep it'); settle(p)
        check(T + 'keep it: back to the list, still kept', len(kept(p)) == 2 and p.is_visible('#list'), '')
        click_door(p, 'Back'); settle(p)
        click_door(p, 'Something is happening now'); settle(p); p.fill('#words', 'my job interview is tomorrow'); click_door(p, 'That’s it'); settle(p)
        check(T + 'their own moment matches by its words', 'You kept something for moments like this.' in speak(p), speak(p))
        click_door(p, 'Not now'); settle(p)
        click_door(p, 'Something is happening now'); settle(p); p.fill('#words', 'I felt this way before about the weather'); click_door(p, 'That’s it'); settle(p)
        check(T + 'no match: says so, and common words like "before" don\'t match', 'Nothing you’ve kept is for a moment like this.' in speak(p), speak(p))

        # THE LIST
        click_door(p, 'Open what I’ve kept'); settle(p)
        items = p.eval_on_selector_all('#list .moment', 'es => es.map(e => e.innerText.replace(/\\s+/g, " "))')
        check(T + 'the list shows only the moments, not the thoughts', items == ['For a big choice 1', 'For before a job interview 1'] and 'Sleep on it' not in p.eval_on_selector('#list', 'e => e.innerText'), items)
        p.screenshot(path=os.path.join(OUT, tag + '-8-list.png'), full_page=True)
        p.locator('#list .moment').nth(1).click(); settle(p)
        click_door(p, 'Let it go now'); settle(p)
        check(T + 'a kept thought can be let go', 'You can let this one go.' in speak(p) and p.is_visible('#hold'), speak(p))
        hold(p, 1300); settle(p, 2600)
        check(T + '... and then it is gone from the device', 'Let go.' in speak(p) and len(kept(p)) == 1 and 'Breathe' not in json.dumps(kept(p)), kept(p))
        click_door(p, 'Done'); settle(p); click_door(p, 'What I’ve kept (1)'); settle(p)
        f = p.locator('#list .door', has_text='Forget all of it'); f.click(); settle(p, 200)
        check(T + 'forget all asks once more', 'Tap again to forget all 1' in p.eval_on_selector('#list', 'e => e.innerText') and len(kept(p)) == 1, '')
        p.locator('#list .door', has_text='Tap again').click(); settle(p)
        check(T + 'forgotten: nothing kept, back home', kept(p) == [] and doors(p) == ['Let it go', 'Keep it for when it’s needed'] and 'Forgotten' in who(p), [doors(p), who(p)])

        # a long thought fits; nothing scrolls sideways
        click_door(p, 'Let it go'); settle(p); p.fill('#words', ('I keep thinking that if I had only said something different that day then none of this would have happened and everyone would still be talking to me and ' * 3)[:280]); click_door(p, 'It’s written'); settle(p)
        fit = p.eval_on_selector('#speak', 'e => [e.scrollHeight, e.clientHeight]')
        check(T + 'the longest thought fits inside the circle', fit[0] <= fit[1] + 1, fit)
        p.screenshot(path=os.path.join(OUT, tag + '-9-long.png'))
        sw = p.evaluate('() => [document.documentElement.scrollWidth, innerWidth]')
        check(T + 'nothing scrolls sideways', sw[0] <= sw[1], sw)
        check(T + 'no errors', not errs, errs)
        ctx.close()

    # stillness: reduced motion lets go at once, with no movement
    ctx = br.new_context(viewport={'width': 390, 'height': 844}, reduced_motion='reduce'); p = ctx.new_page()
    p.goto('file://' + H); settle(p, 300)
    click_door(p, 'Let it go'); settle(p, 100); p.fill('#words', 'not good enough'); click_door(p, 'It’s written'); settle(p, 100)
    hold(p, 1250); settle(p, 600)
    check('still: with motion reduced, it lets go quickly and quietly', 'Let go.' in speak(p), speak(p))
    ctx.close(); br.close()
print('\n%d failed' % len(fails), fails)
sys.exit(1 if fails else 0)
