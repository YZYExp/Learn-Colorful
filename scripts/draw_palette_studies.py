#!/usr/bin/env python3
"""Eight original controlled palette applications; not trend or brand claims."""
from pathlib import Path
import argparse,os,json
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

def latin(n,bold=False,serif=False):
    file=Path('/usr/share/fonts/opentype/urw-base35/NimbusRoman-Italic.otf') if serif else Path('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
    return ImageFont.truetype(str(file) if file.is_file() else FONT,n)

def studies(image_path):
    # The identical photographic image is embedded whole in every comparison.
    # Its colors are fixed; only the surrounding four-role color system changes.
    if not image_path.is_file():raise SystemExit('Missing editorial photograph: '+str(image_path))
    photo=Image.open(image_path).convert('RGB')
    photo.thumbnail((1420,980),Image.Resampling.LANCZOS)
    meta=[]
    for i,(title,bg,ink,main,accent) in enumerate(sets,1):
        im=Image.new('RGB',(1600,2200),bg);d=ImageDraw.Draw(im)
        d.text((90,52),'间色  /  出版与视觉文化',font=ft(31),fill=ink)
        d.text((1120,57),f'COLOR STUDY  {i:02} / 08',font=latin(25),fill=ink)
        d.line((90,120,1510,120),fill=ink,width=2)
        d.text((78,166),'光的形状',font=ft(174),fill=main)
        d.text((92,393),'The Shape of Light',font=latin(83,serif=True),fill=main)
        d.text((1150,405),'EXHIBITION',font=latin(34,bold=True),fill=ink)
        d.text((1150,455),'& OPEN STUDIO',font=latin(25),fill=ink)
        d.rectangle((90,521,1510,533),fill=accent)
        photo_x=90+(1420-photo.width)//2
        im.paste(photo,(photo_x,560))
        bottom=560+photo.height
        d.text((90,bottom+29),'01  /  一份刊物，如何把色彩放进阅读？',font=ft(29),fill=ink)
        d.line((90,bottom+95,1510,bottom+95),fill=ink,width=2)
        d.text((90,bottom+126),'从纸面到空间',font=ft(55),fill=main)
        d.text((92,bottom+207),'阅读 · 摄影 · 编辑设计',font=ft(30),fill=ink)
        d.text((970,bottom+129),'24 OCT — 08 NOV',font=latin(33,bold=True),fill=ink)
        d.text((970,bottom+183),'间色文化空间  /  14:00—18:00',font=ft(27),fill=ink)
        d.text((970,bottom+230),'JIANSE  /  READING ROOM',font=latin(24),fill=ink)
        d.line((90,1870,1510,1870),fill=ink,width=2)
        # Exact numeric study strip remains separate from the application.
        roles=['背景','正文','主色','点缀']
        for j,(role,c) in enumerate(zip(roles,[bg,ink,main,accent])):
            x=90+j*365
            d.rectangle((x,1910,x+325,1962),fill=c,outline=ink,width=1)
            d.text((x,1980),role,font=ft(25),fill=ink)
            d.text((x,2022),c,font=latin(25),fill=ink)
        d.text((90,2110),f'{i:02}  /  {title}',font=ft(27),fill=ink)
        d.text((650,2114),'固定版式与摄影，仅比较周边色彩分工',font=ft(25),fill=ink)
        target=out/f'palette-{i:02}.png'
        temporary=target.with_suffix('.tmp.png')
        im.save(temporary,optimize=True)
        with Image.open(temporary) as check:check.load()
        temporary.replace(target)
        with Image.open(target) as check:check.load()
        print(target.name,target.stat().st_size,flush=True)
        meta.append({'id':i,'title':title,'background':bg,'text':ink,'main':main,'accent':accent,'text_contrast':ratio(ink,bg),'main_contrast':ratio(main,bg)})
    (ROOT/'references/palette-studies.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2))
    print('Generated 8 editorial palette studies with one unchanged AI teaching photograph')

def cover():
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

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--image',type=Path,default=ROOT/'assets/images/case-editorial.png',help='Original fictional AI editorial photograph, embedded without cropping.')
    parser.add_argument('--cover',action='store_true',help='Also rebuild the independent original cover; otherwise leave it unchanged.')
    args=parser.parse_args()
    studies(args.image)
    if args.cover:cover()

if __name__=='__main__':main()
