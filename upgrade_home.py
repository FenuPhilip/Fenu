#!/usr/bin/env python3
"""
Upgrades templates/home.html in place (a .bak copy is saved first).
Run from the project root:   python upgrade_home.py
Or give a path:              python upgrade_home.py path/to/home.html
"""
import sys, shutil, pathlib

p = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'templates/home.html')
if not p.exists():
    sys.exit('Cannot find ' + str(p) + ' - run this from the folder that contains manage.py')
s = p.read_text(encoding='utf-8')
if 'FP-UPGRADE' in s:
    sys.exit('Already upgraded. Restore the .bak copy first if you want to re-run.')
shutil.copy(p, p.with_name(p.name + '.bak'))


def sub(old, new):
    global s
    if s.count(old) != 1:
        sys.exit('Anchor not found exactly once, nothing written:\n  ' + old[:70])
    s = s.replace(old, new, 1)


# ---------- CSS ----------
CSS = r"""
/* FP-UPGRADE */
.pwrap{position:relative}
.real{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 30%;pointer-events:none;-webkit-mask-image:radial-gradient(circle var(--rr,0px) at var(--rx,-99px) var(--ry,-99px),#000 55%,transparent 100%);mask-image:radial-gradient(circle var(--rr,0px) at var(--rx,-99px) var(--ry,-99px),#000 55%,transparent 100%)}

.led{position:fixed;top:0;left:0;z-index:90;height:6px;width:0;pointer-events:none;background:repeating-linear-gradient(90deg,var(--cobalt) 0 10px,transparent 10px 14px);filter:drop-shadow(0 0 4px rgba(47,60,255,.8))}
.led::after{content:"";position:absolute;right:0;top:0;width:10px;height:6px;background:var(--sun)}
.tp{position:fixed;left:0;top:0;z-index:99;pointer-events:none;will-change:transform}

.stk{position:absolute;inset:0;z-index:3;pointer-events:none}
.stk .s{position:absolute;width:clamp(38px,5.4vw,70px);transform:translate3d(calc(var(--px,0)*var(--k,.5)*20px),calc(var(--py,0)*var(--k,.5)*14px - var(--sc,0)*var(--k,.5)*.22px),0) rotate(var(--r,0deg))}
.stk img{width:100%;image-rendering:pixelated;filter:drop-shadow(4px 4px 0 var(--ink));animation:bob 3.4s ease-in-out infinite;animation-delay:calc(var(--k,.5)*-3s)}
@keyframes bob{50%{transform:translateY(-9px) rotate(5deg)}}
@media(max-width:620px){.stk{display:none}}

.kbtn{display:inline-flex;align-items:center;gap:10px;margin-top:22px;padding:.55em 1.1em .55em .6em;font:600 .9rem/1 var(--display);background:var(--paper);border:2px solid var(--ink);border-radius:99px;box-shadow:3px 3px 0 var(--ink);transition:transform .2s var(--ease),box-shadow .2s var(--ease)}
.kbtn:hover{transform:translate(-2px,-2px);box-shadow:5px 5px 0 var(--ink)}
.kbtn kbd{padding:.3em .55em;font:700 .8rem/1 var(--display);background:var(--sun);border:2px solid var(--ink);border-radius:8px}

@media(hover:hover){
  .post{position:relative;transform:perspective(900px) rotateX(var(--ty,0deg)) rotateY(var(--tx,0deg));transition:transform .15s ease-out,box-shadow .25s var(--ease)}
  .post:hover{transform:perspective(900px) translate(-3px,-3px) rotateX(var(--ty,0deg)) rotateY(var(--tx,0deg))}
  .post::after{content:"";position:absolute;inset:0;border-radius:inherit;pointer-events:none;opacity:0;background:radial-gradient(circle at var(--gx,50%) var(--gy,50%),rgba(255,197,46,.24),transparent 45%);transition:opacity .25s}
  .post:hover::after{opacity:1}
}

.play{background:radial-gradient(rgba(47,60,255,.16) 1.4px,transparent 1.8px) 0 0/16px 16px}
.studio{display:grid;gap:32px;align-items:center}
@media(min-width:900px){.studio{grid-template-columns:1fr auto;gap:64px}}
.studio canvas{width:min(100%,440px);aspect-ratio:1;image-rendering:pixelated;touch-action:none;cursor:crosshair;background-color:var(--paper);background-image:linear-gradient(rgba(21,19,59,.09) 1px,transparent 1px),linear-gradient(90deg,rgba(21,19,59,.09) 1px,transparent 1px);background-size:calc(100%/32) calc(100%/32);border:2px solid var(--ink);border-radius:24px 24px 24px 8px;box-shadow:8px 8px 0 var(--cobalt)}
.tools{display:flex;flex-wrap:wrap;gap:12px;align-items:center}
.sw{width:44px;height:44px;background:var(--c);border:2px solid var(--ink);border-radius:50%;box-shadow:3px 3px 0 var(--ink);transition:transform .2s var(--ease)}
.sw.on{transform:translate(-2px,-2px) scale(1.12);outline:3px solid var(--cobalt);outline-offset:3px}
.sw.er{background:repeating-conic-gradient(var(--mist) 0 25%,var(--paper) 0 50%) 0 0/12px 12px}
.tool{padding:.7em 1.2em;font:600 .95rem/1 var(--display);background:var(--sun);border:2px solid var(--ink);border-radius:99px;box-shadow:3px 3px 0 var(--ink);transition:transform .2s var(--ease),box-shadow .2s var(--ease)}
.tool:hover{transform:translate(-2px,-2px);box-shadow:5px 5px 0 var(--ink)}
.tool[aria-pressed=true]{background:var(--ink);color:#fff}

.pal{position:fixed;inset:0;z-index:80;display:grid;align-items:start;justify-items:center;padding:14vh 16px 0;background:rgba(21,19,59,.55);backdrop-filter:blur(4px);-webkit-backdrop-filter:blur(4px)}
.pal-box{width:min(560px,100%);padding:14px;background:var(--paper);border:2px solid var(--ink);border-radius:24px 24px 24px 8px;box-shadow:8px 8px 0 var(--sun);animation:pop .35s var(--ease) both}
.pal input{width:100%;padding:.8em 1em;font:600 1.1rem var(--display);color:var(--ink);background:var(--mist);border:2px solid var(--ink);border-radius:14px}
.pal input:focus{outline:0;box-shadow:4px 4px 0 var(--cobalt)}
.pal ul{list-style:none;margin:10px 0 6px;max-height:42vh;overflow:auto}
.pal li{padding:.7em 1em;font:600 1rem var(--display);border-radius:12px;cursor:pointer}
.pal li.on{background:var(--ink);color:#fff}
.pal li.none{cursor:default;font-weight:400;font-style:italic;color:var(--muted)}
.pal-hint{padding:0 4px;font-size:.85rem;color:var(--muted)}

.rn{position:fixed;top:-20px;z-index:95;pointer-events:none;animation:fall var(--t) linear var(--dl) both}
@keyframes fall{to{transform:translateY(112vh) rotate(200deg)}}

html.night{filter:invert(1) hue-rotate(180deg)}
html.night img,html.night video,html.night canvas,html.night iframe,html.night .rn,html.night .tp{filter:invert(1) hue-rotate(180deg)}
"""

