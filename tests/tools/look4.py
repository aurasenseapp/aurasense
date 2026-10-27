"""Draft 4 look: screenshots of each stage on a phone, plus page errors and frame times. Test-only."""
import os, sys, json
from playwright.sync_api import sync_playwright
SRC='/home/claude/work/out/two-places/the-two-places.html'
OUT='/tmp/claude-0/-home-claude/89e7564b-fd6e-5cd5-8cd5-5383c8af45f8/scratchpad/tp4'
html=('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
      '<style>:root{color-scheme:light}body{margin:0;font:14px system-ui}[hidden]{display:none!important}</style></head><body>'+open(SRC,encoding='utf-8').read()+'</body></html>')
H=os.path.join(OUT,'h.html'); open(H,'w',encoding='utf-8').write(html)
W,Hh,tag=(390,844,'phone') if len(sys.argv)<2 else (1280,800,'laptop')
FT="""() => new Promise(r => { const t=[]; let l=0, n=0; function f(now){ if(l) t.push(now-l); l=now; if(++n<90) requestAnimationFrame(f); else { t.sort((a,b)=>a-b); r({med:t[t.length>>1].toFixed(1), p90:t[Math.floor(t.length*0.9)].toFixed(1)}); } } requestAnimationFrame(f); })"""
with sync_playwright() as pw:
    br=pw.chromium.launch()
    ctx=br.new_context(viewport={'width':W,'height':Hh},device_scale_factor=2 if tag=='phone' else 1,has_touch=(tag=='phone'))
    p=ctx.new_page(); errs=[]
    p.on('pageerror',lambda e: errs.append(str(e))); p.on('console',lambda m: errs.append(m.text) if m.type=='error' else None)
    p.goto('file://'+H); p.wait_for_timeout(700)
    p.click('#tpLet'); p.wait_for_timeout(700)
    p.fill('#tpWords','I always mess everything up'); p.locator('#tpDoors .door',has_text='It’s written').click()
    for i,ms in enumerate([900,700,800]): p.wait_for_timeout(ms); p.screenshot(path=f'{OUT}/{tag}-a{i}-writing.png')
    p.wait_for_function("()=>!!document.getElementById('tpCrumple')",timeout=8000); p.wait_for_timeout(300)
    print('paper frame ms', p.evaluate(FT)); p.screenshot(path=f'{OUT}/{tag}-b-paper.png')
    p.click('#tpCrumple')
    for i,ms in enumerate([800,1300,1300,1300,1300]): p.wait_for_timeout(ms); p.screenshot(path=f'{OUT}/{tag}-c{i}-crumple.png'); print('guide', p.inner_text('#tpGuide').replace('\n',' | '), p.get_attribute('.tpfx','data-p'))
    p.wait_for_function("()=>!!document.getElementById('tpThrow')",timeout=8000); p.wait_for_timeout(500)
    print('ready frame ms', p.evaluate(FT)); p.screenshot(path=f'{OUT}/{tag}-d-ready.png')
    p.click('#tpThrow')
    for i,ms in enumerate([600,700,900,1200,1200,1200,1200,1200]): p.wait_for_timeout(ms); p.screenshot(path=f'{OUT}/{tag}-e{i}-burn.png')
    print('burn frame ms', p.evaluate(FT))
    p.wait_for_function("()=>document.getElementById('speak').innerText.includes('Gone.')",timeout=12000); p.wait_for_timeout(800)
    p.screenshot(path=f'{OUT}/{tag}-f-gone.png')
    print('errors', errs)
    br.close()
