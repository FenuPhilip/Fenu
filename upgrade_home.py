#!/usr/bin/env python3
"""
update.py - graffiti redesign (v3, dry-brush street art) for templates/home.html

What it does
  1. Replaces the FP-GRAFFITI JavaScript block with the new design:
     flat dry-brush lettering (cobalt / yellow / ink), crowns, arrows, X marks,
     speed lines, drips and spray specks. Role text is still split on | , / etc.
  2. Desktop: Developer top-left, Builder centre, last tag beside the pixel portrait.
     Mobile: all tags sit BEHIND the pixel portrait, not behind the headline.
  3. Removes the extra font and CSS that the previous version added.
  4. Saves a backup next to the file: home.html.bak-graffiti-v1 (kept from the first run)

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

NEW_JS = r'''/* FP-GRAFFITI: the role text as dry-brush street-art tags behind the hero (v3) */
(function(){
    var w=d.querySelector('.wall');if(!w)return;
    var parts=(w.getAttribute('data-role')||'').split(/\s*[|\u2022\u00b7\/,]\s*/).map(function(t){return t.trim()}).filter(Boolean).slice(0,3);
    if(!parts.length)return;

    var NS='http://www.w3.org/2000/svg',FONT='Kaushan Script, cursive',
        INK='#15133B',SUN='#FFC52E',COB='#2F3CFF',COLS=[COB,SUN,INK];

    /* SX = how much the letters are squeezed (taller, chunkier); BIAS = which way the spray drifts */
    var SX=[.76,.68,.64],BIAS=[-.16,0,.1];
    /* desktop layout on a 1512px wide hero: [centre x, centre y, text width, rotation] */
    var DESK=[[330,178,520,-11],[860,258,420,-15],[1325,262,340,-22]];
    /* mobile layout: tags stacked behind the portrait. Heights are fractions of the portrait */
    var MOBY=[.13,.43,.73],MOBW=[.8,.76,.78],MOBR=[-8,-7,-10],MOBX=[-4,6,-2];

    function rng(a){return function(){a|=0;a=a+0x6D2B79F5|0;var t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
    function n1(v){return String(Math.round(v*10)/10)}

    /* hand-lettered feel: first letter bigger, small size jitter, baseline climbs a little */
    function letters(t,r){
        var a=[],i,ch;
        for(i=0;i<t.length;i++){
            ch=t.charAt(i);
            a.push({c:ch===' '?'\u00a0':ch,k:i===0?1.24:(i===t.length-1?1.1:.93+r()*.14),dy:i?-(.016+(r()-.5)*.03):0});
        }
        return a;
    }
    function spans(L,S){
        var o='',k;
        for(k=0;k<L.length;k++)o+='<tspan font-size="'+n1(S*L[k].k)+'"'+(k?' dy="'+n1(L[k].dy*S)+'"':'')+'>'+esc(L[k].c)+'</tspan>';
        return o;
    }
    /* natural width of the lettering at 100px and where its vertical middle sits */
    function measure(L){
        var h=d.createElement('div'),bb,res={w:L.length*48,cy:-28};
        h.style.cssText='position:absolute;left:-9999px;top:0;visibility:hidden';
        h.innerHTML='<svg width="10" height="10"><text x="0" y="0" font-family="'+FONT+'" font-size="100">'+spans(L,100)+'</text></svg>';
        d.body.appendChild(h);
        try{bb=h.querySelector('text').getBBox();if(bb.width>0){res.w=bb.width;res.cy=bb.y+bb.height/2}}catch(e){}
        d.body.removeChild(h);
        return res;
    }

    /* tapered brush stroke from (x1,y1) to (x2,y2); bend curves it, th is its thickness in the middle */
    function tap(x1,y1,x2,y2,bend,th){
        var dx=x2-x1,dy=y2-y1,l=Math.sqrt(dx*dx+dy*dy)||1,nx=-dy/l,ny=dx/l,
            cx=(x1+x2)/2+nx*bend,cy=(y1+y2)/2+ny*bend,
            ex=x2-cx,ey=y2-cy,el=Math.sqrt(ex*ex+ey*ey)||1;
        return {d:'M'+n1(x1)+' '+n1(y1)+'Q'+n1(cx+nx*th)+' '+n1(cy+ny*th)+' '+n1(x2)+' '+n1(y2)+'Q'+n1(cx-nx*th)+' '+n1(cy-ny*th)+' '+n1(x1)+' '+n1(y1)+'Z',x:x2,y:y2,tx:ex/el,ty:ey/el};
    }
    function headS(a,h,col){
        var nx=-a.ty,ny=a.tx;
        return '<path d="M'+n1(a.x+a.tx*h*.6)+' '+n1(a.y+a.ty*h*.6)+'L'+n1(a.x-a.tx*h*.4+nx*h*.5)+' '+n1(a.y-a.ty*h*.4+ny*h*.5)+'L'+n1(a.x-a.tx*h*.4-nx*h*.5)+' '+n1(a.y-a.ty*h*.4-ny*h*.5)+'Z" fill="'+col+'" stroke="'+col+'" stroke-width="'+n1(h*.08)+'" stroke-linejoin="round"/>';
    }
    function headO(a,h,col,sw){
        var nx=-a.ty,ny=a.tx;
        return '<path d="M'+n1(a.x-a.tx*h*.7+nx*h*.45)+' '+n1(a.y-a.ty*h*.7+ny*h*.45)+'L'+n1(a.x+a.tx*h*.3)+' '+n1(a.y+a.ty*h*.3)+'L'+n1(a.x-a.tx*h*.7-nx*h*.45)+' '+n1(a.y-a.ty*h*.7-ny*h*.45)+'" fill="none" stroke="'+col+'" stroke-width="'+n1(sw)+'" stroke-linecap="round" stroke-linejoin="round"/>';
    }
    function crown(x,y,rot,sz,col){
        var cs=sz*.0046,sw=sz*.034/cs;
        return '<g transform="translate('+n1(x)+' '+n1(y)+') rotate('+rot+') scale('+cs.toFixed(4)+')" fill="none" stroke="'+col+'" stroke-width="'+n1(sw)+'" stroke-linejoin="round" stroke-linecap="round">'
            +'<path d="M0 62L-6 8L28 32L50 -4L72 32L106 8L100 62Z"/>'
            +'<circle cx="-6" cy="8" r="6" fill="'+col+'"/><circle cx="50" cy="-4" r="6" fill="'+col+'"/><circle cx="106" cy="8" r="6" fill="'+col+'"/></g>';
    }
    function xm(x,y,s,col,sw){
        return '<path transform="translate('+n1(x)+' '+n1(y)+') rotate(8)" d="M'+n1(-s)+' '+n1(-s)+'L'+n1(s)+' '+n1(s)+'M'+n1(s)+' '+n1(-s)+'L'+n1(-s)+' '+n1(s)+'" fill="none" stroke="'+col+'" stroke-width="'+n1(sw)+'" stroke-linecap="round"/>';
    }

    /* dry-brush: wobbly edge, bristle streaks eating the rim, solid core */
    function fBrush(id,sz,seed){
        return '<filter id="'+id+'" x="-12%" y="-35%" width="124%" height="170%" color-interpolation-filters="sRGB">'
            +'<feTurbulence type="fractalNoise" baseFrequency="'+(3.2/sz).toFixed(4)+'" numOctaves="3" seed="'+seed+'" result="wp"/>'
            +'<feDisplacementMap in="SourceGraphic" in2="wp" scale="'+n1(Math.max(3,sz*.05))+'" xChannelSelector="R" yChannelSelector="G" result="rg"/>'
            +'<feTurbulence type="fractalNoise" baseFrequency="'+(.9/sz).toFixed(4)+' '+(15/sz).toFixed(4)+'" numOctaves="2" seed="'+(seed+5)+'" result="st"/>'
            +'<feColorMatrix in="st" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 10 0 0 0 -2.6" result="sm"/>'
            +'<feComposite in="rg" in2="sm" operator="in" result="dry"/>'
            +'<feMorphology in="rg" operator="erode" radius="'+n1(Math.max(1.2,sz*.019))+'" result="core"/>'
            +'<feMerge><feMergeNode in="dry"/><feMergeNode in="core"/></feMerge></filter>';
    }
    /* light version for thin things (crowns, X marks, drips): just a rough edge */
    function fRough(id,sz,seed){
        return '<filter id="'+id+'" x="-12%" y="-35%" width="124%" height="170%" color-interpolation-filters="sRGB">'
            +'<feTurbulence type="fractalNoise" baseFrequency="'+(4/sz).toFixed(4)+'" numOctaves="2" seed="'+seed+'" result="wp"/>'
            +'<feDisplacementMap in="SourceGraphic" in2="wp" scale="'+n1(Math.max(2,sz*.03))+'" xChannelSelector="R" yChannelSelector="G"/></filter>';
    }

    var sig='',busy=0;
    function build(still){
        var W=w.clientWidth,H=w.clientHeight,P=20,u=W/1512,svg='',defs='',
            wr=w.getBoundingClientRect(),pe=d.querySelector('.pwrap'),pr=pe?pe.getBoundingClientRect():null,
            hasP=!!(pr&&pr.width>20&&pr.height>20),mob=W<900,pt=0,pl=0,ph=0,pwid=0;
        if(hasP){pt=pr.top-wr.top;pl=pr.left-wr.left;ph=pr.height;pwid=pr.width}

        defs+='<radialGradient id="fpRf"><stop offset="0" stop-color="#fff"/><stop offset=".5" stop-color="#fff"/><stop offset="1" stop-color="#000"/></radialGradient>';

        parts.forEach(function(t,i){
            var r=rng(100+i*17),L=letters(t,r),m=measure(L),col=COLS[i%3],
                sx=mob?SX[i]*.92:SX[i],nat=m.w/100,wd,cx,cy,rot,cap,sz,tw,ty,sw,hp,
                idB='fpB'+i,idR='fpR'+i,idO='fpO'+i,idP='fpP'+i,T='',O='',sp='',k,a,b,fr,nd,bx,by,bw,bh,dr,body;

            /* where this tag goes */
            if(mob){
                wd=W*MOBW[i];cx=W/2+MOBX[i];rot=MOBR[i];
                cy=hasP?pt+ph*MOBY[i]:H*(.3+i*.12);cap=(hasP?ph:H*.4)*.2;
            }else{
                wd=DESK[i][2]*u;cx=DESK[i][0]*u;cy=DESK[i][1]*u;rot=DESK[i][3];cap=H*.3;
                if(i===2&&hasP){cx=Math.min(pl+pwid/2+W*.12,W-wd*.6-14);cy=pt+ph*.1}
            }
            sz=Math.min(wd/(nat*sx),cap);tw=nat*sz*sx;ty=-m.cy*sz/100;sw=sz*.08;hp=Math.max(6,sz*.08);
            bx=n1(-tw*1.1);by=n1(-sz*1.2);bw=n1(tw*2.2);bh=n1(sz*2.4);

            defs+=fBrush(idB,sz,3+i*7)+fRough(idR,sz,9+i*5);
            defs+='<pattern id="'+idP+'" width="'+n1(hp)+'" height="'+n1(hp)+'" patternUnits="userSpaceOnUse" patternTransform="rotate(-20)"><circle cx="'+n1(hp/2)+'" cy="'+n1(hp/2)+'" r="'+n1(hp*.22)+'" fill="'+col+'"/></pattern>';
            defs+='<mask id="'+idO+'" maskUnits="userSpaceOnUse" x="'+bx+'" y="'+by+'" width="'+bw+'" height="'+bh+'"><ellipse cx="'+n1(BIAS[i]*tw)+'" cy="0" rx="'+n1(tw*.66)+'" ry="'+n1(sz*.8)+'" fill="url(#fpRf)"/></mask>';

            /* the word itself */
            T+='<g transform="scale('+sx.toFixed(3)+' 1)"><text x="0" y="'+n1(ty)+'" text-anchor="middle" font-family="'+FONT+'" font-size="'+n1(sz)+'" fill="'+col+'" stroke="'+col+'" stroke-width="'+n1(sw)+'" stroke-linejoin="round" stroke-linecap="round">'+spans(L,sz)+'</text></g>';

            /* ornaments, per tag */
            if(i===0){
                a=tap(-.16*tw,.62*sz,.26*tw,.5*sz,.07*sz,.11*sz);
                T+='<path d="'+a.d+'" fill="'+col+'"/>'+headS(a,.26*sz,col);
                b=tap(.66*tw,-.5*sz,.5*tw,.04*sz,-.05*sz,.022*sz);
                O+='<path d="'+b.d+'" fill="'+col+'"/>'+headO(b,.15*sz,col,sz*.024);
                O+=xm(.38*tw,.68*sz,.08*sz,col,sz*.034);
                O+=crown(-.46*tw,-.96*sz,-14,sz,col);
            }else if(i===1){
                a=tap(-.36*tw,.64*sz,.4*tw,.42*sz,.1*sz,.12*sz);
                T+='<path d="'+a.d+'" fill="'+col+'"/>';
                b=tap(-.12*tw,.82*sz,.36*tw,.66*sz,.05*sz,.036*sz);
                T+='<path d="'+b.d+'" fill="'+col+'"/>';
                O+='<path d="'+tap(.46*tw,.46*sz,.66*tw,.38*sz,0,.02*sz).d+'" fill="'+col+'"/>';
                O+=xm(-.6*tw,.12*sz,.09*sz,col,sz*.034)+xm(.16*tw,-1.04*sz,.08*sz,col,sz*.034)+xm(.52*tw,-.62*sz,.08*sz,col,sz*.034);
                O+=crown(-.4*tw,-1.02*sz,-10,sz,col);
            }else{
                a=tap(-.12*tw,.74*sz,.5*tw,.42*sz,.2*sz,.1*sz);
                T+='<path d="'+a.d+'" fill="'+col+'"/>'+headS(a,.28*sz,col);
                for(k=0;k<3;k++)O+='<path d="'+tap(-.8*tw,(-.22+k*.17)*sz,-.6*tw,(-.28+k*.17)*sz,0,.024*sz).d+'" fill="'+col+'"/>';
                O+=crown(-.42*tw,-1.0*sz,-12,sz,col);
            }

            /* a few drips */
            nd=tw>sz*3.2?3:2;fr=nd===3?[-.36,.02,.3]:[-.2,.25];
            fr.forEach(function(f,j){
                var x=(f+(r()-.5)*.05)*tw,y0=sz*.2,len=sz*(.22+r()*.3),dw=sz*.032;
                O+='<g class="dr" style="animation-delay:'+(1.2+j*.2+i*.2).toFixed(2)+'s"><path d="M'+n1(x)+' '+n1(y0)+'L'+n1(x)+' '+n1(y0+len)+'" fill="none" stroke="'+col+'" stroke-width="'+n1(dw)+'" stroke-linecap="round"/><circle cx="'+n1(x)+'" cy="'+n1(y0+len+dw)+'" r="'+n1(dw*1.15)+'" fill="'+col+'"/></g>';
            });

            /* spray specks, thicker on the side the spray drifts to */
            for(k=0;k<58;k++){
                var ag=r()*6.2832,rd=Math.pow(r(),.7),px=Math.cos(ag)*rd*tw*.64+BIAS[i]*tw,py=Math.sin(ag)*rd*sz*.88,big=r()<.14;
                sp+='<circle cx="'+n1(px)+'" cy="'+n1(py)+'" r="'+(big?1.8+r()*2.6:.6+r()*1.4).toFixed(1)+'" fill="'+col+'" opacity="'+(.3+r()*.6).toFixed(2)+'"/>';
            }

            body='<rect x="'+bx+'" y="'+by+'" width="'+bw+'" height="'+bh+'" fill="url(#'+idP+')" mask="url(#'+idO+')" opacity=".3"/>'
                +'<g filter="url(#'+idB+')">'+T+'</g><g filter="url(#'+idR+')">'+O+'</g>'+sp;

            svg+='<g class="wg" style="animation-delay:'+(i*.25).toFixed(2)+'s"><g transform="translate('+(cx+P).toFixed(0)+' '+(cy+P).toFixed(0)+') rotate('+rot+')">'+body+'</g></g>';
        });

        w.classList.toggle('still',!!still);
        w.innerHTML='<svg viewBox="0 0 '+(W+40)+' '+(H+40)+'" preserveAspectRatio="none" aria-hidden="true"><defs>'+defs+'</defs>'+svg+'</svg>';
    }

    /* rebuild only when the hero or the portrait actually moved */
    function sigNow(){
        var wr=w.getBoundingClientRect(),pe=d.querySelector('.pwrap'),pr=pe?pe.getBoundingClientRect():null;
        return [w.clientWidth,w.clientHeight,pr?Math.round(pr.top-wr.top):0,pr?Math.round(pr.left-wr.left):0,pr?Math.round(pr.height):0].join();
    }
    function refresh(still){var s=sigNow();if(s===sig)return;sig=s;build(still)}
    function go(){sig='';refresh(false)}

    var ft=d.fonts&&d.fonts.load?d.fonts.load('120px "Kaushan Script"',parts.join('')):Promise.resolve();
    Promise.race([ft,new Promise(function(a){setTimeout(a,1800)})]).then(go,go);
    var rt;
    function later(){clearTimeout(rt);rt=setTimeout(function(){refresh(true)},220)}
    addEventListener('resize',later);
    addEventListener('load',later);
    if(window.ResizeObserver)new ResizeObserver(later).observe(w);
    if(!reduce)addEventListener('pointermove',function(e){
        w.style.setProperty('--wx',((e.clientX/innerWidth-.5)*2).toFixed(2));
        w.style.setProperty('--wy',((e.clientY/innerHeight-.5)*2).toFixed(2));
    },{passive:true});
})();'''

NEW_CSS = ''  # v3 needs no extra CSS (the v2 block is removed below)

EXTRA_FONT = "&family=Sedgwick+Ave+Display"   # added by v2, not needed any more


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

    # 2. drop the Sedgwick font that v2 added (v3 uses Kaushan Script, already loaded)
    html = html.replace(EXTRA_FONT, "")
    if "Kaushan+Script" not in html:
        print("Note: Kaushan Script is missing from your Google Fonts link; add "
              "&family=Kaushan+Script to it, otherwise a fallback font is used.")

    # 3. remove the CSS block that v2 added
    html = re.sub(r"/\* FP-GRAFFITI-V2 \*/.*?/\* /FP-GRAFFITI-V2 \*/\s*", "", html, flags=re.S)

    path.write_text(html, encoding="utf-8")
    print("Done. Updated:", path)
    print("Backup:      ", backup)
    print("Hard-refresh the page (Ctrl+Shift+R) to see it.")


if __name__ == "__main__":
    main()  