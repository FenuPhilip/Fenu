#!/usr/bin/env python3
"""
1) Removes the Visits / Skills counters from the hero (the footer V###.io stays).
2) Replaces the role capsule with the role text as graffiti behind the hero.
   The words still come from profile.role (split on | , / or a dot).
Run from the project root:   python hero_graffiti.py
(or:  python hero_graffiti.py path/to/home.html)
"""
import re, sys, shutil, pathlib

p = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'templates/home.html')
if not p.exists():
    sys.exit('Cannot find ' + str(p) + ' - run this from the folder that contains manage.py')
s = p.read_text(encoding='utf-8')
if 'FP-WALL' in s:
    sys.exit('Graffiti already installed.')


def sub(old, new):
    global s
    if s.count(old) != 1:
        sys.exit('Anchor not found exactly once, nothing written:\n  ' + old[:70])
    s = s.replace(old, new, 1)


CSS = r"""
/* FP-WALL */
.sr-only{position:absolute;width:1px;height:1px;margin:-1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.wall{position:absolute;inset:0;z-index:-1;overflow:hidden;pointer-events:none;user-select:none;-webkit-user-select:none}
.wall::after{content:"";position:absolute;inset:0;background:radial-gradient(circle at 74% 24%,rgba(47,60,255,.35) 0 9px,transparent 10px),radial-gradient(circle at 78% 30%,rgba(255,197,46,.7) 0 5px,transparent 6px),radial-gradient(circle at 70% 31%,rgba(21,19,59,.3) 0 3px,transparent 4px),radial-gradient(circle at 18% 70%,rgba(255,197,46,.6) 0 7px,transparent 8px),radial-gradient(circle at 22% 66%,rgba(47,60,255,.3) 0 3px,transparent 4px)}
.wall-in{position:absolute;left:-3%;top:9%;display:grid;justify-items:start;transform:translate(calc(var(--wx,0)*-18px),calc(var(--wy,0)*-12px)) rotate(-6deg);transform-origin:0 0}
.wall .g{display:block;font:800 clamp(4.2rem,15.5vw,15rem)/.8 var(--display);font-stretch:75%;letter-spacing:-.02em;text-transform:uppercase;white-space:nowrap;color:transparent;-webkit-text-stroke:2px rgba(21,19,59,.3);text-shadow:.045em .045em 0 rgba(21,19,59,.07);animation:paint 1.1s var(--ease) both;animation-delay:calc(var(--i)*.22s + .25s)}
.wall .g1{margin-left:8%;-webkit-text-stroke-color:rgba(47,60,255,.4);text-shadow:.045em .045em 0 rgba(47,60,255,.12)}
.wall .g2{margin-left:2%;color:rgba(255,197,46,.55);-webkit-text-stroke:0;text-shadow:none;-webkit-mask:radial-gradient(circle,#000 58%,transparent 64%) 0 0/7px 7px;mask:radial-gradient(circle,#000 58%,transparent 64%) 0 0/7px 7px}
@keyframes paint{from{clip-path:inset(-10% 101% -10% -2%)}to{clip-path:inset(-10% -6% -10% -2%)}}
.drips{position:absolute;left:0;right:0;top:100%;height:0}
.drips i{position:absolute;top:0;width:8px;height:var(--h);border-radius:0 0 8px 8px;background:rgba(47,60,255,.4);transform-origin:top;animation:drip 1.4s var(--ease) both;animation-delay:calc(1.4s + var(--d))}
@keyframes drip{from{transform:scaleY(0)}}
.spk{position:absolute;width:34px;height:34px;background:var(--sun);clip-path:polygon(50% 0,62% 38%,100% 50%,62% 62%,50% 100%,38% 62%,0 50%,38% 38%);transform:scale(var(--s,1));animation:spin 6s linear infinite}
@keyframes spin{to{transform:scale(var(--s,1)) rotate(360deg)}}
"""

JS = r"""/* FP-WALL: the role text as graffiti behind the hero */
  (function(){
    var w=d.querySelector('.wall');if(!w)return;
    var parts=(w.getAttribute('data-role')||w.textContent).split(/\s*[|\u2022\u00b7\/,]\s*/).map(function(t){return t.trim()}).filter(Boolean).slice(0,4);
    if(!parts.length)return;
    var dr='',k;
    for(k=0;k<7;k++)dr+='<i style="left:'+(6+k*11+(k*7)%9)+'%;--h:'+(26+(k*37)%58)+'px;--d:'+(k*.17).toFixed(2)+'s"></i>';
    w.innerHTML='<div class="wall-in">'+parts.map(function(t,i){return '<span class="g g'+(i%3)+'" style="--i:'+i+'">'+esc(t)+'</span>'}).join('')+'<div class="drips">'+dr+'</div></div>'+
      '<b class="spk" style="left:57%;top:13%"></b><b class="spk" style="left:88%;top:58%;--s:.6"></b>';
    if(!reduce)addEventListener('pointermove',function(e){
      w.style.setProperty('--wx',((e.clientX/innerWidth-.5)*2).toFixed(2));
      w.style.setProperty('--wy',((e.clientY/innerHeight-.5)*2).toFixed(2));
    },{passive:true});
  })();

  /* Init */"""

# 1) remove the counters
s, n = re.subn(r'[ \t]*<div class="stats">\n(?:[ \t]*<div class="stat">[^\n]*</div>\n)+[ \t]*</div>\n', '', s, count=1)
if n != 1:
    sys.exit('Could not find the counters block. Nothing was changed.')

# 2) capsule -> hidden text for screen readers + graffiti wall
sub('<span class="role">{{ profile.role }}</span>', '<span class="sr-only">{{ profile.role }}</span>')
sub('<div class="stk" aria-hidden="true"></div>',
    '<div class="stk" aria-hidden="true"></div>\n    <div class="wall" aria-hidden="true" data-role="{{ profile.role }}"><span class="g g1">{{ profile.role }}</span></div>')
sub('/* Init */', JS)
sub('</style>', CSS + '</style>')

shutil.copy(p, p.with_name(p.name + '.bak6'))
p.write_text(s, encoding='utf-8')
print('Done. Backup saved as ' + p.name + '.bak6. Push to Render and hard-refresh (Ctrl+Shift+R).')