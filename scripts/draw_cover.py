#!/usr/bin/env python3
"""Compose the cover from precise typography and one original AI scene."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageCms
import os
ROOT=Path(__file__).resolve().parents[1]
FONT=os.environ.get('COLOR_BOOK_FONT','/usr/local/share/fonts/investment/NotoSerifCJKsc-Regular.otf')
if not Path(FONT).is_file():
 FONT=next(str(p) for root in ['/usr/share/fonts','/usr/local/share/fonts'] for p in Path(root).rglob('*') if p.suffix in ('.otf','.ttc','.ttf') and 'Noto' in p.name and 'CJK' in p.name)
def main():
 im=Image.new('RGB',(1400,2000),'#F6F1E7');d=ImageDraw.Draw(im)
 def text(x,y,s,size,color):
  f=ImageFont.truetype(FONT,size);box=d.textbbox((x,y),s,font=f)
  assert box[2]<1375 and box[3]<1970,(s,box)
  d.text((x,y),s,font=f,fill=color)
 text(90,65,'COLOR  /  LANGUAGE',34,'#24544B');text(1080,65,'图解读本',31,'#626A66')
 d.line((90,135,1310,135),fill='#202824',width=2)
 text(82,190,'色彩的语言',190,'#202824')
 text(93,475,'从看懂颜色到建立配色系统',54,'#24544B')
 text(93,590,'从光与感知，走进日常物件与完整设计',36,'#626A66')
 with Image.open(ROOT/'assets/images/chapter-v2-extract.png') as photo:
  photo=photo.convert('RGB');photo.thumbnail((1220,900),Image.Resampling.LANCZOS)
  im.paste(photo,((1400-photo.width)//2,760))
 d.line((90,1688,1310,1688),fill='#202824',width=2)
 for x,s,c in [(90,'观察','#24544B'),(410,'关系','#C86345'),(730,'应用','#244799'),(1050,'系统','#24544B')]:
  d.rectangle((x,1745,x+10,1808),fill=c);text(x+27,1740,s,46,'#202824')
 text(90,1885,'六篇 · 二十四章',31,'#626A66');text(985,1885,'色彩知识书',31,'#626A66')
 temp=ROOT/'build/cover-draft.png';temp.parent.mkdir(exist_ok=True);im.save(temp,optimize=True,icc_profile=ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB')).tobytes())
 with Image.open(temp) as check:check.load()
 os.replace(temp,ROOT/'assets/images/cover.png')
if __name__=='__main__':main()
