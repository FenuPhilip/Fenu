#!/usr/bin/env python3
"""
1) Adds a hammer: pick it up, smash the pixel portrait, pixels break off, fall
   and bounce, and your real photo shows where they were.
2) Removes the pixel studio (section, CSS, JS, palette entry).
Run from the project root:   python add_hammer.py
(or:  python add_hammer.py path/to/home.html)
"""
import re, sys, shutil, pathlib

p = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'templates/home.html')
if not p.exists():
    sys.exit('Cannot find ' + str(p) + ' - run this from the folder that contains manage.py')
s = p.read_text(encoding='utf-8')
if 'FP-HAMMER' in s:
    sys.exit('Hammer already installed.')


def sub(old, new):
    global s
    if s.count(old) != 1:
        sys.exit('Anchor not found exactly once, nothing written:\n  ' + old[:70])
    s = s.replace(old, new, 1)


def cut(pattern, minimum, flags=0):
    global s
    s, n = re.subn(pattern, '', s, flags=flags)
    if n < minimum:
        sys.exit('Could not remove expected pixel-studio code (' + pattern[:40] + '). Nothing written.')


CSS = r"""
/* FP-HAMMER */
.real{-webkit-mask-image:radial-gradient(circle var(--rr,0px) at var(--rx,-99px) var(--ry,-99px),#000 55%,transparent 100%),var(--holes,none);mask-image:radial-gradient(circle var(--rr,0px) at var(--rx,-99px) var(--ry,-99px),#000 55%,transparent 100%),var(--holes,none);-webkit-mask-size:auto,100% 100%;mask-size:auto,100% 100%;-webkit-mask-repeat:no-repeat;mask-repeat:no-repeat}
.hrow{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin-top:18px}
.hbtn{display:inline-flex;align-items:center;gap:8px;padding:.55em 1.1em;font:600 .9rem/1 var(--display);background:var(--paper);border:2px solid var(--ink);border-radius:99px;box-shadow:3px 3px 0 var(--ink);transition:transform .2s var(--ease),box-shadow .2s var(--ease)}
.hbtn:hover{transform:translate(-2px,-2px);box-shadow:5px 5px 0 var(--ink)}
.hbtn[aria-pressed=true]{background:var(--sun)}
.hbtn img{width:18px;height:24px;image-rendering:pixelated}
.hammer{position:fixed;left:0;top:0;z-index:99;width:60px;height:80px;transform-origin:30px 76px;pointer-events:none;will-change:transform}
.hammer img{width:100%;height:100%;image-rendering:pixelated;filter:drop-shadow(3px 3px 0 rgba(21,19,59,.35))}
.hring{position:fixed;left:0;top:0;z-index:98;pointer-events:none;border:2px dashed rgba(21,19,59,.55);border-radius:50%}
.deb{position:fixed;inset:0;z-index:97;width:100%;height:100%;pointer-events:none}
html.hm .portrait,html.hm .portrait *{cursor:none!important}
html.hm .tp{display:none}
.thud{animation:thud .18s linear}
@keyframes thud{25%{transform:translate(4px,3px)}50%{transform:translate(-4px,-2px)}75%{transform:translate(2px,-3px)}}
.shock{position:fixed;z-index:96;width:20px;height:20px;margin:-10px 0 0 -10px;border:3px solid var(--sun);box-shadow:0 0 0 3px var(--ink);pointer-events:none;animation:shock .4s ease-out both}
@keyframes shock{from{transform:scale(.3) rotate(0)}to{transform:scale(5) rotate(45deg);opacity:0}}
"""

# Hooks added inside the pixel-portrait code: breaking pixels, holes mask, reset.
HOOKS = r"""var HS=6,hc=d.createElement('canvas'),hx;
    hc.width=gw*HS;hc.height=gh*HS;hx=hc.getContext('2d');hx.fillStyle='#000';
    window.__pxCellPx=function(){return cell};
    window.__pxBreak=function(vx,vy,nc){
      var r=cv.getBoundingClientRect(),k=r.width/W,bx=(vx-r.left)/k,by=(vy-r.top)/k,R=cell*nc,out=[],i,dx,dy,dd,c;
      for(i=0;i<N;i++){
        if(BR[i])continue;
        dx=X[i]+cell/2-bx;dy=Y[i]+cell/2-by;dd=Math.sqrt(dx*dx+dy*dy);
        if(dd<R*(.65+Math.random()*.45)){
          BR[i]=1;c=cells[i];
          hx.fillRect(c[0]*HS-.5,c[1]*HS-.5,HS+1,HS+1);
          out.push({x:r.left+X[i]*k,y:r.top+Y[i]*k,s:cell*k,c:COL[C[i]],dx:dx/(dd||1),dy:dy/(dd||1),f:Math.max(0,1-dd/R)});
        }
      }
      if(out.length){draw();if(real)real.style.setProperty('--holes','url('+hc.toDataURL()+')')}
      return out;
    };
    window.__pxReset=function(){
      BR.fill(0);hx.clearRect(0,0,hc.width,hc.height);
      if(real)real.style.setProperty('--holes','none');
      setup(!reduce);
    };
    function loop(now){if(!vis){run=false;return}step(now);reveal();requestAnimationFrame(loop)}"""

