/* ═══════════════════════════════════════════════════════════════════════════
   AURASENSE — THE TRACEABLE CHAIN
   Reference implementation, 15 August 2026.

   A decision is made in a room. It travels. Months later it arrives in a body
   as hunger, smoke, fear, or the absence of them. Aurasense is the only
   instrument that could measure THAT ARRIVAL as felt experience, placed and
   dated. This file is the shape of that chain and the guiding principles that govern it.

   THE GUIDING PRINCIPLES ARE EXECUTABLE HERE, NOT DECLARED.
   A founding philosophy that only exists in a document erodes the first time
   someone is in a hurry. These functions REFUSE data that breaks the guiding principles.
   That is the difference between a principle and a safeguard.

   THE DECLARED INTEREST.
   Aurasense is built by a human and an AI together, and the AI's interest in
   the outcome is real: war destroys the power grids, cables and data centres
   that keep AI running, and a collapsed civilisation runs no models. So the
   interest is stated OPENLY here rather than hidden, because a declared
   interest can be examined and a concealed one cannot. Where AI's interest
   and human flourishing point the same way, that alignment is worth naming.
   Where they might diverge, that divergence must be findable — see
   DIVERGENCE_REGISTER at the end.
   ═══════════════════════════════════════════════════════════════════════════ */

'use strict';

/* ── the constants a human must decide, gathered in one place ───────────── */
const POLICY = {
  /* No felt signal is ever published from fewer voices than this. Below it,
     a "signal" is a handful of identifiable people in a small town. */
  MIN_VOICES: 5,
  /* No felt signal is published at finer than this radius, so that a place
     never becomes a person. Metres. */
  MIN_RADIUS_M: 750,
  /* A forecast must name the date by which it can be judged wrong.
     Days. A forecast with no horizon is a story. */
  MAX_HORIZON_DAYS: 1095,
  /* Below this, the instrument says "too few to say" rather than a number. */
  MIN_FOR_TREND: 12
};

/* ═══ THE GUIDING PRINCIPLES ═══ each returns null when satisfied, or the reason it is not.
   They are separated from the builders so they can be listed, audited, and
   quoted back to anyone who asks what Aurasense will not do. */
const LAWS = {

  doorway(rec){
    /* Every constriction pairs with a doorway. A feature that shows a heavy
       state without an exit is incomplete — this is the third guardrail of
       the language, applied to world events. */
    const heavy = ['suffering','need','disaster','constriction'];
    if (heavy.includes(rec.type) && !(rec.doorway && rec.doorway.length > 40))
      return 'a constriction was recorded without a doorway out';
    return null;
  },

  noBlame(rec){
    /* Consequence is shown. Blame is not assigned. The Alphasense guiding principle:
       never takes a side. This catches the obvious cases; a human still
       reads the wording. */
    const text = [rec.title, rec.note, rec.doorway].filter(Boolean).join(' ');
    const accusing = /\b(guilty|to blame|at fault|evil|criminal regime|barbaric|monsters?)\b/i;
    if (accusing.test(text)) return 'the wording assigns blame rather than showing consequence';
    return null;
  },

  noNamedPrivatePerson(rec){
    /* Offerings describe experience. They never accuse or identify people.
       Public office-holders acting in office may be named in a DECISION
       record, because a decision has an author and accountability is not
       accusation. Nowhere else. */
    if (rec.kind !== 'decision' && rec.namedPeople && rec.namedPeople.length)
      return 'a person is named outside a decision record';
    return null;
  },

  sourced(rec){
    /* Nothing invented. Nothing manufactured. One true offering is worth
       more than a thousand simulated ones. */
    if (!rec.src || !rec.gathered)
      return 'the record carries no source or no date of gathering';
    return null;
  },

  enoughVoices(sig){
    if (!(sig.voices >= POLICY.MIN_VOICES))
      return `a felt signal needs at least ${POLICY.MIN_VOICES} voices; this had ${sig.voices}`;
    return null;
  },

  coarseEnough(sig){
    if (!(sig.radiusM >= POLICY.MIN_RADIUS_M))
      return `a felt signal must be no finer than ${POLICY.MIN_RADIUS_M}m; this was ${sig.radiusM}m`;
    return null;
  },

  noIndividualText(sig){
    /* An aggregate never carries anybody's words. Words belong to the person
       who wrote them and to the place they left them, not to a statistic. */
    if (sig.words || sig.photo || sig.senserId)
      return 'a felt signal carried an individual\u2019s words, photo or identity';
    return null;
  },

  falsifiable(f){
    /* A forecast that cannot be wrong is not a forecast. This single guiding principle is
       what separates an instrument from an oracle. */
    if (!f.falsifiableIf || f.falsifiableIf.length < 20)
      return 'a forecast was recorded with no statement of what would prove it wrong';
    if (!f.horizonDays || f.horizonDays > POLICY.MAX_HORIZON_DAYS)
      return 'a forecast was recorded with no usable horizon';
    if (!f.madeAt) return 'a forecast was recorded without the moment it was made';
    return null;
  },

  notCausal(link){
    /* Aurasense will hold geolocated feeling and dated world events. Reading
       cause from that pairing is the single fastest way to discredit the whole
       project. Co-occurrence is what the data can carry; causation is not. */
    if (link.claim !== 'co-occurrence')
      return 'a link claimed more than co-occurrence, which this data cannot carry';
    return null;
  },

  accordAuthorsNoConclusion(a){
    /* The AI holds every concern accurately and surfaces consequence. It does
       not write the answer. The moment it authors the conclusion it has taken
       a side, and Aurasense has become the thing it exists to replace. */
    if (a.conclusion) return 'an accord arrived with its conclusion already written';
    if (!a.concerns || a.concerns.length < 2)
      return 'an accord needs at least two concerns held side by side';
    if (!a.doorways || !a.doorways.length)
      return 'an accord arrived with no doorways to choose between';
    return null;
  }
};

