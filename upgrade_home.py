#!/usr/bin/env python3
"""
1) Removes the Visits / Skills counters from the hero (the footer V###.io stays).
2) Replaces the role capsule with spray-paint graffiti behind the hero, built from
   profile.role (split on | , / or a dot): brush lettering, rough spray edges,
   a yellow paint splash, crowns, arrows, splatters and drips.
Run from the project root:   python graffiti_wall.py
(or:  python graffiti_wall.py path/to/home.html)
Safe on a fresh file, and it also upgrades the earlier hero_graffiti.py version.
"""
import re, sys, shutil, pathlib

p = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'templates/home.html')
if not p.exists():
    sys.exit('Cannot find ' + str(p) + ' - run this from the folder that contains manage.py')
s = p.read_text(encoding='utf-8')
if 'FP-GRAFFITI' in s:
    sys.exit('Graffiti already installed.')


def sub(old, new):
    global s
    if s.count(old) != 1:
        sys.exit('Anchor not found exactly once, nothing written:\n  ' + old[:70])
    s = s.replace(old, new, 1)


CSS = r"""
/* FP-GRAFFITI */
.sr-only{position:absolute;width:1px;height:1px;margin:-1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.wall{position:absolute;inset:0;z-index:-1;overflow:hidden;pointer-events:none;user-select:none;-webkit-user-select:none;opacity:var(--wo,.95)}
.wall svg{position:absolute;inset:-20px;width:calc(100% + 40px);height:calc(100% + 40px);overflow:visible;will-change:transform;transform:translate(calc(var(--wx,0)*-10px),calc(var(--wy,0)*-7px))}
.wall .wg{animation:spray 1s var(--ease) both}
@keyframes spray{from{opacity:0;transform:translateX(-40px)}}
.wall .dr{animation:drip 1.3s var(--ease) both;transform-box:fill-box;transform-origin:50% 0}
@keyframes drip{from{transform:scaleY(0)}}
.wall.still .wg,.wall.still .dr{animation:none}
"""

