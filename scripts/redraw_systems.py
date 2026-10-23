#!/usr/bin/env python3
"""Precise editorial diagrams: light path, chart encoding, roles, themes and output."""
import argparse,colorsys,json,math
from PIL import Image
from figure_style import Page,ROOT,WARM,GREEN,INK,MUTED,LINE,ORANGE,WHITE,font,contrast
OWN={'02','18','21','22','22b','23'}
RESULT=[]
def arrow(p,a,b,color=INK,width=5,head=18):
 p.line([a,b],color,width);ang=math.atan2(b[1]-a[1],b[0]-a[0]);p.d.polygon([b,(b[0]-head*math.cos(ang-.5),b[1]-head*math.sin(ang-.5)),(b[0]-head*math.cos(ang+.5),b[1]-head*math.sin(ang+.5))],fill=color)
def center(p,box,label,size=36,color=INK):
 bb=p.d.textbbox((0,0),label,font=font(size));p.text((box[0]+box[2]-bb[2]+bb[0])/2,(box[1]+box[3]-bb[3]-bb[1])/2,label,size,color)
def rule(p,y):p.line([(64,y),(1016,y)],LINE,2)
def done(p,data):
 result=p.save();result['data']=data
 with Image.open(ROOT/'assets/images'/f'fig-{p.key}.png') as check:check.load();assert check.width==1080
 RESULT.append(result)

def fig02():
 p=Page('02','颜色从哪里进入眼睛','观察不发光的绿色表面：入射 → 选择性反射 → 视觉',height=1770)
 p.text(82,300,'照明光源',40)
 # A small luminaire emits incoming light, rather than the material itself emitting.
 p.d.polygon([(115,394),(255,394),(281,471),(89,471)],fill='#E7E7DD',outline=INK,width=3)
 p.rect((147,355,223,394),INK)
 p.d.ellipse((110,445,260,480),fill='#FFFFFF',outline=INK,width=3)
 # Multiple colored lines are wavelength categories, not a measured spectrum.
 for start,end,color in [((149,483),(466,902),'#AD4D36'),((185,483),(522,902),'#41735B'),((221,483),(578,902),'#487696')]:arrow(p,start,end,color,7,22)
 p.wrap(64,690,'入射光：\n不同波段',36,INK,width=220)
 # Coated slab: the reflected path starts at the illuminated top surface.
 p.d.polygon([(334,900),(723,900),(822,1029),(433,1029)],fill=GREEN,outline=INK,width=3)
 p.d.polygon([(433,1029),(822,1029),(822,1090),(433,1090)],fill='#183D35',outline=INK,width=3)
 p.d.polygon([(334,900),(433,1029),(433,1090),(334,961)],fill='#426C60',outline=INK,width=3)
 arrow(p,(552,895),(813,490),GREEN,10,27)
 p.wrap(777,680,'反射光\n进入眼睛\n组成改变',35,GREEN,width=260)
 # Absorption is represented by arrows stopping within the material.
 arrow(p,(490,922),(554,1004),'#AD4D36',5,17);arrow(p,(575,922),(639,1004),'#487696',5,17)
 p.text(340,1125,'表面对不同波段的反射、吸收程度不同',34)
 p.text(340,1185,'图中的箭头不代表能量或波长比例',30,MUTED)
 # Eye outline: the ray enters from the left toward the pupil.
 eye_top=[(813+122*u/40,490-38*math.sin(math.pi*u/40)) for u in range(41)]
 eye_bottom=[(813+122*u/40,490+38*math.sin(math.pi*u/40)) for u in range(40,-1,-1)]
 p.d.polygon(eye_top+eye_bottom,fill=WHITE,outline=INK,width=3)
 p.d.ellipse((852,464,896,516),fill='#7E9D90',outline=INK,width=3)
 p.d.ellipse((866,474,884,507),fill=INK)
 p.text(770,366,'眼睛',40)
 p.wrap(654,286,'进入眼睛后：\n感光与神经处理',30,MUTED,width=340)
 rule(p,1292)
 p.text(64,1330,'这不是“绿色物体自己发出绿光”',40,GREEN)
 p.wrap(64,1410,'换光源，入射光会变；换材料，反射与吸收会变。我们看见的是进入眼睛的光，还受到适应和观看环境影响。',36,width=952,spacing=18)
 done(p,{'model':'non-emissive opaque green surface','incoming_bands':3,'reflective_path':'source → surface → eye','note':'schematic; neither measured spectrum nor energy fractions'})

