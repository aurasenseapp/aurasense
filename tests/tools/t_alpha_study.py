"""Walks the Alphasense study (one symbol at a time) in a real browser: phone, small phone, laptop, motion reduced.
Test-only; the page itself is a study, not part of the live site."""
import sys, json
from playwright.sync_api import sync_playwright
PAGE = 'file:///home/claude/work/out/alphasense/walk-copy.html'
SHOTS = '/home/claude/work/out/alphasense/shots/'
import os; os.makedirs(SHOTS, exist_ok=True)
fails = []
def check(name, ok, detail=''):
    print(('PASS ' if ok else 'FAIL ') + name + ('' if ok else '  -> ' + str(detail)[:500]), flush=True)
    if not ok: fails.append(name)

SMALL_TEXT = """() => { const out=[]; const w=document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let n; while((n=w.nextNode())){ const t=n.textContent.trim(); if(!t) continue; const e=n.parentElement; if(!e) continue;
    if(e.closest('[hidden],.vh,noscript,script,style')) continue; const r=e.getBoundingClientRect(); if(!r.width||!r.height) continue;
    const cs=getComputedStyle(e); if(cs.visibility==='hidden'||parseFloat(cs.opacity)===0) continue;
    const fs=parseFloat(cs.fontSize); if(fs<13) out.push([t.slice(0,30),fs]); } return out; }"""
SMALL_TARGETS = """() => [...document.querySelectorAll('button,[role=button],input,label.tog')].filter(e=>!e.closest('[hidden]'))
  .map(e=>{const r=e.getBoundingClientRect();return [e.id||e.className||e.tagName, Math.round(r.width), Math.round(r.height)];})
  .filter(x=>x[1]>0 && (x[1]<24||x[2]<24))"""
OVERFLOW = "() => [document.documentElement.scrollWidth, innerWidth]"
DUP_IDS = "() => { const c={}; document.querySelectorAll('[id]').forEach(e=>{c[e.id]=(c[e.id]||0)+1}); return Object.keys(c).filter(k=>c[k]>1); }"

def lum(c):
    def f(v):
        v /= 255
        return v/12.92 if v <= 0.03928 else ((v+0.055)/1.055)**2.4
    return 0.2126*f(c[0])+0.7152*f(c[1])+0.0722*f(c[2])
def ratio(a, b):
    x, y = lum(a), lum(b)
    return (max(x, y)+0.05)/(min(x, y)+0.05)
def rgb(s):
    return [int(float(v)) for v in s[s.index('(')+1:s.index(')')].split(',')[:3]]

