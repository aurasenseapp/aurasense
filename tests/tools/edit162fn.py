"""Build 162 · the Mirror's charter, tuned on the real Claude before Karl tries it (22 Oct 2026).
Karl, after Build 157: "It needs way more intelligence and responsiveness." "The mirror has to reflect the Philosophy
written thus far, pointing towards the light, self awareness and understanding and recognition that thoughts are
internal environment noise not identity." "Establish what their future aspired self would say back to them in this
moment ... and say it, help guide them towards this light. Not simply to gratify ego fulfilment - but to take them
through that and beyond."
Charter D, chosen from four drafts heard on eleven invented conversations with Sonnet 5.5 (tests/mirror on the
mirror-tests branch): their words woven in, never "You said" every time; the wiser self speaking when a feeling,
struggle or choice matters (about one reply in three, and a last word as it lands); what is hardest to feel met as a
part asking to be seen; looking freshly, before the old words; senses met simply, never as a "report"; one short
question. The page shows the wiser voice after its own line ("The you who has come through this might say:"), so any
introduction Claude writes itself is let go. Always starts from the live 161 helper; re-runnable."""
import io, json

SRC = '/home/claude/work/mirror.161.js'
DST = '/home/claude/aurasense/functions/api/mirror.js'
CHARTER_TXT = '/home/claude/work/charter-d.txt'
s = io.open(SRC, encoding='utf-8').read()

def rep(old, new, label, count=1):
    global s
    c = s.count(old)
    assert c == count, (label, c)
    s = s.replace(old, new)
    print('ok', label)

rep("""/* ═══ THE MIRROR'S LISTENER · Build 161 · 22 October 2026 · Karl with Claude""",
    """/* ═══ THE MIRROR'S LISTENER · Build 162 · 22 October 2026 · Karl with Claude""", 'title')
rep("""   Build 161: the self-test can run whole conversations in the background (later=1, then job=).
""", """   Build 161: the self-test can run whole conversations in the background (later=1, then job=).
   Build 162: the charter tuned on the real Claude, heard on eleven invented conversations before Karl tries it.
""", 'note 162')

# the charter: replaced whole by charter D (one line per array entry, written as JSON strings)
i = s.index("const CHARTER = [\n")
j = s.index("].join('\\n');", i)
lines = io.open(CHARTER_TXT, encoding='utf-8').read().split('\n')
body = "const CHARTER = [\n" + ',\n'.join(json.dumps(l, ensure_ascii=False) for l in lines) + "\n"
s = s[:i] + body + s[j:]
print('ok charter D in place,', len(lines), 'lines')

rep("""/* ── THE MIRROR'S CHARTER · Build 158 · rewritten around the founding philosophy ─────────────────────────""",
    """/* ── THE MIRROR'S CHARTER · Build 158, tuned in Build 162 on the real Claude ──────────────────────────────""", 'charter heading')

rep("""      wiser_self: { type: 'string', description: 'Include only when it will truly help, and never in two replies running: what the self they are growing into would say to them now, in one to three plain sentences. Leave this field out entirely otherwise.' },""",
    """      wiser_self: { type: 'string', description: 'When they name a feeling, a struggle or a choice that matters, about one reply in three, and never in two replies running: what the self they are growing into would say to them now, in one to three plain sentences. Only its words: the page introduces them. Leave this field out entirely otherwise.' },""",
    'wiser field')

rep("""    aspire: whole(curly(real(s(v.wiser_self || v.aspire), 3)), 480),""",
    """    aspire: whole(curly(real(bare(s(v.wiser_self || v.aspire)), 3)), 480),""", 'wiser words only')
rep("""function real(x, minWords) {""",
    """/* Build 162 · the page introduces the wiser voice itself, so an introduction Claude writes ("The one you are growing
   into might say:") is let go, never shown twice */
const INTRO = /^\\s*(?:the (?:you|one|self|person)\\b[^:.!?]{0,80}\\b(?:might|would|could|will) say\\s*:?|your (?:wiser|future) self (?:might|would|could) say\\s*:?)\\s*/i;
function bare(x) { return String(x || '').replace(INTRO, '').replace(/^\\s*[a-z]/, (c) => c.toUpperCase()); }
function real(x, minWords) {""", 'bare()')

io.open(DST, 'w', encoding='utf-8').write(s)
print('written', DST, len(s))
