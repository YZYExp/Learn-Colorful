#!/usr/bin/env python3
"""Editorial, numerically verified diagrams for colour foundations."""
from pathlib import Path
import argparse, colorsys, json, math
from PIL import Image, ImageDraw
from figure_style import Page, PAPER, WARM, GREEN, INK, MUTED, LINE, ORANGE, WHITE, ROOT


def hx(rgb):return '#'+''.join(f'{round(max(0,min(1,v))*255):02X}' for v in rgb)
def hsl(h,s,l):return hx(colorsys.hls_to_rgb(h/360,l,s))
def rgb(h):return tuple(int(h[i:i+2],16) for i in (1,3,5))
def exact_rect(p,x,y,w,h,c):p.rect((x,y,x+w-1,y+h-1),c)
def assert_pixel(p,xy,color):assert p.im.getpixel(xy)==rgb(color),(p.key,xy,p.im.getpixel(xy),color)
def section(p,y,num,title,note=None):
 p.text(64,y,num,30,GREEN);p.text(140,y-4,title,40)
 if note:p.text(64,y+60,note,30,MUTED)
def samples(p,y,cols,labels,height=142):
 width=147;gap=14
 for j,(col,label) in enumerate(zip(cols,labels)):
  x=64+j*(width+gap);exact_rect(p,x,y,width,height,col)
  p.text(x,y+height+13,label,30,MUTED)
  assert_pixel(p,(x+width//2,y+height//2),col)

def dimensions():
 p=Page('03','把一次修改，拆成三个方向','每次只改变一个 HSL 坐标；其余两个保持不变。',height=1540)
 hs=[0,60,120,180,240,300];ls=[.15,.28,.41,.54,.67,.8];ss=[0,.15,.3,.45,.6,.75]
 section(p,310,'01','换色相 H','S = 50%    ·    L = 45%')
 samples(p,430,[hsl(h,.5,.45) for h in hs],[f'{h}°' for h in hs])
 section(p,680,'02','调明暗 L','H = 160°    ·    S = 35%')
 samples(p,800,[hsl(160,.35,l) for l in ls],[f'{round(l*100)}%' for l in ls])
 section(p,1050,'03','改饱和度 S','H = 160°    ·    L = 45%')
 samples(p,1170,[hsl(160,s,.45) for s in ss],[f'{round(s*100)}%' for s in ss])
 p.wrap(64,1390,'HSL 的 L、S 是模型坐标，不等同于感知明度、彩度。',30,MUTED)
 m=p.save();m['verified']={'H':hs,'L':ls,'S':ss,'fixed':[{'S':.5,'L':.45},{'H':160,'S':.35},{'H':160,'L':.45}],'samples':'18 swatch centre pixels exact'};return m

def context():
 p=Page('04','同一个灰，环境改变了判断','先比较中心，再用下方的同色条复查。',height=1530)
 for y,bg,label in [(330,INK,'01  深墨背景  #202824'),(810,WARM,'02  暖纸背景  #F6F1E7')]:
  p.text(64,y-66,label,36)
  exact_rect(p,64,y,952,300,bg);exact_rect(p,420,y+65,240,170,'#808080')
  assert_pixel(p,(540,y+150),'#808080');assert_pixel(p,(100,y+150),bg)
 p.text(64,1190,'验证：两块中心色，移到同一背景',36)
 exact_rect(p,64,1260,476,84,'#808080');exact_rect(p,540,1260,476,84,'#808080')
 p.text(64,1360,'左半与右半均为 #808080，接缝没有色差。',30,MUTED)
 assert_pixel(p,(539,1300),'#808080');assert_pixel(p,(540,1300),'#808080')
 m=p.save();m['verified']={'centres':'#808080','backgrounds':[INK,WARM],'verification_seam':'two adjacent pixels identical; no divider drawn'};return m

def wheel():
 p=Page('05','色轮给方向，画面定分工','HSL 色相环；不是颜料的混色配方。',height=1770)
 cx,cy,outer,inner=540,555,242,160
 for h in range(360):p.d.pieslice((cx-outer,cy-outer,cx+outer,cy+outer),h-90,h-88,fill=hsl(h,.6,.52))
 p.d.ellipse((cx-inner,cy-inner,cx+inner,cy+inner),fill=PAPER)
 p.text(466,518,'HSL',46);p.text(447,581,'色相角',36,MUTED)
 for h,t in [(0,'0°'),(90,'90°'),(180,'180°'),(270,'270°')]:
  a=math.radians(h-90);x=cx+300*math.cos(a);y=cy+300*math.sin(a)
  p.text(int(x-35),int(y-22),t,32,MUTED)
 data=[(950,'01','单色','H = 160°；L = 30 / 45 / 60%',[hsl(160,.5,l) for l in [.3,.45,.6]],['30%','45%','60%']),
       (1180,'02','邻近','H = 130 / 160 / 190°',[hsl(h,.5,.45) for h in [130,160,190]],['130°','160°','190°']),
       (1410,'03','相对','H = 160 / 340°；相隔 180°',[hsl(h,.5,.45) for h in [160,340]],['160°','340°'])]
 for y,num,t,note,cols,labels in data:
  p.text(64,y,num,30,GREEN);p.text(140,y-4,t,40);p.text(64,y+62,note,30,MUTED)
  x0=620;w=116;gap=20
  for j,(c,l) in enumerate(zip(cols,labels)):
   x=x0+j*(w+gap);exact_rect(p,x,y,w,94,c);p.text(x,y+104,l,30,MUTED);assert_pixel(p,(x+50,y+40),c)
 p.wrap(64,1640,'关系只提供候选；明暗、彩度与面积还要另行安排。',30,MUTED)
 m=p.save();m['verified']={'ring':{'S':.6,'L':.52},'monochrome':{'H':160,'S':.5,'L':[.3,.45,.6]},'analogous':[130,160,190],'opposite':[160,340]};return m

def area():
 p=Page('07','不换颜色，只改变面积','同一矩形、同一位置；陶橘从局部变成半幅。',height=1470)
 counts=[]
 for y,r,label in [(400,.1,'01  陶橘 10%  /  墨绿 90%'),(900,.5,'02  陶橘 50%  /  墨绿 50%')]:
  p.text(70,y-80,label,40)
  w,h=940,250;x=70;split=x+w-round(w*r)
  exact_rect(p,x,y,w,h,GREEN);exact_rect(p,split,y,round(w*r),h,ORANGE)
  pixels=[p.im.getpixel((xx,y+100)) for xx in range(x,x+w)]
  count=pixels.count(rgb(ORANGE));assert count==round(w*r);assert count/w==r
  p.line((split,y+h+22,split,y+h+42),fill=ORANGE,width=3)
  p.text(70,y+h+35,'色区总面积保持不变',30,MUTED)
  counts.append({'ratio':r,'orange_columns':count,'width':w,'height':h,'orange_pixels':count*h,'total_pixels':w*h})
 p.wrap(64,1260,'注意力还受形状、位置与明暗影响；比例不是优劣评分。',30,MUTED)
 m=p.save();m['verified']={'area_counts':counts,'inclusive_pixel_edges':True,'labels_outside_measured_colour_region':True};return m

def rhythm():
 p=Page('08','让重复产生节奏','六个模块尺寸、间距相同；只改变陶橘出现的位置。',height=1400)
 rows=[(380,'01','连续重复',[GREEN]*6,'同一色连续出现，建立稳定的起点。'),(740,'02','规律点缀',[GREEN,GREEN,ORANGE,GREEN,GREEN,ORANGE],'每第三格一次变化，形成可预期的间隔。'),(1100,'03','收尾强调',[GREEN]*5+[ORANGE],'变化只落在末格，形成结束位置的停顿。')]
 for y,n,t,cols,note in rows:
  section(p,y-90,n,t)
  for j,c in enumerate(cols):
   x=64+j*161;exact_rect(p,x,y,147,135,c);assert_pixel(p,(x+73,y+60),c)
  p.text(64,y+157,note,30,MUTED)
 m=p.save();m['verified']={'rows':[[1,1,1,1,1,1],[1,1,2,1,1,2],[1,1,1,1,1,2]],'modules':6,'module_width':147,'gap':14};return m

def relative_warmth():
 p=Page('08b','冷暖，要放在关系里比较','右边的灰褐始终不变；只替换左边的邻接色。',height=1350)
 for y,n,partner,label in [(380,'01',ORANGE,'与偏橘相邻'),(850,'02','#557C94','与偏蓝相邻')]:
  section(p,y-88,n,label)
  exact_rect(p,64,y,476,250,partner);exact_rect(p,540,y,476,250,'#9E8267')
  p.text(64,y+276,partner,34,MUTED);p.text(580,y+276,'固定 #9E8267',34)
  assert_pixel(p,(200,y+100),partner);assert_pixel(p,(700,y+100),'#9E8267')
 p.wrap(64,1210,'比较右侧的相对感受；这不是测量光源色温。',30,MUTED)
 m=p.save();m['verified']={'fixed':'#9E8267','neighbours':[ORANGE,'#557C94'],'right_panels':'pixel-identical RGB values'};return m

def mixing():
 p=Page('02b','加色与减色，是两种模型','理想 RGB / CMY 通道实验；不是颜料配方。',height=1810)
 centres=[(360,170),(590,170),(475,335)];radius=165;panels=[]
 for y,additive,name in [(360,True,'01  RGB：发光相加'),(1090,False,'02  CMY：理想滤色')]:
  p.text(64,y-78,name,40)
  masks=[]
  for cx,cy in centres:
   mask=Image.new('L',(952,500),0);d=ImageDraw.Draw(mask);d.ellipse((cx-radius,cy-radius,cx+radius,cy+radius),fill=255)
   if not additive:mask=mask.point(lambda v:255-v)
   masks.append(mask)
  panel=Image.merge('RGB',masks);p.im.paste(panel,(64,y))
  tests={'single_R_or_C':((300,125),(255,0,0) if additive else (0,255,255)), 'single_G_or_M':((660,125),(0,255,0) if additive else (255,0,255)), 'single_B_or_Y':((475,430),(0,0,255) if additive else (255,255,0)), 'RG_or_CM':((475,90),(255,255,0) if additive else (0,0,255)), 'GB_or_MY':((590,290),(0,255,255) if additive else (255,0,0)), 'BR_or_YC':((360,290),(255,0,255) if additive else (0,255,0)), 'triple':((475,230),(255,255,255) if additive else (0,0,0))}
  for key,(xy,want) in tests.items():assert panel.getpixel(xy)==want,(name,key,panel.getpixel(xy),want)
  panels.append({'mode':'RGB' if additive else 'CMY','verified_sample_pixels':{k:{'xy':list(xy),'rgb':list(want)} for k,(xy,want) in tests.items()}})
  if additive:
   p.text(64,y+528,'R + G = 黄   ·   G + B = 青   ·   B + R = 品红',30)
   p.text(64,y+582,'三束理想通道完全相加，中心为白。',30,MUTED)
  else:
   p.text(64,y+528,'青与品红 → 蓝   ·   品红与黄 → 红',30)
   p.text(64,y+582,'黄与青 → 绿；三种理想滤色交叠为黑。',30,MUTED)
 m=p.save();m['verified']={'exact_8_bit_masks':True,'alpha_blending':False,'panels':panels};return m

DRAWERS={'03':dimensions,'04':context,'05':wheel,'07':area,'08':rhythm,'08b':relative_warmth,'02b':mixing}
def main(only=None):
 only=set(DRAWERS) if only is None else set(only);metadata=[]
 for k,fn in DRAWERS.items():
  if k in only:metadata.append(fn())
 if metadata:
  path=ROOT/'editorial/redraw-foundations.json';old=json.loads(path.read_text()) if path.exists() else []
  merged={m['id']:m for m in old};merged.update({m['id']:m for m in metadata});path.write_text(json.dumps(list(merged.values()),ensure_ascii=False,indent=2)+'\n')
 return metadata
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--only',nargs='+');args=parser.parse_args();print(json.dumps(main(args.only),ensure_ascii=False,indent=2))
