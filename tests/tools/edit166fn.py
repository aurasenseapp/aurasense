"""Build 166 · the Mirror's listener (25 Oct 2026): the signed self-test, made to survive the web reader.
After Build 165 went live, every signed test address was refused, though the same addresses opened the door when
checked here. The likeliest cause: the web reader Claude uses quietly drops address parts with names like "sig"
(as it already drops "ref"). Now the time and the signature travel under plain names, "at" and "seal", and a
refused request that asks "why=1" is told only the names of the parts that arrived, so the next fault is seen,
not guessed. Nothing else changes; the private key stays in Claude's workspace.
Always starts from the live 165 helper; re-runnable."""
import io

SRC = '/home/claude/work/mirror.165.js'
DST = '/home/claude/aurasense/functions/api/mirror.js'
s = io.open(SRC, encoding='utf-8').read()

def rep(old, new, label, count=1):
    global s
    c = s.count(old)
    assert c == count, (label, c)
    s = s.replace(old, new)
    print('ok', label)

rep("""/* ═══ THE MIRROR'S LISTENER · Build 165 · 23 October 2026 · Karl with Claude""",
    """/* ═══ THE MIRROR'S LISTENER · Build 166 · 25 October 2026 · Karl with Claude""", 'title')
rep("""   key never leaves the workspace where Claude tests, so no key ever appears in a message or a web address.
""", """   key never leaves the workspace where Claude tests, so no key ever appears in a message or a web address.
   Build 166: the signed self-test's time and signature travel as "at" and "seal" (the web reader drops some names).
""", 'note 166')
rep("""   GET /api/mirror?selftest=1&ts=SECONDS&branch=BRANCH&suite=NAME[&model=…][&only=…][&turns=1-6][&budget=seconds][&later=1]&sig=SIGNATURE
   GET /api/mirror?selftest=1&ts=SECONDS&job=NUMBER&sig=SIGNATURE   (what a background run found; "running" until done)
   Build 165 · the signature covers every other part of the address (sorted, as name=value, joined by "&").
""", """   GET /api/mirror?selftest=1&at=SECONDS&branch=BRANCH&suite=NAME[&model=…][&only=…][&turns=1-6][&budget=seconds][&later=1]&seal=SIGNATURE
   GET /api/mirror?selftest=1&at=SECONDS&job=NUMBER&seal=SIGNATURE   (what a background run found; "running" until done)
   The signature covers every other part of the address (sorted, as name=value, joined by "&").
   Build 166 · "at" and "seal" (Build 165's "ts" and "sig" are still understood). Add why=1 to a refused request to
   be told only which names arrived: never why a signature failed, and nothing else.
""", 'how it is asked')
rep("""    const sig = url.searchParams.get('sig') || '', ts = Number(url.searchParams.get('ts') || '');""",
    """    const seal = url.searchParams.has('seal') ? 'seal' : 'sig', sig = url.searchParams.get(seal) || '';   /* Build 166 */
    const ts = Number(url.searchParams.get(url.searchParams.has('at') ? 'at' : 'ts') || '');""", 'plain names')
rep("""    for (const [k, v] of url.searchParams) if (k !== 'sig') parts.push(k + '=' + v);""",
    """    for (const [k, v] of url.searchParams) if (k !== seal) parts.push(k + '=' + v);""", 'the signed parts')
rep("""    if (!/^[A-Za-z0-9_-]{86}$/.test(sig) || !Number.isInteger(ts)) return false;
    const now = Math.floor(Date.now() / 1000);
    if (ts > now + 60 || now - ts > SELFTEST_FOR) return false;""",
    """    if (!/^[A-Za-z0-9_-]{86}$/.test(sig) || !Number.isInteger(ts)) { lastWhy = 'shape'; return false; }
    const now = Math.floor(Date.now() / 1000);
    if (ts > now + 60 || now - ts > SELFTEST_FOR) { lastWhy = 'time'; return false; }""", 'reason: shape, time')
rep("""    if (raw.length !== 64) return false;
    const key = await crypto.subtle.importKey('jwk', SELFTEST_KEY, { name: 'ECDSA', namedCurve: 'P-256' }, false, ['verify']);
    return await crypto.subtle.verify({ name: 'ECDSA', hash: 'SHA-256' }, key, raw, new TextEncoder().encode(parts.join('&')));
  } catch (e) { return false; }""",
    """    if (raw.length !== 64) { lastWhy = 'shape'; return false; }
    const key = await crypto.subtle.importKey('jwk', SELFTEST_KEY, { name: 'ECDSA', namedCurve: 'P-256' }, false, ['verify']);
    const ok = await crypto.subtle.verify({ name: 'ECDSA', hash: 'SHA-256' }, key, raw, new TextEncoder().encode(parts.join('&')));
    lastWhy = ok ? '' : 'nomatch';
    return ok;
  } catch (e) { lastWhy = 'threw'; return false; }""", 'reason: nomatch, threw')
rep("""/* Build 165 · is this request signed, recently, for exactly what it asks? */
async function signedOk(url) {""", """/* Build 165 · is this request signed, recently, for exactly what it asks? */
let lastWhy = '';   /* Build 166 · a plain reason for why=1 only: shape, time, nomatch or threw (none helps anyone forge one) */
async function signedOk(url) {
  lastWhy = '';""", 'reason holder')
rep("""  if (!(await signedOk(url))) return reply({ ok: false, code: 'elsewhere' }, 403);   /* Build 165 · the old key opens nothing now */""",
    """  if (!(await signedOk(url))) {   /* Build 165 · the old key opens nothing now */
    if (url.searchParams.get('why') === '1') {   /* Build 166 · only the names that arrived, so a dropped part can be seen */
      const heard = [...new Set([...url.searchParams.keys()])].filter((k) => /^[a-z]{1,12}$/.test(k)).sort().slice(0, 20);
      return reply({ ok: false, code: 'elsewhere', heard, why: lastWhy || 'names' }, 200);
    }
    return reply({ ok: false, code: 'elsewhere' }, 403);
  }""", 'why=1')
io.open(DST, 'w', encoding='utf-8').write(s)
print('written', DST, len(s))

def edit(src, dst, old, new, label):
    t = io.open(src, encoding='utf-8').read()
    assert t.count(old) == 1, (label, t.count(old))
    io.open(dst, 'w', encoding='utf-8').write(t.replace(old, new)); print('ok', label)
edit('/home/claude/work/index-mapbox.165.html', '/home/claude/aurasense/index-mapbox.html',
     'Build <span class="bs-l">23 Oct 2026 · </span>165<span class="bs-l"> · tap to refresh</span>',
     'Build <span class="bs-l">25 Oct 2026 · </span>166<span class="bs-l"> · tap to refresh</span>', 'map stamp')
edit('/home/claude/work/seeking.165.html', '/home/claude/aurasense/seeking.html',
     '>Build 23 Oct 2026 &middot; 165', '>Build 25 Oct 2026 &middot; 166', 'seeking stamp')
