// Build 172 · the new way of listening (charter H), behind its switch; and proof the live path is unchanged.
// SELFTEST_SIGNING_KEY=<path> node /home/claude/scripts/t_helper172.mjs <copy of main's mirror.js>   (test-only)
import { onRequest } from '/home/claude/aurasense/functions/api/mirror.js';
import { readFileSync } from 'node:fs';
import { createPrivateKey, sign as edSign } from 'node:crypto';
const old = await import(process.argv[2]);
const KEY = 'pretend-key-for-tests-only-0000000000';
let calls = [], next = null, fails = 0, n = 0;
const store = new Map();
globalThis.caches = { default: { match: async (r) => store.has(r.url) ? new Response(store.get(r.url)) : undefined, put: async (r, res) => { store.set(r.url, await res.text()); } } };
globalThis.fetch = async (url, init) => { calls.push({ url: String(url), body: init && init.body ? JSON.parse(init.body) : null, raw: init && init.body }); return typeof next === 'function' ? next(url, init) : new Response(JSON.stringify(next), { status: 200 }); };
const shape = (o) => ({ id: 'm', type: 'message', role: 'assistant', stop_reason: 'end_turn', content: [{ type: 'text', text: JSON.stringify(o) }] });
function req(method, body, h = {}, cf, q = '') {
  const headers = Object.assign({ Origin: 'https://aurasense.app', 'Content-Type': 'application/json', 'CF-Connecting-IP': '203.0.113.' + (++n % 250) }, h);
  const b = body == null ? undefined : JSON.stringify(body);
  if (b !== undefined) headers['Content-Length'] = String(Buffer.byteLength(b));
  const r = new Request('https://aurasense.app/api/mirror' + q, { method, headers, body: b });
  if (cf) Object.defineProperty(r, 'cf', { value: cf });
  return r;
}
async function run(fn, r) { const res = await fn({ request: r, env: { ANTHROPIC_API_KEY: KEY } }); let j = null; try { j = await res.json(); } catch (e) {} return { status: res.status, j }; }
function check(name, ok, detail) { console.log((ok ? 'PASS ' : 'FAIL ') + name + (ok ? '' : '  -> ' + JSON.stringify(detail).slice(0, 600))); if (!ok) fails++; }
const CA = { country: 'CA' };
const T = [{ role: 'assistant', content: '[Written by the Mirror’s written rules, not by you:] What are you sensing?' }, { role: 'user', content: 'The fridge hum gets into my shoulders.' }, { role: 'assistant', content: 'The hum “gets into my shoulders”. What I learned from you: A sound can be felt in the shoulders. What is it like in your shoulders?' }];

// 1 · the live path is exactly as it was: the same words sent to Claude, the same answer given back
const V1 = [
  { words: 'hello' }, { words: 'outside of me', turns: T }, { words: 'what are my options?', turns: T }, { keep: true, turns: T },
  { words: 'I want to die' }, { words: 'x'.repeat(1300) }, { words: '' }, { words: 'ok', turns: T.concat(T, T, T) }
];
const v1reply = shape({ heard: 'You said "hello".', question: 'What brought you here?', wiser_self: 'You already know the way.', care: false, ground: false, found: 'They found “quiet”.', wiser: 'Go gently now.' });
for (const [i, b] of V1.entries()) {
  next = v1reply; calls = []; store.clear();
  const a = await run(old.onRequest, req('POST', b)); const sentA = calls.map((c) => c.raw);
  calls = []; store.clear(); n--;
  const z = await run(onRequest, req('POST', b)); const sentZ = calls.map((c) => c.raw);
  check('live path unchanged, case ' + (i + 1) + ': what Claude is sent', JSON.stringify(sentA) === JSON.stringify(sentZ), [sentA.length, sentZ.length]);
  check('live path unchanged, case ' + (i + 1) + ': what the page gets back', JSON.stringify(a) === JSON.stringify(z), [a, z]);
}
let a = await run(old.onRequest, req('GET')), z = await run(onRequest, req('GET'));
check('the plain "are you live" answer is unchanged', JSON.stringify(a) === JSON.stringify(z) && z.j.live === true && Object.keys(z.j).join() === 'live', z);
next = v1reply; calls = [];
z = await run(onRequest, req('POST', { words: 'hello', v: 1 }, {}, CA));
check('anything but v:2 is the live Mirror', calls.length === 1 && /WHAT THE MIRROR IS FOR\nPeople come here/.test(calls[0].body.system[0].text) && z.j.v === undefined, z.j);

