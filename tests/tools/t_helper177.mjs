// Build 177 · naming says which: one symbol, symbols together, or a new sense with its nearest relatives.
// node /home/claude/scripts/t_helper177.mjs   (test-only; a pretend Claude, no real one is called)
import { onRequest } from '/home/claude/aurasense/functions/api/mirror.js';
import { readFileSync } from 'node:fs';
const KEY = 'pretend-key-for-tests-only-0000000000';
let calls = [], next = null, fails = 0, n = 0;
const store = new Map();
globalThis.caches = { default: { match: async (r) => store.has(r.url) ? new Response(store.get(r.url)) : undefined, put: async (r, res) => { store.set(r.url, await res.text()); } } };
globalThis.fetch = async (url, init) => { calls.push({ body: init && init.body ? JSON.parse(init.body) : null }); return new Response(JSON.stringify(next), { status: 200 }); };
const shape = (o) => ({ id: 'm', type: 'message', role: 'assistant', stop_reason: 'end_turn', content: [{ type: 'text', text: JSON.stringify(o) }] });
function check(name, ok, detail) { console.log((ok ? 'PASS ' : 'FAIL ') + name + (ok ? '' : '  -> ' + JSON.stringify(detail).slice(0, 500))); if (!ok) fails++; }
const T = [{ role: 'assistant', content: '[Written by the Mirror’s written rules, not by you:] What are you sensing?' }, { role: 'user', content: 'The fridge hum gets into my shoulders.' }, { role: 'assistant', content: 'The hum “gets into my shoulders”. What is it like?' }];
async function nm(o) {
  next = shape(Object.assign({ sensed: 'A kind of bracing.', learned: 'A body can keep listening.' }, o));
  const b = JSON.stringify({ v: 2, keep: true, turns: T });
  const r = new Request('https://aurasense.app/api/mirror', { method: 'POST', headers: { Origin: 'https://aurasense.app', 'Content-Type': 'application/json', 'Content-Length': String(Buffer.byteLength(b)), 'CF-Connecting-IP': '203.0.113.' + (++n % 250) }, body: b });
  Object.defineProperty(r, 'cf', { value: { country: 'CA' } });
  const res = await onRequest({ request: r, env: { ANTHROPIC_API_KEY: KEY } });
  return (await res.json()).close;
}
let c = await nm({ name: 'Stillness', fits: 'one' });
const sch = calls[0].body.output_config.format.schema;
check('the naming shape is plain: words and yes-or-no only, nothing the API might refuse', Object.keys(sch.properties).join() === 'sensed,name,also,third,fits,working_name,learned,clear_self,offer' && sch.required.join() === 'sensed,name,learned' && !/enum|minLength|maxLength|pattern|"array"/.test(JSON.stringify(sch)), Object.keys(sch.properties));
check('the closing charter asks which of the three it is', /fits: one of these three words: one, together, new/.test(calls[0].body.system[0].text) && calls[0].body.system[0].text.startsWith(readFileSync('/home/claude/mt/tests/mirror/charter-h-close.txt', 'utf8').replace(/\n$/, '')), '');
check('one word fits: one symbol', c.fits === 'one' && c.words.join() === 'Stillness' && c.name === 'Stillness' && c.also === '' && c.working === '', c);
c = await nm({ name: 'Unease', also: 'Fear', fits: 'one' });
check('"one" keeps only the first word', c.fits === 'one' && c.words.join() === 'Unease' && c.also === '', c);
c = await nm({ name: 'Hope', also: 'Grief', third: 'Stillness', fits: 'together' });
check('words together: up to three, in order', c.fits === 'together' && c.words.join() === 'Hope,Grief,Stillness' && c.name === 'Hope' && c.also === 'Grief', c);
c = await nm({ name: 'Hope', also: 'hope', third: 'HOPE', fits: 'together' });
check('"together" with one real word is one symbol', c.fits === 'one' && c.words.join() === 'Hope', c);
c = await nm({ name: 'Unease', also: 'Fear', fits: 'new', working_name: 'the bracing before the bang' });
check('a new sense keeps its nearest relatives, and its own name', c.fits === 'new' && c.words.join() === 'Unease,Fear' && c.name === 'new' && c.also === '' && c.working === 'the bracing before the bang', c);
c = await nm({ name: 'Unease', also: 'Fear' });
check('if Claude does not say, two words are read as together', c.fits === 'together' && c.words.join() === 'Unease,Fear', c);
c = await nm({ name: 'Unease' });
check('if Claude does not say, one word is read as one', c.fits === 'one' && c.words.join() === 'Unease', c);
c = await nm({ name: 'Unease', also: 'Fear', fits: 'whatever <b>' });
check('anything but the three words is ignored', c.fits === 'together', c);
c = await nm({ name: 'Bracewatch', also: 'Unease', fits: 'one' });
check('a name of Claude\'s own making is never shown as Alphasense: it becomes a new sense', c.fits === 'new' && c.name === 'new' && c.working === 'Bracewatch' && c.words.join() === 'Unease', c);
c = await nm({ name: 'new', working_name: 'the hum in the bones' });
check('the older way of saying new is still understood', c.fits === 'new' && c.words.length === 0 && c.working === 'the hum in the bones', c);
c = await nm({ name: 'Nothing', also: 'Nope', fits: 'together' });
check('no real word at all: a new sense, never an invented symbol', c.fits === 'new' && c.words.length === 0 && c.name === 'new', c);
c = await nm({ name: 'Unease', fits: 'one', working_name: 'ignored name' });
check('a working name is kept only for a new sense', c.working === '', c);
console.log('\n' + fails + ' failed');
process.exit(fails ? 1 : 0);
