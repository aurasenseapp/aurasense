"""Test harness (Mirror use): serves files from /home/claude/work/test so a page can be walked in a real browser
before Karl sees it, with a pretend listener helper at /api/mirror. Test-only: never part of the real site."""
import io, json, re, os, urllib.parse
from playwright.sync_api import sync_playwright

WORK = '/home/claude/work'
TEST = WORK + '/test'
BASE = 'http://aurasense.test/'

class Api:
    """The pretend helper. mode: 'absent' (as on Vercel: no helper at all), 'off' (a preview without the key),
    'live'. replies: a list of dicts handed out in order for each POST (the last one repeats)."""
    def __init__(self, mode='absent', replies=None, delay=0):
        self.mode = mode; self.replies = replies or []; self.posts = []; self.gets = 0; self.delay = delay
    def handle(self, route):
        req = route.request
        if self.mode == 'absent':
            return route.fulfill(status=404, body='<!doctype html><title>404</title>', headers={'content-type': 'text/html'})
        if req.method == 'GET':
            self.gets += 1
            return route.fulfill(status=200, body=json.dumps({'live': self.mode == 'live'}), headers={'content-type': 'application/json'})
        body = json.loads(req.post_data or '{}')
        self.posts.append(body)
        if self.mode != 'live':
            return route.fulfill(status=503, body=json.dumps({'ok': False, 'code': 'off'}), headers={'content-type': 'application/json'})
        r = self.replies[min(len(self.posts) - 1, len(self.replies) - 1)] if self.replies else {'ok': True, 'by': 'claude', 'reflect': 'Heard.', 'question': 'What else?', 'aspire': '', 'care': False}
        if callable(r): r = r(body)
        status = r.pop('_status', 200) if isinstance(r, dict) else 200
        return route.fulfill(status=status, body=json.dumps(r), headers={'content-type': 'application/json'})

def make_router(api):
    def router(route):
        url = route.request.url
        if url.startswith(BASE):
            p = urllib.parse.urlparse(url).path.lstrip('/') or 'index-mapbox.html'
            if p == 'api/mirror':
                return api.handle(route)
            fp = os.path.join(TEST, p)
            if os.path.exists(fp):
                ct = 'text/html' if fp.endswith('.html') else ('application/javascript' if fp.endswith('.js') else 'text/plain')
                return route.fulfill(status=200, body=io.open(fp, 'rb').read(), headers={'content-type': ct + '; charset=utf-8'})
            return route.fulfill(status=404, body='')
        return route.abort()
    return router

class Walk:
    def __init__(self, w=1440, h=900, mobile=False, reduce=False, api=None, init=None):
        self.api = api or Api()
        self.pw = sync_playwright().start()
        self.br = self.pw.chromium.launch(args=['--disable-gpu'])
        self.ctx = self.br.new_context(viewport={'width': w, 'height': h}, device_scale_factor=1, is_mobile=mobile, has_touch=mobile,
                                       reduced_motion='reduce' if reduce else 'no-preference')
        self.ctx.route('**/*', make_router(self.api))
        if init: self.ctx.add_init_script(init)
        self.page = self.ctx.new_page()
        self.errors = []
        self.popups = []
        self.ctx.on('page', lambda p: self.popups.append(p))
        self.page.on('pageerror', lambda e: self.errors.append('PAGEERROR ' + str(e)[:300]))
        self.page.on('console', lambda m: self.errors.append('CONSOLE ' + m.text[:300]) if m.type == 'error' and 'ko-fi' not in m.text and 'stripe' not in m.text and 'Failed to load resource' not in m.text else None)   # the browser's own note of a 404 or 503 from the helper is expected
    def open(self, file='mirror-living.html', q='', wait=2600):
        self.page.goto(BASE + file + q)
        self.page.wait_for_timeout(wait)
        return self.page
    def js(self, code, arg=None):
        return self.page.evaluate(code, arg) if arg is not None else self.page.evaluate(code)
    def say(self, text, wait=4200):
        self.js("t=>{const a=document.getElementById('words');a.value=t;document.getElementById('send').click();}", text)
        self.page.wait_for_timeout(wait)
    def speak(self):
        return self.js("document.getElementById('speak').innerText.replace(/\\s+/g,' ').trim()")
    def who(self):
        return self.js("(document.getElementById('who')||{}).textContent||''")
    def visible(self, id):
        return self.js("id=>{const e=document.getElementById(id);if(!e)return false;const s=getComputedStyle(e);return s.display!=='none'&&s.visibility!=='hidden'&&e.getClientRects().length>0;}", id)
    def click_text(self, sel, text):
        return self.js("([s,t])=>{const b=[...document.querySelectorAll(s)].find(x=>x.textContent.trim()===t);if(b){b.click();return true;}return false;}", [sel, text])
    def shot(self, name, clip=None, full=False):
        os.makedirs(WORK + '/shots', exist_ok=True)
        p = WORK + '/shots/' + name + '.png'
        self.page.screenshot(path=p, clip=clip, full_page=full); return p
    def close(self):
        try: self.br.close(); self.pw.stop()
        except Exception: pass
