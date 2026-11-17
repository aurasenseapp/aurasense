# The day's build, checked in its opened state.   cd <site, on the open-the-doors branch>; python3 t_open.py
import os,sys,io,pathlib
from playwright.sync_api import sync_playwright
site=os.getcwd(); fails=0; n=0
def ok(c,name):
    global fails,n; n+=1; print(('PASS ' if c else 'FAIL ')+name); fails+=0 if c else 1
ix=io.open(site+'/index.html',encoding='utf8').read(); ab=io.open(site+'/about.html',encoding='utf8').read(); mp=io.open(site+'/index-mapbox.html',encoding='utf8').read()
S='Free to sense. Free to share. People and AI, learning from each other, for mutual benefit.'
ok('http-equiv="refresh" content="0; url=/m"' in ix and 'coming soon' not in ix and S in ix and '<script' not in ix and 'href="/about"' in ix, 'aurasense.app sends everyone straight on to the Seeking, with the sentence and a way to the About')
ok('noindex' not in ix and 'noindex' not in ab and S in ab, 'the first page and the About may be listed by search')
ok('var OPEN = /^(www\\.)?aurasense\\.app$/.test(location.hostname);' in mp and mp.count('var OPEN = ')==1, 'the curtain\'s switch opens at Aurasense\'s own address only')
def shows(key,host=None):
    with sync_playwright() as p:
        b=p.chromium.launch(); pg=b.new_page()
        if host:
            body=io.open(site+'/index-mapbox.html',encoding='utf8').read()
            def h(r):
                if r.request.url.split('?')[0]==host+'/index-mapbox.html': r.fulfill(status=200,content_type='text/html; charset=utf-8',body=body)
                else: r.abort()
            pg.route('**/*',h); pg.goto(host+'/index-mapbox.html'+key, wait_until='commit')
        else:
            pg.route('**/*', lambda r: r.continue_() if r.request.url.startswith('file:') else r.abort())
            pg.goto(pathlib.Path(site+'/index-mapbox.html').as_uri()+key, wait_until='commit')
        pg.wait_for_timeout(2500)
        r=pg.evaluate("({stamp:!!document.getElementById('build-stamp'),text:(document.body.innerText||'').slice(0,200)})"); b.close(); return r
for host in ('https://www.aurasense.app','https://aurasense.app'):
    r=shows('',host); ok(r['stamp'] and 'Not yet open' not in r['text'], host+': a stranger comes straight in, with no curtain')
r=shows('','https://open-the-doors.example.pages.dev'); ok(not r['stamp'], 'a test copy on another address keeps its curtain for strangers')
r=shows('?key=KHtest','https://open-the-doors.example.pages.dev'); ok(r['stamp'], 'and still lets an invited person in')
print('\n%d checks, %d failed'%(n,fails)); sys.exit(1 if fails else 0)
