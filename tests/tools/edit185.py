# Build 185 · Karl, 17 Nov 2026: the Seeking's countdown is seen (larger, white, above the finger).   python3 edit185.py <site folder>
import sys,io
p=sys.argv[1].rstrip('/')+'/seeking.html'
s=io.open(p,encoding='utf8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:60]); s=s.replace(a,b)
rep("body.night #qNum.on{opacity:.46}",
"""body.night #qNum.on{opacity:.46}
/* Build 185 · Karl, 17 Nov 2026: "The countdown not visible properly. Not white enough or large enough or both";
   "The thumb hides it too". The number is now large and white with a dark halo, so it reads over any colour, and it
   rides just above the finger (a small script below places it), where a thumb cannot cover it. */
#qNum{z-index:9;font-size:clamp(34px,10vmin,56px);font-weight:500;letter-spacing:.04em;color:#fff;
  text-shadow:0 0 3px rgba(44,28,92,.98),0 0 9px rgba(44,28,92,.9),0 0 22px rgba(44,28,92,.7),0 0 44px rgba(44,28,92,.45)}
#qNum.on,body.night #qNum.on{opacity:1}
body.night #qNum{color:#fff;text-shadow:0 0 3px rgba(8,6,20,.98),0 0 10px rgba(8,6,20,.9),0 0 24px rgba(8,6,20,.7)}""")
a="</body>"
assert s.count(a)==1
s=s.replace(a,"""<script>
/* Build 185 · the countdown rides above the finger. It only moves the number; the countdown itself is untouched. */
(function(){
  try{
    var n=document.getElementById('qNum'),w=document.getElementById('ringWrap'); if(!n||!w)return;
    function place(e){
      try{
        if(e.type!=='pointerdown'&&!n.classList.contains('on'))return;
        var r=w.getBoundingClientRect(); if(!r.width)return;
        var lift=(e.pointerType==='mouse')?Math.max(54,r.height*0.2):Math.max(84,r.height*0.3);   /* a thumb covers more than a pointer */
        var x=Math.min(Math.max(e.clientX,36),window.innerWidth-36), y=e.clientY-lift;
        if(y<44)y=e.clientY+lift;                                    /* no room above: it shows below instead */
        n.style.left=(x-r.left)+'px'; n.style.top=(y-r.top)+'px';
      }catch(_){}
    }
    document.addEventListener('pointerdown',place,{passive:true,capture:true});
    document.addEventListener('pointermove',place,{passive:true,capture:true});
  }catch(e){}
})();
</script>
</body>""")
io.open(p,'w',encoding='utf8').write(s)
print('ok')