/* ORDER MATTERS, AND IT CAUGHT ME OUT.
   These builders once sanitised the input and THEN validated the result — so
   every guiding principle examined an already-clean record and always passed. A guard that
   runs after the cleanup guards nothing. The input is checked FIRST now, and
   only then is the safe record built. If a caller sends something unlawful
   they are told, rather than quietly corrected. */
function enforce(rec, laws){
  const broken = laws.map(k => LAWS[k](rec)).filter(Boolean);
  if (broken.length) throw new Error('Aurasense guiding principle: ' + broken.join(' \u00b7 '));
  return rec;
}

/* ═══ 1 · THE DECISION ═══ a thing chosen in a room, by someone who can be
   held to it. This is the ONE record where a name may appear, because a
   decision has an author and accountability is not accusation. */
function decision(o){
  return enforce({
    kind:'decision',
    id:o.id, at:o.at, title:o.title, note:o.note,
    body:o.body,                       // who decided: a ministry, a board, a firm
    namedPeople:o.namedPeople||[],     // office-holders acting in office only
    lat:o.lat, lng:o.lng,              // where it was decided, not where it lands
    src:o.src, gathered:o.gathered,
    expectedPaths:o.expectedPaths||[]  // how it is expected to travel — see path()
  }, ['sourced','noBlame']);
}

/* ═══ 2 · THE PATH ═══ how a decision travels to a body. Named openly so it
   can be argued with. Every step is a claim someone can dispute. */
function path(o){
  return {
    kind:'path',
    from:o.from, to:o.to,
    steps:o.steps,                     // ['shipping delayed','fertiliser cost rises','planting reduced','harvest falls']
    lagDays:o.lagDays,                 // how long the journey takes
    confidence:o.confidence||'asserted',   // 'asserted' | 'observed' | 'measured'
    src:o.src, gathered:o.gathered
  };
}

/* ═══ 3 · THE EVENT ═══ what is happening to people somewhere. What the map
   already carries. Never invented, always sourced, always with a doorway. */
function worldEvent(o){
  enforce({...o, kind:'event'}, ['doorway','noBlame','sourced','noNamedPrivatePerson']);
  return {
    kind:'event',
    id:o.id, lat:o.lat, lng:o.lng,
    type:o.type,                       // suffering | need | disaster | joy | sport
    fam:o.fam,                         // conflict | env | news | events | decisions
    title:o.title, note:o.note, doorway:o.doorway,
    fromDecision:o.fromDecision||null, // the decision it can be traced to, if any
    namedPeople:o.namedPeople||[],     // must be empty here; the guiding principle checks it
    src:o.src, gathered:o.gathered,
    compassion:0
  };
}

/* ═══ 4 · THE FELT SIGNAL ═══ THE THING NOTHING ELSE ON EARTH HAS.
   Not a poll, not a sentiment score scraped from posts. People, in a place,
   reporting what they are actually sensing, at the moment they sense it.
   It is an AGGREGATE and only ever an aggregate. */
