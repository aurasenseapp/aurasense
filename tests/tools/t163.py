"""Build 163 · the Mirror page: the wiser voice's introduction shown once a visit, while Claude still hears it.
Real browser, pretend helper. Test-only."""
import sys, io, os, shutil
sys.path.insert(0, '/home/claude/scripts')
from harness import *
shutil.copy('/home/claude/aurasense/mirror-living.html', TEST + '/mirror-living.html')
fails = []
def check(name, ok, detail=''):
    print(('PASS ' if ok else 'FAIL ') + name + ('' if ok else '  -> ' + str(detail)[:400]), flush=True)
    if not ok: fails.append(name)
CL = lambda refl, q, asp='': {'ok': True, 'by': 'claude', 'reflect': refl, 'question': q, 'aspire': asp, 'care': False, 'ground': False}
W = 'The you who has come through this might say:'
api = Api('live', [CL('“Restless”, you said.', 'Where does it come from?', 'You can rest here.'),
                   CL('“Outside”.', 'What is out there?'),
                   CL('“Quieter”.', 'What changed?', 'The quiet was yours all along.'),
                   CL('“Lighter”.', 'What will you keep?')])
for W_, H_, tag in [(390, 664, 'phone'), (360, 640, 'small phone')]:
    a = Api('live', list(api.replies))
    w = Walk(W_, H_, mobile=True, api=a, init="try{localStorage.setItem('as_mirror_listener','claude')}catch(e){}"); w.open()
    w.click_text('#doors button', 'Something else'); w.page.wait_for_timeout(3000)
    w.say('restless')
    sp1 = w.speak()
    check(tag + ': the first wiser voice comes with its introduction', W in sp1 and '“You can rest here.”' in sp1 and 'Where does it come from?' in sp1, sp1)
    w.say('outside')
    w.say('quieter')
    sp3 = w.speak()
    check(tag + ': the second wiser voice comes alone, its words whole, no introduction', W not in sp3 and '“The quiet was yours all along.”' in sp3 and 'What changed?' in sp3, sp3)
    if tag == 'phone': w.shot('163_second_wiser')
    w.say('lighter')
    last = a.posts[-1]['turns']
    said = [t['content'] for t in last if t['role'] == 'assistant']
    check(tag + ': Claude still hears the introduction both times, so it can count them', sum(1 for t in said if W in t) == 2, said)
    check(tag + ': and the introduction is heard once per wiser voice, never twice', all(t.count(W) <= 1 for t in said), said)
    far = w.js("""(()=>{const m=document.getElementById('mirror').getBoundingClientRect(),cx=m.left+m.width/2,cy=m.top+m.height/2,R=m.width/2;
      let far=0;const tw=document.createTreeWalker(document.getElementById('speak'),NodeFilter.SHOW_TEXT,null);let n;const rg=document.createRange();
      while((n=tw.nextNode())){if(!n.nodeValue.trim()||n.parentNode.offsetParent===null)continue;rg.selectNodeContents(n);
        for(const b of rg.getClientRects()){const dx=Math.max(Math.abs(b.left-cx),Math.abs(b.right-cx)),dy=Math.max(Math.abs(b.top-cy),Math.abs(b.bottom-cy));far=Math.max(far,Math.hypot(dx,dy)/R);}}
      return +far.toFixed(3);})()""")
    check(tag + ': everything sits inside the circle (%.3f of the radius)' % far, far <= 0.9, far)
    check(tag + ': no page errors', not w.errors, w.errors[:3])
    w.close()
print('\n%d failed' % len(fails), fails)
