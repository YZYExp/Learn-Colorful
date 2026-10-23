#!/usr/bin/env python3
"""Deterministic teaching figures. RGB values are sRGB illustrations, not material proofs."""
from PIL import Image,ImageDraw,ImageFont,ImageChops
from pathlib import Path
import colorsys, math, json, os, argparse
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/images';OUT.mkdir(parents=True,exist_ok=True)
_parser=argparse.ArgumentParser(description=__doc__)
_parser.add_argument('--only',nargs='+',help='Only save these figure IDs, e.g. --only 22 22b')
ONLY=set(_parser.parse_args().only or []);SAVED=[]
def find_font():
    explicit=os.environ.get('COLOR_BOOK_FONT')
    if explicit:
        if Path(explicit).is_file(): return explicit
        raise SystemExit('COLOR_BOOK_FONT 指向的字体不存在：'+explicit)
    candidates=[
        '/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc',
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
        '/System/Library/Fonts/PingFang.ttc',
        'C:/Windows/Fonts/msyh.ttc',
    ]
    for path in candidates:
        if Path(path).is_file(): return path
    for root in ['/usr/local/share/fonts','/usr/share/fonts',str(Path.home()/'.fonts')]:
        folder=Path(root)
        if not folder.exists(): continue
        for path in sorted(folder.rglob('*')):
            if path.suffix.lower() in ('.ttf','.otf','.ttc') and any(k in path.name for k in ['NotoSerifCJK','NotoSansCJK','SourceHanSans','SourceHanSerif']):
                return str(path)
    raise SystemExit('未找到中文字体。请安装 Noto CJK / 思源字体，或设置 COLOR_BOOK_FONT 为中文字体文件路径。')
FONT=find_font()
W,H=1200,1600
PAPER='#F6F1E7';GREEN='#24544B';ORANGE='#C86345';INK='#202824';MUTED='#686D67';LINE='#D8D8CE';WHITE='#FFFFFF';GRAY='#E8E7DF'
PALETTE=[GREEN,PAPER,ORANGE,INK]
def font(n):return ImageFont.truetype(FONT,n)
def txt(x,y,s,size=30,color=INK,maxw=None):
    # Keep every string inside the page. Long titles shrink deterministically.
    limit=W-x-64 if maxw is None else maxw
    while d.textbbox((0,0),s,font=font(size))[2]>limit and size>18: size-=1
    box=d.textbbox((x,y),s,font=font(size))
    if box[2]>W-25 or box[3]>H-20:
        raise ValueError(f'Text exceeds page: {s} {box}')
    d.text((x,y),s,font=font(size),fill=color)
def rect(box,fill,outline=None,width=2,r=0):
    if r:d.rounded_rectangle(box,radius=r,fill=fill,outline=outline,width=width)
    else:d.rectangle(box,fill=fill,outline=outline,width=width)
def line(points,fill=LINE,width=3):d.line(points,fill=fill,width=width)
def circle(x,y,r,fill,outline=None):d.ellipse((x-r,y-r,x+r,y+r),fill=fill,outline=outline,width=3)
def base(n,title,sub):
    global im,d
    im=Image.new('RGB',(W,H),'#FCFBF7');d=ImageDraw.Draw(im)
    rect((0,0,18,H),GREEN);txt(64,35,'色彩的语言  /  图 '+(f'{n:02}' if isinstance(n,int) else str(n)),25,MUTED)
    txt(64,91,title,48);txt(66,164,sub,27,MUTED)
    line([(64,220),(1136,220)])
    txt(64,1542,'原创教学图 · sRGB 示意 · 色彩需结合实际媒介验证',23,MUTED)
def save(n):
    key=f'{n:02}' if isinstance(n,int) else str(n)
    if ONLY and key not in ONLY:return
    im.save(OUT/('fig-'+key+'.png'),optimize=True);SAVED.append(key)
def label(y,k,s):txt(70,y,k,29,GREEN);txt(70,y+44,s,26,MUTED)
def swatches(y,cols,labels=None,h=110):
    gap=18;bw=(1060-gap*(len(cols)-1))/len(cols)
    for j,c in enumerate(cols):
        x=70+j*(bw+gap);rect((x,y,x+bw,y+h),c,LINE,r=6)
        if labels:txt(x,y+h+12,labels[j],23)