# ---------- HTML ----------
PLAY = r"""<section class="sec play" id="play">
    <div class="wrap studio">
      <div>
        <div class="head"><h2>Leave your mark.</h2><p>A tiny pixel studio. That bug is yours to recolor. Paint, mirror, then save it as a PNG.</p></div>
        <div class="tools" role="group" aria-label="Pixel tools">
          <button type="button" class="sw on" data-c="#15133B" style="--c:#15133B" aria-label="Ink"></button>
          <button type="button" class="sw" data-c="#2F3CFF" style="--c:#2F3CFF" aria-label="Cobalt"></button>
          <button type="button" class="sw" data-c="#FFC52E" style="--c:#FFC52E" aria-label="Sun"></button>
          <button type="button" class="sw er" data-c="e" aria-label="Eraser"></button>
          <button type="button" class="tool" id="pMir" aria-pressed="false">Mirror</button>
          <button type="button" class="tool" id="pClr">Clear</button>
          <button type="button" class="tool" id="pSave">Save PNG</button>
        </div>
      </div>
      <canvas id="paint" width="32" height="32" role="img" aria-label="Pixel drawing canvas"></canvas>
    </div>
  </section>

  """

PALETTE = r"""<div class="pal" id="pal" hidden role="dialog" aria-modal="true" aria-label="Command palette">
  <div class="pal-box">
    <input id="palIn" placeholder="Type a command: skills, night, email..." autocomplete="off" aria-label="Command">
    <ul id="palList" role="listbox"></ul>
    <p class="pal-hint">Up and down to move. Enter to run. Esc to close.</p>
  </div>
</div>

"""