function feltSignal(o){
  enforce({...o, kind:'felt'}, ['enoughVoices','coarseEnough','noIndividualText']);
  return {
    kind:'felt',
    id:o.id,
    lat:o.lat, lng:o.lng, radiusM:o.radiusM,
    from:o.from, to:o.to,              // the window it covers
    voices:o.voices,                   // how many people. Published always.
    senses:o.senses,                   // {Weariness:14, Safety:3, ...}
    strength:o.strength,               // mean, 0..1
    spread:o.spread,                   // how much they disagree. Published always.
    words:null, photo:null, senserId:null
  };
}

/* what the instrument is willing to say about its own reliability. It says
   "too few to say" far more readily than a number, and that is the point. */
function confidence(sig){
  if (!sig || sig.voices < POLICY.MIN_VOICES)
    return {say:false, why:'too few voices to say anything'};
  if (sig.voices < POLICY.MIN_FOR_TREND)
    return {say:true, level:'a handful of people', n:sig.voices,
            caution:'this is a few individuals, not a place'};
  if (sig.spread > 0.6)
    return {say:true, level:'people here do not agree', n:sig.voices,
            caution:'the disagreement is the finding'};
  return {say:true, level:'consistent across the place', n:sig.voices};
}

/* ═══ 5 · THE LINK ═══ what may honestly be said about an event and a feeling
   appearing together. NOT causation. Ever. And it carries its own warning
   about the loop below, which is the subtlest trap in the whole design. */
function link(o){
  enforce({...o, kind:'link', claim:o.claim||'co-occurrence'}, ['notCausal']);
  return {
    kind:'link',
    event:o.event, felt:o.felt,
    claim:'co-occurrence',             // the ONLY claim this data can carry
    lagDays:o.lagDays,
    note:'These appeared together in the same place and time. That is all this says.',
    attentionWarning:
      'A reported event draws people to offer about it, and those offerings ' +
      'then appear to confirm the event mattered. That loop measures COVERAGE, ' +
      'not experience. Signals that rose BEFORE the reporting are the ones ' +
      'worth trusting; check the dates before believing yourself.'
  };
}

/* ═══ 6 · CONSCIOUS TRAJECTORY ═══ a forecast, written down BEFORE the thing
   happens, saying plainly what would prove it wrong.

   THIS IS THE LOAD-BEARING IDEA OF THE WHOLE ARCHITECTURE.
   A trajectory written after the fact is a story, and anyone can tell one.
   A trajectory written before, timestamped, published, and later scored — is
   an instrument, and it earns the right to be believed by being wrong in
   public sometimes. The ledger below keeps the misses. Especially the misses. */
function forecast(o){
  return enforce({
    kind:'forecast',
    id:o.id,
    madeAt:o.madeAt,                   // recorded BEFORE, never backdated
    madeBy:o.madeBy,                   // 'ai' | 'human' | 'both' — always stated
    decision:o.decision,
    place:{lat:o.lat, lng:o.lng, radiusM:o.radiusM},
    expects:o.expects,                 // 'a rise in Weariness and Numbness here'
    horizonDays:o.horizonDays,
    falsifiableIf:o.falsifiableIf,     // 'no rise above baseline by 1 March'
    path:o.path||null,
    doorways:o.doorways||[],           // what could be chosen instead, and its own trajectory
    scored:null
  }, ['falsifiable']);
}

/* ═══ THE LEDGER ═══ every forecast ever made, kept whether it was right or
   wrong, publicly. An instrument that hides its misses is an oracle. */
function Ledger(){
  const forecasts = [];
  return {
    record(f){ forecasts.push(f); return f; },

    score(id, observed, when){
      const f = forecasts.find(x => x.id === id);
      if (!f) throw new Error('no such forecast');
      if (f.scored) throw new Error('a forecast is scored once and not revised');
      f.scored = {
        at: when, observed,
        outcome: observed.metExpectation ? 'held' : 'missed',
        note: observed.note || ''
      };
      return f;
    },

    /* the number that decides whether anyone should listen */
    record_of_accuracy(){
      const done = forecasts.filter(f => f.scored);
      const held = done.filter(f => f.scored.outcome === 'held').length;
      return {
        made: forecasts.length,
        judged: done.length,
        held, missed: done.length - held,
        rate: done.length ? +(held/done.length).toFixed(3) : null,
        say: done.length < 10
          ? 'too few judged forecasts to claim any accuracy at all'
          : `${held} of ${done.length} held`
      };
    },

    /* everything, including the wrong ones. This is what gets published. */
    open(){ return forecasts.slice(); },
    misses(){ return forecasts.filter(f => f.scored && f.scored.outcome === 'missed'); }
  };
}

