#!/usr/bin/env python3
"""
update.py - graffiti redesign (v2) for templates/home.html

What it does
  1. Replaces the FP-GRAFFITI JavaScript block with a new design.
     Placement, size, rotation and the role-splitting ("A | B | C") are unchanged.
  2. Adds Sedgwick Ave Display (a real graffiti-marker Google Font) to the
     fonts <link>. Kaushan Script stays as the fallback.
  3. Adds a few lines of CSS (sparkle twinkle). Nothing else in the CSS changes.
  4. Saves a backup next to the file: home.html.bak-graffiti-v1

Run from the project root (the folder that contains manage.py):
    python update.py
Or point it at the file:
    python update.py path/to/home.html
Safe to run more than once.
"""
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

NEW_JS = r'''/* FP-GRAFFITI: the role text as clean, layered street-art tags behind the hero (v2) */
(function(){
    var w=d.querySelector('.wall');if(!w)return;
    var parts=(w.getAttribute('data-role')||'').split(/\s*[|\u2022\u00b7\/,]\s*/).map(function(t){return t.trim()}).filter(Boolean).slice(0,3);
    if(!parts.length)return;

    var NS='http://www.w3.org/2000/svg',
        FONT='Sedgwick Ave Display, Kaushan Script, cursive',
        INK='#15133B',SUN='#FFC52E',COB='#2F3CFF',WHT='#FFFFFF';

    /* one palette per tag: g = face gradient, x = 3D extrusion, s = underline swoosh,
       k = big sparkle, m = small sparkle, b = halftone patch behind the tag */
    var PAL=[
        {g:['#7A84FF',COB,'#1B25C4'],x:SUN,s:SUN,k:SUN,m:WHT,b:SUN},
        {g:['#FFE792',SUN,'#FF9E1B'],x:COB,s:COB,k:COB,m:WHT,b:COB},
        {g:[WHT,'#F2F3FF','#BEC6FF'],x:COB,s:SUN,k:SUN,m:COB,b:COB}
    ];

    function rng(a){return function(){a|=0;a=a+0x6D2B79F5|0;var t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
    function n1(v){return String(Math.round(v*10)/10)}

    /* natural width of the text at 100px, so letters are never stretched */
    function measure(t){
        var s=d.createElementNS(NS,'svg'),x=d.createElementNS(NS,'text'),n=0;
        s.setAttribute('width','10');s.setAttribute('height','10');
        s.style.cssText='position:absolute;left:-9999px;top:0;visibility:hidden';
        x.setAttribute('font-family',FONT);x.setAttribute('font-size','100');x.textContent=t;
        s.appendChild(x);d.body.appendChild(s);
        try{n=x.getComputedTextLength()}catch(e){n=0}
        d.body.removeChild(s);
        return n||t.length*52;
    }

    /* four-point sparkle, outlined */
    function star(x,y,s,fill,cls){
        return '<g transform="translate('+n1(x)+' '+n1(y)+') scale('+n1(s)+')"><path class="sp '+cls+'" d="M0-1Q.14-.14 1 0Q.14.14 0 1Q-.14.14-1 0Q-.14-.14 0-1Z" fill="'+fill+'" stroke="'+INK+'" stroke-width="2.4" stroke-linejoin="round" vector-effect="non-scaling-stroke"/></g>';
    }

    var lw=0;
    function build(still){
        var W=w.clientWidth,H=w.clientHeight,P=20,u=W<900?W/420:W/1600,r=rng(11),svg='',defs='';

        /* a barely-there wobble so edges feel hand-painted, not vector-perfect */
        defs+='<filter id="fpEdge" x="-10%" y="-25%" width="120%" height="150%"><feTurbulence type="fractalNoise" baseFrequency=".022" numOctaves="2" seed="6" result="nz"/><feDisplacementMap in="SourceGraphic" in2="nz" scale="3.2" xChannelSelector="R" yChannelSelector="G"/></filter>';
        defs+='<linearGradient id="fpHf" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000"/><stop offset="1" stop-color="#fff"/></linearGradient>';
        defs+='<radialGradient id="fpRf"><stop offset="0" stop-color="#fff"/><stop offset=".55" stop-color="#fff"/><stop offset="1" stop-color="#000"/></radialGradient>';

        /* same placement as before: [centre x, centre y, width, rotation] */
        var L=W<900?[[210,95,360,-8],[215,190,300,-6],[210,285,340,-10]]:[[480,230,800,-9],[980,275,520,-8],[1330,335,560,-17]];

        parts.forEach(function(t,i){
            var c=L[i],p=PAL[i%PAL.length],wd=c[2]*u,nat=measure(t)/100,
                sz=Math.min(wd/nat,H*.3),tw=nat*sz,id='fpT'+i,
                line=sz*.028,ow=sz*.1,n=Math.round(sz*.07)+2,stp=1.3,
                hp=Math.max(6,sz*.075),
                bx=n1(-tw*1.1),by=n1(-sz),bw=n1(tw*2.2),bh=n1(sz*2),
                T='',k,x,y,len,dw,sx1,sx2,yb,mid,sw,fr,dr,sp,sd,sh;

            /* ---- defs for this tag ---- */
            defs+='<text id="'+id+'" x="0" y="0" text-anchor="middle" dominant-baseline="central" font-family="'+FONT+'" font-size="'+n1(sz)+'">'+esc(t)+'</text>';
            defs+='<linearGradient id="'+id+'g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="'+p.g[0]+'"/><stop offset=".5" stop-color="'+p.g[1]+'"/><stop offset="1" stop-color="'+p.g[2]+'"/></linearGradient>';
            defs+='<clipPath id="'+id+'c"><use href="#'+id+'"/></clipPath>';
            defs+='<pattern id="'+id+'h" width="'+n1(hp)+'" height="'+n1(hp)+'" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><circle cx="'+n1(hp/2)+'" cy="'+n1(hp/2)+'" r="'+n1(hp*.24)+'" fill="'+INK+'"/></pattern>';
            defs+='<pattern id="'+id+'b" width="'+n1(hp*1.2)+'" height="'+n1(hp*1.2)+'" patternUnits="userSpaceOnUse" patternTransform="rotate(-20)"><circle cx="'+n1(hp*.6)+'" cy="'+n1(hp*.6)+'" r="'+n1(hp*.26)+'" fill="'+p.b+'"/></pattern>';
            defs+='<mask id="'+id+'m" maskUnits="userSpaceOnUse" x="'+bx+'" y="'+by+'" width="'+bw+'" height="'+bh+'"><rect x="'+bx+'" y="'+n1(-sz*.12)+'" width="'+bw+'" height="'+n1(sz*.7)+'" fill="url(#fpHf)"/></mask>';
            defs+='<mask id="'+id+'o" maskUnits="userSpaceOnUse" x="'+bx+'" y="'+by+'" width="'+bw+'" height="'+bh+'"><ellipse cx="0" cy="'+n1(sz*.05)+'" rx="'+n1(tw*.58)+'" ry="'+n1(sz*.8)+'" fill="url(#fpRf)"/></mask>';

            /* ---- 1. underline swoosh: one tapered brush stroke ---- */
            sx1=-tw*(i===1?.3:.48);sx2=tw*(i===1?.5:.46);yb=sz*.47;mid=(sx1+sx2)/2;
            sw='M'+n1(sx1)+' '+n1(yb+sz*.05)+'Q'+n1(mid)+' '+n1(yb-sz*.1)+' '+n1(sx2)+' '+n1(yb-sz*.1)+'Q'+n1(mid)+' '+n1(yb+sz*.07)+' '+n1(sx1)+' '+n1(yb+sz*.05)+'Z';
            T+='<path d="'+sw+'" transform="translate('+n1(sz*.03)+' '+n1(sz*.03)+')" fill="'+INK+'"/>';
            T+='<path d="'+sw+'" fill="'+p.s+'" stroke="'+INK+'" stroke-width="'+n1(line)+'" stroke-linejoin="round"/>';

            /* ---- 2. 3D extrusion: ink silhouette first, then the coloured side on top of it ---- */
            for(k=n;k>=0;k--)T+='<use href="#'+id+'" x="'+n1(k*stp)+'" y="'+n1(k*stp)+'" fill="'+INK+'" stroke="'+INK+'" stroke-width="'+n1(ow)+'" stroke-linejoin="round"/>';
            for(k=n;k>=1;k--)T+='<use href="#'+id+'" x="'+n1(k*stp)+'" y="'+n1(k*stp)+'" fill="'+p.x+'" stroke="'+p.x+'" stroke-width="'+n1(ow-2*line)+'" stroke-linejoin="round"/>';

            /* ---- 3. ink outline of the front face ---- */
            T+='<use href="#'+id+'" fill="'+INK+'" stroke="'+INK+'" stroke-width="'+n1(ow)+'" stroke-linejoin="round"/>';

            /* ---- 4. a few tidy drips, tucked under the face ---- */
            fr=tw>sz*3?[-.31,.07,.34]:[-.2,.26];
            dr='';
            fr.forEach(function(f,j){
                x=(f+(r()-.5)*.05)*tw;y=sz*.1;len=sz*(.2+r()*.2);dw=sz*.065;
                var cx=x+dw/2,col=p.g[1];
                dr+='<g class="dr" style="animation-delay:'+(1.2+j*.2+i*.2).toFixed(2)+'s">'
                  +'<rect x="'+n1(x)+'" y="'+n1(y)+'" width="'+n1(dw)+'" height="'+n1(len)+'" rx="'+n1(dw/2)+'" fill="'+INK+'" stroke="'+INK+'" stroke-width="'+n1(line*2)+'" stroke-linejoin="round"/>'
                  +'<circle cx="'+n1(cx)+'" cy="'+n1(y+len)+'" r="'+n1(dw*.78)+'" fill="'+INK+'" stroke="'+INK+'" stroke-width="'+n1(line*2)+'"/>'
                  +'<rect x="'+n1(x)+'" y="'+n1(y)+'" width="'+n1(dw)+'" height="'+n1(len)+'" rx="'+n1(dw/2)+'" fill="'+col+'"/>'
                  +'<circle cx="'+n1(cx)+'" cy="'+n1(y+len)+'" r="'+n1(dw*.78)+'" fill="'+col+'"/></g>';
            });
            T+=dr;

            /* ---- 5. front face: gradient fill ---- */
            T+='<use href="#'+id+'" fill="url(#'+id+'g)"/>';

            /* ---- 6. shading clipped to the letters: rim light, halftone, gloss ---- */
            sh=sz*.5;
            T+='<g clip-path="url(#'+id+'c)">'
              +'<use href="#'+id+'" fill="none" stroke="'+WHT+'" stroke-width="'+n1(sz*.075)+'" stroke-linejoin="round" opacity=".9"/>'
              +'<use href="#'+id+'" x="'+n1(sz*.022)+'" y="'+n1(sz*.024)+'" fill="url(#'+id+'g)"/>'
              +'<g mask="url(#'+id+'m)"><rect x="'+bx+'" y="'+by+'" width="'+bw+'" height="'+bh+'" fill="url(#'+id+'h)" opacity=".34"/></g>'
              +'<path d="M'+n1(-tw*.2+sh)+' '+n1(-sz)+'L'+n1(-tw*.2+sh+tw*.06)+' '+n1(-sz)+'L'+n1(-tw*.2+tw*.06)+' '+n1(sz)+'L'+n1(-tw*.2)+' '+n1(sz)+'Z" fill="'+WHT+'" opacity=".2"/>'
              +'<path d="M'+n1(tw*.02+sh)+' '+n1(-sz)+'L'+n1(tw*.02+sh+tw*.022)+' '+n1(-sz)+'L'+n1(tw*.02+tw*.022)+' '+n1(sz)+'L'+n1(tw*.02)+' '+n1(sz)+'Z" fill="'+WHT+'" opacity=".2"/>'
              +'</g>';

            /* ---- specks: a handful of spray dots, kept clear of the letters ---- */
            sp='';
            for(k=0;k<8;k++){
                x=(r()-.5)*tw*1.3;y=(r()<.5?-1:1)*(.46+r()*.36)*sz;
                sp+='<circle cx="'+n1(x)+'" cy="'+n1(y)+'" r="'+(.9+r()*1.9).toFixed(1)+'" fill="'+[INK,p.s,p.x][k%3]+'" opacity="'+(.55+r()*.35).toFixed(2)+'"/>';
            }

            /* ---- sparkles on the side with room ---- */
            sd=(c[0]*u+P+tw/2+sz*.4<W+40)?1:-1;
            var stars=star(sd*(tw*.5+sz*.06),-sz*.42,sz*.2,p.k,'a')
                     +star(sd*(tw*.5+sz*.22),-sz*.08,sz*.1,p.m,'b')
                     +star(-sd*(tw*.5+sz*.02),sz*.4,sz*.09,p.k,'b');

            var g='<rect x="'+bx+'" y="'+by+'" width="'+bw+'" height="'+bh+'" fill="url(#'+id+'b)" mask="url(#'+id+'o)" opacity=".5"/>'
                 +'<g filter="url(#fpEdge)">'+T+'</g>'+sp+stars;

            svg+='<g class="wg" style="animation-delay:'+(i*.25).toFixed(2)+'s"><g transform="translate('+(c[0]*u+P).toFixed(0)+' '+(c[1]*u+P).toFixed(0)+') rotate('+c[3]+')">'+g+'</g></g>';
        });

        w.classList.toggle('still',!!still);
        w.innerHTML='<svg viewBox="0 0 '+(W+40)+' '+(H+40)+'" preserveAspectRatio="none" aria-hidden="true"><defs>'+defs+'</defs>'+svg+'</svg>';
    }

    function go(){lw=w.clientWidth;build(false)}
    var ft=d.fonts&&d.fonts.load?Promise.all([d.fonts.load('120px "Sedgwick Ave Display"',parts.join('')),d.fonts.load('120px "Kaushan Script"')]):Promise.resolve();
    Promise.race([ft,new Promise(function(a){setTimeout(a,1800)})]).then(go,go);
    var rt;
    addEventListener('resize',function(){clearTimeout(rt);rt=setTimeout(function(){if(lw&&w.clientWidth!==lw){lw=w.clientWidth;build(true)}},250)});
    if(!reduce)addEventListener('pointermove',function(e){
        w.style.setProperty('--wx',((e.clientX/innerWidth-.5)*2).toFixed(2));
        w.style.setProperty('--wy',((e.clientY/innerHeight-.5)*2).toFixed(2));
    },{passive:true});
})();'''

