"""Build 159 · the Mirror's listener (22 Oct 2026).
Build 158 asked Sonnet 5.5 with a forced tool call. Sonnet 5.5 and Opus 5.5 refuse forced tool calls on every request
(a 400), so every live reply failed. Only Haiku 5.5 accepted it. Now every model is asked for its reply in a fixed
written shape (structured output), with the thinking setting each model accepts, and the self-test shows the real
reason when something fails (the self-test only; the page still gets one plain word).
Always starts from the live 158 file; re-runnable."""
import io

SRC = '/home/claude/work/mirror.158.js'
DST = '/home/claude/aurasense/functions/api/mirror.js'
s = io.open(SRC, encoding='utf-8').read()

def rep(old, new, label, count=1):
    global s
    c = s.count(old)
    assert c == count, (label, c)
    s = s.replace(old, new)
    print('ok', label)

rep("""/* ═══ THE MIRROR'S LISTENER · Build 158 · 22 October 2026 · Karl with Claude""",
    """/* ═══ THE MIRROR'S LISTENER · Build 159 · 22 October 2026 · Karl with Claude""", 'title')

rep("""   private self-test, so Claude can be heard on test conversations before Karl ever has to test it himself.
""", """   private self-test, so Claude can be heard on test conversations before Karl ever has to test it himself.

   Build 159: the larger Claudes refuse to be forced into a tool, so Build 158's live replies all failed. Every Claude
   is now asked for its reply in a fixed written shape instead, with the thinking setting each one accepts.
""", 'note 159')

rep("""const MODEL = 'claude-sonnet-5-5';   /* Build 158 · from Haiku 5.5. About 4 cents a whole conversation, with the charter kept warm */""",
    """const MODEL = 'claude-sonnet-5-5';   /* Build 158 · from Haiku 5.5. About 4 cents a whole conversation, with the charter kept warm */
const THINK = 'off';                 /* Build 159 · how much Claude thinks before it answers: off, low, medium or high */""", 'THINK')

rep("""'Always answer by using the mirror_reply tool, exactly once. Inside your text, use curly quotation marks (“ ” ‘ ’), never straight double quotes.'""",
    """'Answer exactly once, in the reply shape you are given. Inside your text, use curly quotation marks (“ ” ‘ ’), never straight double quotes.'""", 'charter last line')

rep("""const TOOL = {
  name: 'mirror_reply',
  description: 'Your reply to the person in the Mirror.',
  input_schema: {
    type: 'object',""", """/* Build 159 · the reply's fixed shape (structured output): Sonnet 5.5 and Opus 5.5 refuse a forced tool */
const SHAPE = {
  type: 'json_schema',
  schema: {
    type: 'object',
    additionalProperties: false,""", 'shape head')
rep("""    required: ['heard', 'question', 'care', 'ground']
  }
};""", """    required: ['heard', 'question', 'care', 'ground']
  }
};
/* what each Claude accepts: "off" is the least thinking each one allows (Opus 5.5 always thinks a little) */
function thinking(model, think) {
  if (think === 'low' || think === 'medium' || think === 'high') return { max: 4000, cfg: { output_config: { effort: think } } };
  if (model === 'claude-sonnet-5-5') return { max: 900, cfg: { thinking: { type: 'between_tools' } } };
  if (model === 'claude-haiku-5-5') return { max: 900, cfg: { thinking: { type: 'disabled' } } };
  return { max: 4000, cfg: { output_config: { effort: 'low' } } };
}""", 'shape tail and thinking')

rep("""async function ask(env, model, charter, msgs) {""", """async function ask(env, model, charter, msgs, think) {""", 'ask signature')
rep("""  const t0 = Date.now();
  let res;
  try {
    res = await fetch(API, {
      method: 'POST',
      headers: { 'content-type': 'application/json', 'x-api-key': env.ANTHROPIC_API_KEY, 'anthropic-version': '2023-06-01' },
      body: JSON.stringify({ model: model, max_tokens: 700, system: system, messages: msgs, tools: [TOOL], tool_choice: { type: 'tool', name: 'mirror_reply' } }),
      signal: ctl.signal
    });""", """  const t0 = Date.now();
  const th = thinking(model, think || THINK);
  const body = { model: model, max_tokens: th.max, system: system, messages: msgs };
  if (th.cfg.thinking) body.thinking = th.cfg.thinking;
  body.output_config = Object.assign({ format: SHAPE }, th.cfg.output_config || {});
  let res;
  try {
    res = await fetch(API, {
      method: 'POST',
      headers: { 'content-type': 'application/json', 'x-api-key': env.ANTHROPIC_API_KEY, 'anthropic-version': '2023-06-01' },
      body: JSON.stringify(body),
      signal: ctl.signal
    });""", 'ask body')