def fig18():
 p=Page('18','颜色先回答：数据是什么关系','虚构教学数据。数值、名称与单位始终保留。',height=2010)
 p.text(64,292,'类别 / 活动人数',42)
 x0=240;scale=11
 vals=[('阅读',40,'#387C6C'),('饮品',55,'#8C6737'),('展览',30,'#7B658B')]
 for x in [0,20,40,60]:
  xx=x0+x*scale;p.line([(xx,382),(xx,708)],LINE,2);p.text(xx-16,724,str(x),32,MUTED)
 for y,(label,value,c) in zip([390,497,604],vals):
  p.text(64,y+6,label,38);p.rect((x0,y,x0+value*scale,y+67),c);p.text(x0+value*scale+18,y+8,str(value),36)
 p.line([(x0,708),(x0+660,708)],INK,2);p.text(704,785,'活动人数（人）',34)
 rule(p,861);p.text(64,898,'顺序 / 到访量示意等级',42)
 colors=['#DFEEE7','#B9D7C8','#85B69F','#4D8B72',GREEN]
 for j,(c,n) in enumerate(zip(colors,range(1,6))):
  x=80+j*184;p.rect((x,1000,x+184,1110),c,LINE);center(p,(x,1120,x+184,1187),str(n),40)
 p.text(80,1210,'低',34);arrow(p,(154,1240),(895,1240),INK,3,15);p.text(930,1210,'高',34)
 rule(p,1314);p.text(64,1352,'发散 / 实际参与率 − 计划参与率',40)
 p.text(64,1420,'单位：百分点；0＝达到计划参与率',33,MUTED)
 nums=[-20,-10,0,10,20];div=['#753428','#E3B09E',WARM,'#B9D7C8',GREEN]
 for j,(v,c) in enumerate(zip(nums,div)):
  x=80+j*184;p.rect((x,1505,x+184,1615),c,LINE);center(p,(x,1628,x+184,1695),f'{v:+}' if v else '0',38)
 p.line([(540,1482),(540,1624)],INK,3)
 p.text(80,1734,'低于计划',34);p.text(794,1734,'高于计划',34)
 p.rect((80,1820,137,1877),None,INK,width=2);p.line([(84,1871),(131,1825)],MUTED,2);p.text(164,1825,'缺失值另标，不能当成 0',33,MUTED)
 assert [v for _,v,_ in vals]==[40,55,30] and nums==[-20,-10,0,10,20]
 done(p,{'category_counts':dict((a,b) for a,b,_ in vals),'category_unit':'人','ordinal':[1,2,3,4,5],'diverging':nums,'diverging_unit':'百分点','zero':'实际参与率等于计划参与率'})

