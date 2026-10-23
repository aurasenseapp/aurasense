import re, io, subprocess, sys, os, json
os.makedirs('/home/claude/work/chk', exist_ok=True)
for f in sys.argv[1:]:
    s = io.open(f, encoding='utf-8').read()
    cc = [m.start() for m in re.finditer(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', s)]
    if cc: print(f, 'STRAY CONTROL CHARACTERS at', cc[:8])
    blocks = re.findall(r'<script(?![^>]*\bsrc=)([^>]*)>(.*?)</script>', s, re.S); bad = 0; n = 0
    for i, (attrs, x) in enumerate(blocks):
        t = re.search(r'\btype\s*=\s*["\']?([^"\'\s>]+)', attrs)
        t = t.group(1).lower() if t else ''
        if t and t not in ('text/javascript', 'module', 'application/javascript'):
            if 'json' in t:
                try: json.loads(x)
                except Exception as e: bad += 1; print(f, 'data block', i, 'FAILED', str(e)[:200])
            continue
        n += 1
        p = '/home/claude/work/chk/c%d.js' % i; io.open(p, 'w', encoding='utf-8').write(x)
        r = subprocess.run(['node', '--check', p], capture_output=True, text=True)
        if r.returncode: bad += 1; print(f, 'script', i, 'FAILED', r.stderr[:400])
    print(f, n, 'scripts,', len(blocks) - n, 'data blocks,', bad, 'failed,', len(cc), 'stray characters')