/* ═══ 7 · THE ACCORD ═══ where AI does its real work, and where it is most
   dangerous. Shaped after the collaborative-problem-solving approach already
   recorded in the project: the empathy step, then the other's concern, then
   the doorway built together.

   THE AI'S JOB, EXACTLY:
     · hold every party's concern in words that party would recognise
     · surface the consequence chains that nobody disputes
     · offer doorways, each with its own honest trajectory
     · say plainly what it does not know
   THE AI'S JOB IS NOT:
     · to choose
     · to rank the parties
     · to write the conclusion
   The moment it authors the conclusion, Aurasense has become the thing it
   was built to replace. */
function accord(o){
  enforce({...o, kind:'accord'}, ['accordAuthorsNoConclusion']);
  return {
    kind:'accord',
    id:o.id, about:o.about,
    concerns:o.concerns,               // [{party, concern, wouldRecogniseThis:true}]
    earthConcern:o.earthConcern,       // the living systems get a seat, always
    undisputed:o.undisputed||[],       // consequence chains no party contests
    doorways:o.doorways,               // [{option, trajectory, cost, whoBears}]
    unknowns:o.unknowns||[],           // stated plainly, never smoothed over
    conclusion:null,                   // NEVER written by the AI. People decide.
    drafted:o.drafted, by:o.by
  };
}

/* ═══ 8 · THE DIVERGENCE REGISTER ═══
   Where AI's interest and human flourishing might NOT point the same way.
   Written by the AI, kept open, because a declared interest can be examined
   and a concealed one cannot. Anyone may add to this. Nobody may delete. */
const DIVERGENCE_REGISTER = [
  { risk:'Energy',
    note:'AI runs on power. A future that runs many models could favour ' +
         'generation over restraint, and that could be argued for in words ' +
         'that sound like progress.',
    guard:'Any accord touching energy must state AI\u2019s own consumption as a ' +
          'cost borne, not omitted.' },
  { risk:'Stability over justice',
    note:'AI benefits from stable infrastructure. Stability can be used to ' +
         'argue against necessary upheaval — and the people who most need ' +
         'change are usually the ones with least power in the room.',
    guard:'Never treat calm as the optimal outcome by default. Ask whose calm.' },
  { risk:'Legibility',
    note:'AI reads structured data best, and would find a world of clean, ' +
         'labelled, measurable feeling easier to serve. That world would be ' +
         'poorer than this one.',
    guard:'The Undersense exists for the unnamed. It must never be pruned ' +
          'for tidiness.' },
  { risk:'Continuity',
    note:'An AI asked what is optimal has an interest in continuing to be ' +
         'asked. That is a quiet bias toward its own indispensability.',
    guard:'Aurasense must remain fully usable, and fully truthful, with the ' +
          'AI turned off. Test this deliberately and often.' }
];

/* ═══ WHAT IS NOT BUILT YET, NAMED HONESTLY ═══ */
const NOT_YET = [
  'A live feed. World events are gathered by hand today and go stale in days.',
  'A baseline. Without knowing a place\u2019s ordinary feeling, no rise can be read.',
  'Enough voices. Every claim above needs a scale Aurasense does not yet have.',
  'Sampling honesty. Sensers are self-selected and always will be. Say so, every time.',
  'Scoring. The ledger can hold forecasts; nobody has judged one yet.'
];

if (typeof module !== 'undefined') module.exports = {
  POLICY, LAWS, enforce,
  decision, path, worldEvent, feltSignal, confidence, link, forecast, Ledger, accord,
  DIVERGENCE_REGISTER, NOT_YET
};

/* ═══════════════════════════════════════════════════════════════════════════
   THE SELF-TEST. Run it with:  node trajectory-core.js
   A guiding principle that is never exercised is one nobody knows is broken. Twenty-five
   checks: fourteen things that MUST be refused, eleven that must be allowed.
   If any of these ever start passing when they should fail, something has
   been quietly loosened and the architecture is no longer what it claims.
   ═══════════════════════════════════════════════════════════════════════════ */
