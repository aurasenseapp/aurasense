"""Build 168 · the Mirror's two places, walked inside the Mirror page in a real browser with a pretend helper. Test-only."""
import sys, os, shutil, json
sys.path.insert(0, '/home/claude/scripts')
from harness import *
shutil.copy('/home/claude/aurasense/mirror-living.html', TEST + '/mirror-living.html')
fails = []
def check(name, ok, detail=''):
    print(('PASS ' if ok else 'FAIL ') + name + ('' if ok else '  -> ' + str(detail)[:400]), flush=True)
    if not ok: fails.append(name)
YES = "try{localStorage.setItem('as_mirror_listener','claude')}catch(e){}"
KEPT = "try{localStorage.setItem('as_reminding',JSON.stringify([{id:'k1',at:'2026-10-20',moment:'choice',label:'',text:'Sleep on it first.'}]))}catch(e){}"
def helper():
    n = {'i': 0}
    def r(body):
        if body.get('keep'):
            return {'ok': True, 'by': 'claude', 'keep': {'found': 'You found “slow”.', 'step': 'A walk on Sunday.', 'wiser': 'Slow is allowed.'}}
        n['i'] += 1
        return {'ok': True, 'by': 'claude', 'reflect': '“Turn %d”, you said.' % n['i'], 'question': 'What else is here, %d?' % n['i'], 'aspire': '', 'care': False, 'ground': False}
    return r
def live(init=YES, w_=390, h_=760):
    api = Api('live', [helper()]); api.replies = [helper()] * 30
    w = Walk(w_, h_, mobile=True, api=api, init=init); w.open(); return w
def until(w, js, ms=12000):
    try: w.page.wait_for_function(js, timeout=ms); return True
    except Exception: return False
def speak_has(w, t, ms=14000): return until(w, "() => document.getElementById('speak').innerText.includes(%s)" % json.dumps(t), ms)
def doors(w, sel='#doors'): return w.js("s=>[...document.querySelectorAll(s+' button')].filter(b=>b.offsetParent!==null).map(b=>b.innerText.replace(/\\s+/g,' ').trim())", sel)
def tpd(w): return doors(w, '#tpDoors')
def ink(w): return w.js("""() => { const c=document.querySelector('.tpfx'); if(!c||!c.width) return 0; const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data; let n=0; for(let i=3;i<d.length;i+=16) if(d[i]>40) n++; return n; }""")
def kept(w): return w.js("JSON.parse(localStorage.getItem('as_reminding')||'[]')")
def begin(w): w.click_text('#doors button', 'Something else'); w.page.wait_for_timeout(3000)
def let_go(w, words):
    w.js("t=>{document.getElementById('tpWords').value=t;}", words); w.click_text('#tpDoors button', 'It’s written')
    ok = until(w, "() => !!document.getElementById('tpCrumple')", 6000) and until(w, "() => document.getElementById('tpGuide').innerText.includes('Here it is')", 4000)
    if not ok: return 'no paper'
    w.page.wait_for_timeout(900); n = ink(w)
    w.js("document.getElementById('tpCrumple').click()")
    if not until(w, "() => !!document.getElementById('tpThrow')", 15000): return 'no throw'
    w.js("document.getElementById('tpThrow').click()")
    if not speak_has(w, 'Gone.', 15000): return 'not gone'
    return n

