"""Build 165, names from Build 166 · makes a signed address for the Mirror's private self-test (test-only: never part of the real site).
python3 selftest_url.py suite=keep branch=mirror-tests only=leaving-mum turns=6 budget=55 n=a1
The private signing key stays in /home/claude/work/keys/ (never printed, never copied into a file, a document, a
page or a message). What this prints is an address that works for ten minutes, for exactly this test."""
import sys, time, base64, urllib.parse
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature

KEY = '/home/claude/work/keys/selftest-signing.pem'

def signed(params):
    p = [('selftest', '1'), ('at', str(int(time.time())))] + [(k, v) for k, v in params if k not in ('selftest', 'at', 'seal', 'ts', 'sig')]
    msg = '&'.join(sorted(k + '=' + v for k, v in p)).encode('utf-8')
    k = serialization.load_pem_private_key(open(KEY, 'rb').read(), None)
    r, s = decode_dss_signature(k.sign(msg, ec.ECDSA(hashes.SHA256())))
    sig = base64.urlsafe_b64encode(r.to_bytes(32, 'big') + s.to_bytes(32, 'big')).rstrip(b'=').decode()
    return 'https://aurasense.app/api/mirror?' + urllib.parse.urlencode(p + [('seal', sig)], quote_via=urllib.parse.quote)

if __name__ == '__main__':
    print(signed([a.split('=', 1) for a in sys.argv[1:]]))