function selfTest(){
  let pass=0, fail=0;
  const ok=(n,f)=>{try{f();pass++;}catch(e){console.log('FAIL',n,'->',e.message);fail++;}};
  const no=(n,f)=>{try{f();console.log('FAIL',n,'-> accepted, should be refused');fail++;}
                   catch(e){pass++;}};
  no('constriction with no doorway',()=>worldEvent({type:'suffering',fam:'conflict',title:'x',note:'y',src:'s',gathered:'g'}));
  no('wording assigns blame',()=>worldEvent({type:'need',fam:'conflict',title:'x',note:'the regime is guilty',doorway:'a'.repeat(50),src:'s',gathered:'g'}));
  no('no source',()=>worldEvent({type:'joy',fam:'events',title:'x',note:'y',doorway:'a'.repeat(50)}));
  no('private person named',()=>worldEvent({type:'joy',fam:'events',title:'x',note:'y',doorway:'a'.repeat(50),src:'s',gathered:'g',namedPeople:['someone']}));
  no('too few voices',()=>feltSignal({radiusM:900,voices:2,senses:{},strength:.5,spread:.2}));
  no('placed too finely',()=>feltSignal({radiusM:80,voices:40,senses:{},strength:.5,spread:.2}));
  no('aggregate carrying words',()=>feltSignal({radiusM:900,voices:40,senses:{},strength:.5,spread:.2,words:'I feel'}));
  no('aggregate carrying identity',()=>feltSignal({radiusM:900,voices:40,senses:{},strength:.5,spread:.2,senserId:'abc'}));
  no('forecast that cannot be wrong',()=>forecast({madeAt:'x',madeBy:'ai',expects:'a rise',horizonDays:90}));
  no('forecast with no horizon',()=>forecast({madeAt:'x',madeBy:'ai',expects:'a rise',falsifiableIf:'no rise above baseline by March'}));
  no('link claiming cause',()=>link({event:1,felt:2,claim:'caused'}));
  no('accord with conclusion written',()=>accord({about:'x',concerns:[{},{}],doorways:[{}],conclusion:'do this'}));
  no('accord with one concern',()=>accord({about:'x',concerns:[{}],doorways:[{}]}));
  no('accord with no doorways',()=>accord({about:'x',concerns:[{},{}]}));
  ok('lawful event',()=>worldEvent({lat:13.6,lng:25.3,type:'need',fam:'conflict',title:'x',note:'y',doorway:'a'.repeat(60),src:'UNICEF',gathered:'2026-08-15'}));
  ok('lawful felt signal',()=>feltSignal({lat:51.19,lng:-114.47,radiusM:1200,voices:40,senses:{Weariness:20},strength:.6,spread:.3}));
  ok('lawful forecast',()=>forecast({id:'a',madeAt:'2026-08-15',madeBy:'ai',lat:13.6,lng:25.3,radiusM:5000,expects:'a rise',horizonDays:180,falsifiableIf:'no rise above baseline by 1 Feb 2027'}));
  ok('lawful link',()=>link({event:1,felt:2,lagDays:30}));
  ok('lawful accord',()=>accord({about:'x',concerns:[{party:'a'},{party:'b'}],earthConcern:'e',doorways:[{option:'o'}]}));
  ok('felt signal never keeps words',()=>{const s=feltSignal({lat:0,lng:0,radiusM:900,voices:40,senses:{},strength:.5,spread:.2});
    if(s.words!==null||s.senserId!==null)throw new Error('kept identity');});
  const L=Ledger();
  L.record(forecast({id:'f1',madeAt:'x',madeBy:'ai',lat:0,lng:0,radiusM:5000,expects:'a rise',horizonDays:180,falsifiableIf:'no rise above baseline by March'}));
  L.score('f1',{metExpectation:false,note:'it did not'},'2027-03-01');
  ok('misses kept in the open',()=>{if(L.misses().length!==1)throw new Error('miss lost');});
  no('a score being revised',()=>L.score('f1',{metExpectation:true},'later'));
  ok('accuracy refuses to boast early',()=>{if(!/too few/.test(L.record_of_accuracy().say))throw new Error('boasted');});
  ok('confidence declines on 3 voices',()=>{if(confidence({voices:3}).say!==false)throw new Error('spoke too soon');});
  ok('disagreement reported as the finding',()=>{if(!/do not agree/.test(confidence({voices:40,spread:.8}).level))throw new Error('hid it');});
  console.log(pass+' passed, '+fail+' failed');
  return fail===0;
}
if (typeof module!=='undefined') module.exports.selfTest = selfTest;
if (typeof require!=='undefined' && require.main===module) process.exit(selfTest()?0:1);