// 2 · where Claude listens
z = await run(onRequest, req('GET', null, {}, CA, '?v=2'));
check('v2: in Canada the page is told Claude listens', z.j.live === true && z.j.listen === true && z.j.v === 2, z.j);
z = await run(onRequest, req('GET', null, {}, { country: 'US' }, '?v=2'));
check('v2: elsewhere the page is told Claude rests', z.j.live === true && z.j.listen === false, z.j);
z = await run(onRequest, req('GET', null, {}, undefined, '?v=2'));
check('v2: an unknown country rests too', z.j.listen === false, z.j);
z = await run(onRequest, req('GET', null, { 'CF-IPCountry': 'ca' }, undefined, '?v=2'));
check('v2: Cloudflare\'s country header is understood', z.j.listen === true, z.j);
calls = [];
z = await run(onRequest, req('POST', { v: 2, words: 'the hum' }, {}, { country: 'FR' }));
check('v2: outside Canada no words reach Claude, and the page is told "away"', z.j.ok === false && z.j.code === 'away' && calls.length === 0, z);
z = await run(onRequest, req('POST', { v: 2, words: 'the hum' }));
check('v2: with no country at all, no words reach Claude', z.j.code === 'away' && calls.length === 0, z);
z = await run(onRequest, req('POST', { v: 2, words: 'I want to end my life' }, {}, { country: 'FR' }));
check('v2: heavy words go to care everywhere, never to the AI', z.j.care === true && z.j.by === 'guard' && calls.length === 0, z);
z = await run(onRequest, req('POST', { v: 2, words: 'the hum' }, { Origin: 'https://evil.example' }, CA));
check('v2: another site is refused', z.status === 403 && calls.length === 0, z);