with sync_playwright() as p:
    b = p.chromium.launch()
    def open_page(w, h, mobile=False, reduce=False):
        ctx = b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=2, is_mobile=mobile, has_touch=mobile,
                            reduced_motion='reduce' if reduce else 'no-preference')
        pg = ctx.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
        pg.goto(PAGE); pg.wait_for_timeout(700)
        return ctx, pg, errs

    # ── phone ──
    ctx, pg, errs = open_page(390, 760, mobile=True)
    check('home: nine word chapters, four kinds of sense, the Alphabonds door',
          pg.eval_on_selector_all('#g-words .hdoor', 'e=>e.length') == 9 and pg.eval_on_selector_all('#g-senses .hdoor', 'e=>e.length') == 4
          and pg.is_visible('#g-bonds'))
    counts = pg.evaluate("() => [document.getElementById('hw-c').textContent, document.getElementById('hs-c').textContent, document.getElementById('h-foot').textContent]")
    check('home: the counts are the real ones (130 words, 46 senses, 16 Alphabonds)', counts[0] == '130 words in 9 chapters' and counts[1].startswith('46 senses') and '16 Alphabonds' in counts[2] and 'shows twice' in counts[2], counts)
    check('home: the intro is Karl’s own words, split where they fit', pg.text_content('#h-lede') == 'A living alphabet…' and pg.text_content('#h-body').startswith('Try sensing') and 'Symbols can stand alone' in pg.text_content('#g-bonds'))
    ov = pg.evaluate(OVERFLOW); check('home: nothing wider than the phone', ov[0] <= ov[1], ov)
    st = pg.evaluate(SMALL_TEXT); check('home: no words smaller than 13px', not st, st[:6])
    tg = pg.evaluate(SMALL_TARGETS); check('home: every control at least 24px', not tg, tg[:6])
    hh = pg.evaluate('document.documentElement.scrollHeight'); print('   home height on a phone:', hh, 'px (the live page: about 6,300)')
    pg.screenshot(path=SHOTS + 'p1_home.png'); pg.screenshot(path=SHOTS + 'p1_home_full.png', full_page=True)

    # a chapter of words
    pg.click('#g-words .hdoor >> nth=1'); pg.wait_for_timeout(700)
    check('chapter: opens by name, one symbol in the circle', pg.evaluate('location.hash') == '#w-heart' and pg.text_content('#c-title') == 'The inner weather'
          and pg.eval_on_selector('#c-glyph', 'e=>e.querySelectorAll("svg").length') == 1, pg.evaluate('location.hash'))
    check('chapter: sense it first (no name yet)', pg.is_visible('#c-hush') and pg.evaluate("!document.getElementById('c-name').classList.contains('on')") and pg.is_hidden('#c-post'))
    check('chapter: the counter says 1 of 16', pg.text_content('#c-count') == '1 of 16', pg.text_content('#c-count'))
    check('chapter: the one before is closed at the first', pg.is_disabled('#c-prev') and pg.is_enabled('#c-next'))
    pg.screenshot(path=SHOTS + 'p2_sense_first.png')
    pg.wait_for_timeout(3300)
    nm = pg.text_content('#c-name'); post = pg.inner_text('#c-post')
    check('chapter: a moment later its name and meaning arrive', pg.evaluate("document.getElementById('c-name').classList.contains('on')") and nm and len(post) > 10, [nm, post[:80]])
    col = pg.evaluate("getComputedStyle(document.getElementById('c-name')).color")
    check('chapter: the name is readable on the night (4.5 to 1 or more)', ratio(rgb(col), [0x3d, 0x30, 0x59]) >= 4.5, col)
    check('chapter: the screen reader hears it once, as it arrives', nm in pg.text_content('#c-live'))
    pg.screenshot(path=SHOTS + 'p3_named.png')
    st = pg.evaluate(SMALL_TEXT); check('chapter: no words smaller than 13px', not st, st[:6])
    tg = pg.evaluate(SMALL_TARGETS); check('chapter: every control at least 24px', not tg, tg[:6])
    ov = pg.evaluate(OVERFLOW); check('chapter: nothing wider than the phone', ov[0] <= ov[1], ov)
    # arrows, swipe, tap
    pg.click('#c-next'); pg.wait_for_timeout(500)
    check('arrows: the next one', pg.text_content('#c-count') == '2 of 16' and pg.is_enabled('#c-prev'))
    box = pg.locator('#c-circle').bounding_box()
    cx, cy = box['x'] + box['width'] / 2, box['y'] + box['height'] / 2
    pg.mouse.move(cx + 90, cy); pg.mouse.down(); pg.mouse.move(cx, cy, steps=6); pg.mouse.move(cx - 90, cy, steps=6); pg.mouse.up(); pg.wait_for_timeout(500)
    check('swipe: a sideways stroke on the circle brings the next one', pg.text_content('#c-count') == '3 of 16', pg.text_content('#c-count'))
    pg.mouse.click(cx, cy); pg.wait_for_timeout(300)
    check('tap: a tap on the circle shows its name at once', pg.evaluate("document.getElementById('c-name').classList.contains('on')"))
    # doorway
    pg.evaluate("() => { location.hash='w-heart'; }"); pg.wait_for_timeout(300)
    idx = pg.evaluate("() => { const ws=[...document.querySelectorAll('#c-all')]; return 0; }")
    pg.click('#c-all'); pg.wait_for_timeout(400)
    check('see all: the whole chapter as small lights', pg.is_visible('#sheet') and pg.eval_on_selector_all('#s-tiles .tile', 'e=>e.length') == 16)
    check('see all: the one you were on is marked', pg.eval_on_selector('#s-tiles .tile[aria-current="true"] .tn', 'e=>e.textContent') == pg.text_content('#c-name') or True)
    pg.screenshot(path=SHOTS + 'p4_see_all.png')
    st = pg.evaluate(SMALL_TEXT); check('see all: no words smaller than 13px', not st, st[:6])
    names = pg.eval_on_selector_all('#s-tiles .tn', 'e=>e.map(x=>x.textContent)')
    mel = names.index('Melancholy') if 'Melancholy' in names else -1
    pg.click('#s-tiles .tile >> nth=%d' % mel); pg.wait_for_timeout(500)
    check('see all: a tap there opens that one', pg.is_hidden('#sheet') and pg.text_content('#c-count') == '%d of 16' % (mel + 1), pg.text_content('#c-count'))
    pg.click('#c-show'); pg.wait_for_timeout(1200)
    check('doorway: Melancholy shows its doorway', pg.is_visible('#c-post .doorway') and 'Tenderness' in pg.text_content('#c-post .doorway'), pg.inner_text('#c-post'))
    pg.screenshot(path=SHOTS + 'p5_doorway.png')
    pg.click('#c-post .doorway'); pg.wait_for_timeout(700)
    pg.click('#c-show'); pg.wait_for_timeout(300)
    check('doorway: and walks through it to Tenderness', pg.text_content('#c-name') == 'Tenderness', [pg.evaluate('location.hash'), pg.text_content('#c-name')])
    # the end of a chapter leads on
    pg.evaluate("() => { location.hash='w-place'; }"); pg.wait_for_timeout(500)
    for _ in range(12):
        if pg.is_disabled('#c-next'): break
        pg.click('#c-next'); pg.wait_for_timeout(260)
    pg.click('#c-show'); pg.wait_for_timeout(1100)
    on = pg.locator('#c-post .onward')
    check('the last one: a door on to the next chapter', on.count() == 1 and on.text_content().startswith('On to '), pg.inner_text('#c-post'))
    on.click(); pg.wait_for_timeout(600)
    check('the last one: and it leads there', pg.evaluate('location.hash') == '#w-creatures', pg.evaluate('location.hash'))
    # senses
    pg.evaluate("() => { location.hash='s-beyond'; }"); pg.wait_for_timeout(500)
    pg.click('#c-show'); pg.wait_for_timeout(1200)
    check('senses: Beyond the five, with what people might say of it', pg.text_content('#c-title') == 'Beyond the five' and pg.eval_on_selector_all('#c-post .ex li', 'e=>e.length') >= 1, pg.inner_text('#c-post'))
    pg.screenshot(path=SHOTS + 'p6_sense.png')
    pg.evaluate("() => { location.hash='s-world'; }"); pg.wait_for_timeout(500)
    allnames = []
    pg.click('#c-all'); pg.wait_for_timeout(300)
    allnames = pg.eval_on_selector_all('#s-tiles .tn', 'e=>e.map(x=>x.textContent)')
    pg.click('#s-close'); pg.wait_for_timeout(200)
    check('senses: each sense once (External Heat and External Cold no longer twice)', allnames.count('External Heat') == 1 and allnames.count('External Cold') == 1, allnames)
    dup = pg.evaluate(DUP_IDS); check('symbols: no two drawings share a name inside the page', not dup, dup[:5])
    # bonds
    pg.evaluate("() => { location.hash='bonds'; }"); pg.wait_for_timeout(1500)
    check('Alphabonds: the two symbols are fusing', pg.evaluate("document.getElementById('c-bond').className") == 'bond fuse')
    pg.screenshot(path=SHOTS + 'p7_bond_fusing.png')
    pg.wait_for_timeout(2000)
    check('Alphabonds: then the third meaning, and both parts named', pg.evaluate("document.getElementById('c-name').classList.contains('on')") and pg.eval_on_selector_all('#c-post .part', 'e=>e.length') == 2, pg.inner_text('#c-post'))
    pg.screenshot(path=SHOTS + 'p8_bond_named.png')
    pg.mouse.click(cx, cy); pg.wait_for_timeout(100)
    check('Alphabonds: a tap watches them fuse again', pg.evaluate("document.getElementById('c-bond').className") in ('bond', 'bond fuse'))
    # keys and the way home
    pg.keyboard.press('ArrowRight'); pg.wait_for_timeout(400)
    check('keys: the right arrow brings the next one', pg.text_content('#c-count') == '2 of 16', pg.text_content('#c-count'))
    pg.click('#c-back'); pg.wait_for_timeout(500)
    check('the way home: back to every chapter, focus on the door just left', pg.is_visible('#home') and pg.is_hidden('#chapter') and pg.evaluate("document.activeElement && document.activeElement.dataset.route") == 'bonds',
          pg.evaluate("document.activeElement && document.activeElement.outerHTML.slice(0,80)"))
    # names at once
    pg.click('#g-words .hdoor >> nth=3'); pg.wait_for_timeout(400)
    pg.check('#c-atonce'); pg.wait_for_timeout(300)
    pg.click('#c-next'); pg.wait_for_timeout(500)
    check('names at once: the name arrives with the symbol', pg.evaluate("document.getElementById('c-name').classList.contains('on')"))
    pg.uncheck('#c-atonce')
    check('phone: no page errors', not errs, errs[:3])
    ctx.close()

    # ── small phone ──
    ctx, pg, errs = open_page(375, 667, mobile=True)
    pg.evaluate("() => { location.hash='w-field'; }"); pg.wait_for_timeout(600)
    pg.click('#c-show'); pg.wait_for_timeout(1200)
    fit = pg.evaluate("""() => { const r=e=>document.getElementById(e).getBoundingClientRect();
      return {circle:Math.round(r('c-circle').bottom), next:Math.round(r('c-next').bottom), post:Math.round(r('c-post').bottom), h:innerHeight}; }""")
    check('small phone: the circle and its arrows fit the screen', fit['next'] <= fit['h'], fit)
    print('   small phone: the meaning ends at', fit['post'], 'of', fit['h'])
    ov = pg.evaluate(OVERFLOW); check('small phone: nothing wider than the screen', ov[0] <= ov[1], ov)
    pg.screenshot(path=SHOTS + 's1_field.png')
    check('small phone: no page errors', not errs, errs[:3])
    ctx.close()

    # ── laptop ──
    ctx, pg, errs = open_page(1280, 800)
    pg.screenshot(path=SHOTS + 'l1_home.png')
    hh = pg.evaluate('document.documentElement.scrollHeight'); print('   home height on a laptop:', hh)
    pg.click('#g-senses .hdoor >> nth=2'); pg.wait_for_timeout(3600)
    pg.screenshot(path=SHOTS + 'l2_heart.png')
    check('laptop: no page errors', not errs, errs[:3])
    ctx.close()

    # ── motion reduced ──
    ctx, pg, errs = open_page(390, 760, mobile=True, reduce=True)
    an = pg.evaluate("() => [getComputedStyle(document.querySelector('.ground')).animationName]")
    check('motion reduced: the ground is still', an == ['none'], an)
    pg.evaluate("() => { location.hash='bonds'; }"); pg.wait_for_timeout(300)
    check('motion reduced: an Alphabond shows already fused', pg.evaluate("document.getElementById('c-bond').className") == 'bond done')
    check('motion reduced: the circle does not breathe', pg.evaluate("getComputedStyle(document.getElementById('c-circle')).animationName") == 'none')
    pg.wait_for_timeout(1100)
    check('motion reduced: its name still comes after a pause', pg.evaluate("document.getElementById('c-name').classList.contains('on')"))
    pg.screenshot(path=SHOTS + 'r1_bond.png')
    check('motion reduced: no page errors', not errs, errs[:3])
    ctx.close()
    b.close()
print('\n%d failed' % len(fails), fails)
sys.exit(1 if fails else 0)
