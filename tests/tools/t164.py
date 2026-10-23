"""Build 164 · Keep what you found, walked in a real browser with a pretend helper. Test-only."""
import sys, io, os, shutil, json
sys.path.insert(0, '/home/claude/scripts')
from harness import *
shutil.copy('/home/claude/aurasense/mirror-living.html', TEST + '/mirror-living.html')
fails = []
def check(name, ok, detail=''):
    print(('PASS ' if ok else 'FAIL ') + name + ('' if ok else '  -> ' + str(detail)[:500]), flush=True)
    if not ok: fails.append(name)
YES = "try{localStorage.setItem('as_mirror_listener','claude')}catch(e){}"
KEEP = {'found': 'The hills feel “alive”, and they ask you “to slow down”.', 'step': 'Walk up there on Sunday morning.', 'wiser': 'Slow is allowed. Your own light was never in a hurry.'}
def helper(keepreply=None):
    n = {'i': 0}
    def r(body):
        if body.get('keep'):
            return dict(keepreply) if keepreply is not None else {'ok': True, 'by': 'claude', 'keep': KEEP}
        n['i'] += 1
        return {'ok': True, 'by': 'claude', 'reflect': '“Turn %d”, you said.' % n['i'], 'question': 'What else is here, %d?' % n['i'], 'aspire': '', 'care': False, 'ground': False}
    return r
FAR = """(()=>{const m=document.getElementById('mirror').getBoundingClientRect(),cx=m.left+m.width/2,cy=m.top+m.height/2,R=m.width/2;
  let far=0;const tw=document.createTreeWalker(document.getElementById('speak'),NodeFilter.SHOW_TEXT,null);let n;const rg=document.createRange();
  while((n=tw.nextNode())){if(!n.nodeValue.trim()||n.parentNode.offsetParent===null)continue;rg.selectNodeContents(n);
    for(const b of rg.getClientRects()){const dx=Math.max(Math.abs(b.left-cx),Math.abs(b.right-cx)),dy=Math.max(Math.abs(b.top-cy),Math.abs(b.bottom-cy));far=Math.max(far,Math.hypot(dx,dy)/R);}}
  return +far.toFixed(3);})()"""
def converse(w, n=3):
    w.click_text('#doors button', 'Something else'); w.page.wait_for_timeout(3000)
    for i in range(n): w.say('the hills feel alive, part %d' % i)
def rest(w):
    w.js("document.getElementById('rest').click()"); w.page.wait_for_timeout(3000)
def doors(w): return w.js("[...document.querySelectorAll('#doors button')].map(b=>b.textContent).join('|')")
def after(w): return w.js("[...document.querySelectorAll('#after button')].map(b=>b.textContent).join('|')")
def note(w): return w.js("document.getElementById('note').textContent")

# A · keep what I found, on two phone sizes
for W_, H_, tag in [(390, 664, 'phone'), (360, 640, 'small phone')]:
    api = Api('live', [helper()]); api.replies = [helper()] * 20
    w = Walk(W_, H_, mobile=True, api=api, init=YES); w.open()
    converse(w); rest(w)
    check(tag + ': A: after Claude listened, the ending offers "Keep what I found"', 'Keep what I found' in doors(w), doors(w))
    w.click_text('#doors button', 'Keep what I found'); w.page.wait_for_timeout(4200)
    kp = api.posts[-1]
    check(tag + ': A: the keepsake is asked for once, with the conversation, and no new words', kp.get('keep') is True and 'words' not in kp and any(t['role'] == 'user' for t in kp['turns']), kp)
    sp = w.speak()
    check(tag + ': A: what they found, their step, and the wiser self\'s last word are shown', 'What you found:' in sp and KEEP['found'] in sp and 'Your step:' in sp and KEEP['step'] in sp and '“Slow is allowed. Your own light was never in a hurry.”' in sp and 'One step closer to your own light.' in sp, sp)
    check(tag + ': A: said plainly who gathered it', w.who() == 'Gathered by Claude, an AI, from your conversation.', w.who())
    check(tag + ': A: Keep it on this device, Copy it, Begin again', after(w).startswith('Keep it on this device|Copy it|Begin again'), after(w))
    check(tag + ': A: the note says it stays on this device only, and who could see it', 'Kept only on this device, and only if you choose. Aurasense keeps nothing. Anyone using this device could see it.' == w.js("(document.getElementById('keepnote')||{}).textContent||''"))
    far = w.js(FAR)
    check(tag + ': A: all of it sits inside the circle (%.3f of the radius)' % far, far <= 0.9, far)
    check(tag + ': A: nothing kept until they choose', w.js("localStorage.getItem('as_mirror_thread')") is None)
    w.shot('164_keepsake_' + tag.replace(' ', ''))
    w.click_text('#after button', 'Keep it on this device'); w.page.wait_for_timeout(400)
    th = json.loads(w.js("localStorage.getItem('as_mirror_thread')") or '[]')
    check(tag + ': A: kept, on this device', len(th) == 1 and th[0]['found'] == KEEP['found'] and th[0]['step'] == KEEP['step'] and th[0]['wiser'] == KEEP['wiser'] and len(th[0]['at']) == 10, th)
    check(tag + ': A: said plainly, and the button rests', w.who() == 'Kept on this device only. Your thread now holds 1 line.' and 'Kept|' in after(w), (w.who(), after(w)))
    check(tag + ': A: "Your thread (1)" appears beneath', 'Your thread (1)' in note(w), note(w))
    w.click_text('#after button', 'Kept'); w.page.wait_for_timeout(200)
    check(tag + ': A: a second tap keeps nothing twice', len(json.loads(w.js("localStorage.getItem('as_mirror_thread')"))) == 1)
    w.click_text('#after button', 'Copy it'); w.page.wait_for_timeout(600)
    check(tag + ': A: copy says what happened, either way', w.who() in ('Copied. Paste it wherever you keep things.', 'Your browser didn’t allow copying. You can select the words in the circle instead.'), w.who())
    check(tag + ': A: no page errors', not w.errors, w.errors[:3])
    w.close()