def arrow(y):
    line([(600,y),(600,y+48)],GREEN,5);d.polygon([(588,y+34),(612,y+34),(600,y+50)],fill=GREEN)
def poster(y,mode='paper',height=300,heading='间色 · 周末阅读',note=None):
    x=280;right=1130
    bg= PAPER if mode=='paper' else GREEN if mode=='green' else ORANGE
    fg=INK if mode=='paper' else PAPER
    rect((x,y,right,y+height),bg,LINE,r=10)
    if mode=='equal':
        for j,c in enumerate(PALETTE):rect((x+j*(right-x)/4,y,x+(j+1)*(right-x)/4,y+height),c)
        rect((x+40,y+55,right-40,y+height-45),PAPER)
        fg=INK
    txt(x+42,y+43,heading,40,GREEN if mode in ('paper','equal') else PAPER)
    txt(x+44,y+110,'周六 14:00   阅读 · 饮品 · 小型展览',25,fg)
    circle(right-70,y+65,17,ORANGE)
    rect((x+44,y+height-85,x+270,y+height-35),GREEN if mode in ('paper','equal') else PAPER,r=4)
    txt(x+67,y+height-80,'预约座位',26,PAPER if mode in ('paper','equal') else GREEN)
    if note:txt(70,y+60,note,28)
def contrast(a,b):
    def lum(c):
        v=[int(c[i:i+2],16)/255 for i in (1,3,5)];v=[t/12.92 if t<=.04045 else ((t+.055)/1.055)**2.4 for t in v]
        return .2126*v[0]+.7152*v[1]+.0722*v[2]
    x,y=sorted([lum(a),lum(b)]);return (y+.05)/(x+.05)
def hexrgb(v):return '#'+''.join(f'{round(max(0,min(1,x))*255):02X}' for x in v)

base(1,'看颜色，也看它占了多少','同一组颜色，改变背景与面积，阅读重心随之改变')
poster(280,'paper',note='暖纸作底');poster(680,'green',note='墨绿作底');poster(1080,'equal',note='多色分区')
save(1)

base(2,'颜色形成的一条观察链','简化物理示意：光源、表面与视觉共同参与')
for y,num,title,desc,col in [(290,'01','光源','不同光源的光谱分布可能不同',ORANGE),(680,'02','物体','表面对不同波长的反射不同',GREEN),(1070,'03','眼睛与感知','进入眼睛的光还会受到环境影响',INK)]:
    rect((70,y,1130,y+280),PAPER,LINE,r=12);circle(175,y+140,65,col);txt(138,y+105,num,44,PAPER)
    txt(290,y+65,title,40);txt(290,y+145,desc,30)
    if y<1000:arrow(y+305)
save(2)

base(3,'用三个方向描述颜色','HSL 教学样本；HSL 的 L、S 不等同于感知明度、彩度')
for y,title,desc,vals in [(330,'色相方向','保持 HSL 的 S=50%、L=45%',[hexrgb(colorsys.hls_to_rgb(h/360,.45,.5)) for h in [0,60,120,180,240,300]]),(740,'明暗方向','固定 H=160°、S=35%，改变 L',[hexrgb(colorsys.hls_to_rgb(160/360,l,.35)) for l in [.15,.28,.41,.54,.67,.8]]),(1150,'饱和方向','固定 H=160°、L=45%，改变 S',[hexrgb(colorsys.hls_to_rgb(160/360,.45,s)) for s in [0,.15,.3,.45,.6,.75]])]:
    txt(70,y-65,title,36);swatches(y,vals,h=150);txt(70,y+185,desc,27,MUTED)
save(3)

base(4,'同一个灰，放在不同背景上','两块中心色都精确为 #808080；背景上下对照')
for y,bg,name in [(290,INK,'深墨背景 #202824'),(800,PAPER,'暖纸背景 #F6F1E7')]:
    rect((70,y,1130,y+360),bg,LINE);rect((470,y+90,730,y+270),'#808080');txt(70,y+385,name,29)