# ---------- JS ----------
JS = r"""/* FP-UPGRADE extras */
  (function(){
    var fine=matchMedia('(pointer:fine)').matches;

    /* LED scroll bar */
    var led=$('led');
    function ld(){var h=d.documentElement.scrollHeight-innerHeight;led.style.width=(h>0?Math.min(scrollY/h,1)*100:0)+'%'}
    addEventListener('scroll',ld,{passive:true});ld();

    /* Pixel sprites -> real PNGs (data URLs) */
    var PAL={i:'#15133B',c:'#2F3CFF',s:'#FFC52E',w:'#FFFFFF'}, SP={
      chip:['..i.ii.i..','.iiiiiiii.','iiccccccii','.icccccci.','iiccssccii','iiccssccii','.icccccci.','iiccccccii','.iiiiiiii.','..i.ii.i..'],
      lock:['...iiii...','..i....i..','..i....i..','..i....i..','.iiiiiiii.','.issssssi.','.issiissi.','.issiissi.','.issssssi.','.iiiiiiii.'],
      bug:['.i......i.','..i....i..','...cccc...','..cwccwc..','i.cccccc.i','.iccsscci.','i.ccsscc.i','.icccccci.','i..cccc..i','....ii....']
    };
    function png(rows,k){
      var c=d.createElement('canvas'),g;c.width=c.height=rows.length*k;g=c.getContext('2d');
      rows.forEach(function(r,y){for(var i=0;i<r.length;i++)if(PAL[r[i]]){g.fillStyle=PAL[r[i]];g.fillRect(i*k,y*k,k,k)}});
      return c.toDataURL('image/png');
    }

    /* Floating pixel stickers in the hero, parallax on pointer + scroll */
    var stk=d.querySelector('.stk');
    if(stk){
      [['chip',46,9,-8,.5],['lock',88,56,10,.9],['bug',3,54,-12,.7]].forEach(function(a){
        var s=d.createElement('span'),im=new Image();
        s.className='s';s.style.cssText='left:'+a[1]+'%;top:'+a[2]+'%;--r:'+a[3]+'deg;--k:'+a[4];
        im.src=png(SP[a[0]],8);im.alt='';s.appendChild(im);stk.appendChild(s);
      });
      if(!reduce){
        addEventListener('scroll',function(){stk.style.setProperty('--sc',Math.min(scrollY,1200))},{passive:true});
        addEventListener('pointermove',function(e){
          stk.style.setProperty('--px',((e.clientX/innerWidth-.5)*2).toFixed(2));
          stk.style.setProperty('--py',((e.clientY/innerHeight-.5)*2).toFixed(2));
        },{passive:true});
      }
    }

    /* Pixel trail cursor (mouse only) */
    if(fine&&!reduce){
      var T=[],qx=innerWidth/2,qy=innerHeight/2,go=false,CL=['#FFC52E','#2F3CFF','#15133B'],n,z,el;
      for(n=0;n<8;n++){
        z=12-n;el=d.createElement('i');el.className='tp';
        el.style.cssText='width:'+z+'px;height:'+z+'px;background:'+CL[n%3]+';opacity:'+(1-n*.1);
        d.body.appendChild(el);T.push({e:el,x:qx,y:qy,z:z});
      }
      var qt=function(){
        var ax=qx,ay=qy,moving=false;
        T.forEach(function(t){
          var dx=ax-t.x,dy=ay-t.y;t.x+=dx*.4;t.y+=dy*.4;
          if(Math.abs(dx)+Math.abs(dy)>.5)moving=true;
          t.e.style.transform='translate3d('+(Math.round(t.x/3)*3-t.z/2)+'px,'+(Math.round(t.y/3)*3-t.z/2)+'px,0)';
          ax=t.x;ay=t.y;
        });
        if(moving)requestAnimationFrame(qt);else go=false;
      };
      addEventListener('pointermove',function(e){qx=e.clientX;qy=e.clientY;if(!go){go=true;requestAnimationFrame(qt)}},{passive:true});
    }

    /* Tilt + glow on project cards */
    if(matchMedia('(hover:hover)').matches&&!reduce){
      d.querySelectorAll('.post').forEach(function(p){
        p.addEventListener('pointermove',function(e){
          var r=p.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;
          p.style.setProperty('--tx',(x*7).toFixed(2)+'deg');p.style.setProperty('--ty',(-y*7).toFixed(2)+'deg');
          p.style.setProperty('--gx',((x+.5)*100).toFixed(1)+'%');p.style.setProperty('--gy',((y+.5)*100).toFixed(1)+'%');
        });
        p.addEventListener('pointerleave',function(){p.style.setProperty('--tx','0deg');p.style.setProperty('--ty','0deg')});
      });
    }

    /* Pixel rain easter egg */
    function rain(){
      if(reduce)return;
      var K=['#2F3CFF','#FFC52E','#15133B'],i;
      for(i=0;i<70;i++)(function(){
        var e=d.createElement('i'),sz=6+(Math.random()*14|0);
        e.className='rn';
        e.style.cssText='left:'+(Math.random()*100).toFixed(1)+'vw;width:'+sz+'px;height:'+sz+'px;background:'+K[i%3]+';--t:'+(1.6+Math.random()*1.6).toFixed(2)+'s;--dl:'+(Math.random()*.9).toFixed(2)+'s';
        d.body.appendChild(e);setTimeout(function(){e.remove()},3800);
      })();
    }

    /* Command palette: Ctrl/Cmd+K or / */
    var pal=$('pal'),inp=$('palIn'),ul=$('palList'),sel=0,cur=[],pf=null;
    var cmds=[
      ['Go home','#hero'],['See projects','#projects'],['See skills','#skills'],['Open the pixel studio','#play'],['Go to contact','#contact'],
      ['Send a message',function(){togglePanel()}],['Copy email',function(){copyEmail()}],
      ['Toggle night mode',function(){d.documentElement.classList.toggle('night')}],
      ['Rain pixels',rain]
    ];
    function render(){
      var q=inp.value.toLowerCase();
      cur=cmds.filter(function(c){return c[0].toLowerCase().indexOf(q)>-1&&(typeof c[1]==='function'||$(c[1].slice(1)))});
      sel=Math.min(sel,Math.max(cur.length-1,0));
      ul.innerHTML=cur.length?cur.map(function(c,i){return '<li role="option" data-i="'+i+'"'+(i===sel?' class="on"':'')+'>'+c[0]+'</li>'}).join(''):'<li class="none">No match. Try skills or night.</li>';
    }
    function closeP(){pal.hidden=true;if(pf&&pf.focus)pf.focus()}
    function openP(){pf=d.activeElement;pal.hidden=false;inp.value='';sel=0;render();inp.focus()}
    function run(c){
      closeP();if(!c)return;
      if(typeof c[1]==='function')c[1]();
      else $(c[1].slice(1)).scrollIntoView({behavior:reduce?'auto':'smooth'});
    }
    window.openPalette=openP;
    inp.addEventListener('input',function(){sel=0;render()});
    pal.addEventListener('click',function(e){
      var li=e.target.closest('li[data-i]');
      if(li)run(cur[+li.dataset.i]);else if(e.target===pal)closeP();
    });
    addEventListener('keydown',function(e){
      var t=(d.activeElement||{}).tagName,k=(e.key||'').toLowerCase();
      if(pal.hidden){
        if(((e.ctrlKey||e.metaKey)&&k==='k')||(k==='/'&&t!=='INPUT'&&t!=='TEXTAREA')){e.preventDefault();openP()}
        return;
      }
      if(k==='escape')closeP();
      else if(k==='arrowdown'||k==='arrowup'){e.preventDefault();sel=(sel+(k==='arrowdown'?1:-1)+cur.length)%Math.max(cur.length,1);render()}
      else if(k==='enter'){e.preventDefault();run(cur[sel])}
    });
    var hc=d.querySelector('.hero-copy');
    if(hc){
      var kb=d.createElement('button'),mac=/Mac|iPhone|iPad/.test(navigator.platform||'');
      kb.type='button';kb.className='kbtn';
      kb.innerHTML='<kbd>'+(fine?(mac?'\u2318':'Ctrl')+' K':'Tap')+'</kbd> Command palette';
      kb.onclick=openP;hc.appendChild(kb);
    }

    /* Pixel studio */
    var pc=$('paint');
    if(pc){
      var G=32,x=pc.getContext('2d'),col=PAL.i,dn=false,mir=false,last;
      var cell=function(e){
        var r=pc.getBoundingClientRect();
        return [Math.max(0,Math.min(G-1,Math.floor((e.clientX-r.left)/r.width*G))),Math.max(0,Math.min(G-1,Math.floor((e.clientY-r.top)/r.height*G)))];
      };
      var put=function(a,b){
        (mir?[a,G-1-a]:[a]).forEach(function(u){
          if(col==='e')x.clearRect(u,b,1,1);else{x.fillStyle=col;x.fillRect(u,b,1,1)}
        });
      };
      var line=function(p,q){
        var m=Math.max(Math.abs(q[0]-p[0]),Math.abs(q[1]-p[1]),1),i;
        for(i=0;i<=m;i++)put(Math.round(p[0]+(q[0]-p[0])*i/m),Math.round(p[1]+(q[1]-p[1])*i/m));
      };
      SP.bug.forEach(function(r,y){for(var i=0;i<r.length;i++)if(PAL[r[i]]){x.fillStyle=PAL[r[i]];x.fillRect(6+i*2,6+y*2,2,2)}});
      pc.addEventListener('pointerdown',function(e){dn=true;pc.setPointerCapture(e.pointerId);last=cell(e);line(last,last)});
      pc.addEventListener('pointermove',function(e){if(!dn)return;var c=cell(e);line(last,c);last=c});
      ['pointerup','pointercancel'].forEach(function(t){pc.addEventListener(t,function(){dn=false})});
      d.querySelectorAll('.sw').forEach(function(b){
        b.onclick=function(){col=b.dataset.c;d.querySelectorAll('.sw').forEach(function(o){o.classList.toggle('on',o===b)})};
      });
      $('pMir').onclick=function(){mir=!mir;this.setAttribute('aria-pressed',String(mir))};
      $('pClr').onclick=function(){x.clearRect(0,0,G,G)};
      $('pSave').onclick=function(){
        var t=d.createElement('canvas'),y=t.getContext('2d'),a=d.createElement('a');
        t.width=t.height=512;y.imageSmoothingEnabled=false;y.fillStyle='#EEF0FA';y.fillRect(0,0,512,512);y.drawImage(pc,0,0,512,512);
        a.download='my-pixel-mark.png';a.href=t.toDataURL('image/png');a.click();
      };
    }
  })();

  /* Init */"""