NEW_CSS = '''/* FP-GRAFFITI-V2 */
.wall .sp{transform-box:fill-box;transform-origin:center;animation:twinkle 3s ease-in-out infinite}
.wall .sp.b{animation-delay:-1.5s}
@keyframes twinkle{50%{transform:scale(.55) rotate(25deg)}}
/* /FP-GRAFFITI-V2 */
'''

OLD_FONT = "&family=Kaushan+Script&display=swap"
NEW_FONT = "&family=Kaushan+Script&family=Sedgwick+Ave+Display&display=swap"


def find_file():
    if len(sys.argv) > 1:
        return Path(sys.argv[1]).expanduser().resolve()
    for cand in (HERE / "templates" / "home.html",
                 Path.cwd() / "templates" / "home.html",
                 HERE / "home.html"):
        if cand.exists():
            return cand
    return None


def main():
    path = find_file()
    if not path or not path.exists():
        sys.exit("Could not find templates/home.html. Run this from the project root, "
                 "or pass the path:  python update.py path/to/home.html")

    html = path.read_text(encoding="utf-8")

    # 1. graffiti JS block: from its marker comment up to the "Init" comment
    pat = re.compile(r"/\* FP-GRAFFITI: the role text.*?(?=\s*/\* Init \*/)", re.S)
    if not pat.search(html):
        sys.exit("Could not find the FP-GRAFFITI block in home.html. Nothing was changed.")

    backup = path.with_name(path.name + ".bak-graffiti-v1")
    if not backup.exists():
        shutil.copy2(path, backup)

    html = pat.sub(lambda m: NEW_JS, html, count=1)

    # 2. font link
    if "Sedgwick+Ave+Display" not in html:
        if OLD_FONT in html:
            html = html.replace(OLD_FONT, NEW_FONT, 1)
        else:
            print("Note: could not find the Google Fonts link. Add "
                  "&family=Sedgwick+Ave+Display to it by hand (Kaushan Script will be used until then).")

    # 3. CSS (replace any earlier v2 block, then add before </style>)
    html = re.sub(r"/\* FP-GRAFFITI-V2 \*/.*?/\* /FP-GRAFFITI-V2 \*/\s*", "", html, flags=re.S)
    html = html.replace("</style>", NEW_CSS + "</style>", 1)

    path.write_text(html, encoding="utf-8")
    print("Done. Updated:", path)
    print("Backup:      ", backup)
    print("Hard-refresh the page (Ctrl+Shift+R) to see it.")


if __name__ == "__main__":
    main()