txt(70,1325,'验证条：两块中心色并排，边界处没有色差',28)
rect((70,1390,600,1470),'#808080');rect((600,1390,1130,1470),'#808080');line([(600,1400),(600,1460)],PAPER,2)
save(4)

base(5,'色轮是关系地图','HSL 色相示意；角度关系不能预测颜料混合结果')
cx,cy,r=600,560,230
for h in range(360):
    d.pieslice((cx-r,cy-r,cx+r,cy+r),h-90,h-88,fill=hexrgb(colorsys.hls_to_rgb(h/360,.52,.60)))
circle(cx,cy,130,'#FCFBF7');txt(520,535,'色相关系',32)
for y,title,hs in [(915,'单色：同一色相',[160,160,160]),(1110,'邻近：相邻色相',[130,160,190]),(1305,'对比：相对色相',[160,340])]:
    txt(70,y,title,30);cols=[hexrgb(colorsys.hls_to_rgb(h/360, .3+i*.15 if title.startswith('单') else .45,.5)) for i,h in enumerate(hs)]
    for j,c in enumerate(cols):rect((490+j*210,y-15,680+j*210,y+95),c,r=5)
save(5)

base(6,'文字先要读得清楚','同一文字、同一暖纸底；按 WCAG 相对亮度计算')
for y,fg,name in [(340,'#B9B8A8','低对比'),(850,GREEN,'高对比')]:
    txt(70,y-65,f'{name}  ·  {fg}',32)
    rect((70,y,1130,y+310),PAPER,LINE,r=10)
    txt(120,y+65,'间色 · 周末阅读',46,fg);txt(122,y+155,'周六 14:00   预约你的阅读时间',32,fg)
    txt(70,y+340,f'对比度 {contrast(fg,PAPER):.2f}:1',32,GREEN)
txt(70,1395,'普通文字 AA：至少 4.5:1；大号文字 AA：至少 3:1',29)
save(6)

base(7,'小面积也能成为视觉重心','同样布局、同样颜色；只改变强调色面积')
for y,ratio,name in [(320,.10,'陶橘约占示意色区 10%'),(870,.50,'陶橘约占示意色区 50%')]:
    rect((70,y,1130,y+360),PAPER,LINE,r=10)
    rect((110,y+45,1090,y+315),GREEN)
    rect((1090-980*ratio,y+45,1090,y+315),ORANGE)
    txt(70,y+390,name,30)
txt(70,1390,'面积只是一项变量；位置、明暗、形状也会争夺注意力。',28,MUTED)
save(7)

base(8,'用颜色安排重复与停顿','同一组模块：间距、顺序与强调位置保持可比较')
for y,title,cols in [(350,'连续重复',[GREEN]*6),(760,'规律点缀',[GREEN,GREEN,ORANGE,GREEN,GREEN,ORANGE]),(1170,'强调集中',[GREEN,GREEN,GREEN,GREEN,GREEN,ORANGE])]:
    txt(70,y-65,title,34)
    for j,c in enumerate(cols):rect((70+j*180,y,230+j*180,y+210),c,r=8)
    txt(70,y+245,'中性色背景保留模块之间的间隔',26,MUTED)
save(8)

base(9,'气氛来自整组关系','同一静物构图的两种色彩组织；不是情绪测量结果')
for y,title,cols in [(330,'柔和、低反差的教学设定',[PAPER,'#B3BCAB','#B98570',INK]),(920,'强烈、较高反差的教学设定',[INK,'#6FC4A2','#F18C58',PAPER])]:
    txt(70,y-65,title,32);bg,leaf,pot,shadow=cols
    rect((70,y,1130,y+420),bg,LINE,r=10);d.ellipse((320,y+300,900,y+370),fill=shadow)
    rect((540,y+160,760,y+335),pot,r=25);line([(650,y+180),(600,y+70)],leaf,12)
    d.ellipse((455,y+55,620,y+155),fill=leaf);d.ellipse((610,y+20,800,y+125),fill=leaf)