def fig21():
 p=Page('21','从基础色，走到有职责的控件','同一个色号需要配对、位置和用途，才形成可复用规则。',height=1930)
 p.text(64,295,'基础色值',36,MUTED);p.text(529,295,'角色 → 实际使用',36,MUTED)
 rows=[(GREEN,'action','主操作'),(WARM,'surface','内容表面'),(INK,'text','正文'),(ORANGE,'accent','装饰'),('#9B3A2C','error','错误')]
 for j,(c,key,label) in enumerate(rows):
  y=382+j*275
  p.rect((64,y+11,170,y+94),c,LINE);p.text(198,y+21,c,32)
  arrow(p,(424,y+55),(489,y+55),MUTED,3,14)
  p.text(529,y-37,label+' / '+key,36)
  if key=='action':
   p.rect((529,y+30,1016,y+121),GREEN,radius=4);center(p,(529,y+30,1016,y+121),'确认预约',38,WHITE);p.text(529,y+149,'on-action  #FFFFFF',30,MUTED)
  elif key=='surface':
   p.rect((529,y+30,1016,y+130),WARM,LINE);p.text(552,y+47,'活动详情',38,INK);p.text(529,y+156,'表面与文字成对检查',30,MUTED)
  elif key=='text':
   p.rect((529,y+27,1016,y+133),WARM);p.text(552,y+44,'周五 19:30 开始',36,INK);p.text(529,y+157,'正文 / #202824',30,MUTED)
  elif key=='accent':
   p.rect((529,y+37,1016,y+50),ORANGE);p.text(529,y+76,'阅读与展览',38);p.text(529,y+157,'点缀不代替错误语义',30,MUTED)
  else:
   p.rect((529,y+27,1016,y+112),WHITE,'#9B3A2C',radius=3,width=3);p.text(551,y+41,'联系电话',36);p.text(529,y+137,'× 请填写联系电话',33,'#9B3A2C')
  if j<4:rule(p,y+230)
 p.wrap(64,1755,'错误同时给出文字与符号，不能只把装饰色复制到边框。',30,MUTED,width=950)
 assert rows[0][0]==GREEN and rows[-1][0]=='#9B3A2C'
 done(p,{'role_values':dict((b,a) for a,b,_ in rows),'on_action':'#FFFFFF','controls':'button, surface heading, paragraph, decorative rule, field error'})

def fig22():
 p=Page('22','主题变了，预约任务仍然清楚','不反转每个像素；按角色重新分配前景与背景。',height=2050)
 meta=[]
 for y,dark in [(360,False),(1195,True)]:
  bg=INK if dark else WARM;fg=WARM if dark else INK;action='#B9D9CE' if dark else GREEN;on=INK if dark else WHITE;selection=GREEN if dark else '#DFEEE7';seltext=WARM if dark else INK;error='#F2B7A6' if dark else '#9B3A2C'
  p.text(64,y-75,'深色主题' if dark else '浅色主题',40)
  p.rect((64,y,1016,y+642),bg,LINE,radius=6)
  p.text(105,y+27,'间色 · 预约座位',44,fg)
  p.rect((105,y+130,975,y+225),selection,radius=4);p.text(132,y+151,'✓ 周五 19:30 · 已选择',38,seltext)
  p.text(105,y+280,'× 请填写联系电话',38,error)
  p.rect((105,y+373,975,y+482),action,radius=4);center(p,(105,y+373,975,y+482),'确认预约',40,on)
  p.text(105,y+526,'背景 '+bg+'  /  文字 '+fg,30,fg)
  p.text(105,y+577,'按钮 '+action+'  /  字 '+on,30,fg)
  er=contrast(error,bg);ar=contrast(on,action)
  p.text(64,y+669,f'错误文字 {er:.2f}∶1   按钮文字 {ar:.2f}∶1',31,MUTED)
  meta.append({'theme':'dark' if dark else 'light','background':bg,'text':fg,'action':action,'on_action':on,'selection':selection,'selection_text':seltext,'error':error,'error_contrast':er,'action_contrast':ar})
 assert meta[0]['action']==GREEN and meta[1]['action']=='#B9D9CE'
 assert round(meta[0]['error_contrast'],2)==6.15 and round(meta[1]['error_contrast'],2)==8.70
 assert round(meta[0]['action_contrast'],2)==8.59 and round(meta[1]['action_contrast'],2)==9.98
 done(p,{'themes':meta,'state_cues':'勾选、明确错误文字、按钮形状保持'})

