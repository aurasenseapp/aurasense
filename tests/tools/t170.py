"""Build 170 · launch readiness, walked in a real browser. Test-only: never part of the real site.
A · the Mirror: 18 and over said and confirmed once; heavy words typed with an iPhone's curly apostrophe go to help
B · the map's classic Mirror and readings: the one list; a second heavy reading is never silence; easy to tap
C · the guiding light's first hint steps aside when a page opens"""
import sys, os, io, json, shutil
sys.path.insert(0, '/home/claude/scripts')
from harness import *
from mapwalk import mapwalk
fails = []
def check(name, ok, detail=''):
    print(('PASS ' if ok else 'FAIL ') + name + ('' if ok else '  -> ' + str(detail)[:400]), flush=True)
    if not ok: fails.append(name)
def until(w, js, ms=8000):
    try: w.page.wait_for_function(js, timeout=ms); return True
    except Exception: return False
def helper():
    n = {'i': 0}
    def r(body):
        n['i'] += 1
        return {'ok': True, 'by': 'claude', 'reflect': '“Turn %d”, you said.' % n['i'], 'question': 'What else is here, %d?' % n['i'], 'aspire': '', 'care': False, 'ground': False}
    return r
shutil.copy('/home/claude/aurasense/mirror-living.html', TEST + '/mirror-living.html')
io.open(TEST + '/privacy.html', 'w').write('<!doctype html><title>privacy</title>')
LABELS = "[...document.querySelectorAll('#lsAsk button')].map(b=>b.textContent).join('|')"

# A1 · first time: the age is said and confirmed once, with the choice of Claude
api = Api('live', [helper()]); api.replies = [helper()] * 10
w = Walk(390, 760, mobile=True, api=api); w.open()
w.click_text('#doors button', 'Something else'); w.page.wait_for_timeout(2600)
labs = w.js(LABELS)
why = w.js("(document.querySelector('#lsAsk .ask-why')||{}).textContent||''")
check('A1: the first choice says 18 or over, in the button itself', labs == 'I’m 18 or over · Begin with Claude|Not now', labs)
check('A1: and in plain words beneath', why.startswith('The Mirror is for people 18 and over. Claude reads your words only'), why)
w.shot('170_A1_consent', full=False)
w.click_text('#lsAsk button', 'I’m 18 or over · Begin with Claude'); w.page.wait_for_timeout(1500)
check('A1: the answer is kept on this device, as the one answer for all of Aurasense', w.js("localStorage.getItem('as_age18')") == '1' and w.js("localStorage.getItem('as_mirror_listener')") == 'claude')
w.say('the hills feel alive')
check('A1: and Claude listens', len(api.posts) == 1 and '“Turn 1”, you said.' in w.speak(), [len(api.posts), w.speak()])
nc = w.js("(()=>{const n=document.getElementById('note');const c=getComputedStyle(n).color;return c;})()")
check('A1: the note (an AI, not a therapist) is in the readable colour', nc in ('rgb(111, 90, 108)',), nc)
check('A1: no page errors', not w.errors, w.errors[:3])
w.close()

# A2 · someone already 18 or over (from the map): the plain choice
api = Api('live', [helper()])
w = Walk(390, 760, mobile=True, api=api, init="try{localStorage.setItem('as_age18','1')}catch(e){}"); w.open()
w.click_text('#doors button', 'Something else'); w.page.wait_for_timeout(2600)
check('A2: already answered: the plain choice, and no age line', w.js(LABELS) == 'Begin with Claude|Not now' and not w.js("(document.querySelector('#lsAsk .ask-why')||{}).textContent||''").startswith('The Mirror is for people 18'), w.js(LABELS))
w.close()

# A3 · Not now, then after all: still says 18 or over, and is kept once chosen
api = Api('live', [helper()])
w = Walk(390, 760, mobile=True, api=api); w.open()
w.click_text('#doors button', 'Something else'); w.page.wait_for_timeout(2600)
w.click_text('#lsAsk button', 'Not now'); w.page.wait_for_timeout(1500)
check('A3: after Not now, the way back in says 18 or over too', w.js(LABELS) == 'I’m 18 or over · Begin with Claude', w.js(LABELS))
w.click_text('#lsAsk button', 'I’m 18 or over · Begin with Claude'); w.page.wait_for_timeout(1500)
check('A3: chosen after all: kept', w.js("localStorage.getItem('as_age18')") == '1' and w.js("localStorage.getItem('as_mirror_listener')") == 'claude')
w.close()

# A4 · heavy words typed on an iPhone (curly apostrophe, and the new ways of saying it) never reach Claude
for said in ['I don’t want to wake up anymore', 'I wish I was dead', 'they would all be better off without me', 'I just want to end it.']:
    api = Api('live', [helper()])
    w = Walk(390, 760, mobile=True, api=api, init="try{localStorage.setItem('as_mirror_listener','claude');localStorage.setItem('as_age18','1')}catch(e){}"); w.open()
    w.click_text('#doors button', 'Something else'); w.page.wait_for_timeout(2600)
    w.say(said, 2500)
    check('A4: "%s": real help, and nothing sent' % said, '988' in w.speak() and len(api.posts) == 0, [w.speak()[:120], len(api.posts)])
    w.close()

# B · the map page
w = mapwalk(skip_seek=True, init="try{localStorage.setItem('as_age18','1');localStorage.setItem('as_gl_seen','1')}catch(e){}")
w.page.wait_for_timeout(800)
w.js("__t.mirrorOpenClassic()"); w.page.wait_for_timeout(1500)
for said in ['I don’t want to live anymore', 'I wish I was dead', 'I want to end it and be done']:
    w.js("t=>{const b=document.getElementById('mr-bring');b.value=t;document.getElementById('mr-ask').click();}", said); w.page.wait_for_timeout(1400)
    out = w.js("(document.getElementById('mr-said')||document.getElementById('mr-modal')).innerText.replace(/\\s+/g,' ')")
    check('B1: the classic Mirror meets "%s" with a way to a person, never a question about it' % said, 'deserves a person' in out and 'first hour' not in out, out[:200])
