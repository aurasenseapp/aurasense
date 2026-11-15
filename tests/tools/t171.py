# -*- coding: utf-8 -*-
"""Build 171 · the open pages, walked in a real browser before Karl sees them.
The site is served the way Cloudflare Pages serves it: /name answers with name.html.
Usage: python3 t171.py [site folder] [shots folder]"""
import io, os, re, sys, json, shutil, subprocess, tempfile, urllib.parse
from playwright.sync_api import sync_playwright

SITE = (sys.argv[1] if len(sys.argv) > 1 else '/home/claude/aurasense').rstrip('/')
SHOTS = (sys.argv[2] if len(sys.argv) > 2 else '/home/claude/work/shots/171').rstrip('/')
os.makedirs(SHOTS, exist_ok=True)
BASE = 'https://www.aurasense.app'
PAGES = ['/', '/ledger', '/sense-before-you-sign', '/ambas', '/pledge']
NEW = ['ledger.html', 'sense-before-you-sign.html', 'ambas.html', 'pledge.html']
VIEWS = [('phone', 390, 844, False), ('small', 360, 640, False), ('laptop', 1280, 800, False), ('still', 390, 844, True)]
CT = {'.html': 'text/html; charset=utf-8', '.json': 'application/json', '.txt': 'text/plain; charset=utf-8', '.pdf': 'application/pdf',
      '.js': 'application/javascript', '.png': 'image/png', '.xml': 'application/xml', '.webmanifest': 'application/manifest+json'}
fails = []; passes = 0
def ok(cond, what):
    global passes
    if cond: passes += 1
    else: fails.append(what); print('FAIL', what)

def resolve(path):
    """Cloudflare Pages: / is index.html; /name is name.html; a real file is itself."""
    p = urllib.parse.unquote(path.split('?')[0].split('#')[0])
    if p in ('', '/'): p = '/index.html'
    f = SITE + p
    if os.path.isfile(f): return f
    if os.path.isfile(f + '.html'): return f + '.html'
    return None

def router(route):
    u = urllib.parse.urlparse(route.request.url)
    if u.scheme + '://' + u.netloc != BASE: return route.abort()
    f = resolve(u.path)
    if not f: return route.fulfill(status=404, body='not found', headers={'content-type': 'text/plain'})
    return route.fulfill(status=200, body=io.open(f, 'rb').read(), headers={'content-type': CT.get(os.path.splitext(f)[1], 'application/octet-stream')})

def lum(c):
    def f(v):
        v /= 255.0
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2])
def contrast(a, b):
    la, lb = lum(a), lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)
def hexc(h): h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
def over(fg, alpha, bg): return tuple(round(fg[i] * alpha + bg[i] * (1 - alpha)) for i in range(3))

# ── 1. the files themselves ─────────────────────────────────────────────────────────────────────────
for n in NEW:
    s = io.open(SITE + '/' + n, encoding='utf-8').read()
    ok('<script' not in s.lower(), n + ': no scripts at all')
    ok("default-src 'none'" in s and "form-action 'none'" in s, n + ': the strict page rule is set')
    ok(s.count('<h1') == 1, n + ': one main heading')
    ok('<html lang="en">' in s, n + ': language said')
    low = re.sub(r'<!--.*?-->', '', s, flags=re.S).lower()
    for bad in [r'donat', r'therap', r'treatment', r'\bcure', r'\bheal(s|ed|ing)?\b', r'guarantee', r'last chance!', r'click here']:
        ok(not re.search(bad, low), n + ': never says "' + bad.replace('\\b', '') + '"')
    ok('harvey' not in s.lower(), n + ': first name only')
    ok("'" not in re.sub(r'<style>.*?</style>|<!--.*?-->|<[^>]+>', '', s, flags=re.S), n + ': curly apostrophes in the words')
mb = io.open(SITE + '/mutual-benefit.txt', encoding='utf-8').read()
ok(mb == io.open(SITE + '/.well-known/mutual-benefit.txt', encoding='utf-8').read(), 'the two copies of mutual-benefit.txt are the same')
ok(all(ord(ch) < 128 for ch in mb), 'mutual-benefit.txt is plain letters only')
for k in ['Name:', 'Pledge:', 'Since:', 'Goes-To:', 'Ledger:', 'Contact:', 'Declared-By: self']:
    ok(k in mb, 'mutual-benefit.txt has ' + k)