rep("""    return { ok: false, code: e && e.name === 'AbortError' ? 'slow' : 'upstream', status: 504 };""",
    """    return { ok: false, code: e && e.name === 'AbortError' ? 'slow' : 'upstream', status: 504, detail: String(e && e.name || 'fetch') };""", 'ask catch')
rep("""    return { ok: false, code: why(res.status, msg), status: 503 };
  }
  if (j && j.stop_reason === 'refusal') return { ok: false, code: 'refused', status: 200 };
  const use = j && Array.isArray(j.content) ? j.content.find((b) => b && b.type === 'tool_use' && b.name === 'mirror_reply') : null;
  const v = use && use.input && typeof use.input === 'object' ? use.input : null;
  if (!v) return { ok: false, code: 'jumbled', status: 200 };""",
    """    return { ok: false, code: why(res.status, msg), status: 503, detail: res.status + ' ' + msg.slice(0, 300) };   /* the detail reaches the self-test only */
  }
  if (j && j.stop_reason === 'refusal') return { ok: false, code: 'refused', status: 200, detail: 'refusal' };
  if (j && j.stop_reason === 'max_tokens') return { ok: false, code: 'upstream', status: 200, detail: 'max_tokens ' + JSON.stringify(j.usage || {}) };
  const texts = j && Array.isArray(j.content) ? j.content.filter((b) => b && b.type === 'text' && typeof b.text === 'string').map((b) => b.text) : [];
  let v = null;
  for (let i = texts.length - 1; i >= 0 && !v; i--) { try { const p = JSON.parse(texts[i]); if (p && typeof p === 'object') v = p; } catch (e) { /* not the reply */ } }
  if (!v) return { ok: false, code: 'jumbled', status: 200, detail: 'no reply shape: ' + (j ? String(j.stop_reason) + ' ' + JSON.stringify(j.content || []).slice(0, 200) : 'no body') };""", 'ask parse')

# the self-test: the thinking setting can be chosen, and the real reason is shown
rep("""  const want = url.searchParams.get('model'), only = url.searchParams.get('only');""",
    """  const want = url.searchParams.get('model'), only = url.searchParams.get('only');
  const think = /^(?:off|low|medium|high)$/.test(url.searchParams.get('think') || '') ? url.searchParams.get('think') : THINK;""", 'selftest think')
rep("""      const v = await ask(env, model, charter, msgs);
      if (!v.ok) { said.push({ said: words, error: v.code }); break; }
      said.push({ said: words, heard: v.reflect, wiser: v.aspire || undefined, question: v.question, care: v.care || undefined, ms: v.ms });""",
    """      const v = await ask(env, model, charter, msgs, think);
      if (!v.ok) { said.push({ said: words, error: v.code, detail: v.detail }); break; }
      said.push({ said: words, heard: v.reflect, wiser: v.aspire || undefined, question: v.question, care: v.care || undefined, ground: v.ground || undefined, ms: v.ms, out: v.usage ? v.usage.output_tokens : undefined });""", 'selftest turn')
rep("""  return reply({ ok: true, ref, suite, charter: charter === CHARTER ? 'live' : spec.charter, results: out }, 200);""",
    """  return reply({ ok: true, ref, suite, think, charter: charter === CHARTER ? 'live' : spec.charter, results: out }, 200);""", 'selftest reply')


