/* Aurasense · the ideas page · Build 210 · 25 November 2026 · Karl with Claude
   Plain words only. Nothing is ever read back from the database, and nothing a visitor types is placed as HTML. */
(function () {
  'use strict';

  /* ONE LIST for all of Aurasense (Build 170): copied exactly from functions/api/mirror.js. Heavy words show real help. */
  const HEAVY = /\b(?:kill(?:ing)? my ?self|kms|unalive\w*|suicid\w*|end(?:ing)? (?:my (?:own )?life|it all)|(?:want(?:ing)?|wanna|going|ready|need) to end it(?: all| now| tonight| today)?(?!\s*(?:with|on|before|after|between|for|by|at|in|amicably|properly|early|there|here|so|because|but)\b)|take my (?:own )?life|(?:want(?:ing)?|wanna) (?:to )?die|(?:don'?t|do not|dont) want to (?:live|be here|be alive|exist|wake up(?=\s*(?:again|anymore|any more|tomorrow|ever|[.!?…]|$)))|wish (?:i|i'd) (?:was|were|had been) dead|wish i'?d never been born|hurt(?:ing)? my ?self|harm(?:ing)? my ?self|self[- ]?harm\w*|no reason to (?:live|go on)|better off (?:dead|without me))\b/i;
  function norm(t) { return String(t || '').replace(/[‘’ʼ]/g, "'"); }

  var G = window.AURASENSE_GATE || {};
  var READY = typeof G.url === 'string' && /^https:\/\/[a-z0-9]+\.supabase\.co$/.test(G.url) &&
              typeof G.key === 'string' && /^sb_publishable_[A-Za-z0-9_-]+$/.test(G.key);
  var $ = function (id) { return document.getElementById(id); };
  var form = $('idea-form'), idea = $('idea'), count = $('count'), reply = $('reply'), trap = $('website');
  var help = $('help'), status = $('status'), btn = $('sendbtn'), thanks = $('thanks'), again = $('another');
  if (!form || !idea) return;

  var KEEP = 'You can try again in a moment, or write to hello@aurasense.app.';
  function say(t) { status.textContent = t; }
  function fmt(n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ','); }
  function onInput() {
    count.textContent = fmt(idea.value.length) + ' of 4,000';
    if (HEAVY.test(norm(idea.value))) help.hidden = false;
  }
  idea.addEventListener('input', onInput);
  onInput();

  function done() {
    form.reset(); onInput(); help.hidden = true; say('');
    form.hidden = true; thanks.hidden = false;
    try { $('thanks-h').focus(); } catch (e) {}
  }
  again.addEventListener('click', function () {
    thanks.hidden = true; form.hidden = false; try { idea.focus(); } catch (e) {}
  });

  var busy = false;
  form.addEventListener('submit', function (ev) {
    ev.preventDefault();
    if (busy) return;
    if (trap && trap.value) { done(); return; }            /* a robot filled the hidden box: thank it, send nothing */
    var text = idea.value.replace(/\u0000/g, '').trim();
    if (text.length < 10) { say('A few more words, please: at least ten letters.'); idea.focus(); return; }
    if (text.length > 4000) { say('That is a little long: up to 4,000 letters, please.'); idea.focus(); return; }
    var picked = form.querySelector('input[name="kind"]:checked');
    var kind = picked && /^(person|ai|unsaid)$/.test(picked.value) ? picked.value : 'unsaid';
    var back = reply.value.trim().slice(0, 200) || null;
    if (!READY || !window.fetch) { say('It could not be sent just now. Your words are still here. ' + KEEP); return; }

    busy = true; btn.disabled = true; say('Sending…');
    var ctl = window.AbortController ? new AbortController() : null;
    var timer = setTimeout(function () { if (ctl) ctl.abort(); }, 15000);
    fetch(G.url + '/rest/v1/ideas', {
      method: 'POST',
      headers: { 'apikey': G.key, 'Content-Type': 'application/json', 'Prefer': 'return=minimal' },
      body: JSON.stringify({ from_kind: kind, idea: text, reply_to: back }),
      credentials: 'omit', cache: 'no-store', referrerPolicy: 'no-referrer', redirect: 'error',
      signal: ctl ? ctl.signal : undefined
    }).then(function (r) {
      if (r.ok) { done(); return; }
      return r.text().then(function (body) {
        var m = '';
        try { m = String((JSON.parse(body) || {}).message || ''); } catch (e) {}
        if (/already received/.test(m)) { done(); return; }
        if (/resting/.test(m)) { say('Many ideas have arrived in the last few minutes, so the box is resting. Please try again in ten minutes. Your words are still here.'); return; }
        say('It could not be sent just now. Your words are still here. ' + KEEP);
      });
    }).catch(function () {
      say('It could not be sent just now. Your words are still here. ' + KEEP);
    }).then(function () {
      clearTimeout(timer); busy = false; btn.disabled = false;
    });
  });
})();
