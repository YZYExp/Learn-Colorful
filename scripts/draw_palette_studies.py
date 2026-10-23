#!/usr/bin/env python3
"""Eight original controlled palette applications; not trend or brand claims."""
from pathlib import Path
import os,json
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1]
candidates=[os.environ.get('COLOR_BOOK_FONT',''),'/usr/local/share/fonts/investment/NotoSerifCJKsc-Regular.otf']
candidates += [str(p) for base in ['/usr/share/fonts','/usr/local/share/fonts','/System/Library/Fonts','/Library/Fonts'] if Path(base).exists() for p in Path(base).rglob('*') if p.suffix in ['.otf','.ttc','.ttf'] and any(s in p.name.lower() for s in ['notoserifcjk','notosanscjk','sourcehan','pingfang'])]
FONT=next((p for p in candidates if p and Path(p).is_file()),None)
if not FONT:raise SystemExit('Install a CJK font and set COLOR_BOOK_FONT to its absolute path.')
def ft(n):return ImageFont.truetype(FONT,n)
def lum(h):
 v=[int(h[i:i+2],16)/255 for i in [1,3,5]];v=[c/12.92 if c<=.04045 else ((c+.055)/1.055)**2.4 for c in v]
 return sum(a*b for a,b in zip(v,[.2126,.7152,.0722]))
def ratio(a,b):
 x,y=sorted([lum(a),lum(b)]);return (y+.05)/(x+.05)
sets=[('暖纸与墨绿','#F6F1E7','#202824','#24544B','#C86345'),('深蓝与柠黄','#F3F6FA','#192B52','#244799','#E2BC39'),('浅粉与深梅','#FAEEF2','#44273C','#6A345A','#B86272'),('沙色与灰蓝','#F2E8DC','#3C3027','#465E70','#B45E3D'),('亮蓝与青柠','#F4F6FF','#18233D','#1649BF','#CAE34C'),('深灰与浅金','#242726','#F4EEDC','#F4EEDC','#C4A66C'),('浅灰与鲜红','#F1F1EF','#242424','#303030','#D84235'),('淡紫与深靛','#F0EEF8','#2C2749','#44387A','#BD714C')]
out=ROOT/'assets/images';out.mkdir(exist_ok=True)
meta=[]
for i,(title,bg,ink,main,accent) in enumerate(sets,1):
 im=Image.new('RGB',(1200,820),bg);d=ImageDraw.Draw(im)
 d.text((60,35),f'配色应用研究 {i:02}  /  {title}',font=ft(31),fill=ink)
 d.rectangle((60,110,1140,112),fill=ink)
 d.text((75,165),'周末开放日',font=ft(88),fill=main)
 d.text((80,295),'阅读 · 展览 · 相遇',font=ft(36),fill=ink)
 d.text((80,375),'周六 14:00—18:00',font=ft(30),fill=ink)
 d.ellipse((820,185,1090,455),fill=accent)
 d.rectangle((820,320,1090,455),fill=main)
 d.rectangle((80,500,420,585),fill=main)
 d.text((122,515),'查看活动安排',font=ft(35),fill=bg)
 for j,(role,c) in enumerate(zip(['背景','正文','主色','点缀'],[bg,ink,main,accent])):
  x=60+j*285;d.rectangle((x,640,x+245,690),fill=c,outline=ink,width=1)
  d.text((x,705),role+' '+c,font=ft(25),fill=ink)
 im.save(out/f'palette-{i:02}.png',optimize=True)
 meta.append({'id':i,'title':title,'background':bg,'text':ink,'main':main,'accent':accent,'text_contrast':ratio(ink,bg),'main_contrast':ratio(main,bg)})
(ROOT/'references/palette-studies.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2))
print('Generated 8 original palette application studies')
# Original typographic cover, independent of generated contextual illustrations.
im=Image.new('RGB',(1400,2000),'#F6F1E7');d=ImageDraw.Draw(im)
d.text((105,110),'色彩观察 · 配色实践 · 系统方法',font=ft(33),fill='#24544B')
d.rectangle((105,190,1295,194),fill='#24544B')
d.text((95,290),'色彩的语言',font=ft(178),fill='#202824')
d.text((110,535),'从看懂颜色到建立配色系统',font=ft(51),fill='#24544B')
cols=['#24544B','#C86345','#244799','#E2BC39','#6A345A','#B9D9CE']
for j,c in enumerate(cols):
 x=110+(j%3)*405;y=800+(j//3)*400
 d.rectangle((x,y,x+365,y+360),fill=c)
 d.ellipse((x+85,y+80,x+280,y+275),fill=cols[(j+2)%6])
d.text((110,1730),'从一张色卡，到一个真实场景',font=ft(44),fill='#202824')
d.text((110,1820),'六篇 · 二十四章 · 图解知识读本',font=ft(32),fill='#24544B')
im.save(out/'cover.png',optimize=True)