save(9)

base(10,'同一颜色，在不同语境中阅读','原创符号示意，不代表任何文化中的固定解释')
for y,title,body in [(320,'活动邀请','陶橘圆标 + 欢迎参加'),(740,'输入错误','陶橘边框 + × + 请填写日期'),(1160,'展品编号','陶橘方签 + 作品 03')]:
    rect((70,y,1130,y+260),PAPER,LINE,r=10);txt(115,y+35,title,31)
    if y==320:circle(180,y+160,42,ORANGE);txt(270,y+125,'欢迎参加',42)
    elif y==740:
        rect((120,y+110,1080,y+205),PAPER,ORANGE,4,r=4);txt(150,y+125,'×  请填写日期',35,ORANGE)
    else:rect((130,y+115,230,y+210),ORANGE);txt(280,y+130,'作品 03',40)
    txt(70,y+285,body,26,MUTED)
save(10)

base(11,'一块颜色，背后还有材料与工艺','从原料到使用的路径示意；不模拟历史颜料的真实色样')
for y,num,title,desc in [(310,'01','获得材料','矿物、植物、动物来源或合成路径'),(710,'02','制成可用颜色','研磨、提取、配制与适合载体的工艺'),(1110,'03','进入日常使用','供应、价格、耐久性与使用习惯共同作用')]:
    rect((70,y,1130,y+285),PAPER,LINE,r=12);circle(170,y+130,58,[ORANGE,GREEN,INK][int(num)-1]);txt(137,y+96,num,41,PAPER)
    txt(270,y+58,title,40);txt(270,y+145,desc,28)
    if y<1000:arrow(y+303)
save(11)

base(12,'风格不能只凭几个色号判断','同一套基础色：改变留白、比例与图形组织')
for y,mode,title in [(320,'paper','较多留白'),(850,'green','较大色面')]:
    txt(70,y-65,title,34);poster(y,mode,height=365)
txt(70,1330,'再观察：字体、图像、网格、材料与传播场景。',31)
txt(70,1395,'教学示例不是年度趋势结论，也不代指真实品牌。',28,MUTED)
save(12)

base(13,'取到颜色之后，还要分配角色','原创几何静物取色示意；不是照片采样结果')
rect((70,280,1130,650),PAPER,LINE,r=10);d.ellipse((410,540,900,610),fill=INK);rect((590,410,780,570),ORANGE,r=25);line([(675,440),(610,325)],GREEN,12);d.ellipse((440,300,640,425),fill=GREEN)
txt(100,305,'01 取色示意',29)
txt(70,715,'02 候选颜色',32);swatches(780,PALETTE,PALETTE,h=115)
txt(70,1030,'03 分配角色',32);poster(1100,'paper',height=340)
save(13)

base(14,'同一色卡，三种分工','文字、位置与字号一致；改变色面分配')
poster(280,'equal',note='A 多色分区');poster(680,'paper',note='B 暖纸主导');poster(1080,'green',note='C 墨绿主导')
save(14)

base(15,'每一种颜色都应有明确任务','阅读、图像、行动、装饰分工；功能也靠形状与文字')
rect((230,320,1060,1350),PAPER,LINE,r=12)
txt(280,375,'间色 · 夜读',54,GREEN);txt(282,465,'周五 19:30',34,INK)
rect((280,570,1010,1030),GRAY,r=8);d.ellipse((400,890,900,980),fill=INK);rect((620,735,820,925),ORANGE,r=24);d.ellipse((420,620,680,790),fill=GREEN)
rect((280,1130,1010,1240),GREEN,r=6);txt(550,1150,'预约座位',42,PAPER);circle(995,405,16,ORANGE)
for x,y,s,end in [(70,485,'阅读',(270,485)),(70,780,'图像',(270,780)),(70,1170,'行动',(270,1170))]:
    txt(x,y,s,32);line([(160,y+24),end],MUTED,2)
txt(1070,385,'装饰',28,maxw=100);line([(1070,410),(1015,410)],MUTED,2)
save(15)

