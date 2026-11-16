# -*- coding: utf-8 -*-
"""Build 180 · the new Mirror joined to the map. Test-only: never part of the real site.
A · the Mirror page inside a pretend map: what it sends, what it listens to, the open place for the third
B · the real map page (with a stand-in map library): a sense lands softened, named by its area; the Mirror waits"""
import io, os, re, sys, json, shutil
sys.path.insert(0, '/home/claude/scripts')
from playwright.sync_api import sync_playwright
SITE = '/home/claude/aurasense'
SHOTS = '/home/claude/work/shots/180'; os.makedirs(SHOTS, exist_ok=True)
fails = []; passes = 0
def ok(cond, what, detail=''):
    global passes
    if cond: passes += 1
    else: fails.append(what); print('FAIL ' + what + ('  -> ' + str(detail)[:500] if detail != '' else ''), flush=True)

# ── 0 · the files ──
src = io.open(SITE + '/mirror.html', encoding='utf-8').read()
mp = io.open(SITE + '/index-mapbox.html', encoding='utf-8').read()
ok(len(re.findall(r'innerHTML', src)) == 1 and not re.search(r'__T=|__t\b|sk-ant|harvey', src, flags=re.I), 'the Mirror page: still one checked place for markup, no test hooks, first name only')
ok(not re.search(r'__T=|window\.__t\b|window\.__m\b', mp) and not re.search(r'sk-ant|harvey', mp, flags=re.I), 'the map: no test hooks, no keys, first name only')
ok("fr.src='/mirror.html?in=site'" in mp and "/mirror-living.html?in=site" not in mp, 'the map opens the new Mirror')
ok(os.path.isfile(SITE + '/mirror-living.html') and 'function mirrorOpenClassic(){' in mp, 'the older Mirrors are kept, not retired')
ok(mp.count("e.origin!==location.origin||e.source!==fr.contentWindow") == 1 and src.count("e.origin!==location.origin||e.source!==window.parent") == 1, 'each side listens only to Aurasense\'s own page, and only to the other')

# ── A · the Mirror page inside a pretend map ──
BASE = 'https://www.aurasense.app'
CT = {'.html': 'text/html; charset=utf-8', '.json': 'application/json', '.txt': 'text/plain; charset=utf-8', '.js': 'application/javascript', '.png': 'image/png'}
HOST = """<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><title>pretend map</title>
<style>html,body{margin:0;height:100%}iframe{position:fixed;inset:0;width:100%;height:100%;border:0}</style>
<iframe id=f src="/mirror.html?in=site" sandbox="allow-scripts allow-same-origin allow-popups allow-popups-to-escape-sandbox"></iframe>
<script>window.got=[];addEventListener('message',function(e){if(e.origin===location.origin&&e.source===document.getElementById('f').contentWindow)got.push(e.data);});
function send(m){document.getElementById('f').contentWindow.postMessage(m,location.origin);}</script>"""
R1 = {'ok': True, 'by': 'claude', 'v': 2, 'reflect': 'An old friend was “on my mind”, and then their song played.', 'learned': 'A thought can feel answered by something outside.', 'aspire': '', 'question': 'What was the song like when it came?', 'ready': True, 'care': False, 'ground': False}
def CLOSE(words, fits='together', working=''):
    return {'ok': True, 'by': 'claude', 'v': 2, 'close': {'sensed': 'A friend “on my mind”, and then their song.', 'words': words, 'fits': fits, 'name': words[0], 'also': words[1] if len(words) > 1 else '', 'working': working, 'learned': 'A thought can feel answered.', 'clear': 'You noticed both.', 'offer': 'A thought of an old friend felt answered by a song in a shop.'}}
class Helper:
    def __init__(self): self.posts = []; self.script = []
    def handle(self, route):
        req = route.request; url = req.url
        if not url.startswith(BASE): route.abort(); return
        path = url[len(BASE):]
        if path.startswith('/host180'): route.fulfill(status=200, content_type='text/html; charset=utf-8', body=HOST); return
        if path.startswith('/api/mirror'):
            if req.method == 'GET': route.fulfill(status=200, content_type='application/json', body=json.dumps({'live': True, 'v': 2, 'listen': True})); return
            self.posts.append(json.loads(req.post_data or '{}'))
            ans = self.script.pop(0) if self.script else dict(R1)
            route.fulfill(status=200, content_type='application/json', body=json.dumps(ans)); return
        p = path.split('?')[0]
        for cand in (p, p + '.html'):
            f = SITE + cand
            if os.path.isfile(f): route.fulfill(status=200, content_type=CT.get(os.path.splitext(f)[1], 'application/octet-stream'), body=open(f, 'rb').read()); return
        route.fulfill(status=404, body='not found')