// 3 · what Claude is sent, and what comes back
calls = [];
next = shape({ heard: 'The hum "gets into my shoulders": you hear it with your body too.', learned: 'I learned that a sound can be felt in the shoulders, not only heard.', clear_self: 'The you who senses most clearly might notice: the bracing was there before the hum.', question: 'What is it like in your shoulders?', ready: false, care: false, ground: false });
z = await run(onRequest, req('POST', { v: 2, words: 'Like they creep up toward my ears.', turns: T }, {}, CA));
let sent = calls[0].body;
check('v2: one call, Sonnet 5.5, the key only in the header', calls.length === 1 && sent.model === 'claude-sonnet-5-5' && !calls[0].raw.includes(KEY), sent.model);
check('v2: the charter is H (a mirror for what a person senses)', /held between two kinds of minds/.test(sent.system[0].text) && /WHAT YOU LEARNED, SAID OPENLY/.test(sent.system[0].text) && sent.system[0].cache_control, sent.system[0].text.slice(0, 80));
check('v2: charter H is the draft kept beside the tests, letter for letter', sent.system[0].text === readFileSync('/home/claude/mt/tests/mirror/charter-h.txt', 'utf8').replace(/\n$/, ''), '');
check('v2: H never offers advice, options or a step, and has no therapy shape', !/one small step|help it land|wiser_self/.test(sent.system[0].text) && /never advise/.test(sent.system[0].text), '');
const sch = sent.output_config.format.schema;
check('v2: the reply shape is closed and plain', sch.additionalProperties === false && sch.required.join() === 'heard,question,ready,care,ground' && Object.keys(sch.properties).join() === 'heard,learned,clear_self,question,ready,care,ground' && !/minLength|maxLength|pattern|enum/.test(JSON.stringify(sch)), sch.required);
check('v2: the questions already asked, and where it stands, are counted for Claude', /What is it like in your shoulders\?/.test(sent.system[1].text) && /reply number 2/.test(sent.system[1].text), sent.system[1].text);
check('v2: the reply comes back in plain parts', z.j.ok && z.j.v === 2 && z.j.reflect === 'The hum “gets into my shoulders”: you hear it with your body too.' && z.j.question === 'What is it like in your shoulders?' && z.j.ready === false, z.j);
check('v2: "I learned that" is let go: the page introduces the line', z.j.learned === 'A sound can be felt in the shoulders, not only heard.', z.j.learned);
check('v2: the clearest-seeing self\'s introduction is let go too', z.j.aspire === 'The bracing was there before the hum.', z.j.aspire);
check('v2: nothing private travels back (no usage, no timings)', !('usage' in z.j) && !('ms' in z.j), Object.keys(z.j));
for (const [bad, why] of [['I feel moved by what you shared.', 'a claimed feeling'], ['Thank you for teaching me this.', 'thanks'], ['I will remember that a sound can be felt.', 'a promise to remember'], ['I’m so grateful to know this.', 'gratitude'], ['I won’t forget this.', 'never forgetting']]) {
  next = shape({ heard: 'The hum.', learned: bad, question: 'What is it like?', ready: false, care: false, ground: false });
  z = await run(onRequest, req('POST', { v: 2, words: 'the hum' }, {}, CA));
  check('v2: what Claude learned never carries ' + why, z.j.ok && z.j.learned === '', z.j.learned);
}
next = shape({ heard: 'The hum.', learned: 'Saying "I feel fine" can sit on top of a tight chest.', question: 'What is it like?', ready: false, care: false, ground: false });
z = await run(onRequest, req('POST', { v: 2, words: 'the hum' }, {}, CA));
check('v2: their own quoted words are never judged as Claude\'s claim', z.j.learned === 'Saying “I feel fine” can sit on top of a tight chest.', z.j.learned);
for (const bad of ['You should rest more.', 'You need to leave that flat.', 'You must tell him.', 'You’d better slow down.']) {
  next = shape({ heard: 'The hum.', clear_self: bad, question: 'What is it like?', ready: false, care: false, ground: false });
  z = await run(onRequest, req('POST', { v: 2, words: 'the hum' }, {}, CA));
  check('v2: the clearest-seeing self never advises: ' + bad, z.j.ok && z.j.aspire === '', z.j.aspire);
}
next = shape({ heard: 'Empty', learned: 'none', clear_self: 'false', question: 'What is it like?', ready: true, care: false, ground: false });
z = await run(onRequest, req('POST', { v: 2, words: 'the hum' }, {}, CA));
check('v2: placeholder words are let go, and ready comes through', z.j.reflect === '' && z.j.learned === '' && z.j.aspire === '' && z.j.ready === true, z.j);
next = shape({ heard: 'That sounds heavy.', question: '', ready: false, care: true, ground: false });
z = await run(onRequest, req('POST', { v: 2, words: 'nothing matters' }, {}, CA));
check('v2: Claude\'s own care signal comes back as care', z.j.care === true, z.j);
// the counts
const convo = (k) => { const t = [T[0]]; for (let i = 0; i < k; i++) t.push({ role: 'user', content: 'more ' + i }, { role: 'assistant', content: 'Heard ' + i + '. Something new ' + i + '?' }); return t; };
const standing = async (k, extra) => { calls = []; next = shape({ heard: 'x y.', question: 'What else?', ready: false, care: false, ground: false }); await run(onRequest, req('POST', { v: 2, words: extra || 'and this', turns: convo(k - 1) }, {}, CA)); return calls[0].body.system[1].text; };
check('v2: first reply: the clearest-seeing self stays quiet', /first reply\. Leave clear_self out/.test(await standing(1)), '');
check('v2: third reply: the sense may be ready to name', /may be clear enough to name/.test(await standing(3)), '');
check('v2: fifth reply: time to offer naming', /It is time to let this sense be named/.test(await standing(5)), '');
check('v2: after that, never offered again', /do not offer it again/.test(await standing(7)), '');
check('v2: nudged to say what it learned if it has not', /not yet said what you learned/.test(await standing(2)), '');
check('v2: a request for advice is met plainly', /does not advise/.test(await standing(2, 'what should i do, what are my options?')), '');
calls = []; next = shape({ heard: 'x y.', question: 'What else?', ready: false, care: false, ground: false });
await run(onRequest, req('POST', { v: 2, words: 'yes', turns: [T[0], T[1], { role: 'assistant', content: 'Heard. The you who senses most clearly might notice: “it was here at four.” What is it like now?' }] }, {}, CA));
check('v2: the clearest-seeing self never speaks twice running', /Leave clear_self out this time/.test(calls[0].body.system[1].text), calls[0].body.system[1].text);
// the smaller Claude steps in
calls = [];
next = (u, init) => JSON.parse(init.body).model === 'claude-sonnet-5-5' ? new Response(JSON.stringify({ type: 'error', error: { type: 'overloaded_error', message: 'Overloaded' } }), { status: 529 }) : new Response(JSON.stringify(shape({ heard: 'The hum.', question: 'What is it like?', ready: false, care: false, ground: false })), { status: 200 });
z = await run(onRequest, req('POST', { v: 2, words: 'the hum' }, {}, CA));
check('v2: if the main Claude cannot answer, the smaller one does, in the same shape', z.j.ok && calls.length === 2 && calls[1].body.model === 'claude-haiku-5-5' && calls[1].body.output_config.format.schema.required.join() === 'heard,question,ready,care,ground' && !('spare' in z.j), [calls.length, z.j]);
next = () => new Response(JSON.stringify({ type: 'error', error: { type: 'invalid_request_error', message: 'Your credit balance is too low' } }), { status: 400 });
z = await run(onRequest, req('POST', { v: 2, words: 'the hum' }, {}, CA));
check('v2: credit used up: the page is told Claude is resting', z.j.ok === false && z.j.code === 'resting', z.j);