HAMMER_JS = r"""/* FP-HAMMER: pick up the hammer and smash the pixel portrait */
  (function(){
    var fig=d.querySelector('.portrait'),pw=d.querySelector('.pwrap'),pl=d.querySelector('.plinth');
    if(!fig||!pw||!pl)return;
    var PAL={i:'#15133B',c:'#2F3CFF',s:'#FFC52E',w:'#FFFFFF'},
        HAM=['.iiiiiiiiii.','icwcccccccci','icccccccccci','icccccccccci','.iiiiiiiiii.','....issi....','....issi....','....issi....','....issi....','....issi....','....issi....','....issi....','....issi....','....iiii....','....issi....','....iiii....'];
    function png(rows,k){
      var c=d.createElement('canvas'),g;c.width=rows[0].length*k;c.height=rows.length*k;g=c.getContext('2d');
      rows.forEach(function(r,y){for(var i=0;i<r.length;i++)if(PAL[r[i]]){g.fillStyle=PAL[r[i]];g.fillRect(i*k,y*k,k,k)}});
      return c.toDataURL('image/png');
    }
    var A0=-20,A1=-75,HR=63.5,PVX=-HR*Math.sin(A1*Math.PI/180),PVY=HR*Math.cos(A1*Math.PI/180),RR=32;
    var hm={on:false,x:-999,y:-999,a:A0,t:-1,hit:false},DP=[],dl=0,dprr=1,running=false;
    var hammer=d.createElement('div'),ring=d.createElement('i'),dc=d.createElement('canvas'),dctx=dc.getContext('2d');
    hammer.className='hammer';hammer.hidden=true;hammer.innerHTML='<img alt="" src="'+png(HAM,5)+'">';
    ring.className='hring';ring.hidden=true;dc.className='deb';
    d.body.appendChild(dc);d.body.appendChild(hammer);d.body.appendChild(ring);

    var row=d.createElement('div'),bt=d.createElement('button'),re=d.createElement('button');
    row.className='hrow';
    bt.type='button';bt.className='hbtn';bt.setAttribute('aria-pressed','false');
    bt.innerHTML='<img alt="" src="'+png(HAM,2)+'"><span>Pick up hammer</span>';
    re.type='button';re.className='hbtn';re.hidden=true;re.textContent='Rebuild';
    row.appendChild(bt);row.appendChild(re);fig.appendChild(row);

    function place(){
      hammer.style.transform='translate3d('+(hm.x+PVX-30)+'px,'+(hm.y+PVY-76)+'px,0) rotate('+hm.a+'deg)';
      ring.style.transform='translate('+(hm.x-RR)+'px,'+(hm.y-RR)+'px)';
    }
    function setOn(v){
      hm.on=v;window.__hammer=v;d.documentElement.classList.toggle('hm',v);
      bt.setAttribute('aria-pressed',String(v));bt.lastChild.textContent=v?'Put it down':'Pick up hammer';
      hammer.hidden=ring.hidden=!v;
      if(!v)return;
      var r=pw.getBoundingClientRect();
      if(r.top<0||r.bottom>innerHeight){pw.scrollIntoView({block:'center',behavior:'instant'});r=pw.getBoundingClientRect()}
      RR=(window.__pxCellPx?window.__pxCellPx():4)*8;
      ring.style.width=ring.style.height=RR*2+'px';
      if(hm.x<0||hm.y<r.top-200||hm.y>r.bottom+200){hm.x=r.left+r.width*.5;hm.y=r.top+r.height*.22}
      place();
    }
    window.__hammerToggle=function(){setOn(!hm.on)};
    bt.onclick=function(){setOn(!hm.on)};
    re.onclick=function(){if(window.__pxReset)window.__pxReset();re.hidden=true};
    addEventListener('keydown',function(e){if(e.key==='Escape'&&hm.on&&$('pal').hidden)setOn(false)});

    /* debris: broken pixels fall, bounce on the yellow plinth, then fade */
    function sz(){dprr=Math.min(devicePixelRatio||1,2);dc.width=innerWidth*dprr;dc.height=innerHeight*dprr}
    sz();addEventListener('resize',sz);
    function spawn(list){
      list.forEach(function(o){
        var sp=1.5+o.f*8;
        DP.push({x:o.x,y:o.y,s:o.s,c:o.c,vx:o.dx*sp+(Math.random()-.5)*2,vy:o.dy*sp-1-Math.random()*5*o.f,rest:0,a:1,b:0});
      });
      if(!running){running=true;dl=performance.now();requestAnimationFrame(df)}
    }
    function df(now){
      var dt=Math.min((now-dl)/16.67,3),pr=pl.getBoundingClientRect(),i,q;
      dl=now;dctx.clearRect(0,0,dc.width,dc.height);
      for(i=DP.length-1;i>=0;i--){
        q=DP[i];
        if(q.rest>0){q.rest-=dt;q.a=Math.max(0,q.rest/40);if(q.rest<=0){DP.splice(i,1);continue}}
        else{
          q.vy+=.6*dt;q.x+=q.vx*dt;q.y+=q.vy*dt;
          if(q.vy>0&&q.x+q.s>pr.left&&q.x<pr.right&&q.y+q.s>=pr.top&&q.y+q.s<=pr.top+q.vy*dt+6){
            q.y=pr.top-q.s;
            if(q.vy<2.5||q.b>1){q.rest=80+Math.random()*60;q.vx=q.vy=0}else{q.vy*=-.45;q.vx*=.7;q.b++}
          }
          if(q.y>innerHeight+30){DP.splice(i,1);continue}
        }
        dctx.globalAlpha=q.a;dctx.fillStyle=q.c;dctx.fillRect(q.x*dprr,q.y*dprr,q.s*dprr*1.3,q.s*dprr*1.3);
      }
      dctx.globalAlpha=1;
      if(DP.length)requestAnimationFrame(df);else running=false;
    }

    /* the swing: raise, strike, recover */
    function shock(x,y){
      var e=d.createElement('i');e.className='shock';e.style.left=x+'px';e.style.top=y+'px';
      d.body.appendChild(e);setTimeout(function(){e.remove()},450);
    }
    function smash(){
      var list=window.__pxBreak?window.__pxBreak(hm.x,hm.y,8):[];
      shock(hm.x,hm.y);
      pw.classList.remove('thud');void pw.offsetWidth;pw.classList.add('thud');
      if(list.length){spawn(list);re.hidden=false}
    }
    function sw(now){
      var e=now-hm.t,u;
      if(e<80){u=e/80;hm.a=A0+(A1-A0)*u*u}
      else{
        if(!hm.hit){hm.hit=true;smash()}
        if(e<300){u=(e-80)/220;hm.a=A1+(A0-A1)*(1-Math.pow(1-u,3))}
        else{hm.a=A0;hm.t=-1}
      }
      place();
      if(hm.t>=0)requestAnimationFrame(sw);
    }
    pw.addEventListener('pointerdown',function(e){
      if(!hm.on||hm.t>=0)return;
      e.preventDefault();hm.x=e.clientX;hm.y=e.clientY;hm.hit=false;hm.t=performance.now();
      requestAnimationFrame(sw);
    },true);
    addEventListener('pointermove',function(e){
      if(!hm.on)return;
      hm.x=e.clientX;hm.y=e.clientY;if(hm.t<0)place();
    },{passive:true});
  })();

  /* Init */"""

