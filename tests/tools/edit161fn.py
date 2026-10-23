"""Build 161 · the self-test can run a whole conversation in the background (22 Oct 2026).
Found after Build 160: the web reader Claude uses gives up after about ten seconds, and a whole six-turn
conversation with the larger Claude takes fifteen to twenty. Now "later=1" starts the run, answers at once with a
job number, and keeps going in the background (Cloudflare allows about thirty seconds); "job=<number>" then reads
what Claude said, kept for half an hour in the nearest Cloudflare store. Without "later", a run now stops by itself
after nine seconds. The live Mirror is unchanged.
Always starts from the live 160 helper; re-runnable."""
import io

SRC = '/home/claude/work/mirror.160.js'
DST = '/home/claude/aurasense/functions/api/mirror.js'
s = io.open(SRC, encoding='utf-8').read()

def rep(old, new, label, count=1):
    global s
    c = s.count(old)
    assert c == count, (label, c)
    s = s.replace(old, new)
    print('ok', label)

rep("""/* ═══ THE MIRROR'S LISTENER · Build 160 · 22 October 2026 · Karl with Claude""",
    """/* ═══ THE MIRROR'S LISTENER · Build 161 · 22 October 2026 · Karl with Claude""", 'title')
rep("""   Build 160: the self-test can reach test branches (branch=), run fewer turns (turns=), and always answers in time.
""", """   Build 160: the self-test can reach test branches (branch=), run fewer turns (turns=), and always answers in time.
   Build 161: the self-test can run whole conversations in the background (later=1, then job=).
""", 'note 161')

rep("""   GET /api/mirror?selftest=KEY&branch=BRANCH&suite=NAME[&model=…][&only=…][&turns=1-6][&budget=seconds]""",
    """   GET /api/mirror?selftest=KEY&branch=BRANCH&suite=NAME[&model=…][&only=…][&turns=1-6][&budget=seconds][&later=1]
   GET /api/mirror?selftest=KEY&job=NUMBER   (what a background run found; "running" until it is done)""", 'usage note')

rep("""async function selftest(url, env) {
  if ((await sha256(url.searchParams.get('selftest'))) !== SELFTEST) return reply({ ok: false, code: 'elsewhere' }, 403);
  try { return await selftestRun(url, env); }
  catch (e) { return reply({ ok: false, code: 'threw', why: String((e && e.message) || e).slice(0, 300) }, 200); }   /* a plain reason, never a broken page */
}
async function selftestRun(url, env) {
  const T0 = Date.now();
  const budget = Math.min(55, Math.max(5, parseInt(url.searchParams.get('budget') || '25', 10) || 25)) * 1000;""",
    """const jobAt = (url, id) => new Request(new URL('/__mirror_selftest/' + id, url).toString());
async function selftest(url, env, context) {
  if ((await sha256(url.searchParams.get('selftest'))) !== SELFTEST) return reply({ ok: false, code: 'elsewhere' }, 403);
  const store = typeof caches !== 'undefined' && caches.default ? caches.default : null;
  const job = url.searchParams.get('job');
  if (job) {   /* what a background run found */
    if (!/^[a-f0-9]{24}$/.test(job)) return reply({ ok: false, code: 'bad' }, 400);
    const hit = store ? await store.match(jobAt(url, job)) : null;
    return hit ? new Response(await hit.text(), { status: 200, headers: headers() }) : reply({ ok: false, code: 'running', job }, 200);
  }
  if (url.searchParams.get('later') === '1' && store && context && typeof context.waitUntil === 'function') {
    const id = [...crypto.getRandomValues(new Uint8Array(12))].map((b) => b.toString(16).padStart(2, '0')).join('');
    context.waitUntil((async () => {
      let r;
      try { r = await selftestRun(url, env, true); }
      catch (e) { r = reply({ ok: false, code: 'threw', why: String((e && e.message) || e).slice(0, 300) }, 200); }
      await store.put(jobAt(url, id), new Response(await r.text(), { headers: { 'Content-Type': 'application/json', 'Cache-Control': 'max-age=1800' } }));
    })());
    return reply({ ok: true, job: id, later: true }, 200);
  }
  try { return await selftestRun(url, env, false); }
  catch (e) { return reply({ ok: false, code: 'threw', why: String((e && e.message) || e).slice(0, 300) }, 200); }   /* a plain reason, never a broken page */
}
async function selftestRun(url, env, later) {
  const T0 = Date.now();
  /* the web reader waits about ten seconds; a background run may take nearly thirty */
  const budget = Math.min(later ? 28 : 55, Math.max(5, parseInt(url.searchParams.get('budget') || (later ? '28' : '9'), 10) || 9)) * 1000;""",
    'background runs')

rep("""    if (live && request.method === 'GET' && url.searchParams.has('selftest')) return selftest(url, env);""",
    """    if (live && request.method === 'GET' && url.searchParams.has('selftest')) return selftest(url, env, context);""", 'context passed')

rep("""    const w = await ask(env, SPARE, charter, msgs, 'off', 'tool', 20000);""",
    """    const w = await ask(env, SPARE, charter, msgs, 'off', 'tool', Math.min(20000, Math.max(3000, (wait || WAIT_MS) - (Date.now() - t0))));   /* never past the time it was given */""", 'spare within its time')
rep("""spare && left > 20000, Math.min(WAIT_MS, left - 1000));""", """spare && left > 6000, Math.min(WAIT_MS, left - 1000));""", 'selftest spare when time allows')

io.open(DST, 'w', encoding='utf-8').write(s)
print('written', DST, len(s))
