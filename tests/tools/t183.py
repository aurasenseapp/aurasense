# Build 183 · the opening is ready and still closed; the day's tool opens it and nothing else.  cd <site>; python3 t183.py
import io,os,shutil,subprocess,sys,tempfile,pathlib,re
from playwright.sync_api import sync_playwright
site=os.getcwd(); fails=0; n=0
def ok(c,name):
    global fails,n; n+=1; print(('PASS ' if c else 'FAIL ')+name); fails+=0 if c else 1
mp=io.open(site+'/index-mapbox.html',encoding='utf8').read(); fr=io.open(site+'/about.html',encoding='utf8').read(); ix=io.open(site+'/index.html',encoding='utf8').read()
ok('var OPEN = false;\n  if(OPEN) return;' in mp, 'the switch is in the map and says closed')
ok('coming soon' in ix and 'Enter the map' not in ix, 'the first page is still the holding page')
ok('noindex' in fr and 'href="/m"' in fr and 'coming soon' not in fr and '<script' not in fr and 'For people 18 and over' in fr and 'href="/privacy"' in fr and 'Free to sense. Free to share. People and AI, learning from each other, for mutual benefit.' in fr and not os.path.exists(site+'/front.html'), 'the About page waits at /about: Karl\'s sentence, one way in, no scripts, not listed by search yet')
ok('og:description' in mp and 'Free to sense. Free to share.' in mp, 'a search or a shared link shows the sentence')
ok('Codes can take a few minutes, and sometimes land in spam or junk' in mp and 'Many codes are being asked for just now' in mp, 'a kind word waits for slow or busy sign-in codes')
tmp=tempfile.mkdtemp(); 
for f in ('index.html','about.html','index-mapbox.html'): shutil.copy(site+'/'+f,tmp)
def shows(folder, key):
    with sync_playwright() as p:
        b=p.chromium.launch(); pg=b.new_page()
        pg.route('**/*', lambda r: r.continue_() if r.request.url.startswith('file:') else r.abort())
        pg.goto(pathlib.Path(folder+'/index-mapbox.html').as_uri()+key, wait_until='commit'); pg.wait_for_timeout(2500)
        r=pg.evaluate("({stamp:!!document.getElementById('build-stamp'),text:(document.body.innerText||'').slice(0,300)})"); b.close(); return r
r=shows(tmp,''); ok(not r['stamp'], 'closed: a stranger still meets the curtain, and none of the map')
r=shows(tmp,'?key=KHtest'); ok(r['stamp'], 'closed: an invited person still comes in')
out=subprocess.run([sys.executable,'/home/claude/scripts/open_doors.py',tmp],capture_output=True,text=True)
ix2=io.open(tmp+'/index.html',encoding='utf8').read(); mp2=io.open(tmp+'/index-mapbox.html',encoding='utf8').read(); ab2=io.open(tmp+'/about.html',encoding='utf8').read()
ok(out.returncode==0 and 'url=/m' in ix2 and 'coming soon' not in ix2 and 'Free to sense. Free to share.' in ix2 and '<script' not in ix2, 'the day: aurasense.app sends everyone straight on to the Seeking')
ok('noindex' not in ab2 and ab2.replace('<title>About Aurasense</title>','<title>About Aurasense</title>\n<meta name="robots" content="noindex">')==fr, 'the day: the About page may be listed, and is otherwise unchanged')
ok(mp2.replace('var OPEN = true;','var OPEN = false;')==mp, 'the day: one word changes in the map and nothing else')
r=shows(tmp,''); ok(r['stamp'], 'the day: a stranger comes straight in')
shutil.rmtree(tmp)
print('\n%d checks, %d failed'%(n,fails)); sys.exit(1 if fails else 0)
