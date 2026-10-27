"""Test-only: walk the map page's interface (not the map itself) with a stand-in map library."""
import sys, shutil, io, os; sys.path.insert(0,'/home/claude/scripts')
from harness import *
EXPOSE = "try{window.__t={openQuestPage:openQuestPage,qzOpen:qzOpen,QUESTS:QUESTS,raOpen:raOpen,openAlphaPage:openAlphaPage,openRegister:openRegister,asAgeAsk:asAgeAsk,asAgeOk:asAgeOk,closeQuest:closeQuest,mirrorOpenClassic:mirrorOpenClassic,get myProfile(){return myProfile;}};}catch(e){console.warn('expose',e.message)}"
def prep(src='/home/claude/aurasense/', skip_seek=False):
    for f in ['index-mapbox.html','gate-config.js','aurasense-trajectory-core.js','mirror-living.html','seeking.html','privacy.html','terms.html']:
        shutil.copy(src+f, TEST+'/'+f)
    # test-only: lend a few inner functions to the test, in the TEST COPY only (never the real file)
    t = io.open(TEST+'/index-mapbox.html', encoding='utf-8').read()
    a = '  window.openMyAuraPage = openMyAuraPage;\n'
    assert t.count(a) == 1
    t = t.replace(a, a + '  ' + EXPOSE + '\n')
    if skip_seek:
        b = 'window.AS_SEEK_ALWAYS=true;'; assert t.count(b) == 1; t = t.replace(b, 'window.AS_SEEK_ALWAYS=false;')
    io.open(TEST+'/index-mapbox.html', 'w', encoding='utf-8').write(t)
def mapwalk(w_=390, h_=844, init='', src='/home/claude/aurasense/', skip_seek=False):
    prep(src, skip_seek)
    if skip_seek: init = "try{localStorage.setItem('as_seeking_seen','1')}catch(e){}\n" + init
    fake = io.open('/home/claude/scripts/fakemap.js', encoding='utf-8').read()
    w = Walk(w_, h_, mobile=(w_ < 700), init=fake + '\n' + init)
    w.page.goto(BASE + 'index-mapbox.html', wait_until='domcontentloaded', timeout=60000)
    w.page.wait_for_timeout(4000)
    return w