base(16,'一步只修正一个问题','同一版式、同一字号、同一元素位置的连续修改')
for i,y in enumerate([280,585,890,1195]):
    title=['A 待修正','B 修对比','C 分主次','D 明确行动'][i];txt(70,y+20,title,28)
    x=305;right=1130;rect((x,y,right,y+245),ORANGE if i==0 else PAPER,LINE,r=6)
    rect((x+510,y+20,right-20,y+115),GREEN if i<2 else GRAY,r=4)
    txt(x+30,y+20,'间色 · 夜读',32,'#5E765E' if i==0 else GREEN)
    txt(x+30,y+82,'周五 19:30 · 阅读区',25,'#5E765E' if i==0 else INK)
    circle(right-45,y+35,10,ORANGE)
    rect((x+30,y+150,x+280,y+215),GREEN if i==3 else '#A77C53',r=4)
    txt(x+70,y+159,'预约座位',27,PAPER if i==3 else '#858065')
    txt(x+345,y+166,'活动详情',25,GREEN if i==3 else '#858065')
    if i==3:line([(x+345,y+205),(x+445,y+205)],GREEN,2)
save(16)

base(17,'跨载体保持规则，而非复制版式','原创教学品牌：间色；不是任何真实品牌的截图')
poster(285,'paper',note='海报')
txt(70,740,'阅读手册',30);rect((430,690,980,1050),PAPER,LINE,r=6);rect((430,690,980,725),GREEN);txt(480,780,'间色',64,GREEN);txt(480,885,'阅读与空间',32,INK);circle(910,960,17,ORANGE)
txt(70,1220,'活动票券',30);rect((290,1160,1130,1440),PAPER,LINE,r=6);rect((290,1160,325,1440),GREEN);txt(370,1200,'间色 · 夜读',40,GREEN);txt(370,1280,'周五 19:30   入场 01',29,INK);circle(1050,1230,17,ORANGE)
save(17)

base(18,'先判断数据关系，再选择颜色','以下均为虚构教学数据；颜色之外保留文字与符号')
txt(70,270,'类别：活动人数（人）',32)
for y,name,v,col in [(345,'阅读',40,'#387C6C'),(430,'饮品',55,'#8C6737'),(515,'展览',30,'#7B658B')]:
    txt(70,y,name,28);rect((250,y,250+v*12,y+50),col,r=4);txt(270+v*12,y,str(v),28)
txt(70,680,'顺序：到访量等级（1 低 → 5 高）',32);swatches(755,['#DFEEE7','#B9D7C8','#85B69F','#4D8B72',GREEN],['1','2','3','4','5'],h=115)
txt(70,1035,'发散：实际参与率 − 计划参与率（百分点）',32);swatches(1110,['#753428','#E3B09E',PAPER,'#B9D7C8',GREEN],['-20','-10','0','+10','+20'],h=100)
txt(70,1290,'0＝达到计划参与率；缺失值需另标。非感知均匀标度。',26,MUTED)
rect((70,1370,1130,1470),PAPER,ORANGE,3,r=6);txt(110,1390,'×  请输入日期：错误也要有文字说明',30,INK)
save(18)

base(19,'同一种识别色，进入不同载体','形状是示意；屏幕色块不能证明真实材料的一致性')
for y,title,desc in [(280,'围裙','织物 · 记录面料与观察光源'),(680,'杯具','釉面 · 记录光泽与样品'),(1080,'饮品包装','纸张 · 记录印刷与表面处理')]:
    rect((70,y,1130,y+310),PAPER,LINE,r=10);txt(100,y+35,title,34);txt(100,y+220,desc,27,MUTED)
    if y==280:d.polygon([(780,y+35),(900,y+35),(930,y+110),(990,y+260),(690,y+260),(750,y+110)],fill=GREEN)
    elif y==680:
        rect((735,y+70,945,y+230),GREEN,r=18);d.arc((910,y+90,1020,y+200),270,90,fill=GREEN,width=18)
    else:rect((740,y+45,960,y+265),GREEN,r=8);rect((760,y+65,940,y+100),PAPER)
    txt(760,y+135,'间色',34,PAPER)
save(19)

