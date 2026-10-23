#!/usr/bin/env python3
"""Draw complete applied color lessons with precise typography and an unchanged AI photograph.

All output PNGs carry an sRGB ICC profile. The cross-media illustrations are
workflow/record examples, never a CMYK conversion, gamut-mapping experiment or
ICC soft proof. Run from any directory; dependencies: Pillow and a CJK font.
"""
from pathlib import Path
import os,json
from PIL import Image,ImageDraw,ImageFont,ImageCms
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/images'
FONT=next((p for p in [os.environ.get('COLOR_BOOK_FONT',''),'/usr/local/share/fonts/investment/NotoSerifCJKsc-Regular.otf'] if p and Path(p).is_file()),None)
if not FONT:raise SystemExit('Set COLOR_BOOK_FONT to an installed CJK font.')
SANS='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
PAPER='#F6F1E7';INK='#202824';GREEN='#24544B';ORANGE='#C86345';ERROR='#9B3A2C';MUTED='#59625B';LINE='#C6CDC6'
ICC=ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB')).tobytes()
PHOTO=Image.open(ROOT/'assets/images/case-editorial.png').convert('RGB')
RECORD=[]
def ft(n):return ImageFont.truetype(FONT,n)
def en(n,bold=False):return ImageFont.truetype(BOLD if bold else SANS,n)
def text(d,xy,s,size=30,color=INK,font=None):d.text(xy,s,font=font or ft(size),fill=color)
def center(d,box,s,size=30,color=INK):
 f=ft(size);b=d.textbbox((0,0),s,font=f);x=(box[0]+box[2]-(b[2]-b[0]))/2;y=(box[1]+box[3]-(b[3]-b[1]))/2-b[1];d.text((x,y),s,font=f,fill=color)
