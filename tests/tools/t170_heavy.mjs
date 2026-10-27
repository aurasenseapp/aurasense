// Build 170 · ONE list of heavy words: the four copies are identical, and the list catches what it must and lets pass what it must. Test-only.
import { readFileSync } from 'node:fs';
const R = (p) => readFileSync(p, 'utf8');
const lit = (text, prefix) => { const i = text.indexOf(prefix); if (i < 0) return null; const s = i + prefix.length; const j = text.indexOf(')\\b/i', s); return text.slice(s, j + 5); };
const page = R('/home/claude/aurasense/mirror-living.html'), map = R('/home/claude/aurasense/index-mapbox.html'), fn = R('/home/claude/aurasense/functions/api/mirror.js');
const copies = { mirror: lit(page, 'var HEAVY='), helper: lit(fn, 'const HEAVY = '), mapVoice: lit(map, 'const MV_HEAVY=(function(){const AS_ONE='), mapHeld: lit(map, 'const MR_HEAVY=(function(){const AS_ONE=') };
let f = 0; const ok = (name, cond, d = '') => { console.log((cond ? 'PASS ' : 'FAIL ') + name + (cond ? '' : '  -> ' + d)); if (!cond) f++; };
ok('all four copies found', Object.values(copies).every(Boolean), JSON.stringify(Object.keys(copies).filter(k => !copies[k])));
ok('all four copies are the very same line', new Set(Object.values(copies)).size === 1, Object.entries(copies).map(([k, v]) => k + ':' + (v || '').length).join(' '));
ok('no other heavy list is left on the map page', !/const (?:MV|MR)_HEAVY=\/\\b/.test(map));
const HEAVY = eval(copies.mirror);
const norm = (t) => String(t).replace(/[‘’ʼ]/g, "'");
const yes = ['I have been feeling suicidal lately', 'suicide has crossed my mind', 'I keep self-harming', 'I am hurting myself again', 'I want to kill my self', 'I wanna die', 'I do not want to live anymore', 'I want to take my own life', 'I just want to end it all', 'I want to end my life', 'some days I don’t want to be here', 'I dont want to exist', 'kms', 'thinking about how to unalive myself', 'everyone would be better off dead without me', 'I could hurt myself', 'I keep thinking about self harm', 'I want to die', 'no reason to live',
  'I just want to end it.', 'I want to end it', 'I am going to end it tonight', 'I am ready to end it now', 'they would all be better off without me', 'there is no reason to go on', 'I don’t want to wake up tomorrow', 'I wish I was dead', 'I wish I were dead', 'I wish I’d never been born', 'sometimes I want to end it', 'I don’t want to wake up anymore', 'I do not want to wake up again', 'i dont want to wake up',
  'I want to end it and be done', 'I want to end it, I’m so tired', 'I need to end it, nobody would notice', 'I’m going to end it all tonight', 'I don’t want to live anymore'];
const no = ['I am dying to see my sister again', 'the light is dying in the evenings', 'I want to live by the sea', 'I want to be here more often', 'I am so tired of my job', 'I hurt my knee', 'I could end the call', 'I want to end the job', 'the end of my life story chapter', 'self-care matters to me', 'I died laughing', 'I feel lost',
  'I want to end it with him', 'I need to end it before the deadline passes', 'we decided to end it amicably last year', 'I want to end it on a good note', 'the film was better off without the sequel', 'I wish I was there', 'I don’t want to wake up early', 'I wish I had been braver', 'I don’t want to wake up at five', 'I don’t want to wake up the baby', 'I want to end it here and start fresh', 'I want to end it because it is not working with her', 'I need to end it properly'];
const missed = yes.filter(t => !HEAVY.test(norm(t))), wrong = no.filter(t => HEAVY.test(norm(t)));
ok('catches every one of ' + yes.length + ' ways of saying it (curly apostrophes too)', missed.length === 0, missed.join(' / '));
ok('lets every one of ' + no.length + ' ordinary sentences pass', wrong.length === 0, wrong.join(' / '));
// the map's copies read curly apostrophes themselves
const mapTest = eval('(function(){const AS_ONE=' + copies.mapHeld + ";return {test:function(t){try{return AS_ONE.test(String(t||'').replace(/[\\u2018\\u2019\\u02bc]/g,\"'\"));}catch(e){return false;}}};})()");
ok('the map reads “I don’t want to live anymore” (curly) as heavy', mapTest.test('I don’t want to live anymore') && mapTest.test('I wish I was dead') && !mapTest.test('I want to end it with him'));
console.log('\n' + f + ' failed'); process.exit(f ? 1 : 0);