base(20,'大面积的颜色，会包围使用者','保持房形与家具相同，仅改变墙面与导向色面积')
def room(y,warm):
    wall=PAPER if warm else ORANGE
    rect((70,y,1130,y+430),wall,LINE)
    d.polygon([(70,y),(1130,y),(1020,y+70),(180,y+70)],fill='#EAE7DD')
    d.polygon([(70,y+430),(1130,y+430),(1020,y+330),(180,y+330)],fill='#B5A48D')
    rect((250,y+100,430,y+270),'#D8E1D9',INK);rect((650,y+220,1000,y+340),GREEN,r=8)
    rect((890,y+100,1040,y+170),ORANGE if warm else PAPER,r=4);txt(910,y+111,'阅读 →',26,INK)
    txt(90,y+15,'顶',25,INK);txt(90,y+150,'墙',25,INK);txt(90,y+370,'地',25,INK);txt(680,y+265,'活动物',28,PAPER)
txt(70,270,'A 陶橘墙面',32);room(340,False);txt(70,870,'B 暖纸墙面 + 小面积陶橘导向',32);room(940,True)
save(20)

base(21,'基础色与语义角色分开管理','先给颜色命名，再说明它在当前方案中的职责')
roles=[(GREEN,'action','主要行动'),(PAPER,'surface','内容表面'),(INK,'text','正文文字'),(ORANGE,'accent','少量强调')]
for j,(c,key,name) in enumerate(roles):
    y=300+j*235;rect((70,y,1130,y+180),WHITE,LINE,r=8);rect((95,y+25,255,y+155),c,LINE,r=5)
    txt(300,y+28,c,30);txt(570,y+28,key,34,GREEN);txt(570,y+98,name,29)
rect((70,1290,1130,1470),PAPER,LINE,r=10);txt(110,1320,'error 是独立角色',35);txt(110,1380,'装饰用 accent 不自动等于错误提示色。',29,MUTED)
save(21)

base(22,'主题改变映射，保留使用语义','同一预约卡：形状、文字与状态提示都保持清楚')
for y,dark in [(290,False),(900,True)]:
    bg=INK if dark else PAPER;fg=PAPER if dark else INK;action='#B9D9CE' if dark else GREEN;buttonfg=INK if dark else WHITE
    txt(70,y-45,'深色主题' if dark else '浅色主题',30)
    rect((70,y,1130,y+460),bg,LINE,r=12);txt(115,y+35,'间色 · 预约座位',42,fg)
    rect((115,y+125,1085,y+220),GREEN if dark else '#DFEEE7',r=5);txt(145,y+145,'✓ 周五 19:30 · 已选择',31,PAPER if dark else INK)
    txt(115,y+255,'× 请填写联系电话',31,'#F2B7A6' if dark else '#9B3A2C')
    rect((115,y+330,1085,y+415),action,r=5);txt(500,y+343,'确认预约',37,buttonfg)
save(22)

base(23,'把颜色交付给明确的目标条件','配置文件描述条件；屏幕预览不能代替实物确认')
for y,num,title,desc in [(290,'01','带配置文件的原稿','保留源文件、嵌入的配置文件与版本'),(690,'02','目标 ICC 转换 / 软打样','先明确输出条件，再检查映射结果'),(1090,'03','目标纸张实物打样','在约定观察条件下确认，再记录修订')]:
    rect((70,y,1130,y+280),PAPER,LINE,r=12);circle(165,y+135,60,GREEN);txt(132,y+100,num,43,PAPER)
    txt(270,y+55,title,36);txt(270,y+140,desc,28)
    if y<1000:arrow(y+300)
txt(70,1435,'注意：赋予配置文件 ≠ 转换到配置文件。',30,ORANGE)
save(23)

base(24,'把配色做成可验证的方案','同一组规则，落实到菜单、预约和空间导向')
for y,title,desc in [(280,'01 任务','阅读清楚、行动可辨、空间识别一致'),(530,'02 角色','长文用深墨 · 主操作用墨绿 · 陶橘作点缀')]:
    rect((70,y,1130,y+180),PAPER,LINE,r=8);txt(105,y+25,title,34,GREEN);txt(105,y+95,desc,29)
