# Build 188 · Alphasense One by One, as a page standing alone.   cd <site>; python3 t188.py
import os,sys,io,json,pathlib,re
from playwright.sync_api import sync_playwright
site=os.getcwd(); fails=0; n=0
def ok(c,name):
    global fails,n; n+=1; print(('PASS ' if c else 'FAIL ')+name); fails+=0 if c else 1
s=io.open(site+'/alphasense.html',encoding='utf8').read()
j=json.load(io.open(site+'/alphasense.json',encoding='utf8'))
ok("default-src 'none'" in s and "connect-src" not in s and "base-uri 'none'" in s and "form-action 'none'" in s, 'the page may connect to nothing at all')
ok('name="robots" content="noindex"' in s, 'search is asked not to list it yet')
ok('http://' not in s and 'https://' not in s and 'window.claude' not in s and 'eval(' not in s, 'it reaches for nothing outside itself')
ok(all((w['w'] in s) for w in j['words']) and len(j['words'])==130, 'every one of today\'s 130 Alphasense words is in it')
ok('not yet on the site' not in s and 'One symbol at a time' in s, 'its first line is true now')
for f in ('index.html','index-mapbox.html','about.html','mirror.html','seeking.html'):
    t=io.open(site+'/'+f,encoding='utf8').read()
    ok('alphasense.html' not in t and 'href="/alphasense"' not in t, f+': nothing links to it yet (Karl feels it first)')
ok(not re.search(r'[Hh]arvey|yahoo|KHtest', s), 'no private word is in the page')
with sync_playwright() as p:
    b=p.chromium.launch()
    for tag,(w,h) in {'phone':(390,844),'small':(320,568),'laptop':(1280,800)}.items():
        c=b.new_context(viewport={'width':w,'height':h},device_scale_factor=1); pg=c.new_page()
        out=[]; pg.on('request', lambda r: out.append(r.url) if not r.url.startswith(('file:','data:')) else None)
        errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)[:120]))
        pg.goto(pathlib.Path(site+'/alphasense.html').as_uri()); pg.wait_for_timeout(900)
        d=pg.evaluate("({sw:document.documentElement.scrollWidth,iw:innerWidth,cnt:[...document.querySelectorAll('.cnt')].map(e=>e.textContent)})")
        ok(d['sw']<=d['iw'] and d['cnt'][0]=='130 words in 9 chapters', tag+': fits the screen and counts 130 words in 9 chapters')
        pg.locator('#home button').first.click(); pg.wait_for_timeout(900)
        e=pg.evaluate("({vis:!document.getElementById('chapter').hidden,sw:document.documentElement.scrollWidth,iw:innerWidth,t:document.getElementById('chapter').innerText})")
        ok(e['vis'] and e['sw']<=e['iw'] and 'Sense it first' in e['t'], tag+': a chapter opens one symbol, sensed before it is named')
        ok(not out and not errs, tag+': nothing is asked of the outside world, and no faults (%s %s)'%(out[:1],errs[:1]))
        c.close()
    b.close()
print('\n%d checks, %d failed'%(n,fails)); sys.exit(1 if fails else 0)