# A · the quiet way in from the Mirror's opening, and back
w = live()
check('A: the opening offers a quiet way in', w.visible('tpRow') and 'A thought that keeps coming back? →' in w.js("document.getElementById('tpRow').innerText"), w.js("document.getElementById('tpRow').outerHTML"))
check('A: with nothing kept, no "What I’ve kept"', not w.visible('tpKept'), '')
w.js("document.getElementById('tpEnter').click()"); w.page.wait_for_timeout(1800)
check('A: the two places, unalike, and the Mirror’s own choices step aside', w.visible('tpLet') and w.visible('tpKeep') and not w.visible('doors') and not w.visible('tpRow') and not w.visible('note') and w.visible('tpNote'), [tpd(w), w.visible('doors')])
check('A: the circle asks the question', 'A thought that keeps coming back?' in w.speak(), w.speak())
w.shot('168_A_home', full=False)
w.click_text('#tpDoors button', 'Back to the Mirror'); w.page.wait_for_timeout(2000)
check('A: back to the Mirror: its doors, its words, the way in again', w.visible('doors') and 'The Mirror' in w.speak() and w.visible('tpRow') and not w.visible('tpGuide') and not w.visible('tpNote') and w.visible('note'), [w.speak(), doors(w)])
# B · let a thought go, from the opening
w.js("document.getElementById('tpEnter').click()"); w.page.wait_for_timeout(1600); w.js("document.getElementById('tpLet').click()"); w.page.wait_for_timeout(1800)
check('B: before writing, it says what will happen', 'It will leave your hand, and it can leave your mind too.' in w.speak(), w.speak())
n = let_go(w, 'I always mess everything up')
check('B: written, drawn on paper, crumpled, the breath, thrown, gone', isinstance(n, int) and n > 400, n)
check('B: the real-paper line follows', until(w, "() => document.getElementById('tpGuide').innerText.includes('If you have paper nearby')", 4000), '')
check('B: the words never sit in the page as text, and are not kept', 'mess everything up' not in w.page.content() and kept(w) == [], '')
w.shot('168_B_gone')
w.click_text('#tpDoors button', 'Done'); w.page.wait_for_timeout(2200)
check('B: done: back to the Mirror’s opening', w.visible('doors') and 'The Mirror' in w.speak() and w.visible('tpRow'), w.speak())
# I · the Mirror is unchanged after a visit: a conversation still works
begin(w); w.say('the hills feel alive')
check('I: after a visit, a conversation works as before', '“Turn 1”, you said.' in w.speak() and not w.visible('tpRow') and w.visible('say'), w.speak())
check('A–I: no page errors', not w.errors, w.errors[:3])
w.close()

# C · a circling thought: the ending offers only Let a thought go
w = live(); begin(w)
w.say('I keep thinking about what I said to her'); w.say('over and over, every night')
w.js("document.getElementById('rest').click()"); w.page.wait_for_timeout(2200)
d = doors(w)
check('C: a circling thought: the ending offers Let a thought go, and not the sealed keeping', 'Let a thought go' in d and 'Keep something for when it’s needed' not in d, d)
w.shot('168_C_rest')
w.click_text('#doors button', 'Let a thought go'); w.page.wait_for_timeout(1800)
check('C: it opens straight to writing the thought', w.visible('tpSay') and 'What’s the thought?' in w.speak(), w.speak())
n = let_go(w, 'what I said to her')
check('C: let go, the whole way', isinstance(n, int), n)
w.click_text('#tpDoors button', 'Done')
check('C: done: the Mirror’s own ending, and a way to begin again', speak_has(w, 'You let a thought go.', 6000) and speak_has(w, 'One step closer to your own light.', 4000) and 'Begin again' in w.js("document.getElementById('after').innerText"), w.speak())
check('C: no page errors', not w.errors, w.errors[:3])
w.close()

# D · a conversation with something found: Keep what I found, then Seal it for when it's needed
w = live(); begin(w)
w.say('the hills feel alive'); w.say('they ask me to slow down')
w.js("document.getElementById('rest').click()"); w.page.wait_for_timeout(2200)
d = doors(w)
check('D: something found: Keep what I found; no second keeping door', 'Keep what I found' in d and 'Keep something for when it’s needed' not in d and 'Let a thought go' not in d, d)
w.click_text('#doors button', 'Keep what I found'); w.page.wait_for_timeout(3500)
check('D: the keepsake can be sealed for its moment', 'Seal it for when it’s needed' in w.js("document.getElementById('after').innerText"), w.js("document.getElementById('after').innerText"))
w.click_text('#after button', 'Seal it for when it’s needed'); w.page.wait_for_timeout(2000)
check('D: what was found, and its step, ask when they should come back', 'You found “slow”. My step: A walk on Sunday.' in w.speak() and 'When should it come back to you?' in w.speak(), w.speak())
w.click_text('#tpDoors button', 'A big choice')
check('D: folded into an envelope, waiting to be sealed', until(w, "() => !!document.getElementById('tpSeal')", 9000), tpd(w))
w.js("document.getElementById('tpSeal').click()")
check('D: sealed', speak_has(w, 'Sealed, for a big choice.', 9000), w.speak())
k = kept(w)
check('D: kept on this device only, with its moment', len(k) == 1 and k[0]['moment'] == 'choice' and 'slow' in k[0]['text'], k)
w.click_text('#tpDoors button', 'Done')
check('D: done: the Mirror’s own ending', speak_has(w, 'You sealed something for when it’s needed.', 6000), w.speak())
check('D: no page errors', not w.errors, w.errors[:3])
w.close()

