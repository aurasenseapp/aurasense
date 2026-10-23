"""Build 163 · the Mirror's listener, from Karl's first conversation with Build 162 (23 Oct 2026).
Karl: "Some things sound out of context somehow." "The you who has come through this.. on repeat too."
His screenshots showed: after about six replies the whole conversation was summed up again on every turn; the wiser
self spoke too often in a long conversation; a tone he did not show was guessed ("You made a joke of it"); and asked
for a copy, the Mirror said the page could be copied (its earlier turns are not all shown).
Now: the landing is asked for once (at their sixth reply), and after it the Mirror follows what they bring, freshly;
the wiser self speaks at most three times in a conversation (twice already: only at a real turning point); charter E
(charter D, plus placing a feeling truly, which is where Karl's own relief began; landing once; no guessed tones; an
honest answer about keeping); "heard" is never empty; and the self-test can begin a conversation part-way, from an
invented history, so long conversations can be heard. Always starts from the live 162 helper; re-runnable."""
import io, json

SRC = '/home/claude/work/mirror.162.js'
DST = '/home/claude/aurasense/functions/api/mirror.js'
CHARTER_TXT = '/home/claude/work/charter-e.txt'
s = io.open(SRC, encoding='utf-8').read()

def rep(old, new, label, count=1):
    global s
    c = s.count(old)
    assert c == count, (label, c)
    s = s.replace(old, new)
    print('ok', label)

rep("""/* ═══ THE MIRROR'S LISTENER · Build 162 · 22 October 2026 · Karl with Claude""",
    """/* ═══ THE MIRROR'S LISTENER · Build 163 · 23 October 2026 · Karl with Claude""", 'title')
rep("""   Build 162: the charter tuned on the real Claude, heard on eleven invented conversations before Karl tries it.
""", """   Build 162: the charter tuned on the real Claude, heard on eleven invented conversations before Karl tries it.
   Build 163: from Karl's first conversation with 162: it lands once, then follows freshly; the wiser self speaks at
   most three times; no guessed tones; placing a feeling truly (where his own relief began).
""", 'note 163')

# the charter: replaced whole by charter E
i = s.index("const CHARTER = [\n")
j = s.index("].join('\\n');", i)
lines = io.open(CHARTER_TXT, encoding='utf-8').read().split('\n')
s = s[:i] + "const CHARTER = [\n" + ',\n'.join(json.dumps(l, ensure_ascii=False) for l in lines) + "\n" + s[j:]
print('ok charter E in place,', len(lines), 'lines')
rep("""/* ── THE MIRROR'S CHARTER · Build 158, tuned in Build 162 on the real Claude ──────────────────────────────""",
    """/* ── THE MIRROR'S CHARTER · Build 158, tuned on the real Claude in Builds 162 and 163 ───────────────────────""", 'charter heading')

rep("""      heard: { type: 'string', description: 'A few of their own words in curly quotation marks, and the heart of what you understood, in plain everyday words. One to three short sentences.' },""",
    """      heard: { type: 'string', description: 'A few of their own words in curly quotation marks, and the heart of what you understood, in plain everyday words. One to three short sentences. Never empty.' },""",
    'heard never empty')

rep("""  if (users >= 6) out.push('It is time to help it land (what they found, one small step, what has shifted), unless they have just opened something new and important.');""",
    """  /* Build 163 · Karl's screenshots: the whole conversation was summed up again on every turn after the sixth. Once only. */
  if (users === 6) out.push('It is time to help it land, once (what they found, one small step, what has shifted), unless they have just opened something new and important.');
  else if (users > 6) out.push('You have already been asked to help this conversation land. Do not sum up the whole conversation again, and do not repeat what was found earlier: answer what they bring now, freshly, as its own moment. Gather it all up again only if they say they are leaving, or ask for it.');""",
    'land once')
rep("""  if (last.indexOf(WISER) >= 0) out.push('Your last reply spoke as their wiser self. Leave wiser_self out this time.');""",
    """  const wisers = mine.filter((m) => m.content.indexOf(WISER) >= 0).length;   /* Build 163 · not on repeat */
  if (last.indexOf(WISER) >= 0) out.push('Your last reply spoke as their wiser self. Leave wiser_self out this time.');
  else if (wisers >= 3) out.push('Their wiser self has already spoken ' + wisers + ' times in this conversation. Leave wiser_self out from now on.');
  else if (wisers === 2) out.push('Their wiser self has already spoken twice in this conversation. Let it speak again only at a real turning point.');""",
    'wiser at most three times')

# the self-test can begin part-way, from an invented history
rep("""    const turns = [{ role: 'assistant', content: '[Written by the Mirror’s written rules, not by you:] ' + String(c.door || 'What’s here for you today?') }];""",
    """    const turns = [{ role: 'assistant', content: '[Written by the Mirror’s written rules, not by you:] ' + String(c.door || 'What’s here for you today?') }];
    (Array.isArray(c.history) ? c.history : []).slice(0, 24).forEach((t) => {   /* Build 163 · begin part-way: an invented conversation so far */
      if (t && (t.role === 'user' || t.role === 'assistant') && typeof t.content === 'string') turns.push({ role: t.role, content: t.content });
    });""", 'selftest history')

io.open(DST, 'w', encoding='utf-8').write(s)
print('written', DST, len(s))