# ---------- apply ----------
sub('<span id="emailText">{{ profile.name|lower|cut:" " }}@portfolio.io</span>',
    '<span id="emailText">fenuphilip19@gmail.com</span>')

sub('<canvas id="pix" role="img" aria-label="Pixel portrait of {{ profile.name }}"></canvas>',
    r"""<div class="pwrap">
          <img class="real" src="{% static 'bluefenu.png' %}" alt="" aria-hidden="true">
          <canvas id="pix" role="img" aria-label="Pixel portrait of {{ profile.name }}"></canvas>
        </div>""")

sub('<header class="top">', '<div class="led" id="led" aria-hidden="true"></div>\n<header class="top">')
sub('<section class="hero" id="hero">', '<section class="hero" id="hero">\n    <div class="stk" aria-hidden="true"></div>')
sub('<section class="contact" id="contact">', PLAY + '<section class="contact" id="contact">')
sub('<div class="toast" id="emailToast"', PALETTE + '<div class="toast" id="emailToast"')

sub("scan=-1,nextScan=0;", "scan=-1,nextScan=0,real=d.querySelector('.real'),rx=0,ry=0,rr=0;")
sub('function loop(now){if(!vis){run=false;return}step(now);requestAnimationFrame(loop)}',
    r"""function reveal(){
      var R=cell*9,act=px>-900;
      if(act){rx=px;ry=py}
      rr+=((act?R:0)-rr)*.16;
      if(real){real.style.setProperty('--rr',rr.toFixed(1)+'px');real.style.setProperty('--rx',rx+'px');real.style.setProperty('--ry',ry+'px')}
    }
    function loop(now){if(!vis){run=false;return}step(now);reveal();requestAnimationFrame(loop)}""")
sub('function pos(e){var r=cv.getBoundingClientRect();px=e.clientX-r.left;py=e.clientY-r.top}',
    r"""function pos(e){var r=cv.getBoundingClientRect();px=e.clientX-r.left;py=e.clientY-r.top;if(reduce){rr=cell*9;reveal()}}
    if(reduce)cv.addEventListener('pointerleave',function(){rr=0;px=-999;reveal()});""")

sub('/* Init */', JS)
sub('</style>', CSS + '</style>')

p.write_text(s, encoding='utf-8')
print('Done. Backup saved as ' + p.name + '.bak. Hard-refresh the page (Ctrl+Shift+R).')