def to_naming(fr, h, words, fits='together', working=''):
    fr.fill('#words', 'An old friend was on my mind, then their song played in a shop.') if not fr.input_value('#words') else None
    fr.click('#send')
    if fr.locator('#ask').is_visible(): fr.click('#ask button.btn:not(.quiet)')
    fr.wait_for_selector('.reply')
    h.script = [CLOSE(words, fits, working)]
    fr.click('#nameIt'); fr.wait_for_selector('#closeCard')

with sync_playwright() as pw:
    br = pw.chromium.launch(args=['--disable-gpu'])
    for vname, w, hh in [('phone', 390, 844), ('laptop', 1280, 800)]:
        h = Helper()
        ctx = br.new_context(viewport={'width': w, 'height': hh}, device_scale_factor=1, is_mobile=(w < 500), has_touch=(w < 500))
        ctx.route('**/*', h.handle); pg = ctx.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)[:200])); pg.on('console', lambda mm: errs.append(mm.text[:200]) if mm.type == 'error' and 'Failed to load resource' not in mm.text else None)
        pg.goto(BASE + '/host180', wait_until='load'); pg.wait_for_timeout(600)
        fr = [f for f in pg.frames if 'mirror.html' in f.url][0]
        T = 'A ' + vname
        ok(fr.locator('#back').is_visible() and fr.locator('#older').is_visible() and fr.inner_text('#older') == 'Your balance of light', T + ': inside the map, a way back and a way to the older balance view')
        pg.evaluate("send({as:'mirror-host',act:'begin',q:'What do you sense?',a:'An old friend was on my mind, then their song played.'})"); pg.wait_for_timeout(200)
        ok(fr.input_value('#words') == 'An old friend was on my mind, then their song played.' and len(h.posts) == 0, T + ': words from the guiding light wait in the box, unsent')
        to_naming(fr, h, ['Synchronicity', 'Nostalgia'])
        fr.click('.doors3 button:has-text("Offer it to the map")')
        t = fr.inner_text('#close')
        ok('never at your door' in t and fr.locator('#close .row button', has_text='Offer it to the map').count() == 1 and 'Hold it ready' not in t, T + ': the offer card says where it will rest')
        fr.fill('#offer', 'The song at 1420 Main Street answered me.'); fr.click('#close .row button:has-text("Offer it to the map")')
        ok('take out numbers' in fr.inner_text('#close') and pg.evaluate('got.length') == 0, T + ': an address is still refused, and nothing is sent')
        fr.fill('#offer', 'A thought of an old friend felt answered by a song in a shop.'); fr.click('#close .row button:has-text("Offer it to the map")')
        pg.wait_for_timeout(200); got = pg.evaluate('got')
        ok(len(got) == 1 and got[0] == {'as': 'mirror', 'act': 'offer', 'text': 'A thought of an old friend felt answered by a song in a shop.', 'words': ['Synchronicity', 'Nostalgia'], 'fresh': False, 'working': ''}, T + ': only the offered sentence and its symbols go to the map', got)
        ok('Going to the map' in fr.inner_text('#close') and fr.evaluate("localStorage.getItem('as_mirror_offers')") is None, T + ': the conversation waits; nothing is stored')
        pg.evaluate("send({as:'mirror-host',act:'held'})"); pg.wait_for_timeout(200)
        t = fr.inner_text('#close')
        ok('It was not offered. Your sense is still here.' in t and 'Keep it' in t and 'Let it go' in t, T + ': if the map could not take it, the sense is still here with its three doors')
        fr.click('.doors3 button:has-text("Offer it to the map")'); fr.click('#close .row button:has-text("Offer it to the map")'); pg.wait_for_timeout(150)
        pg.evaluate("send({as:'other',act:'fresh'})"); pg.evaluate("send({as:'mirror-host',act:'landed',area:'Sunset Ridge, Cochrane <b>x</b>'})"); pg.wait_for_timeout(250)
        t = fr.inner_text('#close')
        ok('Offered to the map' in t and 'in the area of Sunset Ridge, Cochrane <b>x</b>, with no name' in t and fr.locator('#close b').count() == 0, T + ': landed: told as the area, in plain words (markup is never run)', t)
        ok(fr.locator('#close button', has_text='Carry on with this conversation').count() == 1 and fr.locator('#close button', has_text='Begin a new one').count() == 1, T + ': two choices: the same conversation, or a new one')
        if vname == 'phone': pg.screenshot(path=SHOTS + '/A-landed.png')
        d = fr.evaluate("""() => { const W = document.documentElement.clientWidth, out = []; for (const b of document.querySelectorAll('#close button')) { const r = b.getBoundingClientRect(); if (r.height < 44 || r.right > W + 1) out.push(b.textContent + ' ' + Math.round(r.height)); } return out; }""")
        ok(not d, T + ': the choices are easy to tap and fit the screen', d)
        fr.click('#close button:has-text("Carry on with this conversation")')
        ok(fr.locator('#say').is_visible() and fr.locator('#thread .reply').count() == 1 and not fr.locator('#close').is_visible(), T + ': carry on: the same conversation is there, with the box to write in')
        pg.evaluate("send({as:'mirror-host',act:'landed',area:'x'})"); pg.wait_for_timeout(150)
        ok(not fr.locator('#close').is_visible(), T + ': a stray "landed" with nothing offered changes nothing')
        pg.evaluate("send({as:'mirror-host',act:'fresh'})"); pg.wait_for_timeout(200)
        ok(fr.locator('#thread > *').count() == 0 and fr.locator('#hero').is_visible() and fr.input_value('#words') == '', T + ': begin a new one: a clean start')
        # the open place for the third
        to_naming(fr, h, ['Synchronicity', 'Nostalgia'])
        fr.click('.doors3 button:has-text("Keep it")'); fr.wait_for_selector('text=Begin again')
        kept = json.loads(fr.evaluate("localStorage.getItem('as_mirror_senses')"))
        ok(kept[-1].get('third') == '' and 'An open place is kept beside it, for what the two say together' in fr.inner_text('#close'), T + ': a kept meeting of inner and outer holds an open place for the third')
        fr.click('#close button:has-text("Begin again")')
        to_naming(fr, h, ['Unease', 'Fear'])
        fr.click('.doors3 button:has-text("Keep it")'); fr.wait_for_selector('text=Begin again')
        kept = json.loads(fr.evaluate("localStorage.getItem('as_mirror_senses')"))
        ok('third' not in kept[-1] and 'open place' not in fr.inner_text('#close'), T + ': other senses are kept as before')
        fr.click('#note button:has-text("Your kept senses (2)")')
        ok(fr.locator('#close input[type=text]').count() == 1 and fr.locator('#third0').is_visible() and 'WHAT THE TWO SAY TOGETHER' in fr.inner_text('#close').upper(), T + ': the open place shows beside that kept sense only')
        fr.fill('#third0', 'I want to die'); fr.click('#close .third button:has-text("Keep")'); fr.wait_for_timeout(250)
        kept = json.loads(fr.evaluate("localStorage.getItem('as_mirror_senses')"))
        ok(kept[0]['third'] == '' and '988' in fr.inner_text('main'), T + ': heavy words there go to real help, and are not kept')
        fr.evaluate("document.getElementById('note').querySelector('button') && 0")
        pg.goto(BASE + '/host180', wait_until='load'); pg.wait_for_timeout(500); fr = [f for f in pg.frames if 'mirror.html' in f.url][0]
        fr.click('#note button:has-text("Your kept senses (2)")')
        fr.fill('#third0', 'Both were about  leaving well.'); fr.click('#close .third button:has-text("Keep")'); fr.wait_for_timeout(150)
        kept = json.loads(fr.evaluate("localStorage.getItem('as_mirror_senses')"))
        ok(kept[0]['third'] == 'Both were about leaving well.' and 'Kept on this device only.' in fr.inner_text('#close .third') and len(h.posts) == 6, T + ': the third meaning is kept on the device only; nothing is sent', [kept[0], len(h.posts)])
        if vname == 'phone': pg.screenshot(path=SHOTS + '/A-third.png')
        d = fr.evaluate("""() => { const W = document.documentElement.clientWidth, out = []; for (const b of document.querySelectorAll('#close button, #close input')) { const r = b.getBoundingClientRect(); if (r.height < 44 || r.right > W + 1) out.push((b.textContent || b.id) + ' ' + Math.round(r.height)); } return out; }""")
        ok(not d, T + ': the open place is easy to tap and fits the screen', d)
        fr.click('#older'); pg.wait_for_timeout(150)
        ok(pg.evaluate('got[got.length-1]') == {'as': 'mirror', 'act': 'classic'}, T + ': the older balance view is still one tap away')
        ok(not errs, T + ': no errors on the page', errs)
        ctx.close()
    # standing alone, nothing changes
    h = Helper(); ctx = br.new_context(viewport={'width': 390, 'height': 844}); ctx.route('**/*', h.handle); pg = ctx.new_page()
    pg.goto(BASE + '/mirror', wait_until='load'); pg.wait_for_timeout(300)
    to_naming(pg, h, ['Synchronicity', 'Nostalgia'])
    pg.click('.doors3 button:has-text("Offer it to the map")')
    ok('Hold it ready for the map' in pg.inner_text('#close') and 'never at your door' not in pg.inner_text('#close') and not pg.locator('#older').is_visible() and not pg.locator('#back').is_visible(), 'standing alone, the Mirror page is as it was')
    ctx.close(); br.close()

