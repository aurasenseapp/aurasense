"""Builds the Alphasense study page (one symbol at a time) from the site's own symbols, words and bonds.
The data (alpha-data.json) was read from the live map page in a test browser and is embedded unchanged.
The two drawing functions are copied verbatim from the live map page, so the study draws exactly as the site does."""
import io, json, re
SRC = '/home/claude/aurasense/index-mapbox.html'
OUT = '/home/claude/work/out/alphasense/'
D = json.load(io.open(OUT + 'alpha-data.json', encoding='utf-8'))
site = io.open(SRC, encoding='utf-8').read()

def lift(name):
    m = re.search(r'\nfunction ' + name + r'\([^)]*\)\{.*?\n\}\n', site, re.S)
    assert m, name
    return m.group(0).strip()
ag, fg = lift('alphaGlyph'), lift('fuseGlyphs')
assert 'drop-shadow' in ag and 'linearGradient' in fg

# checks on the data the page relies on
for s in D['senses']:
    assert 'width="22" height="22"' in D['symbols'].get(s['id'], ''), s['id']
names = {w['w'] for w in D['words']}
missing_doors = sorted({w['door'] for w in D['words'] if w.get('door') and w['door'] not in names})
missing_bonds = [j for j in D['junctions'] if j[0] not in names or j[1] not in names]
print('doorways that are not words:', missing_doors)
print('bonds missing a word:', missing_bonds)

data = json.dumps(D, ensure_ascii=False).replace('</', '<\\/')   # nothing in the data can close the script early
page = io.open(OUT + 'template.html', encoding='utf-8').read()
for k in ('/*__DATA__*/null', '/*__ALPHAGLYPH__*/', '/*__FUSEGLYPHS__*/'):
    assert page.count(k) == 1, k
page = page.replace('/*__ALPHAGLYPH__*/', ag).replace('/*__FUSEGLYPHS__*/', fg).replace('/*__DATA__*/null', data)
io.open(OUT + 'alphasense-one-by-one.html', 'w', encoding='utf-8').write(page)
# a local copy wrapped the way the artifact host wraps a page, for the walk only
shell = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
         '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
         '<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}'
         'body{margin:0;font:14px system-ui,sans-serif}img{max-width:100%}[hidden]{display:none!important}</style>'
         '</head><body>' + page + '</body></html>')
io.open(OUT + 'walk-copy.html', 'w', encoding='utf-8').write(shell)
print('written', len(page))