# ---- hooks inside the existing pixel portrait code ----
sub('DL=new Float32Array(N),C=new Uint8Array(N);', 'DL=new Float32Array(N),C=new Uint8Array(N),BR=new Uint8Array(N);')
sub('if(C[i]===c)ctx.rect(', 'if(C[i]===c&&!BR[i])ctx.rect(')
sub('if(el<DL[i])continue;', 'if(el<DL[i]||BR[i])continue;')
sub('if(d2<R2&&d2>.01){', 'if(!window.__hammer&&d2<R2&&d2>.01){')
sub('var R=cell*9,act=px>-900;', 'var R=cell*9,act=px>-900&&!window.__hammer;')
sub("cv.addEventListener('pointerdown',function(e){", "cv.addEventListener('pointerdown',function(e){if(window.__hammer)return;")
sub('function loop(now){if(!vis){run=false;return}step(now);reveal();requestAnimationFrame(loop)}', HOOKS)

# ---- palette command ----
sub("['Rain pixels',rain]", "['Rain pixels',rain],['Pick up the hammer',function(){if(window.__hammerToggle)window.__hammerToggle()}]")

# ---- remove the pixel studio ----
cut(r'[ \t]*<section class="sec play" id="play">.*?</section>\n\n?', 1, re.S)
cut(r'(?m)^(?:\.(?:play|studio|tools|sw|tool)\b[^\n]*|@media\(min-width:900px\)\{\.studio\{[^\n]*)\n', 10)
cut(r"    /\* Pixel studio \*/.*?\n    \}\n(?=  \}\)\(\);)", 1, re.S)
sub("['Open the pixel studio','#play'],", '')

# ---- add the hammer code and styles ----
sub('/* Init */', HAMMER_JS)
sub('</style>', CSS + '</style>')

shutil.copy(p, p.with_name(p.name + '.bak4'))
p.write_text(s, encoding='utf-8')
print('Done. Backup saved as ' + p.name + '.bak4. Push to Render and hard-refresh (Ctrl+Shift+R).')