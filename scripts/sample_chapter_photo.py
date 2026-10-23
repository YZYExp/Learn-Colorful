#!/usr/bin/env python3
"""Read fixed pixels from a fictional scene; never infer material colors."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
source=ROOT/'assets/images/chapter-v2-extract.png'
font=next(p for p in [Path('/usr/local/share/fonts/investment/NotoSerifCJKsc-Regular.otf'),*Path('/usr/share/fonts').rglob('*CJK*.ttc')] if p.is_file())
def ft(size):return ImageFont.truetype(str(font),size)
points=[('浅石地',950,710),('陶墙',1470,160),('海水',970,550),('叶片',335,160),('拱廊阴影',1300,380)]
with Image.open(source) as im:
 im=im.convert('RGB');im.load();width,height=im.size
 samples=[]
 for name,x,y in points:
  rgb=im.getpixel((x,y));hexcode='#'+''.join(f'{c:02X}' for c in rgb)
  samples.append({'name':name,'x':x,'y':y,'rgb':rgb,'hex':hexcode})
out=Image.new('RGB',(1200,920),'#F6F1E7');d=ImageDraw.Draw(out)
d.text((60,36),'固定输入，再记录采样位置',font=ft(42),fill='#202824')
d.text((60,105),f'源图 {width} × {height} px · 左上角为 (0, 0)',font=ft(26),fill='#465E70')
for i,s in enumerate(samples):
 y=180+i*126;d.rectangle((60,y,295,y+94),fill=s['hex'])
 d.text((330,y+4),s['name'],font=ft(32),fill='#202824')
 d.text((610,y+4),s['hex'],font=ft(31),fill='#202824')
 d.text((330,y+52),f"坐标 ({s['x']}, {s['y']}) · RGB {tuple(s['rgb'])}",font=ft(24),fill='#465E70')
d.text((60,841),'文件像素采样 ≠ 材料本色；不同位置可能读到不同的光影。',font=ft(25),fill='#465E70')
out.save(ROOT/'assets/images/sample-v2-extract.png',optimize=True)
(ROOT/'references/photographic-samples-v2.json').write_text(json.dumps({'source':str(source.relative_to(ROOT)),'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'width':width,'height':height,'samples':samples},ensure_ascii=False,indent=2)+'\n')
print(json.dumps(samples,ensure_ascii=False))
