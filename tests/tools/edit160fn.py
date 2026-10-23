"""Build 160 · the self-test, made able to reach Claude's test branches and to always answer in time (22 Oct 2026).
Found after Build 159: the web reader Claude uses drops an address part named "ref", so every test ran from main;
and longer runs with the larger Claude took longer than the reader waits, so nothing came back at all.
Now: branch= (ref= still works), turns= (how many turns of each conversation), and a time budget (budget=, in
seconds, 25 by default): no new turn starts once it is spent, and the run says it stopped. Anything unexpected comes
back as a plain reason instead of a broken page. The live Mirror is unchanged.
Always starts from the live 159 helper; re-runnable."""
import io

SRC = '/home/claude/work/mirror.159.js'
DST = '/home/claude/aurasense/functions/api/mirror.js'
s = io.open(SRC, encoding='utf-8').read()

def rep(old, new, label, count=1):
    global s
    c = s.count(old)
    assert c == count, (label, c)
    s = s.replace(old, new)
    print('ok', label)

rep("""/* ═══ THE MIRROR'S LISTENER · Build 159 · 22 October 2026 · Karl with Claude""",
    """/* ═══ THE MIRROR'S LISTENER · Build 160 · 22 October 2026 · Karl with Claude""", 'title')

rep("""   is now asked for its reply in a fixed written shape instead, with the thinking setting each one accepts.
""", """   is now asked for its reply in a fixed written shape instead, with the thinking setting each one accepts.
   Build 160: the self-test can reach test branches (branch=), run fewer turns (turns=), and always answers in time.
""", 'note 160')

rep("""async function answer(env, model, charter, msgs, think, how, spare) {
  const t0 = Date.now();
  let v = await ask(env, model, charter, msgs, think, how, WAIT_MS);""",
    """async function answer(env, model, charter, msgs, think, how, spare, wait) {
  const t0 = Date.now();
  let v = await ask(env, model, charter, msgs, think, how, wait || WAIT_MS);""", 'answer wait')

rep("""   GET /api/mirror?selftest=KEY&ref=BRANCH&suite=NAME[&model=…][&only=…]""",
    """   GET /api/mirror?selftest=KEY&branch=BRANCH&suite=NAME[&model=…][&only=…][&turns=1-6][&budget=seconds]""", 'usage note')

rep("""async function selftest(url, env) {
  if ((await sha256(url.searchParams.get('selftest'))) !== SELFTEST) return reply({ ok: false, code: 'elsewhere' }, 403);
  const ref = url.searchParams.get('ref') || 'main', suite = url.searchParams.get('suite') || 'basic';""",
    """async function selftest(url, env) {
  if ((await sha256(url.searchParams.get('selftest'))) !== SELFTEST) return reply({ ok: false, code: 'elsewhere' }, 403);
  try { return await selftestRun(url, env); }
  catch (e) { return reply({ ok: false, code: 'threw', why: String((e && e.message) || e).slice(0, 300) }, 200); }   /* a plain reason, never a broken page */
}
async function selftestRun(url, env) {
  const T0 = Date.now();
  const budget = Math.min(55, Math.max(5, parseInt(url.searchParams.get('budget') || '25', 10) || 25)) * 1000;
  const most = Math.min(6, Math.max(1, parseInt(url.searchParams.get('turns') || '6', 10) || 6));
  /* "branch" because the web reader drops an address part named "ref" */
  const ref = url.searchParams.get('branch') || url.searchParams.get('ref') || 'main', suite = url.searchParams.get('suite') || 'basic';""",
    'selftest wrapper, budget, turns, branch')

rep("""    for (const words of c.said.slice(0, 6)) {
      const msgs = conversation(turns, String(words));
      if (msgs.some((m) => m.role === 'user' && heavy(m.content))) { said.push({ said: words, care: true, by: 'guard' }); break; }
      const v = await answer(env, model, charter, msgs, think, how, spare);""",
    """    for (const words of c.said.slice(0, most)) {
      const left = budget - (Date.now() - T0);
      if (left < 4000) { said.push({ said: words, stopped: 'time' }); break; }   /* no new turn once the time is spent */
      const msgs = conversation(turns, String(words));
      if (msgs.some((m) => m.role === 'user' && heavy(m.content))) { said.push({ said: words, care: true, by: 'guard' }); break; }
      const v = await answer(env, model, charter, msgs, think, how, spare && left > 20000, Math.min(WAIT_MS, left - 1000));""",
    'selftest turn loop')

rep("""  return reply({ ok: true, ref, suite, think, how, spare, charter: charter === CHARTER ? 'live' : spec.charter, results: out }, 200);""",
    """  return reply({ ok: true, ref, suite, think, how, spare, turns: most, ms: Date.now() - T0, charter: charter === CHARTER ? 'live' : spec.charter, results: out }, 200);""",
    'selftest reply')

io.open(DST, 'w', encoding='utf-8').write(s)
print('written', DST, len(s))