JS = r"""/* FP-GRAFFITI: the role text as spray-paint graffiti behind the hero */
  (function(){
    var w=d.querySelector('.wall');if(!w)return;
    var parts=(w.getAttribute('data-role')||'').split(/\s*[|\u2022\u00b7\/,]\s*/).map(function(t){return t.trim()}).filter(Boolean).slice(0,3);
    if(!parts.length)return;
    function rng(a){return function(){a|=0;a=a+0x6D2B79F5|0;var t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
    function blob(r,rx,ry){
      var n=14,p=[],i,a,k,q,z,s;
      for(i=0;i<n;i++){a=i/n*6.2832;k=.8+r()*.4;p.push([Math.cos(a)*rx*k,Math.sin(a)*ry*k])}
      s='M'+((p[0][0]+p[n-1][0])/2).toFixed(0)+' '+((p[0][1]+p[n-1][1])/2).toFixed(0);
      for(i=0;i<n;i++){q=p[i];z=p[(i+1)%n];s+='Q'+q[0].toFixed(0)+' '+q[1].toFixed(0)+' '+((q[0]+z[0])/2).toFixed(0)+' '+((q[1]+z[1])/2).toFixed(0)}
      return s+'Z';
    }
    var DEF='<defs><filter id="fpSpray" x="-15%" y="-40%" width="130%" height="180%"><feTurbulence type="fractalNoise" baseFrequency=".035" numOctaves="2" seed="4" result="wp"/><feDisplacementMap in="SourceGraphic" in2="wp" scale="9" xChannelSelector="R" yChannelSelector="G" result="core"/><feGaussianBlur in="core" stdDeviation="7" result="halo"/><feTurbulence type="fractalNoise" baseFrequency=".8" numOctaves="1" seed="2" result="gr"/><feColorMatrix in="gr" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  14 0 0 0 -7.4" result="gm"/><feComposite in="halo" in2="gm" operator="in" result="dots"/><feMerge><feMergeNode in="dots"/><feMergeNode in="core"/></feMerge></filter><filter id="fpRough" x="-10%" y="-30%" width="120%" height="160%"><feTurbulence type="fractalNoise" baseFrequency=".03" numOctaves="2" seed="9" result="wp"/><feDisplacementMap in="SourceGraphic" in2="wp" scale="16" xChannelSelector="R" yChannelSelector="G"/></filter></defs>';
    var lw=0;
    function build(still){
      var W=w.clientWidth,H=w.clientHeight,P=20,u=W<900?W/420:W/1600,r=rng(7),svg='';
      var L=W<900?[[210,95,360,-8],[215,190,300,-6],[210,285,340,-10]]:[[480,230,800,-9],[980,275,520,-8],[1330,335,560,-17]];
      var C=[['#2F3CFF','#2F3CFF'],['#15133B','#FFC52E'],['#1A1660','#2F3CFF']];
      parts.forEach(function(t,i){
        var c=L[i],wd=c[2]*u,sz=Math.min(wd/(Math.max(t.length,4)*.5),H*.3),tc=C[i][0],ac=C[i][1],g='',k,x,y,len;
        var s=sz/160,x1=-wd*.42,y1=sz*.62,x2=wd*.42,y2=sz*.26,my=sz*.78,an=Math.atan2(y2-my,x2),hl=sz*.26;
        if(i===1)g+='<path d="'+blob(r,wd*.62,sz*.85)+'" fill="#FFC52E" filter="url(#fpRough)"/>';
        for(k=0;k<30;k++){
          x=(r()-.5)*wd*1.4;y=(r()-.5)*sz*2.1;
          g+='<circle cx="'+x.toFixed(1)+'" cy="'+y.toFixed(1)+'" r="'+(1+r()*r()*8).toFixed(1)+'" fill="'+(r()<.7?ac:tc)+'" opacity="'+(.4+r()*.5).toFixed(2)+'"/>';
        }
        g+='<text x="0" y="0" text-anchor="middle" dominant-baseline="central" textLength="'+wd.toFixed(0)+'" lengthAdjust="spacingAndGlyphs" font-family="Kaushan Script,cursive" font-size="'+sz.toFixed(0)+'" fill="'+tc+'" stroke="'+tc+'" stroke-width="'+(sz*.03).toFixed(1)+'" stroke-linejoin="round" filter="url(#fpSpray)">'+esc(t)+'</text>';
        g+='<path transform="translate('+(-wd*.4).toFixed(0)+' '+(-sz*.62).toFixed(0)+') scale('+s.toFixed(2)+')" d="M0 0L8-24 22-6 34-30 46-6 60-24 68 0Z" fill="none" stroke="'+(i===0?ac:tc)+'" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"/>';
        g+='<path d="M'+x1.toFixed(0)+' '+y1.toFixed(0)+'Q0 '+my.toFixed(0)+' '+x2.toFixed(0)+' '+y2.toFixed(0)+
           'M'+(x2+hl*Math.cos(an+2.65)).toFixed(0)+' '+(y2+hl*Math.sin(an+2.65)).toFixed(0)+'L'+x2.toFixed(0)+' '+y2.toFixed(0)+'L'+(x2+hl*Math.cos(an-2.65)).toFixed(0)+' '+(y2+hl*Math.sin(an-2.65)).toFixed(0)+
           '" fill="none" stroke="'+ac+'" stroke-width="'+(sz*.06).toFixed(1)+'" stroke-linecap="round" stroke-linejoin="round" filter="url(#fpRough)"/>';
        for(k=0;k<4;k++){
          x=(-.38+k*.26+r()*.08)*wd;y=sz*.18+r()*sz*.2;len=sz*.25+r()*sz*.55;
          g+='<g class="dr" style="animation-delay:'+(1.2+k*.18+i*.2).toFixed(2)+'s"><rect x="'+x.toFixed(0)+'" y="'+y.toFixed(0)+'" width="'+(sz*.035).toFixed(1)+'" height="'+len.toFixed(0)+'" rx="3" fill="'+(k%2?tc:ac)+'"/><circle cx="'+(x+sz*.0175).toFixed(1)+'" cy="'+(y+len+sz*.02).toFixed(0)+'" r="'+(sz*.03).toFixed(1)+'" fill="'+(k%2?tc:ac)+'"/></g>';
        }
        svg+='<g class="wg" style="animation-delay:'+(i*.25).toFixed(2)+'s"><g transform="translate('+(c[0]*u+P).toFixed(0)+' '+(c[1]*u+P).toFixed(0)+') rotate('+c[3]+')">'+g+'</g></g>';
      });
      w.classList.toggle('still',!!still);
      w.innerHTML='<svg viewBox="0 0 '+(W+40)+' '+(H+40)+'" preserveAspectRatio="none" aria-hidden="true">'+DEF+svg+'</svg>';
    }
    function go(){lw=w.clientWidth;build(false)}
    var ft=d.fonts&&d.fonts.load?d.fonts.load('180px "Kaushan Script"',parts.join('')):Promise.resolve();
    Promise.race([ft,new Promise(function(a){setTimeout(a,1800)})]).then(go,go);
    var rt;
    addEventListener('resize',function(){clearTimeout(rt);rt=setTimeout(function(){if(lw&&w.clientWidth!==lw){lw=w.clientWidth;build(true)}},250)});
    if(!reduce)addEventListener('pointermove',function(e){
      w.style.setProperty('--wx',((e.clientX/innerWidth-.5)*2).toFixed(2));
      w.style.setProperty('--wy',((e.clientY/innerHeight-.5)*2).toFixed(2));
    },{passive:true});
  })();

  /* Init */"""

# 0) upgrade from the earlier (CSS-text) version, if it was applied
if 'FP-WALL' in s:
    s = re.sub(r'\n/\* FP-WALL \*/.*?@keyframes spin\{[^\n]*\}\n', '\n', s, count=1, flags=re.S)
    s = re.sub(r'/\* FP-WALL: the role text.*?\}\)\(\);\n\n  (?=/\* Init \*/)', '', s, count=1, flags=re.S)
    s = re.sub(r'[ \t]*<div class="wall"[^\n]*</div>\n', '', s, count=1)

# 1) remove the counters (skipped if they are already gone)
s = re.sub(r'[ \t]*<div class="stats">\n(?:[ \t]*<div class="stat">[^\n]*</div>\n)+[ \t]*</div>\n', '', s, count=1)

# 2) capsule -> hidden text for screen readers, plus the graffiti wall
if '<span class="role">{{ profile.role }}</span>' in s:
    sub('<span class="role">{{ profile.role }}</span>', '<span class="sr-only">{{ profile.role }}</span>')
elif 'class="sr-only">{{ profile.role }}' not in s:
    sys.exit('Could not find the role capsule. Nothing was changed.')
sub('<div class="stk" aria-hidden="true"></div>',
    '<div class="stk" aria-hidden="true"></div>\n    <div class="wall" aria-hidden="true" data-role="{{ profile.role }}"></div>')
sub('1,6..72,400..500&display=swap', '1,6..72,400..500&family=Kaushan+Script&display=swap')
sub('/* Init */', JS)
sub('</style>', CSS + '</style>')

shutil.copy(p, p.with_name(p.name + '.bak7'))
p.write_text(s, encoding='utf-8')
print('Done. Backup saved as ' + p.name + '.bak7. Push to Render and hard-refresh (Ctrl+Shift+R).')