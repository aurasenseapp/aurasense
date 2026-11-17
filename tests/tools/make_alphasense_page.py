# Build 188 · Alphasense One by One becomes a page of the site (standing alone, not linked, not listed), made from
# Claude's study of 28 October 2026 (the artifact "Alphasense One by One").   python3 make_alphasense_page.py <study.html> <site folder>
import sys,io,re,json
src=io.open(sys.argv[1],encoding='utf8').read(); site=sys.argv[2].rstrip('/')
L=src.split('\n')
def find(tag,start=0):
    for i in range(start,len(L)):
        if L[i].strip().startswith(tag): return i
    raise SystemExit('missing '+tag)
s0=find('<style>',1); s1=find('</style>',s0); m0=find('<main',s1); m1=find('</main>',m0); j0=find('<script>',m1); j1=find('</script>',j0)
style='\n'.join(L[s0+1:s1]); main='\n'.join(L[m0:m1+1]); script='\n'.join(L[j0+1:j1])
assert 'http://' not in style+main+script and 'https://' not in style+main+script, 'the study must reach for nothing outside itself'
assert 'eval(' not in script and 'new Function' not in script and 'window.claude' not in script
head='''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; img-src data:; base-uri 'none'; form-action 'none'">
<meta name="referrer" content="no-referrer">
<meta name="robots" content="noindex">
<title>Alphasense One by One</title>
<meta name="description" content="Alphasense, one symbol at a time: each sensed before it is named.">
<!--
  ALPHASENSE ONE BY ONE · Build 188 · 17 November 2026 · Karl with Claude
  Claude's study of 28 October 2026, brought into the site as its own page so Karl can feel it at a real address.
  It stands alone: nothing links to it yet, and search is asked not to list it. It asks for nothing, sends nothing,
  and reaches for nothing outside itself (the rule above allows no connection at all).
  What a person has seen is remembered on their own device only.
-->
<style>
'''
back='''
/* Build 188 · a quiet way home */
.as-home{display:block;margin:26px auto 30px;text-align:center;font:15px/1.5 var(--serif);color:var(--soft)}
.as-home a{color:inherit;text-underline-offset:3px}
'''
out=head+style+back+'</style>\n</head>\n<body>\n'+main.replace('</main>','  <p class="as-home"><a href="/about">About Aurasense</a></p>\n</main>')+'\n<script>\n'+script+'\n</script>\n</body>\n</html>\n'
old='A study to feel · not yet on the site'
assert out.count(old)==1, 'the study\'s first line has changed'
out=out.replace(old,'One symbol at a time')
io.open(site+'/alphasense.html','w',encoding='utf8').write(out)
j=json.load(io.open(site+'/alphasense.json',encoding='utf8'))
names=[w.get('name') or w.get('w') or w.get('word') for w in j['words']]
miss=[n for n in names if n and n not in out]
print('written', len(out), 'bytes; words today', len(names), '; missing from the page', len(miss), miss[:10])