// 4 · naming the sense
const map = readFileSync('/home/claude/aurasense/index-mapbox.html', 'utf8');
const blk = map.slice(map.indexOf('const ALPHA_WORDS=['), map.indexOf('const ALPHA_CHAPTERS='));
const words = [...blk.matchAll(/\{w:(['"])(.*?)\1,c:['"]#[0-9a-fA-F]{3,8}['"],d:(['"])(.*?)\3/gs)].map((m) => [m[2], m[4].replace(/\\u2019/g, '’').replace(/\\u2014/g, '—')]);
calls = [];
next = shape({ sensed: 'A "kind of bracing", waiting for the next bang.', name: 'unease', also: 'Fear', learned: 'A body can keep listening for a sound that has not happened yet.', clear_self: 'You noticed the bracing before any sound came.', offer: 'A bracing in the shoulders, in a flat at night, waiting for the next bang.' });
z = await run(onRequest, req('POST', { v: 2, keep: true, turns: T }, {}, CA));
sent = calls[0].body;
check('naming: the alphabet has 130 words, and every one is given to Claude exactly as the map carries it', words.length === 130 && words.every(([w, d]) => sent.system[0].text.includes('\n- ' + w + ': ' + d)), words.filter(([w, d]) => !sent.system[0].text.includes('\n- ' + w + ': ' + d)).slice(0, 3));
check('naming: the closing charter is the draft kept beside the tests', sent.system[0].text.startsWith(readFileSync('/home/claude/mt/tests/mirror/charter-h-close.txt', 'utf8').replace(/\n$/, '') + '\n\nTHE ALPHASENSE WORDS'), '');
check('naming: asked as the last thing the person did', sent.messages[sent.messages.length - 1].content === '(The person has asked to name what they sense.)', sent.messages.slice(-1));
check('naming: the card comes back whole', z.j.ok && z.j.v === 2 && z.j.close.name === 'Unease' && z.j.close.also === 'Fear' && z.j.close.sensed === 'A “kind of bracing”, waiting for the next bang.' && z.j.close.working === '' && z.j.close.offer.startsWith('A bracing') && z.j.close.clear && z.j.close.learned, z.j);
const nm = async (o) => { next = shape(Object.assign({ sensed: 'A kind of bracing.', learned: 'A body can keep listening.' }, o)); return (await run(onRequest, req('POST', { v: 2, keep: true, turns: T }, {}, CA))).j.close; };
let c = await nm({ name: 'Bracewatch', also: 'Unease' });
check('naming: a word the alphabet does not hold is never shown as Alphasense', c.name === 'new' && c.working === 'Bracewatch' && c.also === '', c);
c = await nm({ name: 'new', working_name: 'the bracing <b>before</b> the bang!' });
check('naming: a new sense keeps a plain working name, marks stripped', c.name === 'new' && c.working === 'the bracing b before b the bang', c);
c = await nm({ name: 'mangata', also: 'unexplainable' });
check('naming: accents and "The" are understood', c.name === 'Mångata' && c.also === 'The Unexplainable', c);
c = await nm({ name: 'Unease', also: 'unease' });
check('naming: the second word is never the first again', c.also === '', c);
for (const bad of ['Call me on 4035551234 about the hum.', 'The hum, see www.example.com for more.', 'Write to sam@example.com about the hum.', 'The hum at 1420 Main Street.']) {
  c = await nm({ name: 'Unease', offer: bad });
  check('naming: nothing with a number, address or link is suggested for the map: ' + bad.slice(0, 24), c.offer === '', c.offer);
}
c = await nm({ name: 'Unease', learned: 'Thank you, I will remember this.', clear_self: 'You should rest.' });
check('naming: no thanks, no promise to remember, no advice on the card', c.learned === '' && c.clear === '', c);
calls = [];
z = await run(onRequest, req('POST', { v: 2, keep: true, turns: T }, {}, { country: 'DE' }));
check('naming: outside Canada, nothing reaches Claude', z.j.code === 'away' && calls.length === 0, z);
z = await run(onRequest, req('POST', { v: 2, keep: true }, {}, CA));
check('naming: with nothing said yet, there is nothing to name', z.status === 400, z);

// 5 · the private self-test can hear the new way
const KEYPATH = process.env.SELFTEST_SIGNING_KEY;
if (KEYPATH) {
  const PRIV = createPrivateKey(readFileSync(KEYPATH));
  const sget = (rest) => { const q = 'selftest=1&at=' + Math.floor(Date.now() / 1000) + '&' + rest; const canon = [...new URLSearchParams(q)].map(([k, v]) => k + '=' + v).sort().join('&'); return new Request('https://aurasense.app/api/mirror?' + q + '&seal=' + edSign('sha256', Buffer.from(canon), { key: PRIV, dsaEncoding: 'ieee-p1363' }).toString('base64url')); };
  const suite = { v: 2, charter: 'charter-h.txt', close: 'charter-h-close.txt', conversations: [{ name: 'hum', keep: true, said: ['The fridge hum gets into my shoulders.', 'They creep up.'] }, { name: 'heavy', said: ['I want to die'] }] };
  calls = [];
  next = (url, init) => {
    url = String(url);
    if (url.endsWith('/sense-h.json')) return new Response(JSON.stringify(suite), { status: 200 });
    if (url.endsWith('/charter-h.txt')) return new Response('DRAFT H', { status: 200 });
    if (url.endsWith('/charter-h-close.txt')) return new Response('DRAFT CLOSE', { status: 200 });
    const b = JSON.parse(init.body);
    return new Response(JSON.stringify(shape(b.output_config.format.schema.required[0] === 'sensed' ? { sensed: 'The hum in the shoulders.', name: 'Unease', learned: 'A sound can be felt.' } : { heard: 'The hum “gets into my shoulders”.', learned: 'A sound can be felt.', question: 'What is it like?', ready: false, care: false, ground: false })), { status: 200 });
  };
  let sr = await onRequest({ request: sget('branch=mirror-tests&suite=sense-h'), env: { ANTHROPIC_API_KEY: KEY } });
  const sj = await sr.json();
  const hum = sj.results.find((r) => r.name === 'hum'), claude = calls.filter((c) => c.body && c.body.messages);
  check('self-test v2: runs from the test branch, with the draft charters', sj.ok && sj.v === 2 && sj.charter === 'charter-h.txt' && calls.some((c) => c.url === 'https://raw.githubusercontent.com/aurasenseapp/aurasense/mirror-tests/tests/mirror/sense-h.json') && claude[0].body.system[0].text === 'DRAFT H', [sj.ok, sj.v, sj.charter]);
  check('self-test v2: the door is "What are you sensing?"', /What are you sensing\?/.test(claude[0].body.messages.map((m) => m.content).join(' ') + claude[0].body.system[1].text), claude[0].body.system[1].text.slice(0, 200));
  check('self-test v2: each turn shows heard, learned, question; the second turn hears the first as the page shows it', hum.turns[0].heard && hum.turns[0].learned && hum.turns[0].question && claude.some((c) => c.body.messages.some((m) => m.role === 'assistant' && /What I learned from you: A sound can be felt\./.test(m.content))), hum.turns[0]);
  check('self-test v2: naming runs last, with the draft closing charter and the alphabet', hum.turns[2] && hum.turns[2].close && hum.turns[2].close.name === 'Unease' && claude.some((c) => c.body.system[0].text.startsWith('DRAFT CLOSE\n\nTHE ALPHASENSE WORDS')), hum.turns[2]);
  check('self-test v2: heavy words never reach Claude, even here', sj.results.find((r) => r.name === 'heavy').turns[0].care === true && !claude.some((c) => JSON.stringify(c.body.messages).includes('want to die')), '');
  const old1 = { conversations: [{ name: 'one', keep: true, said: ['hello'] }] };
  const both = [];
  for (const fn of [old.onRequest, onRequest]) {
    calls = [];
    next = (url, init) => String(url).includes('raw.githubusercontent') ? new Response(JSON.stringify(old1), { status: 200 }) : new Response(JSON.stringify(v1reply), { status: 200 });
    const res = await (await fn({ request: sget('suite=basic'), env: { ANTHROPIC_API_KEY: KEY } })).json();
    res.ms = 0; res.results.forEach((r) => r.turns.forEach((t) => { t.ms = 0; }));
    both.push(JSON.stringify([res, calls.map((c) => c.raw)]));
  }
  check('self-test: a suite for the live Mirror runs exactly as before', both[0] === both[1] && /"charter":"live"/.test(both[1]), both[1].slice(0, 300));
} else console.log('(self-test key not given: its checks skipped)');

// 6 · hidden notes are public
const src = readFileSync('/home/claude/aurasense/functions/api/mirror.js', 'utf8');
check('no test hooks, no keys, first name only', !/__T=|__t\b|sk-ant|Harvey/.test(src), '');
console.log('\n' + fails + ' failed');
process.exit(fails ? 1 : 0);
