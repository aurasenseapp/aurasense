# -*- coding: utf-8 -*-
"""Build 174 · the new Mirror page, walked in a real browser with a pretend helper (no real Claude is called).
The site is served the way Cloudflare Pages serves it. Usage: python3 t174.py [site folder] [shots folder]"""
import io, os, re, sys, json
from playwright.sync_api import sync_playwright

SITE = (sys.argv[1] if len(sys.argv) > 1 else '/home/claude/aurasense').rstrip('/')
SHOTS = (sys.argv[2] if len(sys.argv) > 2 else '/home/claude/work/shots/177').rstrip('/')
os.makedirs(SHOTS, exist_ok=True)
BASE = 'https://www.aurasense.app'
CT = {'.html': 'text/html; charset=utf-8', '.json': 'application/json', '.txt': 'text/plain; charset=utf-8', '.js': 'application/javascript', '.png': 'image/png'}
fails = []; passes = 0
def ok(cond, what):
    global passes
    if cond: passes += 1
    else: fails.append(what); print('FAIL ' + what)

# ── 1. the files themselves ──
src = io.open(SITE + '/mirror.html', encoding='utf-8').read()
helper = io.open(SITE + '/functions/api/mirror.js', encoding='utf-8').read()
ok("default-src 'none'" in src and "connect-src 'self'" in src and "form-action 'none'" in src, 'the strict page rule is set: the page can talk only to Aurasense itself')
ok(not re.search(r'__T=|__t\b|sk-ant|harvey', src, flags=re.I), 'no test hooks, no keys, first name only')
ok('<form' not in src.lower() and 'eval(' not in src and 'document.write' not in src, 'no forms, nothing evaluated')
ok(len(re.findall(r'innerHTML', src)) == 1, 'markup is placed in exactly one spot: the checked symbol')
h1 = re.search(r'^const HEAVY = (/.*/i);$', helper, flags=re.M).group(1)
h2 = re.search(r'^var HEAVY=(/.*/i);', src, flags=re.M).group(1)
ok(h1 == h2, 'one heavy-words list: the page carries the helper\'s, letter for letter')
A = json.load(io.open(SITE + '/alphasense.json', encoding='utf-8'))
m = io.open(SITE + '/index-mapbox.html', encoding='utf-8').read()
blk = m[m.index('const ALPHA_WORDS=['):m.index('const ALPHA_CHAPTERS=')]
mapw = [(x.group(2), x.group(4)) for x in re.finditer(r"\{w:(['\"])(.*?)\1,c:['\"]#[0-9a-fA-F]{6}['\"],d:(['\"])(.*?)\3", blk, flags=re.S)]
un = lambda t: t.replace('\\u2019', '’').replace('\\u2014', '—')
ok(len(A['words']) == 130 and [(w['w'], w['d']) for w in A['words']] == [(un(a), un(b)) for a, b in mapw], 'the alphabet file is the map\'s alphabet, word for word')
ok(all(w['g'] and w['g'] in blk for w in A['words']), 'every symbol is the map\'s own drawing')
hw = set(json.loads('"' + x + '"') for x in re.findall(r'\["((?:[^"\\]|\\.)+)", "', helper[helper.index('const ALPHA = ['):helper.index('const ALPHA_TEXT')]))
ok(hw - set(c['name'] for c in A['chapters']) == set(w['w'] for w in A['words']), 'the helper and this file hold the very same words')
for label in ['What I learned from you:', 'The you who senses most clearly might notice:', '[Written by the Mirror’s written rules, not by you:] ']:
    ok(label in src and label in helper, 'the page and the helper say it the same way: ' + label.strip())
ok('You can keep writing here while you reach someone' in src, 'Karl\'s words: the page gently stays')
low = re.sub(r'<!--.*?-->|<script>.*?</script>|<style>.*?</style>', '', src, flags=re.S).lower()
for bad in [r'\bcure', r'\bheal(s|ed|ing)?\b', r'treatment', r'guarantee', r'diagnos']:
    ok(not re.search(bad, low + src[src.index('<script>'):].lower()), 'never says "' + bad.replace('\\b', '') + '"')

# ── 2. the walk ──
def resolve(path):
    path = path.split('?')[0].split('#')[0]
    if path in ('', '/'): path = '/index.html'
    for cand in (path, path + '.html'):
        f = SITE + cand
        if os.path.isfile(f): return f
    return None

