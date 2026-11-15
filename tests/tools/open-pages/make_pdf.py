import sys, asyncio
from playwright.async_api import async_playwright
src, out = sys.argv[1], sys.argv[2]
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto("file://" + src)
        await pg.wait_for_timeout(400)
        # overflow check: any page whose content is taller than the sheet
        over = await pg.evaluate("""() => [...document.querySelectorAll('.page')].map((s,i)=>{
            const r=s.getBoundingClientRect(); let maxb=0;
            s.querySelectorAll('*').forEach(el=>{ if(el.closest('.foot')) return; const rr=el.getBoundingClientRect(); if(rr.height>0) maxb=Math.max(maxb, rr.bottom-r.top); });
            const foot=s.querySelector('.foot'); const ft = foot? foot.getBoundingClientRect().top - r.top : r.height;
            return {page:i+1, contentBottom:Math.round(maxb), footTop:Math.round(ft), height:Math.round(r.height)};
        })""")
        await pg.pdf(path=out, format="Letter", print_background=True, margin={"top":"0","right":"0","bottom":"0","left":"0"})
        await b.close()
        print("errors:", errs)
        for o in over: print(o, "OVERLAP" if o["contentBottom"] > o["footTop"] - 4 else "ok")
asyncio.run(main())
