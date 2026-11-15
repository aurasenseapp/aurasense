"""Build 174 · makes alphasense.json from the map's own alphabet, and keeps the new Mirror page's heavy-words list
letter for letter the same as the helper's (one list, never two that drift).
python3 make_mirror_data.py [site folder]      (test-only tool: never part of the real site)"""
import io, re, sys, json
SITE = (sys.argv[1] if len(sys.argv) > 1 else '/home/claude/aurasense').rstrip('/') + '/'
m = io.open(SITE + 'index-mapbox.html', encoding='utf-8').read()
blk = m[m.index('const ALPHA_WORDS=['):m.index('const ALPHA_CHAPTERS=')]
chap = json.loads(re.search(r'const ALPHA_CHAPTERS=(\[.*?\]);', m, flags=re.S).group(1))
un = lambda t: t.replace('\\u2019', '’').replace('\\u2014', '—').replace("\\'", "'")
words = []
for x in re.finditer(r"\{w:(['\"])(.*?)\1,c:['\"](#[0-9a-fA-F]{6})['\"],d:(['\"])(.*?)\4(.*?)\},?\s*\n", blk, flags=re.S):
    rest = x.group(6)
    g = re.search(r"g:'([^']*)'", rest)
    fam = re.search(r'fam:"([a-z]+)"', rest)
    door = re.search(r'door:"([^"]*)"', rest)
    src = re.search(r'src:"([^"]*)"', rest)
    w = {'w': un(x.group(2)), 'c': x.group(3).lower(), 'd': un(x.group(5)), 'fam': fam.group(1) if fam else 'first', 'g': g.group(1) if g else ''}
    if door: w['door'] = un(door.group(1))
    if src: w['src'] = un(src.group(1))
    words.append(w)
assert len(words) == 130, len(words)
OKG = re.compile(r'^(?:<(?:path|circle|line|ellipse|rect|polyline|polygon)(?: (?:d|cx|cy|r|rx|ry|x|y|x1|y1|x2|y2|width|height|points|opacity|class|transform|stroke-width|stroke-dasharray|stroke-linecap|fill)="[A-Za-z0-9 .,#()\-]*")+/>)+$')
bad = [w['w'] for w in words if not OKG.match(w['g'])]
assert not bad, ('a symbol the page would refuse to draw', bad[:5])
names = set(w['w'] for w in words)
assert all(w.get('door', w['w']) in names for w in words), 'every doorway is a word in the alphabet'
io.open(SITE + 'alphasense.json', 'w', encoding='utf-8').write(json.dumps({'note': 'The Alphasense alphabet, exactly as the map carries it. Made by a tool from the map; never edited by hand.', 'chapters': chap, 'words': words}, ensure_ascii=False, separators=(',', ':')) + '\n')
# one heavy-words list
h = io.open(SITE + 'functions/api/mirror.js', encoding='utf-8').read()
heavy = re.search(r'^const HEAVY = (/.*/i);$', h, flags=re.M).group(1)
p = SITE + 'mirror.html'
s = io.open(p, encoding='utf-8').read()
s2, n = re.subn(r'^var HEAVY=/.*/i;.*$', lambda _: 'var HEAVY=' + heavy + ';   /* the helper\'s own list, letter for letter (a tool keeps them the same) */', s, flags=re.M)
assert n == 1, n
io.open(p, 'w', encoding='utf-8').write(s2)
print('alphasense.json: %d words, %d chapters; heavy list in step' % (len(words), len(chap)))
