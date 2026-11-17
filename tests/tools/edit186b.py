# Build 186 (second part) · the Usability Law, question 6: "What does Calm Mode do to it? If the answer is nothing,
# the motion was never wired at its source." In Calm Mode, or with reduced motion, the waking light arrives whole and
# only swells: nothing spins up, and no ripples are sent.   python3 edit186b.py <site folder>
import sys,io
p=sys.argv[1].rstrip('/')+'/seeking.html'
s=io.open(p,encoding='utf8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:70]); s=s.replace(a,b)
rep("var qNight=false, qDusk=false,","var qCalm=false, qNight=false, qDusk=false,")
rep("  qDusk=!document.body.classList.contains('night');\n  qNight=true;",
    "  qDusk=!document.body.classList.contains('night');\n  qNight=true;\n  try{ qCalm=!!seekSmokeOff(); }catch(e){ qCalm=false; }   /* Calm Mode on the map behind, or reduced motion: the Law's question 6 */")
rep("  var vPace=qFade*(0.06+0.94*Math.pow(k,1.45));    /* speed of everything */",
    "  var vPace=qFade*(0.06+0.94*Math.pow(k,1.45));    /* speed of everything */\n  if(qCalm)vPace=qFade*0.06;                       /* Calm: it arrives whole and only swells; nothing quickens */")
rep("  if(ts-qLastRip>iv){ qLastRip=ts; qRips.push({age:0}); }",
    "  if(!qCalm&&ts-qLastRip>iv){ qLastRip=ts; qRips.push({age:0}); }   /* Calm: no ripples are sent */")
io.open(p,'w',encoding='utf8').write(s)
print('ok')
