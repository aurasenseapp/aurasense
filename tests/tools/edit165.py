"""Build 165 · the Mirror page (23 Oct 2026). Karl, of the little lights: "wondering if people would like to click
back, to see what they wrote and what was said. Or if this lack of review is a more suitable means of staying
present." Then: "Both at different times, I agree." and, of the hint: "Yes."
The little lights under the Mirror already hold each earlier moment. Once, on this device, a quiet line under them
says so: "Tap a light to see that moment again." It stays until a light is touched, the conversation rests, or two
more moments have come; never on a clock. Stamps 165. Always starts from the live 164 pages; re-runnable."""
import io

def edit(src, dst, pairs):
    s = io.open(src, encoding='utf-8').read()
    for old, new, label in pairs:
        c = s.count(old)
        assert c == 1, (label, c)
        s = s.replace(old, new)
        print('ok', label)
    io.open(dst, 'w', encoding='utf-8').write(s)
    print('written', dst, len(s))

edit('/home/claude/work/mirror-living.164.html', '/home/claude/aurasense/mirror-living.html', [
    ("""  23 Oct 2026 · Build 164: Keep what you found.""",
     """  23 Oct 2026 · Build 165: once, a quiet line under the little lights: "Tap a light to see that moment again."
  23 Oct 2026 · Build 164: Keep what you found.""",
     'note at the top'),
    (""".trail button:focus-visible{outline:2px solid var(--ink);outline-offset:3px}
""", """.trail button:focus-visible{outline:2px solid var(--ink);outline-offset:3px}
/* 23 Oct 2026 · Build 165 · once, a quiet line saying what the little lights hold */
.trailhint{margin:0 auto 6px;max-width:min(420px,90vw);font-size:.84rem;font-style:italic;color:var(--soft);text-align:center;opacity:0;transition:opacity .7s ease}
.trailhint.on{opacity:1}
@media (prefers-reduced-motion:reduce){.trailhint{transition:none}}
""", 'the hint, styled'),
    ("""  <div class="trail" id="trail" aria-label="Your turns so far"></div>
""", """  <div class="trail" id="trail" aria-label="Your turns so far"></div>
  <p class="trailhint" id="trailHint" hidden aria-hidden="true">Tap a light to see that moment again.</p>
""", 'the hint, placed'),
    ("""  b.addEventListener('click',function(){show(S.turns[i].parts,S.turns[i].rim);mark(i);});
  tr.appendChild(b);mark(i);
}
""", """  b.addEventListener('click',function(){show(S.turns[i].parts,S.turns[i].rim);mark(i);hintGo();});
  tr.appendChild(b);mark(i);hintCheck();
}
/* 23 Oct 2026 · Build 165 · Karl: "Both at different times, I agree." Presence during; a look back when wanted.
   Once on this device, when there is something to look back at, a quiet line says what the lights hold. It stays
   until a light is touched, the conversation rests, or two more moments have come; never on a clock.
   Its line is held open from the first moment of the conversation, so nothing on the page moves when it comes or goes. */
var TH={held:false,shown:false,at:0,gone:false};
function hintSeen(){try{return localStorage.getItem('as_trail_hint')==='1';}catch(e){return false;}}
function hintCheck(){var h=$('trailHint');if(!h)return;
  if(!TH.held){TH.held=true;if(hintSeen()){TH.gone=true;return;}h.hidden=false;}   /* the line's room, quietly kept */
  if(TH.gone)return;
  if(TH.shown){if(S.turns.length>=TH.at+2)hintGo();return;}
  if(S.turns.length<3||LS.heavy||LS.rest)return;
  TH.shown=true;TH.at=S.turns.length;try{localStorage.setItem('as_trail_hint','1');}catch(e){}
  h.removeAttribute('aria-hidden');requestAnimationFrame(function(){h.classList.add('on');});}
function hintGo(){var h=$('trailHint');if(!h||TH.gone)return;TH.gone=true;h.classList.remove('on');h.setAttribute('aria-hidden','true');}
""", 'the hint, once'),
    ("""function rest(){
  LS.gen++;""", """function rest(){
  hintGo();   /* 23 Oct 2026 · Build 165 */
  LS.gen++;""", 'the hint rests with the conversation'),
])
edit('/home/claude/work/index-mapbox.164.html', '/home/claude/aurasense/index-mapbox.html', [
    ('Build <span class="bs-l">23 Oct 2026 · </span>164<span class="bs-l"> · tap to refresh</span>',
     'Build <span class="bs-l">23 Oct 2026 · </span>165<span class="bs-l"> · tap to refresh</span>', 'map stamp')])
edit('/home/claude/work/seeking.164.html', '/home/claude/aurasense/seeking.html', [
    ('>Build 23 Oct 2026 &middot; 164', '>Build 23 Oct 2026 &middot; 165', 'seeking stamp')])