class Helper:
    def __init__(self, live=True, listen=True): self.live = live; self.listen = listen; self.posts = []; self.gets = 0; self.script = []; self.other = []
    def handle(self, route):
        req = route.request; url = req.url
        if not url.startswith(BASE): self.other.append(url); route.abort(); return
        path = url[len(BASE):]
        if path.startswith('/api/mirror'):
            if req.method == 'GET':
                self.gets += 1
                route.fulfill(status=200, content_type='application/json', body=json.dumps({'live': self.live, 'v': 2, 'listen': self.live and self.listen})); return
            body = json.loads(req.post_data or '{}'); self.posts.append(body)
            ans = self.script.pop(0) if self.script else {'ok': True, 'by': 'claude', 'v': 2, 'reflect': 'Heard.', 'learned': '', 'aspire': '', 'question': 'What else is there?', 'ready': False, 'care': False, 'ground': False}
            status = ans.pop('_status', 200)
            route.fulfill(status=status, content_type='application/json', body=json.dumps(ans)); return
        f = resolve(path)
        if not f: route.fulfill(status=404, body='not found'); return
        route.fulfill(status=200, content_type=CT.get(os.path.splitext(f)[1], 'application/octet-stream'), body=open(f, 'rb').read())

R1 = {'ok': True, 'by': 'claude', 'v': 2, 'reflect': 'The fridge hum “gets into my shoulders”: you hear it with your body too.', 'learned': 'A sound can be felt in the shoulders, not only heard.', 'aspire': '', 'question': 'What is it like in your shoulders when the hum is there?', 'ready': False, 'care': False, 'ground': False}
R2 = {'ok': True, 'by': 'claude', 'v': 2, 'reflect': 'The tightness “was there before” the hum. <img src=x onerror="window.__pwn=1">', 'learned': '', 'aspire': 'The tightness was with you before the hum.', 'question': 'What is the tightness like right now?', 'ready': True, 'care': False, 'ground': False}
CLOSE = {'ok': True, 'by': 'claude', 'v': 2, 'close': {'sensed': 'A tightness that “was there before” the hum.', 'words': ['Unease', 'Fear'], 'fits': 'together', 'name': 'Unease', 'also': 'Fear', 'working': '', 'learned': 'A body can hold a tightness for hours.', 'clear': 'The part of you that notices is still here.', 'offer': 'A hum in the flat seemed to get into my shoulders.'}}
LAY = """() => { const W = document.documentElement.clientWidth, out = {sw: document.documentElement.scrollWidth, w: W, wide: [], small: [], taps: []};
  for (const e of document.querySelectorAll('body *')) { const r = e.getBoundingClientRect(); if (!r.width || !r.height) continue; const cs = getComputedStyle(e);
    if (cs.position === 'fixed' || e.closest('svg')) continue;
    if (r.right > W + 1 || r.left < -1) out.wide.push(e.tagName + '.' + e.className);
    const own = [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
    if (own && parseFloat(cs.fontSize) < 12.5) out.small.push(e.tagName + '.' + e.className + ' ' + cs.fontSize); }
  for (const b of document.querySelectorAll('button, summary, a[href]')) { const r = b.getBoundingClientRect(); if (!r.width) continue; const cs = getComputedStyle(b);
    if (cs.display === 'inline') continue; if (r.height < 44) out.taps.push((b.textContent || '').trim().slice(0, 24) + ' ' + Math.round(r.height)); }
  return out; }"""
def layout(pg, tag):
    d = pg.evaluate(LAY)
    ok(d['sw'] <= d['w'] and not d['wide'], tag + ': nothing wider than the screen ' + '; '.join(d['wide'][:3]))
    ok(not d['small'], tag + ': no words smaller than 12.5px ' + '; '.join(d['small'][:3]))
    ok(not d['taps'], tag + ': every button is at least 44px tall ' + '; '.join(d['taps'][:4]))
def say(pg, t): pg.fill('#words', t); pg.click('#send')
def vis(pg, sel): return pg.locator(sel).first.is_visible()
def text(pg, sel='main'): return pg.inner_text(sel)

