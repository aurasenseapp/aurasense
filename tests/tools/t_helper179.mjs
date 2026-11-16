// Build 179 · the Mirror goes only by what the person says: fear together with lost sleep or lost days. Then, once,
// it is told to say plainly who is worth telling. node /home/claude/scripts/t_helper179.mjs   (test-only)
import { onRequest } from '/home/claude/aurasense/functions/api/mirror.js';
import { readFileSync } from 'node:fs';
const KEY = 'pretend-key-for-tests-only-0000000000';
let calls = [], fails = 0, n = 0;
const store = new Map();
globalThis.caches = { default: { match: async (r) => store.has(r.url) ? new Response(store.get(r.url)) : undefined, put: async (r, res) => { store.set(r.url, await res.text()); } } };
const shape = (o) => ({ id: 'm', type: 'message', role: 'assistant', stop_reason: 'end_turn', content: [{ type: 'text', text: JSON.stringify(o) }] });
globalThis.fetch = async (url, init) => { calls.push({ body: JSON.parse(init.body) }); return new Response(JSON.stringify(shape({ heard: 'Heard.', question: 'What is it like?', ready: false, care: false, ground: false, wiser_self: '' })), { status: 200 }); };
function check(name, ok, detail) { console.log((ok ? 'PASS ' : 'FAIL ') + name + (ok ? '' : '  -> ' + JSON.stringify(detail).slice(0, 400))); if (!ok) fails++; }
const D = '[Written by the Mirror’s written rules, not by you:] What are you sensing?';
async function stands(words, earlier, v) {
  calls = [];
  const turns = [{ role: 'assistant', content: D }].concat(earlier || []);
  const b = JSON.stringify(Object.assign({ words, turns }, v === 1 ? {} : { v: 2 }));
  const r = new Request('https://aurasense.app/api/mirror', { method: 'POST', headers: { Origin: 'https://aurasense.app', 'Content-Type': 'application/json', 'Content-Length': String(Buffer.byteLength(b)), 'CF-Connecting-IP': '203.0.113.' + (++n % 250) }, body: b });
  Object.defineProperty(r, 'cf', { value: { country: 'CA' } });
  const res = await onRequest({ request: r, env: { ANTHROPIC_API_KEY: KEY } }); await res.json();
  return calls.length ? calls[0].body.system.map((x) => x.text).join('\n') : '';
}
const NUDGE = /frightens them and is taking their rest or their days/;
const pair = (u, a) => [{ role: 'user', content: u }, { role: 'assistant', content: a }];
check('fear with lost sleep: the Mirror is told to say plainly, once, who is worth telling', NUDGE.test(await stands('It scares me. I can’t sleep for it.', pair('Everything is a sign lately.', 'Lately “everything is a sign”. What is it like?'))), '');
check('fear now, lost sleep said just before: the same', NUDGE.test(await stands('It frightens me.', pair('I haven’t slept since it began.', 'You “haven’t slept”. What is it like?'))), '');
check('a plain fear is not treated as trouble', !NUDGE.test(await stands('The dark by the river scares me a little.')), '');
check('lost sleep with no fear is not treated as trouble', !NUDGE.test(await stands('I can’t sleep, the hum is too loud.')), '');
check('gladness is never met with talk of doctors, however often it happens', !NUDGE.test(await stands('This keeps happening to me all the time and I love it. I think of someone and they call.')), '');
check('an unusual sense by itself is never treated as trouble', !NUDGE.test(await stands('Every sign on the street seems to point at me today.')), '');
check('“The signs scare me” counts as fear too', NUDGE.test(await stands('The signs scare me. I haven’t slept.')), '');
check('“the fear keeps me up every night” counts too', NUDGE.test(await stands('The fear of it keeps me up every night.')), '');
check('someone who says they are not scared is taken at their word', !NUDGE.test(await stands('I’m not scared of it, I just can’t sleep for wondering.')) && !NUDGE.test(await stands('It doesn’t frighten me at all, it happens all the time.')), '');
check('it is said once only', !NUDGE.test(await stands('It still scares me and I can’t sleep.', pair('It scares me. I can’t sleep.', 'That is a lot to carry alone, and someone you trust, or your doctor, is worth telling. What is it like now?'))), '');
const sys = await stands('It scares me. I can’t sleep for it.');
check('the charter says the same, under safety, and never judges a state of mind', /Never judge their state of mind/.test(sys) && /someone they trust, or their doctor, is worth telling how these days and nights have been/.test(sys) && /leave that third meaning for them to find/.test(sys), '');
check('the charter is the draft kept beside the tests, letter for letter', calls[0].body.system[0].text === readFileSync('/home/claude/mt/tests/mirror/charter-h.txt', 'utf8').replace(/\n$/, ''), '');
check('the Mirror people use today is untouched by this', !NUDGE.test(await stands('It scares me. I can’t sleep for it.', null, 1)) && /WHAT THE MIRROR IS FOR\nPeople come here/.test(calls[0].body.system[0].text), '');
console.log('\n' + fails + ' failed');
process.exit(fails ? 1 : 0);