def image(im,box,src=PHOTO):
 pic=src.copy();pic.thumbnail((box[2]-box[0],box[3]-box[1]),Image.Resampling.LANCZOS);im.paste(pic,(box[0]+(box[2]-box[0]-pic.width)//2,box[1]+(box[3]-box[1]-pic.height)//2))
def save(im,name,chapter,lesson):
 target=OUT/name;tmp=target.with_suffix('.tmp.png');im.save(tmp,icc_profile=ICC,optimize=True)
 with Image.open(tmp) as check:check.load()
 tmp.replace(target)
 RECORD.append({'image':'assets/images/'+name,'chapter':chapter,'method':'Pillow精确排印与绘制；原比例嵌入同一AI虚构书刊摄影；嵌入sRGB ICC','lesson':lesson,'photo_source':'assets/images/case-editorial.png'})
def top(d,label,n=1200):
 text(d,(60,30),label,27);d.line((60,90,n-60,90),fill=INK,width=2)

def contrast(a,b):
 def L(h):
  c=[int(h[i:i+2],16)/255 for i in (1,3,5)];c=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in c];return sum(x*y for x,y in zip(c,(.2126,.7152,.0722)))
 x,y=sorted((L(a),L(b)));return (y+.05)/(x+.05)

def poster(chapter,stage):
 im=Image.new('RGB',(1200,1640),'#E7E8E3');d=ImageDraw.Draw(im)
 if chapter==6:
  low=stage==0;title='A  低对比版本' if low else 'B  保持版式，只修正文字颜色';top(d,title)
  title_bg=PAPER;info_bg=PAPER;title_color=body_color='#B9B8A8' if low else GREEN;accent=ORANGE;button_bg=PAPER;button_color=body_color
 else:
  labels=['A  起点：三种竞争同时发生','B  第一步：先恢复信息可读性','C  第二步：让装饰退后','D  第三步：明确预约入口'];top(d,labels[stage])
  title_bg='#24544B' if stage<2 else PAPER;info_bg='#C86345' if stage==0 else PAPER
  title_color='#B9D9CE' if stage<2 else GREEN;body_color='#D78D70' if stage==0 else INK;accent=GREEN if stage<2 else '#D8D6C7';button_bg=ORANGE if stage<3 else GREEN;button_color='#D78D70' if stage==0 else (INK if stage<3 else '#FFFFFF')
 d.rectangle((40,115,1160,1590),fill=PAPER)
 text(d,(80,150),'间色文化空间',24,color=body_color);text(d,(710,153),'JIANSE / READING SERIES',font=en(21),color=body_color)
 d.rectangle((80,225,1120,390),fill=title_bg)
 text(d,(101,236),'光与纸的夜晚',105,title_color)
 text(d,(90,414),'A NIGHT OF LIGHT & PAPER',font=en(30,True),color=body_color)
 d.rectangle((80,477,1120,495),fill=accent)
 image(im,(80,525,1120,1218))
 d.rectangle((80,1237,1120,1545),fill=info_bg)
 text(d,(100,1250),'周五夜读 · 第四期',33,body_color)
 text(d,(100,1305),'10月30日  19:30—21:00',34,body_color)
 text(d,(100,1363),'间色文化空间 · 二层阅读室',28,body_color)
 d.rounded_rectangle((100,1430,610,1517),radius=3,fill=button_bg)
 center(d,(100,1430,610,1517),'预约座位',36,button_color)
 text(d,(700,1450),'查看活动须知',27,body_color)
 if chapter==16 and stage==3:d.line((700,1492,868,1492),fill=body_color,width=2)
 name=f'applied-v2-{chapter:02}-'+chr(97+stage)+'.png'
 lesson=('完整海报：低对比文字与高对比文字，摄影/版式/字号不变；文字对比为'+f'{contrast(title_color,PAPER):.2f}:1') if chapter==6 else '同一海报冻结骨架，分步恢复阅读、减少竞争、明确预约入口；最后增加链接下划线'
 save(im,name,chapter,lesson)

def ui(danger=False):
 im=Image.new('RGB',(1200,1740),PAPER);d=ImageDraw.Draw(im)
 top(d,'B  我的预约：危险操作需独立语义' if danger else 'A  活动预约：品牌色、链接与选中状态')
 text(d,(70,125),'间色',42,GREEN);text(d,(780,141),'活动    我的预约',28)
 d.line((70,214,1130,214),fill=LINE,width=2)
 if not danger:
  text(d,(70,254),'预约一场夜读',62,GREEN)
  text(d,(73,348),'光与纸的夜晚  /  每场19:30开始',31)
  image(im,(70,415,1130,860))
  text(d,(70,896),'1  选择到店日期',32)
  for box,label,selected in [((70,970,575,1065),'✓ 10月30日 周五',True),((600,970,1130,1065),'10月31日 周六',False)]:
   d.rounded_rectangle(box,8,fill='#E5EDE8' if selected else '#FFFFFF',outline=GREEN if selected else LINE,width=3 if selected else 2);center(d,box,label,31,GREEN if selected else INK)
  text(d,(70,1115),'2  联系电话',32);d.rounded_rectangle((70,1180,1130,1268),5,fill='#FFFFFF',outline=ERROR,width=3)
  text(d,(98,1196),'请输入手机号',29,MUTED);text(d,(70,1293),'！请填写联系电话，以便接收预约通知。',28,ERROR)
  text(d,(70,1360),'查看预约规则',28,GREEN);d.line((70,1400,238,1400),fill=GREEN,width=2)
  text(d,(70,1451),'单人入场  ¥ 0  /  需要提前预约',29)
  d.rounded_rectangle((70,1523,1130,1625),5,fill=GREEN);center(d,(70,1523,1130,1625),'确认预约',38,'#FFFFFF')
  text(d,(70,1660),'颜色提示方向；文字、边框和勾选确认具体含义。',25,MUTED)
 else:
  text(d,(70,255),'我的预约',62,GREEN)
  d.rounded_rectangle((70,390,1130,680),8,fill='#FFFFFF',outline=LINE,width=2)
  text(d,(105,420),'✓ 预约已确认',32,GREEN);text(d,(105,483),'光与纸的夜晚',43)
  text(d,(105,555),'10月30日 19:30—21:00  /  1位',30);text(d,(105,611),'预约编号  JS-1030-018',26,MUTED)
  d.rounded_rectangle((70,760,1130,1425),8,fill='#FFFDF9',outline=ERROR,width=3)
  text(d,(110,798),'！取消这次预约？',48,ERROR)
  text(d,(110,909),'取消后将释放座位。若活动满额，',33);text(d,(110,965),'再次预约可能无法保留原座位。',33)
  d.line((110,1060,1090,1060),fill=LINE,width=2)
  d.rounded_rectangle((110,1110,1090,1220),5,fill=ERROR);center(d,(110,1110,1090,1220),'确认取消预约',38,'#FFFFFF')
  d.rounded_rectangle((110,1255,1090,1360),5,fill='#FFFFFF',outline=GREEN,width=3);center(d,(110,1255,1090,1360),'保留预约，返回详情',34,GREEN)
  text(d,(70,1500),'危险操作使用明确动词，而不是只把品牌按钮染红。',28,MUTED)
  text(d,(70,1560),'“预约已确认”是状态；“保留预约”是操作。',28,MUTED)
 save(im,'applied-v2-21-'+('b' if danger else 'a')+'.png',21,'完整预约界面显示背景/正文/主操作/链接/选中/错误/危险角色；用词、边框、图标补充颜色')

def delivery(paper=False):
 im=Image.new('RGB',(1200,1660),PAPER);d=ImageDraw.Draw(im)
 top(d,'B  纸张样张：先登记条件，再比较实物' if paper else 'A  屏幕交付：颜色数值需要解释条件')
 text(d,(70,135),'样张不是屏幕截图' if paper else '同一方案，分开交付',58,GREEN)
 text(d,(73,225),'示意记录 · 非 ICC 软打样 · 非实际印刷预测',26,ERROR)
 if paper:
  d.rectangle((72,310,1128,1040),fill='#DDD7C7')
  d.rectangle((130,350,1065,1000),fill='#FFFDF7',outline='#A9AC9E',width=2)
  text(d,(170,386),'间色 / 纸张样张登记卡',36,GREEN)
  image(im,(170,470,1025,1040-120))
  text(d,(170,932),'JIANSE  /  原稿、纸张与实物分开记录',24)
  rows=[('目标纸张','由承印方确认；图中纸色仅作情境示意'),('输出配置','记录承印方提供的 ICC 名称和版本'),('核对项目','深绿与深墨、细字边缘、暖纸底与纸白'),('确认依据','实际样张 + 约定照明；不是这张生成图')]
 else:
  d.rounded_rectangle((70,310,1130,1030),12,fill='#303735')
  d.rectangle((100,345,1100,970),fill='#FFFFFF')
  image(im,(130,375,1070,920))
  text(d,(135,927),'JIANSE / WEB PREVIEW',font=en(22,True),color=GREEN)
  rows=[('屏幕副本','jianse-event-web-v1.png'),('颜色解释','sRGB；导出时嵌入正确配置文件'),('输出尺寸','按发布位置决定像素，不拿屏幕图替印刷稿'),('保留主文件','可编辑文字、摄影、图形与版本记录')]
 y=1090
 for label,value in rows:
  d.line((70,y,1130,y),fill=LINE,width=2);text(d,(70,y+20),label,29,GREEN);text(d,(70,y+69),value,26);y+=125
 text(d,(70,1605),'本图只示意交付条件，不做色域转换、纸张或油墨模拟。',24,ERROR)
 save(im,'applied-v2-23-'+('b' if paper else 'a')+'.png',23,'跨媒介交付记录：全部图像sRGB，不做CMYK/gamut映射；纸张外观是情境示意而非实际软打样')

def main():
 for i in range(2):poster(6,i)
 for i in range(4):poster(16,i)
 ui();ui(True);delivery();delivery(True)
 (ROOT/'editorial/applied-case-v2.json').write_text(json.dumps({'generator':'scripts/draw_applied_cases.py','run':'python scripts/draw_applied_cases.py','photo_status':'AI生成虚构书刊；不是实际品牌、建筑或出版物','cases':RECORD},ensure_ascii=False,indent=2))
 for r in RECORD:
  with Image.open(ROOT/r['image']) as check:check.load()
 print('Generated and decoded',len(RECORD),'applied teaching panels')
if __name__=='__main__':main()