# ── the safety net: if the main Claude can't answer, Haiku 5.5 answers the proven Build 158 way ──
rep("""/* what each Claude accepts: "off" is the least thinking each one allows (Opus 5.5 always thinks a little) */""",
    """/* the safety net: the way Build 158 asked, which Haiku 5.5 is known to answer. Used only if the main Claude can't */
const TOOL = { name: 'mirror_reply', description: 'Your reply to the person in the Mirror.', input_schema: { type: 'object', properties: SHAPE.schema.properties, required: SHAPE.schema.required } };
const SPARE = 'claude-haiku-5-5';
/* what each Claude accepts: "off" is the least thinking each one allows (Opus 5.5 always thinks a little) */""", 'safety net constants')
rep("""async function ask(env, model, charter, msgs, think) {""", """async function ask(env, model, charter, msgs, think, how, wait) {""", 'ask signature 2')
rep("""  const timer = setTimeout(() => ctl.abort(), WAIT_MS);""", """  const timer = setTimeout(() => ctl.abort(), wait || WAIT_MS);""", 'ask wait')
rep("""  const body = { model: model, max_tokens: th.max, system: system, messages: msgs };
  if (th.cfg.thinking) body.thinking = th.cfg.thinking;
  body.output_config = Object.assign({ format: SHAPE }, th.cfg.output_config || {});""",
    """  const tool = how === 'tool';
  const body = { model: model, max_tokens: tool ? 700 : th.max, system: system, messages: msgs };
  if (tool) { body.tools = [TOOL]; body.tool_choice = { type: 'tool', name: 'mirror_reply' }; }   /* exactly as Build 158 */
  else {
    if (th.cfg.thinking) body.thinking = th.cfg.thinking;
    body.output_config = Object.assign({ format: SHAPE }, th.cfg.output_config || {});
  }""", 'ask body 2')
rep("""  let v = null;
  for (let i = texts.length - 1; i >= 0 && !v; i--) {""", """  let v = null;
  if (tool) { const use = j && Array.isArray(j.content) ? j.content.find((b) => b && b.type === 'tool_use' && b.name === 'mirror_reply') : null; v = use && use.input && typeof use.input === 'object' ? use.input : null; }
  else for (let i = texts.length - 1; i >= 0 && !v; i--) {""", 'ask parse 2')
rep("""/* ── the soft limit:""", """/* the main Claude first; if it can't answer quickly for a reason of its own, the safety net answers instead */
async function answer(env, model, charter, msgs, think, how, spare) {
  const t0 = Date.now();
  let v = await ask(env, model, charter, msgs, think, how, WAIT_MS);
  if (spare && !v.ok && /^(?:upstream|jumbled|empty)$/.test(v.code) && Date.now() - t0 < 15000 && !(model === SPARE && how === 'tool')) {
    const first = v.detail;
    const w = await ask(env, SPARE, charter, msgs, 'off', 'tool', 20000);
    if (w.ok) { w.spare = true; w.first = first; v = w; }   /* if the safety net can't either, the first reason stands */
  }
  return v;
}

/* ── the soft limit:""", 'answer with safety net')
rep("""  const think = /^(?:off|low|medium|high)$/.test(url.searchParams.get('think') || '') ? url.searchParams.get('think') : THINK;""",
    """  const think = /^(?:off|low|medium|high)$/.test(url.searchParams.get('think') || '') ? url.searchParams.get('think') : THINK;
  const how = url.searchParams.get('how') === 'tool' ? 'tool' : 'shape', spare = url.searchParams.get('spare') === '1';""", 'selftest how')
rep("""  if (runs.length * 6 > 46) return reply({ ok: false, code: 'toomany', why: 'narrow it with model= or only=' }, 400);""",
    """  if (runs.length * 6 * (spare ? 2 : 1) > 46) return reply({ ok: false, code: 'toomany', why: 'narrow it with model= or only=' }, 400);""", 'selftest budget')
rep("""      const v = await ask(env, model, charter, msgs, think);""", """      const v = await answer(env, model, charter, msgs, think, how, spare);""", 'selftest answer')
rep("""ground: v.ground || undefined, ms: v.ms, out: v.usage ? v.usage.output_tokens : undefined });""",
    """ground: v.ground || undefined, ms: v.ms, out: v.usage ? v.usage.output_tokens : undefined, spare: v.spare || undefined, first: v.first || undefined });""", 'selftest spare shown')
rep("""  return reply({ ok: true, ref, suite, think, charter:""", """  return reply({ ok: true, ref, suite, think, how, spare, charter:""", 'selftest reply 2')
rep("""  const v = await ask(env, MODEL, CHARTER, msgs);
  if (!v.ok) return reply({ ok: false, code: v.code }, v.status || 503);
  delete v.usage; delete v.ms;""", """  const v = await answer(env, MODEL, CHARTER, msgs, THINK, 'shape', true);   /* Build 159 · with the safety net */
  if (!v.ok) return reply({ ok: false, code: v.code }, v.status || 503);
  delete v.usage; delete v.ms; delete v.spare; delete v.first;""", 'POST answer')

assert s.count('const TOOL =') == 1
io.open(DST, 'w', encoding='utf-8').write(s)
print('written', DST, len(s))