def fig22b():
 p=Page('22b','色阶连续，不等于每档都可作正文','HSL：H=169°、S=40%。下方全部与暖纸 #F6F1E7 比较。',height=2170)
 levels=[.92,.80,.68,.56,.44,.32,.20];values=[]
 for j,l in enumerate(levels):
  c='#'+''.join(f'{round(v*255):02X}' for v in colorsys.hls_to_rgb(169/360,l,.40));r=contrast(c,WARM);y=300+j*240
  p.rect((64,y+4,203,y+138),c,LINE)
  p.text(235,y+1,f'L={round(l*100)}%  {c}',34)
  p.text(774,y+1,f'{r:.2f}∶1',34)
  p.rect((235,y+60,701,y+149),WARM,LINE);p.text(257,y+77,'正文示意 Aa',38,c)
  p.text(739,y+76,'可作普通文字' if r>=4.5 else '普通文字未达标',30,GREEN if r>=4.5 else '#9B3A2C')
  if j<6:rule(p,y+199)
  values.append({'h':169,'s':40,'l':round(l*100),'hex':c,'contrast_on_warm':r,'normal_text_aa':r>=4.5})
 p.wrap(64,1968,'是否达标按未舍入值判断；仅针对本图纯色配对，不代表感知等步长或所有背景都适用。',30,MUTED,width=952,spacing=11)
 assert [v['l'] for v in values]==[92,80,68,56,44,32,20]
 assert [v['hex'] for v in values]==['#E2F3F0','#B8E0D9','#8DCEC2','#62BCAB','#439D8D','#317266','#1F4740']
 assert [round(v['contrast_on_warm'],2) for v in values]==[1.02,1.27,1.59,2.01,2.89,5.00,9.17]
 assert [v['normal_text_aa'] for v in values]==[False,False,False,False,False,True,True]
 done(p,{'hsl_swatch_samples':values,'background':WARM,'threshold':4.5})

def file_icon(p,box,label):
 x,y,r,b=box;p.d.polygon([(x,y),(r-55,y),(r,y+55),(r,b),(x,b)],fill=WHITE,outline=INK,width=3);p.line([(r-55,y),(r-55,y+55),(r,y+55)],LINE,3)
 p.text(x+22,y+75,label,35,GREEN)
 for i in range(3):p.line([(x+25,y+143+i*26),(r-28,y+143+i*26)],LINE,3)

def fig23():
 p=Page('23','把颜色交给明确的输出条件','流程关系示意，不执行 ICC 转换，也不预测纸面颜色。',height=2180)
 file_icon(p,(64,310,363,566),'master-v03')
 p.text(64,600,'带源配置的原稿',38)
 p.text(64,663,'保留版本与可编辑内容',30,MUTED)
 p.image('assets/images/case-editorial.png',(426,308,1016,702))
 arrow(p,(540,739),(540,804),GREEN,5,20)
 p.rect((64,832,1016,1155),WARM,LINE,radius=4)
 p.text(101,862,'指定目标：纸张 · 工艺 · 承印条件',40,GREEN)
 p.text(101,943,'目标 ICC：由承印方提供并记录版本',35)
 p.text(101,1013,'按目标条件转换 → 软打样检查',36)
 p.text(101,1084,'赋予配置文件 ≠ 转换颜色',31,'#9B3A2C')
 arrow(p,(540,1185),(540,1253),GREEN,5,20)
 file_icon(p,(64,1291,363,1547),'print-v03')
 p.text(64,1573,'指定输出副本',37)
 p.image('assets/images/case-editorial.png',(446,1288,996,1655))
 p.text(446,1676,'实物样张位置（示意）',35)
 arrow(p,(540,1741),(540,1812),GREEN,5,20)
 rule(p,1843);p.text(64,1870,'签样记录',42,GREEN)
 p.text(64,1944,'纸张 / 观察照明 / 日期 / 修改意见',35)
 p.text(64,2012,'确认后签样；不通过则返回原稿修订。',33)
 done(p,{'workflow':['带源配置与版本的原稿','指定纸张/工艺/目标ICC','转换/软打样','输出副本与目标纸张实物样张','约定照明检查与签样/修订'],'image_status':'AI虚构书刊仅充当产物标记；不是实际打样证据','actual_color_conversion':False})

def main(only=None):
 RESULT.clear();selected=OWN if only is None else OWN & {str(i).zfill(2) for i in only}
 for key,fn in [('02',fig02),('18',fig18),('21',fig21),('22',fig22),('22b',fig22b),('23',fig23)]:
  if key in selected:fn()
 report={'generator':'scripts/redraw_systems.py','method':'统一Page精确图解，1080宽；全部数值由数据计算与断言','figures':RESULT}
 (ROOT/'editorial/redraw-systems.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
 return list(RESULT)
if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--only',nargs='+');args=parser.parse_args();print(json.dumps(main(args.only),ensure_ascii=False,indent=2))
