#!/usr/bin/env python3
"""
Aligns the real photo under the pixel portrait.
Run from the project root:   python fix_portrait_align.py
(or:  python fix_portrait_align.py path/to/home.html)
"""
import sys, shutil, pathlib

p = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'templates/home.html')
if not p.exists():
    sys.exit('Cannot find ' + str(p) + ' - run this from the folder that contains manage.py')
s = p.read_text(encoding='utf-8')
if 'FP-ALIGN' in s:
    sys.exit('Alignment fix already applied. Tune the --fx / --fy / --fs / --fdy values in the CSS instead.')

OLD = '<img class="real" src="{% static \'bluefenu.png\' %}" alt="" aria-hidden="true">'
NEW = '<div class="real"><img src="{% static \'bluefenu.png\' %}" alt="" aria-hidden="true"></div>'
if s.count(OLD) != 1 or s.count('</style>') != 1:
    sys.exit('Could not find the expected lines. Nothing was changed.')

CSS = """
/* FP-ALIGN: the mask stays on .real, the photo is scaled and moved on the img inside it.
   --fs  = zoom (bigger = bigger head)
   --fx / --fy = the point the zoom grows from (put it on the face)
   --fdy = how far the photo moves up (negative) or down (positive) after zooming */
.real{overflow:hidden;--fx:58%;--fy:39%;--fs:2.05;--fdy:-26%}
.real img{width:100%;height:100%;object-fit:cover;object-position:50% 30%;transform-origin:var(--fx) var(--fy);transform:translateY(var(--fdy)) scale(var(--fs))}
"""

shutil.copy(p, p.with_name(p.name + '.bak2'))
s = s.replace(OLD, NEW, 1).replace('</style>', CSS + '</style>', 1)
p.write_text(s, encoding='utf-8')
print('Done. Backup saved as ' + p.name + '.bak2. Hard-refresh the page (Ctrl+Shift+R).')