# ── B · the map ──
from harness import *
from mapwalk import mapwalk
for f in ['mirror.html', 'alphasense.json']: shutil.copy(SITE + '/' + f, TEST + '/' + f)
STUB = """
window.__geo={mode:'ok',lat:51.1894,lng:-114.4668};
try{Object.defineProperty(navigator,'geolocation',{configurable:true,value:{getCurrentPosition:function(a,b){setTimeout(function(){if(window.__geo.mode==='ok')a({coords:{latitude:window.__geo.lat,longitude:window.__geo.lng}});else b({code:1});},60);},watchPosition:function(){return 1;},clearWatch:function(){}}});}catch(e){}
(function(){var of=window.fetch;window.fetch=function(u,o){var s=String(u);
  if(s.indexOf('api.mapbox.com/geocoding')>-1){var body=s.indexOf('types=neighborhood,locality,place')>-1?{features:[{text:'Sunset Ridge',context:[{id:'place.1',text:'Cochrane'}]}]}:{features:[{text:'Riverview Drive',address:'12',place_type:['address'],context:[{id:'place.1',text:'Cochrane'},{id:'country.1',text:'Canada'}]}]};
    return Promise.resolve(new Response(JSON.stringify(body),{status:200,headers:{'content-type':'application/json'}}));}
  return of.apply(this,arguments);};})();
try{localStorage.setItem('as_age18','1');localStorage.setItem('as_gl_seen','1')}catch(e){}
"""
OFFER = "m=>{window.parent.postMessage(m,location.origin);}"
M1 = {'as': 'mirror', 'act': 'offer', 'text': 'A thought of an old friend felt answered by a song in a shop.', 'words': ['Synchronicity', 'Nostalgia'], 'fresh': False, 'working': ''}
HAV = "(a,b,c,d)=>haversine(a,b,c,d)"
for vname, ww, hh in [('phone', 390, 844), ('laptop', 1280, 800)]:
    T = 'B ' + vname
    import mapwalk as MW
    MW.prep(SITE + '/', True)
    t = io.open(TEST + '/index-mapbox.html', encoding='utf-8').read()
    a = '  window.openMyAuraPage = openMyAuraPage;\n'; assert t.count(a) == 1
    t = t.replace(a, a + "  try{window.__m={get auraPoints(){return auraPoints;},get selSense(){return selSense;},get myOfferings(){return myOfferings;},get AREAS(){return AS_MIRROR_AREAS;},mirrorOpen:mirrorOpen,haversine:haversine,reverseAddress:reverseAddress,gateRow:gateRow,showSharedPopup:showSharedPopup,mirrorParse:mirrorParse,mirrorPopLine:mirrorPopLine,mirrorKind:mirrorKind,hookPopup:function(){openPopup=function(a,b,h){window.__pop=h;throw new Error('stand-in');};}};}catch(e){console.error('expose '+e);}\n")
    io.open(TEST + '/index-mapbox.html', 'w', encoding='utf-8').write(t)
    for f in ['mirror.html', 'alphasense.json']: shutil.copy(SITE + '/' + f, TEST + '/' + f)
    fake = io.open('/home/claude/scripts/fakemap.js', encoding='utf-8').read()
    w = Walk(ww, hh, mobile=(ww < 700), init=fake + "\ntry{localStorage.setItem('as_seeking_seen','1')}catch(e){}\n" + STUB)
    w.page.goto(BASE + 'index-mapbox.html', wait_until='domcontentloaded', timeout=60000); w.page.wait_for_timeout(4600)
    n0 = w.js("__m.auraPoints.length"); sel0 = w.js("__m.selSense")
    w.js("__m.mirrorOpen()"); w.page.wait_for_timeout(1500)
    fr = [f for f in w.page.frames if 'mirror.html' in f.url]
    ok(len(fr) == 1 and fr[0].url.endswith('/mirror.html?in=site') and w.js("document.getElementById('as-living-mirror').classList.contains('on')"), T + ': the map opens the new Mirror over itself')
    fr = fr[0]
    ok(fr.inner_text('h1') == 'What are you sensing?' and fr.locator('#back').is_visible(), T + ': and it is the Mirror that asks "What are you sensing?"')
    fr.evaluate("window.__mark=7;window.__heard=[];addEventListener('message',function(e){if(e.data&&e.data.as==='mirror-host')__heard.push(e.data);})")
    fr.evaluate(OFFER, M1); w.page.wait_for_timeout(1400)
    ok(w.js("(()=>{const o=document.getElementById('as-living-mirror');return o.classList.contains('away')&&getComputedStyle(o).visibility==='hidden';})()"), T + ': the Mirror steps aside and waits underneath')
    n1 = w.js("__m.auraPoints.length"); ap = w.js("(()=>{const p=__m.auraPoints[__m.auraPoints.length-1];return {lat:p.lat,lng:p.lng,sense:p.sense,text:p.text,scale:p.scale};})()")
    ok(n1 == n0 + 1 and ap['sense'] == 'synchronicity' and ap['text'] == M1['text'] + ' ✧ Synchronicity + Nostalgia' and ap['scale'] == 'street', T + ': the sense lands once, with its symbols carried in its own words', ap)
    dist = w.js("([a,b,c,d])=>__m.haversine(a,b,c,d)", [ap['lat'], ap['lng'], 51.1894, -114.4668])
    ok((ap['lat'], ap['lng']) != (51.1894, -114.4668) and dist < 1300, T + ': it rests in the area (within about a kilometre), never on the spot the person stood', dist)
    ok(w.js("__m.selSense") == sel0, T + ': the map\'s own chosen sense is left as it was')
    ok(w.js("__m.AREAS.length===1&&__m.AREAS[0].name") == 'Sunset Ridge, Cochrane', T + ': the area is named')
    ra = w.js("([a,b])=>__m.reverseAddress(a,b)", [ap['lat'], ap['lng']]); ra2 = w.js("([a,b])=>__m.reverseAddress(a,b)", [ap['lat'] + 0.02, ap['lng']])
    ok(ra == 'Sunset Ridge, Cochrane' and ra2 == '12 Riverview Drive', T + ': that spot is told as its area, never a house number; other places are told as before', [ra, ra2])
    w.page.wait_for_timeout(600)
    ok(w.js("__m.myOfferings[0].text") == ap['text'] and w.js("__m.myOfferings[0].place") == 'Sunset Ridge, Cochrane', T + ': it joins the person\'s own aura, with the area as its place', w.js("[__m.myOfferings[0].text,__m.myOfferings[0].place]"))
    row = w.js("__m.gateRow({sense:'synchronicity',text:__m.auraPoints[__m.auraPoints.length-1].text,lat:1,lng:2,place:'Sunset Ridge, Cochrane',scale:'street'})")
    ok(sorted(row.keys()) == ['lat', 'lng', 'place', 'priv', 'scale', 'sense', 'session_id', 'text'], T + ': what is stored has the same parts as any offering: nothing new', sorted(row.keys()))
    ok(fr.evaluate("__heard.length===1&&__heard[0].act==='landed'&&__heard[0].area") == 'Sunset Ridge, Cochrane', T + ': the Mirror is told it landed, and where')
    w.page.wait_for_timeout(3600)
    card = w.js("(()=>{const c=document.getElementById('as-mirror-land');if(!c)return null;const r=c.getBoundingClientRect();return {t:c.innerText,on:c.classList.contains('on'),l:r.left,r:r.right,top:r.top,b:[...c.querySelectorAll('button')].map(x=>[x.textContent,Math.round(x.getBoundingClientRect().height),Math.round(x.getBoundingClientRect().right)])};})()")
    ok(card and card['on'] and 'Your sense rests in the area of Sunset Ridge, Cochrane.' in card['t'] and [b[0] for b in card['b']] == ['Back to the Mirror', 'Begin a new one', 'Stay on the map'], T + ': after landing: back to the Mirror, begin a new one, or stay', card)
    ok(card and card['l'] >= 0 and card['r'] <= ww and card['top'] >= 0 and all(b[1] >= 44 and b[2] <= ww for b in card['b']), T + ': the card fits the screen and is easy to tap', card)
    hit = w.js("(()=>{const c=document.getElementById('as-mirror-land'),b=c.querySelector('button'),r=b.getBoundingClientRect(),e=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2);return e===b||b.contains(e);})()")
    ok(hit, T + ': nothing covers the card\'s first button')
    w.shot('180/B-land-' + vname) if os.path.isdir(WORK + '/shots/180') else None
    w.js("document.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',bubbles:true}));window.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape'}))"); w.page.wait_for_timeout(700)
    ok(w.js("!!document.getElementById('as-living-mirror')"), T + ': Escape on the map does not throw the waiting conversation away')
    w.click_text('#as-mirror-land button', 'Back to the Mirror'); w.page.wait_for_timeout(700)
    ok(w.js("(()=>{const o=document.getElementById('as-living-mirror');return o.classList.contains('on')&&!o.classList.contains('away')&&getComputedStyle(o).visibility==='visible'&&!document.getElementById('as-mirror-land');})()") and fr.evaluate("window.__mark") == 7, T + ': back to the Mirror: the very same page, never reloaded')
    # again, then a new one
    fr.evaluate(OFFER, dict(M1, words=['Unease'], text='A hum in the flat seemed to get into my shoulders.')); w.page.wait_for_timeout(1400)
    ap2 = w.js("(()=>{const p=__m.auraPoints[__m.auraPoints.length-1];return {sense:p.sense,text:p.text};})()")
    ok(ap2 == {'sense': 'intuition', 'text': 'A hum in the flat seemed to get into my shoulders. ✧ Unease'}, T + ': a word the map has no kind for travels under "intuition", with its own symbol', ap2)
    w.js("__m.mirrorOpen()"); w.page.wait_for_timeout(600)
    ok(w.js("document.querySelectorAll('#as-living-mirror').length===1&&document.getElementById('as-living-mirror').classList.contains('on')") and fr.evaluate("window.__mark") == 7, T + ': opening the Mirror from the map while it waits brings back the same conversation')
    fr.evaluate(OFFER, dict(M1, words=[], text='The quiet after the snow.')); w.page.wait_for_timeout(5400)
    ok(w.js("__m.auraPoints[__m.auraPoints.length-1].text") == 'The quiet after the snow.', T + ': with no symbol chosen, the words travel alone')
    w.click_text('#as-mirror-land button', 'Begin a new one'); w.page.wait_for_timeout(700)
    ok(fr.evaluate("__heard[__heard.length-1].act") == 'fresh' and w.js("document.getElementById('as-living-mirror').classList.contains('on')"), T + ': begin a new one: the Mirror comes back and starts clean')
    # refused: a sentence that already carries the star; nothing lands
    n2 = w.js("__m.auraPoints.length")
    fr.evaluate(OFFER, dict(M1, text='Words ✧ Joy')); w.page.wait_for_timeout(900)
    ok(w.js("__m.auraPoints.length") == n2 and fr.evaluate("__heard[__heard.length-1].act") == 'held' and w.js("document.getElementById('as-living-mirror').classList.contains('on')"), T + ': words that try to carry symbols of their own are not offered')
    # no location
    w.js("window.__geo.mode='no'")
    fr.evaluate(OFFER, M1); w.page.wait_for_timeout(900)
    c = w.js("(document.getElementById('as-mirror-land')||{}).innerText||''")
    ok('Your device keeps its place to itself' in c and 'Offer it where the map is looking' in c and w.js("__m.auraPoints.length") == n2, T + ': when the device keeps its place to itself, the person is asked; nothing lands by itself', c)
    w.click_text('#as-mirror-land button', 'Back to the Mirror'); w.page.wait_for_timeout(600)
    ok(fr.evaluate("__heard[__heard.length-1].act") == 'held' and w.js("document.getElementById('as-living-mirror').classList.contains('on')") and w.js("__m.auraPoints.length") == n2, T + ': back to the Mirror: the sense is still held there')
    fr.evaluate(OFFER, M1); w.page.wait_for_timeout(900)
    w.click_text('#as-mirror-land button', 'Offer it where the map is looking'); w.page.wait_for_timeout(1400)
    ap3 = w.js("(()=>{const p=__m.auraPoints[__m.auraPoints.length-1];return {lat:p.lat,lng:p.lng};})()")
    ok(w.js("__m.auraPoints.length") == n2 + 1 and w.js("([a,b,c,d])=>__m.haversine(a,b,c,d)", [ap3['lat'], ap3['lng'], 51.19, -114.47]) < 1300, T + ': or it rests in the area the map is showing')
    # the aura, tapped
    w.js("window.__pop='';__m.hookPopup()")
    w.js("([a,b,t])=>{try{__m.showSharedPopup(a,b,'synchronicity',t,'12 Riverview Drive, Cochrane');}catch(e){}}", [ap['lat'], ap['lng'], ap['text']]); w.page.wait_for_timeout(200)
    pop = w.js("window.__pop")
    ok('pop-mirror' in pop and pop.count('<svg') >= 2 and 'Synchronicity + Nostalgia' in pop and '"A thought of an old friend felt answered by a song in a shop."' in pop and '✧ Synchronicity' not in pop, T + ': tapped, the aura shows its Alphasense symbols and the words alone', pop[:600])
    ok('near Riverview Drive' in pop and '12 Riverview' not in pop, T + ': and its place is told as the street it is near, never a door')
    w.js("([a,b])=>{try{__m.showSharedPopup(a,b,'sound','The bells at noon.','12 Riverview Drive, Cochrane');}catch(e){}}", [ap['lat'] + 0.05, ap['lng']]); w.page.wait_for_timeout(200)
    pop = w.js("window.__pop")
    ok('pop-mirror' not in pop and '12 Riverview Drive' in pop and 'Sound' in pop, T + ': every other aura opens exactly as before')
    pl = w.js("__m.mirrorPopLine(__m.mirrorParse('The hush. ✧ new sense: the hush of first snow (Belonging + Awe)'))")
    ok(pl.count('<svg') == 1 and '“the hush of first snow” · a new sense, near Belonging + Awe' in pl, T + ': a new sense shows one fused symbol and its name', pl[-200:])
    ok(w.js("__m.mirrorParse('x ✧ new sense: <img src=x onerror=1> (Belonging + Awe)')") is not None and '<img' not in w.js("__m.mirrorPopLine(__m.mirrorParse('x ✧ new sense: <img src=x onerror=1> (Belonging + Awe)'))"), T + ': a stranger\'s name for a sense is shown as plain words, never run')
    ok(w.js("__m.mirrorParse('x ✧ Notaword')") is None and w.js("__m.mirrorParse('plain words')") is None and w.js("__m.mirrorParse('x ✧ Joy + Joy + Joy + Joy + Joy')") is None, T + ': only Alphasense\'s own words are ever drawn')
    ok(w.js("[__m.mirrorKind(['Prediction dream']),__m.mirrorKind(['Unease','Joy']),__m.mirrorKind([])]") == ['preddream', 'joy', 'intuition'], T + ': the kind is chosen from the words')
    # the Mirror closed: everything is cleared
    fr.evaluate("window.parent.postMessage({as:'mirror',act:'close'},location.origin)"); w.page.wait_for_timeout(900)
    ok(w.js("!document.getElementById('as-living-mirror')&&!document.getElementById('as-mirror-land')"), T + ': closing the Mirror leaves nothing behind')
    w.js("__m.mirrorOpen()"); w.page.wait_for_timeout(1200)
    fr = [f for f in w.page.frames if 'mirror.html' in f.url][0]
    fr.evaluate("window.parent.postMessage({as:'mirror',act:'classic'},location.origin)"); w.page.wait_for_timeout(1400)
    ok(w.js("!!document.getElementById('mr-modal')&&!document.getElementById('as-living-mirror')"), T + ': the older balance view still opens from the Mirror')
    ok(not w.errors, T + ': no errors on the map', w.errors[:4])
    w.close()

print('\n%d checks passed, %d failed' % (passes, len(fails)))
sys.exit(1 if fails else 0)