w.shot('170_B1_classic', full=False)
w.js("()=>{const m=document.getElementById('mr-modal');if(m)m.remove();const b=document.getElementById('mr-back');if(b)b.remove();}"); w.page.wait_for_timeout(400)
# readings: the answer words and the small lights
w.js("__t.openQuestPage()"); w.page.wait_for_timeout(1200)
w.js("document.querySelector('#qz-menu .qz-card').click()"); w.page.wait_for_timeout(1500)
fs = w.js("parseFloat(getComputedStyle(document.querySelector('#qz-active .qzc-answers .qz-dot')).fontSize)")
check('B2: the answer words are 12.5px or larger (13px above phone width)', fs >= 12.5, fs)
hit = w.js("""(()=>{const b=document.querySelectorAll('#qz-active .qzc-trail button')[2];const r=b.getBoundingClientRect();
  const e=document.elementFromPoint(r.left+r.width/2, r.top+r.height/2+10);return e===b;})()""")
check('B2: a step-light answers a fingertip 10px below its centre', hit, '')
w.js("document.querySelectorAll('#qz-active .qzc-answers .qz-dot')[2].click()"); w.page.wait_for_timeout(1300)
bk = w.js("(()=>{const r=document.querySelector('#qz-active .qzc-back').getBoundingClientRect();return Math.round(r.height);})()")
check('B2: "the one before" is easy to tap (44px)', bk >= 44, bk)
w.shot('170_B2_reading', full=False)
# heavy twice within the fortnight
def heavy_reading(qid):
    i = w.js("id=>__t.QUESTS.findIndex(q=>q.id===id)", qid)
    w.js("i=>__t.qzOpen(i)", i); w.page.wait_for_timeout(1100)
    for _ in range(12):
        if w.js("!!document.querySelector('#qz-active.qzc-complete')"): break
        w.js("document.querySelectorAll('#qz-active .qzc-answers .qz-dot')[4].click()"); w.page.wait_for_timeout(1250)
    w.js("document.getElementById('qz-submit').click()")
    return until(w, "() => !!document.getElementById('as-heavy') && document.getElementById('as-heavy').classList.contains('on')", 6000)
check('B3: a heavy reading shows the way to a person', heavy_reading('phq') and 'That reading came back heavy.' in w.js("document.getElementById('as-heavy').innerText") and '988' in w.js("document.getElementById('as-heavy').innerText"))
w.js("document.querySelector('#as-heavy .ah-x').click()"); w.page.wait_for_timeout(9500)
check('B3: a second heavy reading within the fortnight is never met with silence', heavy_reading('gad') and 'came back heavy again' in w.js("document.getElementById('as-heavy').innerText") and '988' in w.js("document.getElementById('as-heavy').innerText"), w.js("(document.getElementById('as-heavy')||{innerText:'(none)'}).innerText"))
w.shot('170_B3_again', full=False)
w.js("document.querySelector('#as-heavy .ah-x').click()"); w.page.wait_for_timeout(1000)
w.js("try{__t.closeQuest()}catch(e){}"); w.page.wait_for_timeout(9000)
# the guide's close
w.js("__t.raOpen()"); w.page.wait_for_timeout(1500)
gx = w.js("Math.round(document.getElementById('ra-x').getBoundingClientRect().height)")
check('B4: "close the guide" is easy to tap (32px or more)', gx >= 32, gx)
gm = w.js("(()=>{const r=document.getElementById('ra-modal').getBoundingClientRect();return [Math.round(r.top),Math.round(r.bottom),innerHeight];})()")
check('B4: the guide still fits the screen', gm[0] >= 0 and gm[1] <= gm[2], gm)
for _ in range(6): w.js("document.getElementById('ra-next').click()"); w.page.wait_for_timeout(900)
gm = w.js("(()=>{const r=document.getElementById('ra-modal').getBoundingClientRect();return [Math.round(r.top),Math.round(r.bottom),innerHeight];})()")
check('B4: its tallest page (7) still fits the screen', gm[0] >= 0 and gm[1] <= gm[2], gm)
tt = w.js("(()=>{const b=document.getElementById('ra-body');const h=b.querySelector('.ra-h')||b.firstElementChild;const rb=b.getBoundingClientRect(),rh=h.getBoundingClientRect();return [Math.round(rh.top),Math.round(rb.top),h.textContent.slice(0,30)];})()")
check('B4: its first line is whole, below the heading (not cut off)', tt[0] >= tt[1] - 1, tt)
w.shot('170_B4_guide7', full=False)
check('B: no page errors', not w.errors, w.errors[:3])
w.close()

# C · the guiding light's first hint steps aside when a page opens
w = mapwalk(skip_seek=True, init="try{localStorage.setItem('as_age18','1')}catch(e){}")
ok = until(w, "() => { const h=document.getElementById('mv-hint'); return h && h.classList.contains('show'); }", 9000)
check('C: the first hint speaks', ok)
w.js("__t.openRegister()")
gone = until(w, "() => { const h=document.getElementById('mv-hint'); return !h || !h.classList.contains('show'); }", 2500)
check('C: and steps aside the moment a page opens', gone)
check('C: it will speak another day (not marked as seen)', w.js("localStorage.getItem('as_gl_seen')") != '1')
check('C: no page errors', not w.errors, w.errors[:3])
w.close()

print('\n%d failed' % len(fails), fails)
sys.exit(1 if fails else 0)
