"""Build 167 · the Mirror's listener (25 Oct 2026): charter G, heard on the real Claude before it goes live.
Karl, 23 Oct: a question asking him to swap places and imagine what someone else would want to hear did not make
sense to him. Charter G (F2, plus: one plain idea per question; never two questions joined; never a swapped place,
an imagined scene, or a guess at what others would say; never the words "picture" or "imagine" in a question; a
goodbye met with rest, never "when will you"). Tested on 25 Oct on thirteen invented conversations (G, then G2,
G3 and G4), live F2 alongside for comparison. Also a small safety net: a question repeated at the end of heard is
said once, below it, as it should be.
Always starts from the live 166 helper; re-runnable."""
import io, json

SRC = '/home/claude/work/mirror.166.js'
DST = '/home/claude/aurasense/functions/api/mirror.js'
CHARTER_TXT = '/home/claude/work/charter-g4.txt'
s = io.open(SRC, encoding='utf-8').read()

def rep(old, new, label, count=1):
    global s
    c = s.count(old)
    assert c == count, (label, c)
    s = s.replace(old, new)
    print('ok', label)

rep("""/* ═══ THE MIRROR'S LISTENER · Build 166 · 25 October 2026 · Karl with Claude""",
    """/* ═══ THE MIRROR'S LISTENER · Build 167 · 25 October 2026 · Karl with Claude""", 'title')
rep("""   Build 166: the signed self-test's time and signature travel as "at" and "seal" (the web reader drops some names).
""", """   Build 166: the signed self-test's time and signature travel as "at" and "seal" (the web reader drops some names).
   Build 167: charter G, heard first on the real Claude: one plain question at a time, never a swapped place or an
   imagined scene, and a goodbye met with rest. A question repeated inside heard is said once.
""", 'note 167')

# the charter: G4, as tested on 25 October
i = s.index("const CHARTER = [\n")
j = s.index("].join('\\n');", i)
lines = io.open(CHARTER_TXT, encoding='utf-8').read().rstrip('\n').split('\n')
assert lines[0].startswith('You are the listener in the Mirror') and lines[-1].startswith('Answer exactly once'), (lines[0][:40], lines[-1][:40])
s = s[:i] + "const CHARTER = [\n" + ',\n'.join(json.dumps(l, ensure_ascii=False) for l in lines) + "\n" + s[j:]
print('ok charter G in place,', len(lines), 'lines')
rep("""/* ── THE MIRROR'S CHARTER · Build 158, tuned on the real Claude in Builds 162, 163 and 164 ──────────────────""",
    """/* ── THE MIRROR'S CHARTER · Build 158, tuned on the real Claude in Builds 162, 163, 164 and 167 ────────────""", 'charter heading')

# the safety net: a question said once
rep("""function curly(x) { return String(x || '').replace(/"([^"\\n]{1,300})"/g, '“$1”').replace(/"/g, ''); }
""", """function curly(x) { return String(x || '').replace(/"([^"\\n]{1,300})"/g, '“$1”').replace(/"/g, ''); }
/* Build 167 · on 25 Oct the real Claude once ended heard with the very question shown below it, so the page said it
   twice. A sentence of heard that is the question again is let go; heard itself is never emptied. */
function unrepeat(heard, question) {
  const norm = (x) => String(x || '').toLowerCase().replace(/[^\\p{L}\\p{N}]+/gu, ' ').trim();
  const q = norm(question);
  if (!q || !heard) return heard;
  const parts = String(heard).match(/[^.!?]+[.!?]+[”’"]*\\s*|[^.!?]+$/g) || [String(heard)];
  const kept = parts.filter((p) => norm(p) !== q);
  return kept.length && kept.length < parts.length ? kept.join('').trim() : heard;
}
""", 'unrepeat')
rep("""  if (!out.care && !out.reflect && !out.question && !out.aspire) return { ok: false, code: 'empty', status: 200 };
  out.usage = j.usage || null;""",
    """  out.reflect = unrepeat(out.reflect, out.question);   /* Build 167 · the question is said once */
  if (!out.care && !out.reflect && !out.question && !out.aspire) return { ok: false, code: 'empty', status: 200 };
  out.usage = j.usage || null;""", 'question said once')
io.open(DST, 'w', encoding='utf-8').write(s)
print('written', DST, len(s))

def edit(src, dst, old, new, label):
    t = io.open(src, encoding='utf-8').read()
    assert t.count(old) == 1, (label, t.count(old))
    io.open(dst, 'w', encoding='utf-8').write(t.replace(old, new)); print('ok', label)
edit('/home/claude/work/index-mapbox.166.html', '/home/claude/aurasense/index-mapbox.html',
     'Build <span class="bs-l">25 Oct 2026 · </span>166<span class="bs-l"> · tap to refresh</span>',
     'Build <span class="bs-l">25 Oct 2026 · </span>167<span class="bs-l"> · tap to refresh</span>', 'map stamp')
edit('/home/claude/work/seeking.166.html', '/home/claude/aurasense/seeking.html',
     '>Build 25 Oct 2026 &middot; 166', '>Build 25 Oct 2026 &middot; 167', 'seeking stamp')
