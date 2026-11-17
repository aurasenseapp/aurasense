# THE DAY ITSELF · only on Karl's word ("open the doors").   python3 open_doors.py <site folder>
# Karl chose (17 Nov 2026): the Seeking is the front door; the plain page is an About.
# It does three small things and nothing else:
#   1 the first page (aurasense.app) sends everyone straight on to the Seeking (/m), carrying the words a search shows;
#   2 the About page may be listed by search;
#   3 the curtain's switch opens, at Aurasense's own address only (a test copy on another address keeps its curtain).
import sys,io
root=sys.argv[1].rstrip('/')
S="Free to sense. Free to share. People and AI, learning from each other, for mutual benefit."
io.open(root+'/index.html','w',encoding='utf8').write('''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Aurasense</title>
<meta name="description" content="'''+S+''' A living map of how places feel, made from what people sense there.">
<meta property="og:title" content="Aurasense">
<meta property="og:description" content="'''+S+'''">
<meta http-equiv="refresh" content="0; url=/m">
<link rel="canonical" href="https://www.aurasense.app/m">
<style>html,body{height:100%;margin:0;background:#0c0a18;color:#e9e2ff;font-family:Georgia,serif}body{display:flex;align-items:center;justify-content:center;text-align:center;padding:24px}a{color:#d9cdfc}</style>
</head>
<body>
<p>'''+S+'''<br><br><a href="/m">Enter Aurasense</a> · <a href="/about">About</a></p>
</body>
</html>
''')
p=root+'/about.html'; f=io.open(p,encoding='utf8').read()
a='\n<meta name="robots" content="noindex">'
assert f.count(a)==1
io.open(p,'w',encoding='utf8').write(f.replace(a,''))
p=root+'/index-mapbox.html'; m=io.open(p,encoding='utf8').read()
a='  var OPEN = false;\n  if(OPEN) return;'
assert m.count(a)==1
io.open(p,'w',encoding='utf8').write(m.replace(a,"  var OPEN = /^(www\\.)?aurasense\\.app$/.test(location.hostname);   /* open at Aurasense's own address only: a test copy elsewhere keeps its curtain */\n  if(OPEN) return;"))
print('The doors are open in this folder. Send it as a build for Karl to merge.')