txt(70,770,'03 三种应用',34)
for j,(title,c) in enumerate([('菜单',PAPER),('预约',GREEN),('导向',PAPER)]):
    x=70+j*365;rect((x,850,x+330,1120),c,LINE,r=8);txt(x+40,885,'间色',40,PAPER if c==GREEN else GREEN);txt(x+40,960,title,31,PAPER if c==GREEN else INK);circle(x+280,1070,13,ORANGE)
rect((70,1210,1130,1460),PAPER,LINE,r=8);txt(105,1240,'04 验证与反馈',34,GREEN);txt(105,1310,'对比度 → 实物打样 → 用户任务 → 修订记录',29)
save(24)


base('02b','发光相加，与理想滤色相减','理想 RGB / CMY 通道示意；不是实际颜料配方')
def channel_circles(y,additive):
    # One exact 8-bit mask per ideal channel. No alpha-blending approximation.
    channels=[]
    for cx,cy in [(410,175),(650,175),(530,325)]:
        mask=Image.new('L',(1060,500),0);md=ImageDraw.Draw(mask)
        md.ellipse((cx-170,cy-170,cx+170,cy+170),fill=255)
        channels.append(mask if additive else ImageChops.invert(mask))
    panel=Image.merge('RGB',channels);im.paste(panel,(70,y))
    if additive:
        txt(130,y+28,'RGB 加色',29,PAPER)
    else:txt(130,y+28,'CMY 理想减色',29,INK)
channel_circles(265,True)
txt(70,790,'R + G = Y   ·   G + B = C   ·   B + R = M',29)
channel_circles(900,False)
txt(70,1425,'C 与 M 交叠为蓝；三种理想滤色完全交叠为黑。',28)
save('02b')

base('08b','冷暖是一种相对关系','固定同一个中心色，改变相邻色；不等于光源色温')
for y,partner,title in [(330,ORANGE,'与偏橘色相邻'),(900,'#557C94','与偏蓝色相邻')]:
    txt(70,y-65,title,34)
    rect((70,y,1130,y+360),PAPER,LINE,r=8)
    rect((200,y+60,600,y+300),partner)
    rect((600,y+60,1000,y+300),'#9E8267')
    txt(200,y+380,partner,28);txt(600,y+380,'固定 #9E8267',28)
txt(70,1400,'比较右侧同色块的关系感受，而非为它测一个温度。',28,MUTED)
save('08b')

base('22b','排成色阶，还要逐项验算','HSL：H=169°、S=40%；L 的等步长不等于感知等步长')
for j,l in enumerate([.92,.80,.68,.56,.44,.32,.20]):
    y=280+j*170;c=hexrgb(colorsys.hls_to_rgb(169/360,l,.40));ratio=contrast(c,PAPER)
    rect((70,y,1130,y+140),PAPER,LINE,r=8)
    rect((90,y+20,300,y+120),c,LINE,r=4)
    txt(340,y+13,f'L={round(l*100)}%   {c}',27)
    txt(340,y+65,'正文示意 Aa',32,c)
    txt(790,y+15,f'{ratio:.2f}:1',31)
    txt(790,y+70,'达到 4.5' if ratio>=4.5 else '未达 4.5',28,GREEN if ratio>=4.5 else ORANGE)
txt(70,1490,'数值均相对于暖纸 #F6F1E7；不代表所有背景组合可用。',26,MUTED)
save('22b')

metadata={'format':'1200×1600 RGB PNG','method':'Pillow deterministic drawing','palette':PALETTE,'font_file':Path(FONT).name,'figure_count':27,'notes':['RGB illustrations are not physical material proofs.','Figures 3 and 5 use HSL; not perceptually uniform.','Figure 6 uses WCAG relative luminance formula.','Figure 18 uses fictitious data.'],'contrasts':{c:round(contrast(c,PAPER),4) for c in ['#B9B8A8',GREEN]}}
(ROOT/'editorial/figure-production.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2))
print(f'Wrote {len(SAVED)} figures to',OUT)
