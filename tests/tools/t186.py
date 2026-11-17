# Build 186 · the Seeking, walked at phone size: felt within ten seconds, the waking light on its own dusk, the countdown
# above the finger, the line of honesty at the moment of offering, and no faults.   cd <site>; python3 t186.py
import os,sys,pathlib,io
from playwright.sync_api import sync_playwright
site=os.getcwd(); fails=0; n=0
def ok(c,name):
    global fails,n; n+=1; print(('PASS ' if c else 'FAIL ')+name); fails+=0 if c else 1
src=io.open(site+'/seeking.html',encoding='utf8').read()
ok('qDusk=!document.body.classList.contains(\'night\')' in src and "'38,24,74'" in src, 'by day the light wakes on its own plum dusk')
ok('function qVivid' in src and '(255-c)' not in src[src.index('function qVivid'):src.index('function qA(')], 'each sense keeps its own colour: pushed up, never whitened, never darkened')
ok('The place is shown on the map; who left it is not. People and AI both learn from it, for mutual benefit.' in src and 'href="/about" target="_blank" rel="noopener"' in src, 'the line of honesty sits at the moment of offering, with About one tap away')
ok(src.count('<div class="tiny"')>=1 and '#typed #honest{font-size:15px' in src, 'the line of honesty is 15px, not 12px italic')
with sync_playwright() as p:
    b=p.chromium.launch(); c=b.new_context(viewport={'width':390,'height':844},device_scale_factor=1); pg=c.new_page()
    pg.route('**/*', lambda r: r.continue_() if r.request.url.startswith('file:') else r.abort())
    errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)[:140]))
    pg.goto(pathlib.Path(site+'/seeking.html').as_uri())
    pg.wait_for_timeout(9500)
    ok(pg.evaluate("(()=>{const h=document.getElementById('sHead');if(!h)return false;let o=1,e=h;while(e&&e!==document.body){o*=parseFloat(getComputedStyle(e).opacity);e=e.parentElement}return o>.5})()"), 'felt, and its one line of guidance shown, within ten seconds')
    pg.wait_for_timeout(4000)
    r=pg.evaluate("(()=>{const r=document.getElementById('ringWrap').getBoundingClientRect();return [r.left,r.top,r.width,r.height]})()")
    x=r[0]+r[2]*0.5+30; y=r[1]+r[3]*0.62-20
    pg.mouse.move(x-30,y+20); pg.mouse.down(); pg.mouse.move(x,y,steps=4); pg.wait_for_timeout(1300)
    q=pg.evaluate("(()=>{const n=document.getElementById('qNum'),r=n.getBoundingClientRect(),s=getComputedStyle(n);return {on:n.classList.contains('on'),cy:r.top+r.height/2,fs:parseFloat(s.fontSize),op:s.opacity,col:s.color,cv:document.getElementById('qCanvas').classList.contains('on')}})()")
    ok(q['on'] and q['cv'] and q['fs']>=34 and q['op']=='1' and q['col']=='rgb(255, 255, 255)', 'the countdown is large, white and fully shown while the light wakes')
    ok(q['cy']<y-40, 'the countdown rides above the finger')
    px=pg.evaluate("(()=>{const c=document.getElementById('qCanvas');const x=c.getContext('2d');const d=x.getImageData(Math.round(c.width*0.5),Math.round(c.height*0.16),1,1).data;return [d[0],d[1],d[2],d[3]]})()")
    ok(px[3]>20 and px[2]>px[1], 'a dusk is drawn out past the ring, where no thumb reaches (%s)'%px)
    pg.wait_for_timeout(3600); pg.mouse.up(); pg.wait_for_timeout(5500)
    t=pg.evaluate("(()=>{const h=document.getElementById('honest');const r=h.getBoundingClientRect();let o=1,e=h;while(e&&e!==document.body){o*=parseFloat(getComputedStyle(e).opacity);e=e.parentElement}return {txt:h.textContent,o:o,fs:getComputedStyle(h).fontSize,fits:r.left>=0&&r.right<=innerWidth,sw:document.documentElement.scrollWidth<=innerWidth}})()")
    ok(t['o']>.5 and 'mutual benefit' in t['txt'] and t['fs']=='15px' and t['fits'] and t['sw'], 'after the hold, the placing moment shows the line of honesty, readable and within the screen')
    ok(not errs, 'no faults while walking (%s)'%errs[:2])
    # the Law's question 6: with reduced motion (or Calm Mode) the waking light only swells
    c2=b.new_context(viewport={'width':390,'height':844},device_scale_factor=1,reduced_motion='reduce'); p2=c2.new_page()
    p2.route('**/*', lambda r: r.continue_() if r.request.url.startswith('file:') else r.abort())
    e2=[]; p2.on('pageerror', lambda e: e2.append(str(e)[:140]))
    p2.goto(pathlib.Path(site+'/seeking.html').as_uri()); p2.wait_for_timeout(13500)
    r=p2.evaluate("(()=>{const r=document.getElementById('ringWrap').getBoundingClientRect();return [r.left,r.top,r.width,r.height]})()")
    x=r[0]+r[2]*0.5+30; y=r[1]+r[3]*0.62-20
    p2.mouse.move(x-30,y+20); p2.mouse.down(); p2.mouse.move(x,y,steps=4); p2.wait_for_timeout(2200)
    cq=p2.evaluate("({calm:qCalm,rips:qRips.length,on:document.getElementById('qCanvas').classList.contains('on'),num:document.getElementById('qNum').classList.contains('on')})")
    ok(cq['calm'] and cq['rips']==0 and cq['on'] and cq['num'] and not e2, 'with reduced motion the light still wakes and counts, but sends no ripples and never quickens (%s)'%cq)
    p2.mouse.up(); b.close()
print('\n%d checks, %d failed'%(n,fails)); sys.exit(1 if fails else 0)
