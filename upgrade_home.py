#!/usr/bin/env python3
"""
Builds align_tool.html: a standalone page (no Django, no database, no server)
where you drag and zoom your photo over the pixel portrait, then copy the CSS.

Run from the project root (the folder with manage.py):
    python make_align_tool.py
Then double-click align_tool.html to open it in your browser.
"""
import re, sys, pathlib

home = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'templates/home.html')
if not home.exists():
    sys.exit('Cannot find ' + str(home) + ' - run this from the folder that contains manage.py')
m = re.search(r"SPR='([^']+)'", home.read_text(encoding='utf-8'))
if not m:
    sys.exit('Could not find the pixel sprite (SPR=...) in ' + str(home))

photo = pathlib.Path('feed/static/bluefenu.png')
if not photo.exists():
    print('Warning: feed/static/bluefenu.png not found from here. The page will show a red note.')

TEMPLATE = r"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>Portrait align tool</title>
<style>
*{box-sizing:border-box}
body{margin:0;padding:32px;display:flex;gap:48px;justify-content:center;flex-wrap:wrap;background:#EEF0FA;color:#15133B;font:600 14px/1.3 system-ui,sans-serif}
.stage{width:280px;touch-action:none;cursor:grab}
.stage:active{cursor:grabbing}
.pwrap{position:relative;width:280px;outline:2px dashed rgba(21,19,59,.4)}
.real{position:absolute;inset:0;overflow:hidden;--fx:58%;--fy:39%;--fs:1.7;--fdx:0%;--fdy:-32%}
.real img{display:block;width:100%;height:100%;object-fit:cover;object-position:50% 30%;transform-origin:var(--fx) var(--fy);transform:translate(var(--fdx),var(--fdy)) scale(var(--fs));user-select:none;-webkit-user-drag:none}
canvas{position:relative;display:block;width:100%;opacity:.5;pointer-events:none}
.panel{width:340px;display:grid;gap:12px;align-content:start}
.panel h1{margin:0;font-size:20px}
.panel p{margin:0;font-weight:400;color:rgba(21,19,59,.75)}
label{display:grid;gap:4px}
output{color:#2F3CFF;font-weight:700}
input[type=range]{width:100%}
textarea{width:100%;height:150px;padding:10px;font:12px/1.4 monospace;border:2px solid #15133B;border-radius:12px;background:#fff}
button{padding:.7em 1.2em;font:700 14px/1 system-ui,sans-serif;background:#FFC52E;border:2px solid #15133B;border-radius:99px;cursor:pointer}
#err{display:none;color:#c00}
</style></head><body>
<div class="stage" id="stage"><div class="pwrap">
  <div class="real" id="real"><img id="photo" src="feed/static/bluefenu.png" alt=""></div>
  <canvas id="cv"></canvas>
</div></div>
<div class="panel">
  <h1>Portrait align tool</h1>
  <p>Drag the photo to move it. Scroll the mouse wheel over it to zoom. Line your head up with the pixel head, then copy the CSS.</p>
  <p id="err">Photo not found. Keep this file in the project root so feed/static/bluefenu.png is next to it.</p>
  <label>Pixel opacity <output id="oo"></output><input type="range" id="op" min="0" max="1" step="0.05" value="0.5"></label>
  <div id="sl" style="display:grid;gap:12px"></div>
  <button type="button" id="copy">Copy CSS</button>
  <textarea id="out" readonly></textarea>
  <p>Paste the copied CSS just above the closing style tag in templates/home.html, then commit and push.</p>
</div>
<script>
var SPR='__SPR__';
var hd=SPR.split(';'),gw=+hd[0].split(',')[0],gh=+hd[0].split(',')[1],re=/([a-e])(\d+)/g,m,idx=0,k,cells=[];
while((m=re.exec(hd[1]))){for(k=0;k<+m[2];k++,idx++)if(m[1]!=='a')cells.push([idx%gw,(idx/gw)|0,m[1].charCodeAt(0)-98])}
var COL=['#15133B','#2F3CFF','#FFC52E','#FFFFFF'],W=280,cell=W/gw,H=cell*gh,dpr=2;
var cv=document.getElementById('cv'),ctx=cv.getContext('2d');
cv.width=W*dpr;cv.height=H*dpr;cv.style.height=H+'px';
cells.forEach(function(c){ctx.fillStyle=COL[c[2]];ctx.fillRect(c[0]*cell*dpr,c[1]*cell*dpr,cell*dpr*.94,cell*dpr*.94)});
document.querySelector('.pwrap').style.height=H+'px';

var $=function(id){return document.getElementById(id)},real=$('real');
$('photo').onerror=function(){$('err').style.display='block'};
var V={fs:1.7,fdx:0,fdy:-32,fx:58,fy:39};
var S=[['fs','Zoom',0.5,4,0.01,''],['fdx','Move left / right',-60,60,0.5,'%'],['fdy','Move up / down',-90,60,0.5,'%'],['fx','Zoom point, left / right',0,100,1,'%'],['fy','Zoom point, up / down',0,100,1,'%']];
$('sl').innerHTML=S.map(function(a){return '<label>'+a[1]+' <output id="o_'+a[0]+'"></output><input type="range" id="r_'+a[0]+'" min="'+a[2]+'" max="'+a[3]+'" step="'+a[4]+'"></label>'}).join('');
var r1=function(n){return Math.round(n*10)/10};
function apply(){
  V.fs=Math.max(0.5,Math.min(4,V.fs));
  S.forEach(function(a){
    var v=a[0]==='fs'?Math.round(V.fs*100)/100:r1(V[a[0]]);
    real.style.setProperty('--'+a[0],v+a[5]);
    $('o_'+a[0]).textContent=v+a[5];$('r_'+a[0]).value=v;
  });
  $('out').value='.real{overflow:hidden;--fx:'+r1(V.fx)+'%;--fy:'+r1(V.fy)+'%;--fs:'+(Math.round(V.fs*100)/100)+';--fdx:'+r1(V.fdx)+'%;--fdy:'+r1(V.fdy)+'%}\n'+
    '.real img{width:100%;height:100%;object-fit:cover;object-position:50% 30%;transform-origin:var(--fx) var(--fy);transform:translate(var(--fdx),var(--fdy)) scale(var(--fs))}';
}
S.forEach(function(a){$('r_'+a[0]).addEventListener('input',function(){V[a[0]]=parseFloat(this.value);apply()})});
$('op').addEventListener('input',function(){cv.style.opacity=this.value;$('oo').textContent=this.value});
$('oo').textContent='0.5';

var st=$('stage'),dx0,dy0,dragging=false;
st.addEventListener('pointerdown',function(e){dragging=true;dx0=e.clientX;dy0=e.clientY;st.setPointerCapture(e.pointerId)});
st.addEventListener('pointermove',function(e){
  if(!dragging)return;
  V.fdx+=(e.clientX-dx0)/W*100;V.fdy+=(e.clientY-dy0)/H*100;dx0=e.clientX;dy0=e.clientY;apply();
});
['pointerup','pointercancel'].forEach(function(t){st.addEventListener(t,function(){dragging=false})});
st.addEventListener('wheel',function(e){e.preventDefault();V.fs*=(e.deltaY<0?1.03:0.97);apply()},{passive:false});
$('copy').onclick=function(){
  var o=$('out');o.focus();o.select();
  try{document.execCommand('copy')}catch(x){}
  if(navigator.clipboard)navigator.clipboard.writeText(o.value).catch(function(){});
  this.textContent='Copied';var b=this;setTimeout(function(){b.textContent='Copy CSS'},1500);
};
apply();
</script></body></html>
"""

pathlib.Path('align_tool.html').write_text(TEMPLATE.replace('__SPR__', m.group(1)), encoding='utf-8')
print('Done. Open align_tool.html in your browser (double-click it).')