"""Build 169 · the Mirror (27 Oct 2026): draft 4 of Let it go, and the Stripe support link.
Karl on draft 3: "breath in on the crumple and out on the burning ... this needs to be really alive, enough to feel the
energy of its emotion being captured and written and then the release." And: "Just adding this for you now, in case
you can work it into what you are currently doing" (the Stripe link). The shared code (TP CSS and TP MODULE) is copied,
unchanged, from the tested study page. Listen Forward now opens Stripe, worded as payment for the listening just had
(Stripe: a tip is for a service already given). Privacy and terms say so. Always starts from the live build-168 files."""
import io
STUDY = '/home/claude/work/out/two-places/the-two-places.html'
W = '/home/claude/work/'; A = '/home/claude/aurasense/'
STRIPE = 'https://buy.stripe.com/aFacN7aoI9Eo6Ahale87K00'
st = io.open(STUDY, encoding='utf-8').read()
def between(text, a, b):
    i = text.index(a); j = text.index(b, i) + len(b); return text[i:j]
TP_CSS = between(st, '/* ══ TP CSS BEGIN', '/* ══ TP CSS END ══ */')
TP_MODULE = between(st, '/* ══ TP MODULE BEGIN', '/* ══ TP MODULE END ══ */')
assert 'function TwoPlaces(env)' in TP_MODULE and '.tpfx{' in TP_CSS and 'fireStep' in TP_MODULE and '.door.throw' in TP_CSS

def edit(name, pairs):
    t = io.open(W + name + '.168.html', encoding='utf-8').read()
    for old, new, label in pairs:
        c = t.count(old); assert c == 1, (name, label, c)
        t = t.replace(old, new); print('ok', name, label)
    io.open(A + name + '.html', 'w', encoding='utf-8').write(t)
    return t

m = io.open(W + 'mirror-living.168.html', encoding='utf-8').read()
OLD_CSS = between(m, '/* ══ TP CSS BEGIN', '/* ══ TP CSS END ══ */')
OLD_MOD = between(m, '/* ══ TP MODULE BEGIN', '/* ══ TP MODULE END ══ */')
GIFT_OLD = """  g.appendChild(el('p','','If you’d like, you can listen forward: keep it open for the next person.'));
  var row=el('div','row'),a=el('a','btn lead','Listen forward');a.href='https://ko-fi.com/aurasense';a.target='_blank';a.rel='noopener noreferrer';"""
GIFT_NEW = """  g.appendChild(el('p','','If it helped, you can pay what feels right for it, and keep it open for the next person.'));
  var row=el('div','row'),a=el('a','btn lead','Listen forward');a.href='""" + STRIPE + """';a.target='_blank';a.rel='noopener noreferrer';   /* 27 Oct 2026 · Build 169 · Stripe */"""
SMALL_OLD = "Listen forward opens Aurasense’s Ko-fi page. Support pays for Claude’s listening first, then Karl’s living and workspace as he builds Aurasense. Nothing changes if you don’t."
SMALL_NEW = "Listen forward opens a secure Stripe page where you choose the amount. It pays for the listening you’ve just had: Claude’s listening first, then Karl’s living and workspace as he builds Aurasense. Nothing changes if you don’t."
edit('mirror-living', [
  ("""  27 Oct 2026 · Build 168: the Mirror's two places. Let it go: the thought on paper, crumpled slowly, a deep breath,
  then into the fire, where the words char and fall away as ash and light. The Re-minding: folded, sealed, kept on
  this device for the moment it is needed. Nothing written in either ever leaves the device.
""", """  27 Oct 2026 · Build 168: the Mirror's two places. Let it go: the thought on paper, crumpled slowly, a deep breath,
  then into the fire, where the words char and fall away as ash and light. The Re-minding: folded, sealed, kept on
  this device for the moment it is needed. Nothing written in either ever leaves the device.
  27 Oct 2026 · Build 169: Let it go, draft 4. Dusk falls in the circle and a living fire burns at its foot; the words
  write themselves onto the paper; it crumples slowly on the breath in; it goes into the fire on the breath out, and
  the words glow, char and fall away. Listen Forward opens Stripe, where the person chooses the amount.
""", 'header note'),
  (OLD_CSS, TP_CSS, 'TP CSS'),
  (OLD_MOD, TP_MODULE, 'TP MODULE'),
  (GIFT_OLD, GIFT_NEW, 'listen forward: Stripe'),
  (SMALL_OLD, SMALL_NEW, 'listen forward: plain words'),
])
edit('index-mapbox', [('Build <span class="bs-l">27 Oct 2026 · </span>168<span class="bs-l"> · tap to refresh</span>',
     'Build <span class="bs-l">27 Oct 2026 · </span>169<span class="bs-l"> · tap to refresh</span>', 'map stamp')])
edit('seeking', [('>Build 27 Oct 2026 &middot; 168', '>Build 27 Oct 2026 &middot; 169', 'seeking stamp')])
edit('privacy', [
  ("Last updated: 23 October 2026.", "Last updated: 27 October 2026.", 'date'),
  ("""<li><strong>Ko-fi</strong>, with its payment partners (Stripe or PayPal) — only if you choose to support Aurasense. They handle the payment under their own terms, and we never see your card. We see only what Ko-fi shows us about a supporter, such as the name and message you choose to leave. United Kingdom and the United States.</li>""",
   """<li><strong>Stripe</strong> — only if you choose to pay for the listening you've had. Stripe handles the payment under its own terms, and we never see your card. We see only what Stripe shows us about a payment, such as the amount, the date, and the name and email address you give it. The United States and the other countries where Stripe operates.</li>""", 'Stripe, not Ko-fi'),
  ("for Anthropic your Mirror words if you choose Claude, in the <strong>United States</strong>", "for Anthropic your Mirror words if you choose Claude, for Stripe your payment if you choose to make one, in the <strong>United States</strong>", 'outside Canada'),
])
edit('terms', [
  ("Last updated: 22 October 2026.", "Last updated: 27 October 2026.", 'date'),
  ("""<p>You can support Aurasense through <a href="https://ko-fi.com/aurasense">Ko-fi</a>. Support is a <strong>gift, not a purchase</strong>: it buys nothing, unlocks nothing, and nothing changes for anyone who doesn't give. Aurasense is not a registered charity and can't give tax receipts. Ko-fi and its payment partners handle every payment under their own terms. If something goes wrong with a gift, write to hello@aurasense.app.</p>""",
   '<p>After the Mirror has listened to you, you can <strong>pay what feels right</strong> for that listening, through <a href="' + STRIPE + '" rel="noopener noreferrer">' + """a secure Stripe page</a> where you choose the amount. It is a thank-you for what you have already been given: it unlocks nothing, and nothing changes for anyone who doesn't pay. Aurasense is not a registered charity and can't give tax receipts. Stripe handles every payment under its own terms. If something goes wrong with a payment, write to hello@aurasense.app.</p>""", 'pay what feels right'),
])
print('done')