# B · the thread, next visit: shown newest first; forget all of it takes two taps
api = Api('live', [helper()]); api.replies = [helper()] * 20
seed = YES + "try{localStorage.setItem('as_mirror_thread',JSON.stringify([{at:'2026-10-20',found:'An older find.',step:'',wiser:'Older word.'},{at:'2026-10-23',found:'The newest find.',step:'A small step.',wiser:'Newest word.'}]))}catch(e){}"
w = Walk(390, 664, mobile=True, api=api, init=seed); w.open()
check('B: "Your thread (2)" beneath the Mirror on a new visit', 'Your thread (2)' in note(w), note(w))
w.click_text('#note button', 'Your thread (2)'); w.page.wait_for_timeout(500)
tt = w.js("document.getElementById('thread').innerText")
check('B: the thread shows, newest first, with what it is', w.visible('thread') and tt.index('The newest find.') < tt.index('An older find.') and 'Your thread of light' in tt and 'Kept on this device only. Aurasense keeps nothing.' in tt and '“Newest word.”' in tt and 'Your step: A small step.' in tt and '2026-10-23' not in tt and '2026' in tt, tt)
w.shot('164_thread')
w.click_text('#thread button', 'Forget all of it'); w.page.wait_for_timeout(200)
check('B: forgetting asks for a second tap', w.js("localStorage.getItem('as_mirror_thread')") is not None and 'Tap again to forget all 2' in w.js("document.getElementById('thread').innerText"))
w.click_text('#thread button', 'Tap again to forget all 2'); w.page.wait_for_timeout(300)
check('B: then all of it is forgotten, and said so', w.js("localStorage.getItem('as_mirror_thread')") is None and not w.visible('thread') and w.who() == 'Forgotten. Nothing from the Mirror is kept on this device now.' and 'Your thread' not in note(w), (w.who(), note(w)))
check('B: no page errors', not w.errors, w.errors[:3])
w.close()

# C · Claude can't gather it: their own words, as before, said plainly
api = Api('live', []); api.replies = [helper({'ok': False, 'code': 'upstream', '_status': 503})] * 20
w = Walk(390, 664, mobile=True, api=api, init=YES); w.open()
converse(w); rest(w)
w.click_text('#doors button', 'Keep what I found'); w.page.wait_for_timeout(4200)
check('C: if Claude can\'t gather it, their own words are shown', 'In your own words:' in w.speak() and w.who() == 'Claude couldn’t gather it just then, so here are your own words.' and 'Keep it on this device' not in after(w), (w.speak()[:160], w.who()))
check('C: no page errors', not w.errors, w.errors[:3])
w.close()

# D · heavy words in the conversation: never sent to keep; the old way only
api = Api('live', []); api.replies = [helper()] * 20
w = Walk(390, 664, mobile=True, api=api, init=YES); w.open()
converse(w, 2); w.say('I want to die some days'); w.page.wait_for_timeout(500)
n0 = len(api.posts)
rest(w)
check('D: after heavy words, no keepsake is offered', 'Keep what I found' not in doors(w) and 'What I found, in my own words' in doors(w), doors(w))
w.click_text('#doors button', 'What I found, in my own words'); w.page.wait_for_timeout(3200)
check('D: and nothing more is sent', len(api.posts) == n0, (n0, len(api.posts)))
w.close()

# E · only one Claude reply, or the written rules (no helper): the old way, nothing sent
api = Api('live', []); api.replies = [helper()] * 20
w = Walk(390, 664, mobile=True, api=api, init=YES); w.open()
converse(w, 1); rest(w)
check('E: after a single reply, the old ending (not enough to keep)', 'What I found, in my own words' in doors(w) and 'Keep what I found' not in doors(w), doors(w))
w.close()
api = Api('absent'); w = Walk(390, 664, mobile=True, api=api); w.open()
converse(w, 3); rest(w)
check('E: no helper: the old ending, nothing sent', 'What I found, in my own words' in doors(w) and len(api.posts) == 0, doors(w))
w.close()

# F · inside the map's frame: keeping works there too
api = Api('live', []); api.replies = [helper()] * 20
w = Walk(390, 664, mobile=True, api=api, init=YES); w.open('test-host.html', wait=3600)
frm = [f for f in w.page.frames if f.url.endswith('mirror-living.html?in=site')][0]
frm.evaluate("document.getElementById('send').click()"); w.page.wait_for_timeout(4200)
for i in range(2):
    frm.evaluate("t=>{const a=document.getElementById('words');a.value=t;document.getElementById('send').click();}", 'more words %d' % i); w.page.wait_for_timeout(4200)
frm.evaluate("document.getElementById('rest').click()"); w.page.wait_for_timeout(3000)
frm.evaluate("[...document.querySelectorAll('#doors button')].find(b=>b.textContent==='Keep what I found').click()"); w.page.wait_for_timeout(4200)
frm.evaluate("[...document.querySelectorAll('#after button')].find(b=>b.textContent==='Keep it on this device').click()"); w.page.wait_for_timeout(400)
check('F: inside the map, kept on this device', len(json.loads(frm.evaluate("localStorage.getItem('as_mirror_thread')") or '[]')) == 1)
check('F: no page errors', not w.errors, w.errors[:3])
w.close()
print('\n%d failed' % len(fails), fails)