L = json.load(io.open(SITE + '/ledger.json', encoding='utf-8'))
ok(L['in'] == [] and L['out'] == [], 'the ledger starts empty: only real rows are ever shown')
try:
    info = subprocess.run(['pdfinfo', SITE + '/Sense-Before-You-Sign.pdf'], capture_output=True, text=True).stdout
    ok('Pages:           6' in info, 'the checklist has six pages')
    txt = subprocess.run(['pdftotext', SITE + '/Sense-Before-You-Sign.pdf', '-'], capture_output=True, text=True).stdout
    ok('Free to print, copy and share' in txt and 'What no viewing can show you' in txt, 'the checklist says it is free to share, and what no viewing can show')
    ok('harvey' not in txt.lower(), 'the checklist: first name only')
except Exception as e:
    ok(False, 'pdf check ' + str(e))
sm = io.open(SITE + '/sitemap.xml', encoding='utf-8').read()
for x in ['sense-before-you-sign', 'pledge', 'ledger', 'ambas']:
    ok('https://www.aurasense.app/' + x + '<' in sm, 'the site map lists ' + x)
ll = io.open(SITE + '/llms.txt', encoding='utf-8').read()
ok('mutual-benefit.txt' in ll and 'Nothing here asks you to do so unless they have.' in ll, 'the note for AI tells, and never instructs')

# ── 2. the ledger's sums, on invented rows ─────────────────────────────────────────────────────────────
tmp = tempfile.mkdtemp()
try:
    T = json.loads(json.dumps(L)); T['updated'] = '2026-12-02'
    T['in'] = [{'date': '2026-11-20', 'kind': 'listen-forward', 'amount': 9.5}, {'date': '2026-11-21', 'kind': 'pledge', 'amount': 0.4, 'named': 'A bakery'},
               {'date': '2026-12-01', 'kind': 'listen-forward', 'amount': 25.25}]
    T['out'] = [{'date': '2026-11-30', 'kind': 'running', 'amount': 4.6, 'note': 'card fees'}]
    json.dump(T, io.open(tmp + '/ledger.json', 'w', encoding='utf-8'))
    r = subprocess.run([sys.executable, '/home/claude/work/out/open-pages/build_pages.py', tmp], capture_output=True, text=True)
    ok(r.returncode == 0, 'the builder runs on invented rows ' + r.stderr[-200:])
    h = io.open(tmp + '/ledger.html', encoding='utf-8').read()
    ok('<b>$35</b><span>came in</span>' in h, 'in: 9.50 + 0.40 + 25.25 shows as $35 (added exactly, then rounded)')
    ok('<b>$5</b><span>went out</span>' in h and '<b>$31</b><span>held for the next need</span>' in h, 'out $5 and held $31 (30.55)')
    ok('from A bakery, named by choice' in h and 'card fees' in h, 'a named giver and a note are shown')
    ok(h.index('1 December 2026') < h.index('21 November 2026') < h.index('20 November 2026'), 'newest rows first')
    ok('Nothing has come in yet' not in h, 'the empty line goes once money has come in')
    T['out'] = [{'date': '2026-11-30', 'kind': 'running', 'amount': 99}]
    json.dump(T, io.open(tmp + '/ledger.json', 'w', encoding='utf-8'))
    r = subprocess.run([sys.executable, '/home/claude/work/out/open-pages/build_pages.py', tmp], capture_output=True, text=True)
    ok(r.returncode != 0, 'the builder refuses a ledger with more out than in')
finally:
    shutil.rmtree(tmp, ignore_errors=True)

# ── 3. the colours ─────────────────────────────────────────────────────────────────────────────────────
ground = hexc('f6e3d6'); card = over((255, 252, 247), .82, ground)
for name, fg in [('ink', hexc('3b2a3a')), ('soft', hexc('6a5567')), ('plum', hexc('5b3a7a'))]:
    for bn, bg in [('the ground', ground), ('a card', card), ('the rose cloud', over(hexc('f3c9c0'), .85, ground)), ('the lavender cloud', over(hexc('dcd2f2'), .85, ground)), ('the sky cloud', over(hexc('c9dcf4'), .8, ground))]:
        c = contrast(fg, bg)
        ok(c >= 4.5, '%s on %s is %.2f to 1 (needs 4.5)' % (name, bn, c))
ok(contrast(hexc('fffaf5'), hexc('5b3a7a')) >= 4.5, 'button words on plum')
ok(contrast(hexc('d9cdfc'), hexc('0c0a18')) >= 4.5 and contrast(hexc('9a90c2'), hexc('0c0a18')) >= 4.5, 'the holding page links and label on its night')