with sync_playwright() as pw:
    br = pw.chromium.launch(args=['--disable-gpu'])
    def open_page(h, w=390, hh=844, still=False, path='/mirror'):
        ctx = br.new_context(viewport={'width': w, 'height': hh}, device_scale_factor=1, is_mobile=(w < 500), has_touch=(w < 500), reduced_motion='reduce' if still else 'no-preference')
        ctx.route('**/*', h.handle)
        pg = ctx.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)[:200])); pg.on('console', lambda mm: errs.append(mm.text[:200]) if mm.type == 'error' and 'Failed to load resource: the server responded with a status of' not in mm.text else None)
        pg.goto(BASE + path, wait_until='load'); pg.wait_for_timeout(250)
        return ctx, pg, errs

    # A · in Canada: the choice, the conversation, naming, the three doors
    for vname, w, hh, still in [('phone', 390, 844, False), ('small', 360, 640, False), ('laptop', 1280, 800, False), ('still', 390, 844, True)]:
        h = Helper(); ctx, pg, errs = open_page(h, w, hh, still)
        tag = 'A ' + vname
        ok(pg.inner_text('h1') == 'What are you sensing?' and h.gets == 1, tag + ': opens on the question, and asks once whether Claude listens here')
        layout(pg, tag + ' arrival')
        if vname == 'phone': pg.screenshot(path=SHOTS + '/1-arrival.png', full_page=True)
        say(pg, 'The fridge hum gets into my shoulders.')
        ok(vis(pg, '#ask') and len(h.posts) == 0 and 'May Claude listen?' in text(pg), tag + ': first, the choice; nothing has been sent')
        layout(pg, tag + ' choice')
        h.script = [dict(R1)]
        pg.click('#ask button.btn:not(.quiet)'); pg.wait_for_selector('.reply')
        b = h.posts[0]
        ok(b.get('v') == 2 and b['words'] == 'The fridge hum gets into my shoulders.' and b['turns'][0]['content'].endswith('What are you sensing?') and b['turns'][0]['content'].startswith('[Written by the Mirror’s written rules'), tag + ': the words go the new way, after the yes')
        t = text(pg)
        ok('you hear it with your body too' in t and 'WHAT I LEARNED FROM YOU' in t.upper() and 'A sound can be felt in the shoulders' in t and 'What is it like in your shoulders' in t, tag + ': heard, what Claude learned, and one question')
        ok(vis(pg, '#nameIt') and 'quiet' in pg.get_attribute('#nameIt', 'class'), tag + ': naming is offered quietly after the first reply')
        ok('Claude, an AI made by Anthropic, is listening as a learner' in pg.inner_text('#note'), tag + ': who is listening is always said')
        layout(pg, tag + ' reply')
        if vname == 'phone': pg.screenshot(path=SHOTS + '/2-reply.png', full_page=True)
        h.script = [dict(R2)]
        say(pg, 'It was there before I noticed the hum.'); pg.locator('.reply').nth(1).wait_for()
        b = h.posts[1]
        ok(any(x['role'] == 'assistant' and 'What I learned from you: A sound can be felt in the shoulders, not only heard.' in x['content'] for x in b['turns']) and b['turns'][-1]['role'] == 'assistant' and b['turns'][-2]['content'] == 'The fridge hum gets into my shoulders.', tag + ': Claude hears its own last reply the way the person read it')
        ok(pg.evaluate("!window.__pwn && !document.querySelector('.reply img')") and '<img src=x' in text(pg), tag + ': markup in a reply is shown as plain words, never run')
        ok('THE YOU WHO SENSES MOST CLEARLY MIGHT NOTICE' in text(pg).upper() and 'quiet' not in pg.get_attribute('#nameIt', 'class'), tag + ': the clearest-seeing self speaks; naming steps forward when the sense is ready')
        h.script = [json.loads(json.dumps(CLOSE))]
        pg.click('#nameIt'); pg.wait_for_selector('#closeCard')
        b = h.posts[2]
        ok(b.get('v') == 2 and b.get('keep') is True and 'words' not in b and b['turns'][-1]['role'] == 'assistant', tag + ': naming is asked the new way')
        t = text(pg, '#close')
        ok('“was there before”' in t and 'Unease' in t and 'a field that will not settle' in t and 'Fear' in t and pg.locator('#closeCard .sym svg').count() == 2, tag + ': the sense in their words, with its Alphasense words, meanings and symbols')
        ok('SYMBOLS TOGETHER' in t.upper() and pg.locator('#closeCard .bond .bw').count() == 2 and pg.locator('#closeCard .bond .sym svg').count() == 2 and 'only an offer' in t, tag + ': two symbols together, as an offer')
        ok('A body can hold a tightness for hours.' in t and 'The part of you that notices is still here.' in t, tag + ': what Claude learned, and the clearest-seeing self')
        ok(all(x in t for x in ['Offer it to the map', 'Keep it', 'Let it go']) and not vis(pg, '#say'), tag + ': three doors')
        layout(pg, tag + ' naming')
        if vname == 'phone': pg.screenshot(path=SHOTS + '/3-naming.png', full_page=True)
        pg.click('text=Only Unease'); ok(pg.inner_text('#closeCard .word b') == 'Unease' and 'carries a doorway: Safety' in text(pg, '#closeCard'), tag + ': one symbol alone can be chosen, and shows its doorway from the language itself')
        pg.click('text=Add or change symbols'); pg.wait_for_selector('.grid button')
        ok(pg.locator('.chips button').count() == 9 and pg.locator('.grid button').count() >= 5, tag + ': the whole alphabet can be looked through, chapter by chapter')
        layout(pg, tag + ' alphabet')
        if vname == 'phone': pg.screenshot(path=SHOTS + '/4-alphabet.png', full_page=True)
        pg.click('.chips button:has-text("The inner weather")'); pg.click('.grid button:has-text("Serenity")')
        ok('Chosen: Unease + Serenity' in text(pg, '#close') and pg.get_attribute('.grid button:has-text("Serenity")', 'aria-pressed') == 'true', tag + ': a symbol is added by tapping it')
        pg.evaluate("[...document.querySelectorAll('.grid button[aria-pressed=false]')].slice(0,4).forEach(b=>b.click())")
        ok(pg.evaluate("document.querySelectorAll('.grid button[aria-pressed=true]').length") == 4 and 'Up to four symbols can join' in text(pg, '#close'), tag + ': up to four symbols can join, and no more')
        layout(pg, tag + ' choosing')
        pg.evaluate("[...document.querySelectorAll('.grid button[aria-pressed=true]')].filter(b=>!b.textContent.includes('Serenity')&&!b.textContent.includes('Unease')).forEach(b=>b.click())")
        pg.click('text=Done'); pg.wait_for_selector('#closeCard')
        ok(pg.locator('#closeCard .bond .bw').count() == 2 and 'Serenity' in text(pg, '#closeCard') and 'Unease' in text(pg, '#closeCard'), tag + ': the chosen symbols come back together')
        pg.click('text=This is a new sense')
        ok(pg.locator('#closeCard .fuse svg g').count() == 2 and 'Formed from Unease and Serenity' in text(pg, '#closeCard') and 'A NEW SYMBOL, FORMED JUST NOW' in text(pg, '#closeCard').upper(), tag + ': a new symbol is formed in the moment from the nearest ones')
        layout(pg, tag + ' new symbol')
        if vname == 'phone': pg.screenshot(path=SHOTS + '/8-new-symbol.png', full_page=True)
        pg.fill('#working', 'the bracing before the bang')
        pg.click('.doors3 button:has-text("Keep it")'); pg.wait_for_selector('text=Begin again')
        kept = json.loads(pg.evaluate("localStorage.getItem('as_mirror_senses')"))
        ok(len(kept) == 1 and kept[0]['working'] == 'the bracing before the bang' and kept[0]['word'] == '' and kept[0]['fresh'] is True and kept[0]['words'] == ['Unease', 'Serenity'] and 'was there before' in kept[0]['sensed'] and len(h.posts) == 3, tag + ': kept on this device only; nothing more was sent')
        ok('Your kept senses (1)' in pg.inner_text('#note'), tag + ': the kept sense can be found again')
        layout(pg, tag + ' kept')
        pg.click('text=Begin again')
        ok(vis(pg, '#hero') and pg.locator('#thread > *').count() == 0 and vis(pg, '#say') and not vis(pg, '#nameIt'), tag + ': beginning again leaves nothing of the last conversation')
        ok(not errs and not h.other, tag + ': no errors, and nothing asked of any other site ' + '; '.join(errs + h.other)[:200])
        ctx.close()

    # B · let it go; offer it to the map
    h = Helper(); ctx, pg, errs = open_page(h)
    pg.evaluate("localStorage.setItem('as_age18','1');localStorage.setItem('as_mirror_listener','claude')"); pg.reload(); pg.wait_for_timeout(250)
    h.script = [dict(R1), json.loads(json.dumps(CLOSE))]
    say(pg, 'The fridge hum gets into my shoulders.'); pg.wait_for_selector('.reply')
    ok(not vis(pg, '#ask') and len(h.posts) == 1, 'B: a yes given before is remembered on this device')
    pg.click('#nameIt'); pg.wait_for_selector('#closeCard')
    pg.click('.doors3 button:has-text("Offer it to the map")')
    ok(pg.input_value('#offer') == 'A hum in the flat seemed to get into my shoulders.' and 'Its symbols: Unease + Fear.' in text(pg, '#close'), 'B: the offer is shown first, in words with no name, and can be changed')
    pg.fill('#offer', 'The hum at 1420 Main Street gets into my shoulders.'); pg.click('text=Hold it ready for the map')
    ok('Please take out numbers' in text(pg, '#close') and pg.evaluate("localStorage.getItem('as_mirror_offers')") is None, 'B: an offer with a number or address is not held')
    pg.fill('#offer', 'I want to die'); pg.click('text=Hold it ready for the map')
    ok(vis(pg, '#care') and pg.evaluate("localStorage.getItem('as_mirror_offers')") is None, 'B: heavy words in an offer go to real help, never toward the map')
    ctx.close()
    h = Helper(); ctx, pg, errs = open_page(h)
    pg.evaluate("localStorage.setItem('as_age18','1');localStorage.setItem('as_mirror_listener','claude')"); pg.reload(); pg.wait_for_timeout(250)
    h.script = [dict(R1), json.loads(json.dumps(CLOSE))]
    say(pg, 'The fridge hum gets into my shoulders.'); pg.wait_for_selector('.reply'); pg.click('#nameIt'); pg.wait_for_selector('#closeCard')
    pg.click('.doors3 button:has-text("Offer it to the map")'); pg.click('text=Hold it ready for the map'); pg.wait_for_selector('text=Held ready for the map')
    off = json.loads(pg.evaluate("localStorage.getItem('as_mirror_offers')"))
    ok(len(off) == 1 and off[0]['words'] == ['Unease', 'Fear'] and off[0]['fresh'] is False and off[0]['text'].startswith('A hum in the flat') and len(h.posts) == 2 and 'nothing has been sent' in text(pg, '#close'), 'B: the offer waits on this device; nothing is sent until the map asks where it belongs')
    pg.click('text=Begin again'); h.script = [dict(R1), json.loads(json.dumps(CLOSE))]
    say(pg, 'The fridge hum gets into my shoulders.'); pg.wait_for_selector('.reply'); pg.click('#nameIt'); pg.wait_for_selector('#closeCard')
    pg.click('.doors3 button:has-text("Let it go")'); pg.wait_for_selector('text=It’s gone', timeout=6000)
    ok(pg.locator('#thread > *').count() == 0 and pg.evaluate("localStorage.getItem('as_mirror_senses')") is None, 'B: let it go: nothing is kept, and the conversation is cleared')
    pg.screenshot(path=SHOTS + '/5-gone.png', full_page=True)
    ok(not errs, 'B: no errors ' + '; '.join(errs)[:200]); ctx.close()

    # C · outside Canada: the written Mirror, and nothing leaves the page
    h = Helper(listen=False); ctx, pg, errs = open_page(h)
    say(pg, 'A heaviness in the room since the chair went.'); pg.wait_for_selector('.reply')
    ok(not vis(pg, '#ask') and len(h.posts) == 0, 'C: outside Canada there is no question about Claude, and nothing is sent')
    t = text(pg)
    ok('THE WRITTEN MIRROR' in t.upper() and 'You wrote: “A heaviness in the room since the chair went.”' in t and 'What is it like?' in t, 'C: the written Mirror gives their words back and asks the first plain side')
    ok('Claude listens in Canada first' in pg.inner_text('#note') and 'nothing leaves this page' in pg.inner_text('#note'), 'C: it says why, and that nothing leaves the page')
    for i, q in enumerate(['Where does it sit', 'When did it first come', 'Does it belong to this place']):
        say(pg, 'answer %d' % i); pg.locator('.reply').nth(i + 1).wait_for()
        ok(q in pg.locator('.reply').last.inner_text(), 'C: the written Mirror walks the four sides: ' + q)
    ok('quiet' not in pg.get_attribute('#nameIt', 'class'), 'C: after the four sides, naming steps forward')
    pg.click('#nameIt'); pg.wait_for_selector('#closeCard')
    ok(len(h.posts) == 0 and '“A heaviness in the room since the chair went.”' in text(pg, '#closeCard') and 'No symbol has been chosen' in text(pg, '#closeCard'), 'C: naming without Claude: their own first words, and no word pressed on them')
    pg.click('text=Look through the symbols'); pg.click('.chips button:has-text("Of place")'); pg.locator('.grid button').first.click(); pg.click('text=Done')
    ok(pg.locator('#closeCard .word b').count() == 1, 'C: they can choose a symbol themselves')
    pg.click('text=No symbol'); pg.click('text=This is a new sense')
    ok(pg.locator('#closeCard .fuse svg').count() == 1 and 'An open ring' in text(pg, '#closeCard') and pg.locator('#working').count() == 1, 'C: a new sense with no relatives yet shows an open ring, and takes their own name')
    layout(pg, 'C written naming'); pg.screenshot(path=SHOTS + '/6-written.png', full_page=True)
    ok(len(h.posts) == 0 and not errs, 'C: still nothing sent, no errors ' + '; '.join(errs)[:200]); ctx.close()

    # D · heavy words: real help first, the page gently stays, and nothing is ever sent
    h = Helper(); ctx, pg, errs = open_page(h)
    pg.evaluate("localStorage.setItem('as_age18','1');localStorage.setItem('as_mirror_listener','claude')"); pg.reload(); pg.wait_for_timeout(250)
    say(pg, 'Some days I don’t want to be here')
    t = text(pg)
    ok(vis(pg, '#care') and len(h.posts) == 0, 'D: heavy words never leave the page, even with Claude chosen')
    ok('Please reach a person now' in t and pg.locator('#care a[href="tel:988"]').count() == 1 and 'findahelpline.com' in t, 'D: real help is shown, with a number that can be tapped')
    ok('You can keep writing here while you reach someone. Nothing you write now leaves this page.' in t and vis(pg, '#words') and not vis(pg, '#nameIt'), 'D: the page gently stays, without the AI')
    say(pg, 'I am still here, writing')
    ok('I am still here, writing' in text(pg) and 'Only here. Nothing is sent.' in text(pg) and len(h.posts) == 0, 'D: what they write afterwards stays on the page; nothing is sent')
    layout(pg, 'D care'); pg.screenshot(path=SHOTS + '/7-care.png', full_page=True)
    ok(not errs, 'D: no errors ' + '; '.join(errs)[:200]); ctx.close()
    h = Helper(); ctx, pg, errs = open_page(h)
    pg.evaluate("localStorage.setItem('as_age18','1');localStorage.setItem('as_mirror_listener','claude')"); pg.reload(); pg.wait_for_timeout(250)
    h.script = [{'ok': True, 'care': True, 'by': 'claude', 'v': 2, 'reflect': 'That sounds heavy.', 'question': ''}]
    say(pg, 'nothing matters much any more'); pg.wait_for_selector('#care:not(.hide)')
    ok('Claude heard something heavy' in pg.inner_text('#who') and vis(pg, '#care'), 'D: when Claude hears something heavy, real help comes first')
    say(pg, 'more words'); ok(len(h.posts) == 1, 'D: after that, nothing more is sent'); ctx.close()

    # E · when Claude cannot answer, the written Mirror carries on
    h = Helper(); ctx, pg, errs = open_page(h)
    pg.evaluate("localStorage.setItem('as_age18','1');localStorage.setItem('as_mirror_listener','claude')"); pg.reload(); pg.wait_for_timeout(250)
    h.script = [{'ok': False, 'code': 'busy', '_status': 429}, dict(R1), {'ok': False, 'code': 'resting', '_status': 503}]
    say(pg, 'the hum'); pg.wait_for_selector('.reply')
    ok('THE WRITTEN MIRROR' in text(pg).upper() and 'carries on for a moment' in pg.inner_text('#who'), 'E: a busy moment: the written Mirror answers this once')
    say(pg, 'in my shoulders'); pg.locator('.reply').nth(1).wait_for()
    ok(len(h.posts) == 2 and 'you hear it with your body too' in pg.locator('.reply').last.inner_text(), 'E: Claude listens again on the next words')
    ok(any(x['content'].startswith('[Written by the Mirror’s written rules') and 'You wrote' in x['content'] for x in h.posts[1]['turns']), 'E: Claude is told which reply the written rules gave')
    say(pg, 'still there'); pg.locator('.reply').nth(2).wait_for()
    say(pg, 'and now'); pg.locator('.reply').nth(3).wait_for()
    ok(len(h.posts) == 3 and 'Claude is resting' in pg.inner_text('#note'), 'E: when Claude rests, nothing more is sent this visit')
    h2 = Helper(); h2.script = [{'ok': False, 'code': 'away'}]
    ctx2, pg2, e2 = open_page(h2); pg2.evaluate("localStorage.setItem('as_age18','1');localStorage.setItem('as_mirror_listener','claude')"); pg2.reload(); pg2.wait_for_timeout(250)
    say(pg2, 'the hum'); pg2.wait_for_selector('.reply')
    ok('Claude listens in Canada first' in pg2.inner_text('#note'), 'E: if the helper says "away", the page says Canada first and stops sending'); ctx2.close()
    ok(not errs, 'E: no errors ' + '; '.join(errs)[:200]); ctx.close()

    # F · not now; stop sharing; the helper missing altogether
    h = Helper(); ctx, pg, errs = open_page(h)
    say(pg, 'the hum'); pg.click('#ask button.quiet'); pg.wait_for_selector('.reply')
    ok(len(h.posts) == 0 and 'THE WRITTEN MIRROR' in text(pg).upper() and pg.evaluate("localStorage.getItem('as_mirror_listener')") is None, 'F: "Not now" sends nothing, and the written Mirror asks instead')
    ok(pg.locator('#note button:has-text("Let Claude listen")').count() == 1, 'F: the way back to Claude stays open')
    pg.click('#note button:has-text("Let Claude listen")'); pg.click('#ask button.btn:not(.quiet)'); h.script = [dict(R1)]
    say(pg, 'in my shoulders'); pg.locator('.reply').nth(1).wait_for()
    ok(len(h.posts) == 1, 'F: after a later yes, Claude listens')
    pg.click('#note button:has-text("Stop sharing my words")'); say(pg, 'more'); pg.locator('.reply').nth(2).wait_for()
    ok(len(h.posts) == 1 and pg.evaluate("localStorage.getItem('as_mirror_listener')") is None, 'F: "Stop sharing my words" stops at once, and forgets the yes')
    ctx.close()
    h = Helper(live=False); ctx, pg, errs = open_page(h)
    say(pg, 'the hum'); pg.wait_for_selector('.reply')
    ok(len(h.posts) == 0 and 'Claude is resting' in pg.inner_text('#note'), 'F: where Claude is switched off, the written Mirror asks and nothing is sent'); ctx.close()

    # H · Build 176 · asking in words for a name opens the naming, as the button does (from Karl's first use)
    h = Helper(); ctx, pg, errs = open_page(h)
    pg.evaluate("localStorage.setItem('as_age18','1');localStorage.setItem('as_mirror_listener','claude')"); pg.reload(); pg.wait_for_timeout(250)
    h.script = [dict(R1)]
    say(pg, 'Please help me name this feeling in my shoulders.'); pg.wait_for_selector('.reply')
    ok(h.posts[0].get('keep') is None and h.posts[0]['words'].startswith('Please help me name'), 'H: a first message is always heard as a sense, whatever its words')
    h.script = [dict(R1)]
    say(pg, 'yes'); pg.locator('.reply').nth(1).wait_for()
    ok(len(h.posts) == 2 and h.posts[1].get('keep') is None, 'H: a plain "yes" is only a yes when naming was not just offered')
    h.script = [json.loads(json.dumps(CLOSE))]
    say(pg, 'Can you help me name it given what I’ve told you about it?'); pg.wait_for_selector('#closeCard')
    ok(len(h.posts) == 3 and h.posts[2].get('keep') is True and 'Can you help me name it' in text(pg, '#thread') and 'Unease' in text(pg, '#closeCard'), 'H: "can you help me name it" opens the naming at once, with a word offered')
    ok(not any('help me name it' in x['content'] for x in h.posts[2]['turns']), 'H: the request itself is not sent as if it were a sense')
    pg.click('text=Stay with it a little longer')
    h.script = [dict(R2)]
    say(pg, 'It was there before I noticed the hum.'); pg.locator('.reply').nth(2).wait_for()
    h.script = [dict(R1)]
    say(pg, 'I would like to stay with it a little longer'); pg.locator('.reply').nth(3).wait_for()
    ok(h.posts[-1].get('keep') is None, 'H: wanting to stay with it is heard, never taken as a yes')
    h.script = [dict(R2)]
    say(pg, 'more of it'); pg.locator('.reply').nth(4).wait_for()
    h.script = [json.loads(json.dumps(CLOSE))]
    say(pg, 'Yes please'); pg.wait_for_selector('#closeCard')
    ok(h.posts[-1].get('keep') is True, 'H: "yes please", right after naming is offered, opens the naming')
    for phrase in ['what would you call this?', 'is there a word for this', 'Give it a name', 'find me a word for it']:
        ok(pg.evaluate("(t) => { const NAMEASK = %s; return NAMEASK.test(t); }" % __import__('re').search(r'var NAMEASK=(/.*/i);', src).group(1), phrase), 'H: understood as asking for a name: ' + phrase)
    for phrase in ['my name is not important', 'the name of the street is noisy', 'it has no name and I like that', 'I cannot name what I lost']:
        ok(not pg.evaluate("(t) => { const NAMEASK = %s; return NAMEASK.test(t); }" % __import__('re').search(r'var NAMEASK=(/.*/i);', src).group(1), phrase), 'H: not mistaken for asking for a name: ' + phrase)
    ok(not errs, 'H: no errors ' + '; '.join(errs)[:200]); ctx.close()
    h = Helper(listen=False); ctx, pg, errs = open_page(h)
    say(pg, 'A heaviness in the room.'); pg.wait_for_selector('.reply')
    say(pg, 'help me name it'); pg.wait_for_selector('#closeCard')
    ok(len(h.posts) == 0 and 'Look through the symbols' in text(pg, '#close'), 'H: with the written Mirror too, asking for a name opens the words to choose from'); ctx.close()

    # G · inside the map: one way back, and only "close" is ever said
    h = Helper(); ctx = br.new_context(viewport={'width': 390, 'height': 844});
    def host(route):
        if route.request.url == BASE + '/host-test':
            route.fulfill(status=200, content_type='text/html', body='<!doctype html><iframe id="f" src="/mirror.html?in=site" style="width:380px;height:700px"></iframe><script>window.got=[];addEventListener("message",function(e){window.got.push([e.origin,JSON.stringify(e.data)]);});</script>'); return
        h.handle(route)
    ctx.route('**/*', host); pg = ctx.new_page(); pg.goto(BASE + '/host-test'); pg.wait_for_timeout(500)
    fr = pg.frame_locator('#f'); fr.locator('#back').click(); pg.wait_for_timeout(150)
    ok(pg.evaluate('window.got') == [[BASE, '{"as":"mirror","act":"close"}']], 'G: inside the map, "Back to the map" says only "close", only to Aurasense')
    ctx.close()
    h = Helper(); ctx, pg, errs = open_page(h); ok(not vis(pg, '#back'), 'G: opened by itself, there is no map button'); ctx.close()

    # I · Build 177 · one symbol, symbols together, or a new symbol formed in the moment
    def named(close):
        h = Helper(); ctx, pg, errs = open_page(h)
        pg.evaluate("localStorage.setItem('as_age18','1');localStorage.setItem('as_mirror_listener','claude')"); pg.reload(); pg.wait_for_timeout(250)
        c = json.loads(json.dumps(CLOSE)); c['close'].update(close)
        for k in [k for k, v in close.items() if v is None]: del c['close'][k]
        h.script = [dict(R1), c]
        say(pg, 'The fridge hum gets into my shoulders.'); pg.wait_for_selector('.reply'); pg.click('#nameIt'); pg.wait_for_selector('#closeCard')
        return h, ctx, pg, errs
    h, ctx, pg, errs = named({'words': ['Hope', 'Grief'], 'fits': 'together', 'name': 'Hope', 'also': 'Grief'})
    ok('In Alphasense, Hope and Grief meet as: “mourning with light in it' in text(pg, '#closeCard'), 'I: where the language already knows what two symbols mean together, the Mirror says so')
    ok(not errs, 'I: no errors ' + '; '.join(errs)[:200]); ctx.close()
    h, ctx, pg, errs = named({'words': ['Unease', 'Fear'], 'fits': 'new', 'name': 'new', 'also': '', 'working': 'the bracing before the bang'})
    t = text(pg, '#closeCard')
    ok(pg.locator('#closeCard .fuse svg g').count() == 2 and 'Formed from Unease and Fear' in t and pg.input_value('#working') == 'the bracing before the bang', 'I: a new sense arrives with its new symbol already formed, and a name in their own words to change')
    pg.click('text=Not new: the symbols together'); ok(pg.locator('#closeCard .bond .bw').count() == 2, 'I: the person can say it is not new after all')
    pg.click('text=Back to what was offered'); ok(pg.locator('#closeCard .fuse svg').count() == 1, 'I: and can go back to what was offered')
    pg.click('.doors3 button:has-text("Offer it to the map")')
    ok('A new sense: the bracing before the bang, formed from Unease and Fear.' in text(pg, '#close'), 'I: the offer says plainly that it is a new sense, and what it was formed from')
    pg.click('text=Hold it ready for the map'); pg.wait_for_selector('text=Held ready for the map')
    off = json.loads(pg.evaluate("localStorage.getItem('as_mirror_offers')"))
    ok(off[0]['fresh'] is True and off[0]['words'] == ['Unease', 'Fear'] and off[0]['working'] == 'the bracing before the bang' and off[0]['word'] == '', 'I: what is held for the map carries the new sense, its name and its relatives')
    ok(not errs, 'I: no errors ' + '; '.join(errs)[:200]); ctx.close()
    h, ctx, pg, errs = named({'words': ['Stillness'], 'fits': 'one', 'name': 'Stillness', 'also': ''})
    ok(pg.locator('#closeCard .word b').count() == 1 and pg.inner_text('#closeCard .word b') == 'Stillness' and pg.locator('#closeCard .bond').count() == 0, 'I: when one word fits, one symbol is shown'); ctx.close()
    h, ctx, pg, errs = named({'words': None, 'fits': None, 'name': 'Unease', 'also': 'Fear'})
    ok(pg.locator('#closeCard .bond .bw').count() == 2, 'I: an answer in the older form is still understood'); ctx.close()
    h, ctx, pg, errs = named({'words': ['Unease', '<img src=x onerror=1>', 'Unease', 'Nope'], 'fits': 'together', 'name': 'Unease', 'also': ''})
    ok(pg.locator('#closeCard .word b').count() == 1 and pg.evaluate("!document.querySelector('#close img')"), 'I: only symbols the alphabet holds are ever shown'); ctx.close()
    br.close()

print('\n%d checks passed, %d failed' % (passes, len(fails)))
sys.exit(1 if fails else 0)