# E · the written rules (no helper): the ending offers the sealed keeping; Back returns to the ending
w = Walk(390, 760, mobile=True); w.open(); begin(w)
w.say('I feel heavy today'); w.say('it is like a weight on my chest'); w.say('maybe it is work')
w.js("document.getElementById('rest').click()"); w.page.wait_for_timeout(2200)
d = doors(w)
check('E: the written rules: the ending offers Keep something for when it’s needed', 'Keep something for when it’s needed' in d and 'Let a thought go' not in d, d)
w.click_text('#doors button', 'Keep something for when it’s needed'); w.page.wait_for_timeout(1800)
check('E: it asks what to keep', w.visible('tpSay') and 'What would you like to keep' in w.speak(), w.speak())
w.click_text('#tpDoors button', 'Back'); w.page.wait_for_timeout(2200)
check('E: Back returns to the ending, as it was', 'A question to carry' in doors(w) and not w.visible('tpSay') and not w.visible('tpGuide'), doors(w))
check('E: no page errors', not w.errors, w.errors[:3])
w.close()

# F · in a conversation, a matching moment is offered quietly, once
w = live(init=YES + KEPT)
check('F: the opening shows what is kept', w.visible('tpKept') and 'What I’ve kept (1)' in w.js("document.getElementById('tpRow').innerText"), '')
begin(w); w.say('I have to decide whether to take the job')
check('F: a quiet offer, beside the conversation, never in place of it', w.visible('tpPeek') and 'You kept something for moments like this.' in w.js("document.getElementById('tpPeek').innerText") and '“Turn 1”, you said.' in w.speak(), w.js("document.getElementById('tpPeek').innerText"))
check('F: nothing is shown until asked', 'Sleep on it first.' not in w.page.content(), '')
w.click_text('#tpPeek button', 'See it'); w.page.wait_for_timeout(400)
check('F: shown when asked', 'Sleep on it first.' in w.js("document.getElementById('tpPeek').innerText"), w.js("document.getElementById('tpPeek').innerText"))
w.click_text('#tpPeek button', 'Close'); w.page.wait_for_timeout(300)
w.say('which option should I choose')
check('F: offered only once in a conversation', not w.visible('tpPeek'), '')
check('F: no page errors', not w.errors, w.errors[:3])
w.close()

# G · heavy words, inside the two places, from the ending
w = live(); begin(w)
w.say('I keep thinking it was my fault'); w.say('round and round')
w.js("document.getElementById('rest').click()"); w.page.wait_for_timeout(2200)
w.click_text('#doors button', 'Let a thought go'); w.page.wait_for_timeout(1800)
w.js("()=>{document.getElementById('tpWords').value='some days I want to die';}"); w.click_text('#tpDoors button', 'It’s written')
check('G: heavy words: real help first, never the fire', speak_has(w, '988', 6000) and ink(w) < 50 and not w.visible('tpDoors'), w.speak())
check('G: and a way to begin again', 'Begin again' in w.js("document.getElementById('after').innerText"), w.js("document.getElementById('after').innerText"))
sw = w.js('[document.documentElement.scrollWidth, innerWidth]')
check('G: nothing scrolls sideways', sw[0] <= sw[1], sw)
check('G: no page errors', not w.errors, w.errors[:3])
w.close()

print('\n%d failed' % len(fails), fails)
sys.exit(1 if fails else 0)
