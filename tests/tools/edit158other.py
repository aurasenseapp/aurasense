"""Build 158 · privacy and terms without the written rules as a choice; stamps 158. From the live 157 pages; re-runnable."""
import io
def edit(src, dst, pairs):
    s = io.open(src, encoding='utf-8').read()
    for old, new, label in pairs:
        c = s.count(old); assert c == 1, (label, c); s = s.replace(old, new); print('ok', label)
    io.open(dst, 'w', encoding='utf-8').write(s); print('written', dst, len(s))
W = '/home/claude/work/'; A = '/home/claude/aurasense/'
edit(W + 'privacy.157.html', A + 'privacy.html', [
    ("<li><strong>In the Mirror, you choose who listens.</strong> With the written rules, nothing leaves your device. If you choose Claude, an AI, your words go to it only to shape each reply: <strong>Aurasense keeps nothing</strong>, and your words are not used to train AI.</li>",
     "<li><strong>In the Mirror, Claude, an AI, listens only if you choose to begin.</strong> Your words go to it only to shape each reply: <strong>Aurasense keeps nothing</strong>, and your words are not used to train AI.</li>", 'short version'),
    ("<p>Your Mirror conversations when the written rules answer, your well-being and Aurawellness notes,",
     "<p>Your well-being and Aurawellness notes,", 'kept on the device'),
    ("<li>Before anything you write leaves the page, the Mirror asks who you would like to listen: <strong>Claude</strong>, an AI made by Anthropic, or the Mirror's <strong>written rules</strong>, which run on your own device. Your choice is remembered on your device, and you can change it at any moment from the line beneath the Mirror.</li>",
     "<li>Before anything you write leaves the page, the Mirror asks whether you would like <strong>Claude</strong>, an AI made by Anthropic, to listen. <strong>If you say not now, nothing leaves.</strong> Your yes is remembered on your device, and you can take it back at any moment with <em>Stop sharing my words</em>, beneath the Mirror.</li>", 'the Mirror asks first'),
])
edit(W + 'terms.157.html', A + 'terms.html', [
    ("<li>In the Mirror, you choose who listens: its written rules, or Claude, an AI. Either way, it reflects; it never advises.</li>",
     "<li>In the Mirror, Claude, an AI, listens only if you choose to begin. It reflects; it never advises.</li>", 'short version'),
    ("including the Mirror, whether its written rules or Claude, an AI, are answering, and any reflective feature",
     "including the Mirror, where Claude, an AI, answers, and any reflective feature", 'not advice'),
])
edit(W + 'index-mapbox.157.html', A + 'index-mapbox.html', [
    ('Build <span class="bs-l">22 Oct 2026 · </span>157<span class="bs-l"> · tap to refresh</span>',
     'Build <span class="bs-l">22 Oct 2026 · </span>158<span class="bs-l"> · tap to refresh</span>', 'map stamp')])
edit(W + 'seeking.157.html', A + 'seeking.html', [('>Build 22 Oct 2026 &middot; 157', '>Build 22 Oct 2026 &middot; 158', 'seeking stamp')])
