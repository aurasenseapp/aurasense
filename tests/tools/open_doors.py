# THE DAY ITSELF · only on Karl's word ("open the doors").   python3 open_doors.py <site folder>
# It does two things and nothing else: the front door becomes the first page, and the curtain's switch says true.
import sys,io
root=sys.argv[1].rstrip('/')
f=io.open(root+'/front.html',encoding='utf8').read()
a='\n<meta name="robots" content="noindex">'
assert f.count(a)==1
io.open(root+'/index.html','w',encoding='utf8').write(f.replace(a,''))
p=root+'/index-mapbox.html'; m=io.open(p,encoding='utf8').read()
a='  var OPEN = false;\n  if(OPEN) return;'
assert m.count(a)==1
io.open(p,'w',encoding='utf8').write(m.replace(a,'  var OPEN = true;\n  if(OPEN) return;'))
print('The doors are open in this folder. Send it as a build for Karl to merge.')