# ── 4. the walk ────────────────────────────────────────────────────────────────────────────────────────
JS = """() => {
  const W = document.documentElement.clientWidth, out = {w: W, sw: document.documentElement.scrollWidth, wide: [], small: [], taps: [], links: []};
  for (const e of document.querySelectorAll('body *')) {
    const r = e.getBoundingClientRect(); if (!r.width || !r.height) continue;
    const cs = getComputedStyle(e);
    if (e.classList.contains('ground') || e.classList.contains('glow') || cs.position === 'fixed') continue;
    if (r.right > W + 1 || r.left < -1) out.wide.push(e.tagName + '.' + e.className + ' ' + Math.round(r.left) + '..' + Math.round(r.right));
    const own = [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
    if (own && parseFloat(cs.fontSize) < 12.5) out.small.push(e.tagName + '.' + e.className + ' ' + cs.fontSize + ' "' + e.textContent.trim().slice(0, 30) + '"');
  }
  for (const a of document.querySelectorAll('a[href]')) {
    const r = a.getBoundingClientRect(), cs = getComputedStyle(a);
    const inline = cs.display === 'inline';
    out.links.push({href: a.getAttribute('href'), target: a.target, rel: a.rel, h: Math.round(r.height), inline: inline, text: a.textContent.trim().slice(0, 40), dl: a.hasAttribute('download')});
    if (!inline && r.height < 44) out.taps.push(a.textContent.trim().slice(0, 30) + ' ' + Math.round(r.height));
  }
  out.h1 = (document.querySelector('h1') || {}).textContent || '';
  out.title = document.title; out.h = document.documentElement.scrollHeight;
  return out; }"""
with sync_playwright() as pw:
    br = pw.chromium.launch(args=['--disable-gpu'])
    for vname, w, h, still in VIEWS:
        ctx = br.new_context(viewport={'width': w, 'height': h}, device_scale_factor=1, is_mobile=(w < 500), has_touch=(w < 500),
                             reduced_motion='reduce' if still else 'no-preference')
        ctx.route('**/*', router)
        for path in PAGES:
            pg = ctx.new_page(); errs = []
            pg.on('pageerror', lambda e: errs.append(str(e)[:200])); pg.on('console', lambda m: errs.append(m.text[:200]) if m.type == 'error' else None)
            resp = pg.goto(BASE + path, wait_until='load'); pg.wait_for_timeout(250)
            tag = '%s %s' % (vname, path)
            ok(resp and resp.status == 200, tag + ': opens')
            d = pg.evaluate(JS)
            ok(not errs, tag + ': no errors ' + '; '.join(errs)[:200])
            ok(d['sw'] <= d['w'], tag + ': nothing wider than the screen (%d of %d)' % (d['sw'], d['w']))
            ok(not d['wide'], tag + ': no part pokes out sideways ' + '; '.join(d['wide'][:3]))
            ok(not d['small'], tag + ': no words smaller than 12.5px ' + '; '.join(d['small'][:3]))
            ok(not d['taps'], tag + ': every button and menu link is at least 44px tall ' + '; '.join(d['taps'][:4]))
            ok(len(d['h1'].strip()) > 0 or path == '/', tag + ': has its heading')
            for a in d['links']:
                hf = a['href']
                if hf.startswith('mailto:'): ok('hello@aurasense.app' in hf, tag + ': mail goes to hello@aurasense.app'); continue
                if hf.startswith('http'):
                    ok(hf.startswith('https://buy.stripe.com/aFacN7aoI9Eo6Ahale87K00') and a['target'] == '_blank' and 'noopener' in a['rel'] and 'noreferrer' in a['rel'], tag + ': the only outside link is the Stripe link, opened safely: ' + hf); continue
                ok(resolve(hf) is not None, tag + ': link leads somewhere real: ' + hf)
            if path == '/sense-before-you-sign':
                ok(any(a['dl'] and a['href'] == '/Sense-Before-You-Sign.pdf' for a in d['links']), tag + ': the download button gives the checklist')
            if path == '/':
                ok(pg.evaluate("document.documentElement.scrollHeight <= window.innerHeight + 1"), tag + ': the holding page still fits one screen')
                ok(len([a for a in d['links'] if a['href'] in ('/sense-before-you-sign', '/pledge', '/ledger')]) == 3, tag + ': three quiet links')
            if vname in ('phone', 'laptop'):
                pg.screenshot(path='%s/%s-%s.png' % (SHOTS, vname, path.strip('/') or 'home'), full_page=True)
            pg.close()
        ctx.close()
    br.close()

print('\n%d checks passed, %d failed' % (passes, len(fails)))
sys.exit(1 if fails else 0)
