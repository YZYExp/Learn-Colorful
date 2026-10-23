"""Shared editorial drawing primitives for the revised precise figures."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageCms
from functools import lru_cache
import os, textwrap
ROOT=Path(__file__).resolve().parents[1]
W=1080
PAPER='#FBFAF6';WARM='#F6F1E7';GREEN='#24544B';INK='#202824';MUTED='#626A66';LINE='#D6DBD5';ORANGE='#C86345';WHITE='#FFFFFF'
FONT=os.environ.get('COLOR_BOOK_FONT','/usr/local/share/fonts/investment/NotoSerifCJKsc-Regular.otf')
if not Path(FONT).is_file():
 FONT=next(str(p) for base in ['/usr/share/fonts','/usr/local/share/fonts'] for p in Path(base).rglob('*') if p.suffix in ('.ttc','.otf','.ttf') and any(v in p.name for v in ('NotoSerifCJK','NotoSansCJK','SourceHan')))
@lru_cache(maxsize=100)
def font(n):return ImageFont.truetype(FONT,n)
def contrast(a,b):
 def lum(h):
  x=[int(h[i:i+2],16)/255 for i in (1,3,5)];x=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in x]
  return sum(u*v for u,v in zip(x,(.2126,.7152,.0722)))
 x,y=sorted((lum(a),lum(b)));return (y+.05)/(x+.05)
class Page:
 def __init__(self,key,title,subtitle='',height=1500):
  self.key=str(key).zfill(2);self.im=Image.new('RGB',(W,height),PAPER);self.d=ImageDraw.Draw(self.im);self.h=height;self.boxes=[]
  self.text(64,35,'色彩的语言    /    '+self.key,26,MUTED)
  self.d.line((64,91,W-64,91),fill=LINE,width=2)
  self.text(64,119,title,51,INK)
  if subtitle:self.wrap(64,198,subtitle,30,MUTED,W-128,spacing=12)
  self.d.line((64,height-84,W-64,height-84),fill=LINE,width=2)
  self.text(64,height-63,'原创精确图解  ·  关系与数值见正文',25,MUTED)
 def text(self,x,y,s,size=36,color=INK,maxw=None):
  f=font(size);b=self.d.textbbox((x,y),str(s),font=f)
  if b[0]<0 or b[2]>W-24 or b[3]>self.h-20:raise ValueError(f'Out of page {self.key} {s} {b}')
  if maxw and b[2]-b[0]>maxw:raise ValueError(f'Text too wide {self.key} {s}')
  self.d.text((x,y),str(s),font=f,fill=color);self.boxes.append(b);return b[3]
 def wrap(self,x,y,s,size=36,color=INK,width=None,spacing=12):
  width=width or W-x-64;line='';step=size+spacing
  for c in str(s):
   if c=='\n' or self.d.textbbox((0,0),line+c,font=font(size))[2]>width:
    self.text(x,y,line,size,color);y+=step;line='' if c=='\n' else c
   else:line+=c
  if line:self.text(x,y,line,size,color);y+=step
  return y
 def rect(self,box,fill,outline=None,radius=0,width=2):
  if radius:self.d.rounded_rectangle(box,radius=radius,fill=fill,outline=outline,width=width)
  else:self.d.rectangle(box,fill=fill,outline=outline,width=width)
 def line(self,points,fill=LINE,width=2):self.d.line(points,fill=fill,width=width)
 def image(self,path,box):
  with Image.open(ROOT/path) as src:
   src.load();src=src.convert('RGB');src.thumbnail((box[2]-box[0],box[3]-box[1]),Image.Resampling.LANCZOS)
   self.im.paste(src,(int(box[0]+(box[2]-box[0]-src.width)/2),int(box[1]+(box[3]-box[1]-src.height)/2)))
 def save(self):
  scratch=ROOT/'build/figure-drafts';scratch.mkdir(parents=True,exist_ok=True);dest=scratch/f'fig-{self.key}.png'
  profile=ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB')).tobytes()
  self.im.save(dest,optimize=True,icc_profile=profile)
  with Image.open(dest) as check:check.load()
  os.replace(dest,ROOT/'assets/images'/f'fig-{self.key}.png')
  return {'id':self.key,'width':W,'height':self.h,'text_items':len(self.boxes),'profile':'sRGB'}
