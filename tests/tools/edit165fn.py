"""Build 165 · the Mirror's listener (23 Oct 2026): the private self-test opens only with a signed, short-lived request.
On 23 October a safety guard (rightly) stopped Claude printing the old self-test key into the conversation. Karl:
"Yes to safer ways..." Now the self-test is opened by a signature that lasts ten minutes and fits only the exact
test it was made for. The private half of the signing key never leaves the workspace where Claude tests; only the
public half lives here. The old key is retired: its fingerprint is gone, so it opens nothing.
Always starts from the live 164 helper; re-runnable."""
import io

SRC = '/home/claude/work/mirror.164.js'
DST = '/home/claude/aurasense/functions/api/mirror.js'
s = io.open(SRC, encoding='utf-8').read()

def rep(old, new, label, count=1):
    global s
    c = s.count(old)
    assert c == count, (label, c)
    s = s.replace(old, new)
    print('ok', label)

rep("""/* ═══ THE MIRROR'S LISTENER · Build 164 · 23 October 2026 · Karl with Claude""",
    """/* ═══ THE MIRROR'S LISTENER · Build 165 · 23 October 2026 · Karl with Claude""", 'title')
rep("""   lessons of 23 Oct: the light named plainly; feelings in layers; relief that returns is not failure; the body.
""", """   lessons of 23 Oct: the light named plainly; feelings in layers; relief that returns is not failure; the body.
   Build 165: the private self-test opens only with a signed request that lasts ten minutes. The private half of its
   key never leaves the workspace where Claude tests, so no key ever appears in a message or a web address.
""", 'note 165')

rep("""/* the self-test: only someone holding the key whose fingerprint this is can run it. It runs fixed test
   conversations kept in this project's own repository, and costs a few cents a run. */
const SELFTEST = '58f9202e82e563c20fed3650a565c3ba76cdb410880afa610271de183c38745d';
""", """/* the self-test: it runs fixed test conversations kept in this project's own repository, and costs a few cents a run.
   Build 165 · it opens only for a request signed with the private half of this key, made in the last ten minutes,
   for exactly this test. Only the public half lives here: it can check a signature, never make one. A signature
   seen by anyone else opens nothing after ten minutes, and nothing but the same test before then. */
const SELFTEST_KEY = { kty: 'EC', crv: 'P-256', x: 'VOmSZRoj94shYzw17Rp7ko_x8cZyfSqqWFde-UUcUZA', y: '8RVlrfWkvAZJgHpLkxp_fJuurGCrSJxo8ajD_7eC8XM' };
const SELFTEST_FOR = 600;   /* seconds a signature lasts */
""", 'the public half of the key')

rep("""   GET /api/mirror?selftest=KEY&branch=BRANCH&suite=NAME[&model=…][&only=…][&turns=1-6][&budget=seconds][&later=1]
   GET /api/mirror?selftest=KEY&job=NUMBER   (what a background run found; "running" until it is done)
""", """   GET /api/mirror?selftest=1&ts=SECONDS&branch=BRANCH&suite=NAME[&model=…][&only=…][&turns=1-6][&budget=seconds][&later=1]&sig=SIGNATURE
   GET /api/mirror?selftest=1&ts=SECONDS&job=NUMBER&sig=SIGNATURE   (what a background run found; "running" until done)
   Build 165 · the signature covers every other part of the address (sorted, as name=value, joined by "&").
""", 'how it is asked')

rep("""const jobAt = (url, id) => new Request(new URL('/__mirror_selftest/' + id, url).toString());
async function selftest(url, env, context) {
  if ((await sha256(url.searchParams.get('selftest'))) !== SELFTEST) return reply({ ok: false, code: 'elsewhere' }, 403);
""", """const jobAt = (url, id) => new Request(new URL('/__mirror_selftest/' + id, url).toString());
/* Build 165 · is this request signed, recently, for exactly what it asks? */
async function signedOk(url) {
  try {
    const sig = url.searchParams.get('sig') || '', ts = Number(url.searchParams.get('ts') || '');
    if (!/^[A-Za-z0-9_-]{86}$/.test(sig) || !Number.isInteger(ts)) return false;
    const now = Math.floor(Date.now() / 1000);
    if (ts > now + 60 || now - ts > SELFTEST_FOR) return false;
    const parts = [];
    for (const [k, v] of url.searchParams) if (k !== 'sig') parts.push(k + '=' + v);
    parts.sort();
    const raw = Uint8Array.from(atob(sig.replace(/-/g, '+').replace(/_/g, '/') + '=='), (c) => c.charCodeAt(0));
    if (raw.length !== 64) return false;
    const key = await crypto.subtle.importKey('jwk', SELFTEST_KEY, { name: 'ECDSA', namedCurve: 'P-256' }, false, ['verify']);
    return await crypto.subtle.verify({ name: 'ECDSA', hash: 'SHA-256' }, key, raw, new TextEncoder().encode(parts.join('&')));
  } catch (e) { return false; }
}
async function selftest(url, env, context) {
  if (!(await signedOk(url))) return reply({ ok: false, code: 'elsewhere' }, 403);   /* Build 165 · the old key opens nothing now */
""", 'the signed door')

assert 'SELFTEST =' not in s and "'58f9202e" not in s
io.open(DST, 'w', encoding='utf-8').write(s)
print('written', DST, len(s))
