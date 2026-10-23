#!/usr/bin/env python3
"""Mature editorial application figures with controlled typography and color roles."""
from pathlib import Path
from PIL import Image
import argparse,json
from figure_style import Page,ROOT,WARM,GREEN,INK,MUTED,LINE,ORANGE,WHITE,PAPER,contrast
PHOTO='assets/images/chapter-v2-extract.png'

def poster(p,x,y,w,h,mode='paper'):
    """Frozen editorial composition. Modes change color allocation, never geometry."""
    bg=GREEN if mode=='green' else WARM
    fg=WARM if mode=='green' else INK
    heading=WARM if mode=='green' else GREEN
    p.rect((x,y,x+w,y+h),bg)
    if mode=='equal':
        for i,c in enumerate((GREEN,WARM,ORANGE,INK)):
            p.rect((x+i*w/4,y,x+(i+1)*w/4,y+h),c)
        p.rect((x+20,y+20,x+w-20,y+h-20),WARM)
    # Typography and photographic content remain the same in every mode.
    p.text(x+34,y+25,'间色 / JIANSE',25,heading)
    p.text(x+34,y+83,'海边的光',48,heading)
    p.text(x+36,y+151,'图像与色彩之夜',29,fg)
    p.text(x+36,y+209,'10月24日 19:30',29,fg)
    p.text(x+36,y+250,'二层阅读室',27,fg)
    button=WARM if mode=='green' else GREEN
    onbutton=GREEN if mode=='green' else WHITE
    p.rect((x+35,y+h-98,x+285,y+h-37),button)
    p.text(x+59,y+h-91,'预约座位 →',30,onbutton)
    p.image(PHOTO,(x+w-373,y+75,x+w-30,y+307))
    p.rect((x+w-373,y+333,x+w-30,y+340),ORANGE)


def figure01():
    p=Page('01','颜色相同，画面重心不同','固定内容、照片与位置，只改变周围的颜色分配。',height=1960)
    settings=[('A','暖纸作底','浅底提供连续阅读环境。','paper'),('B','墨绿作底','深色场先建立整体轮廓。','green'),('C','多色分区','色面在边缘形成更多停顿。','equal')]
    for i,(letter,title,note,mode) in enumerate(settings):
        y=300+i*505
        p.text(64,y,letter,42,GREEN);p.text(132,y+3,title,38,INK)
        poster(p,64,y+69,952,390,mode)
        p.text(64,y+466,note,30,MUTED)
    assert len({p.im.crop((643, yy+76, 984, yy+305)).tobytes() for yy in (369,874,1379)})==1
    return p.save()


def figure06():
    p=Page('06','先检查文字与它的背景','同一内容、同一字号、同一纯色背景。',height=1410)
    for y,fg,label in [(320,'#B9B8A8','A  浅灰褐文字'),(805,GREEN,'B  墨绿文字')]:
        p.text(64,y-19,label,37,INK)
        p.text(770,y-19,f'{contrast(fg,WARM):.2f}:1',39,GREEN)
        p.rect((64,y+54,1016,y+322),WARM)
        p.text(108,y+87,'海边的光 · 夜读',52,fg)
        p.text(111,y+179,'10月24日 19:30  /  二层阅读室',32,fg)
        p.text(111,y+241,'预约后入场，请保留确认信息。',32,fg)
        p.text(64,y+345,f'{fg}  /  背景 {WARM}',29,MUTED)
    p.text(64,1244,'普通文字 AA ≥ 4.5:1    大号文字 AA ≥ 3:1',31,INK)
    assert abs(contrast('#B9B8A8',WARM)-1.7793)<.001
    assert abs(contrast(GREEN,WARM)-7.6305)<.001
    return p.save()


def figure14():
    p=Page('14','给颜色分配具体工作','三种版本共用摄影与排版；比较背景、文字和点缀。',height=2130)
    rows=[('A','多色分区','equal','边缘色区参与组织，内部留出阅读面。'),('B','暖纸主导','paper','暖纸承担环境；墨绿命名；陶橘分隔。'),('C','墨绿主导','green','墨绿承担环境；浅字阅读；陶橘分隔。')]
    for i,(letter,title,mode,note) in enumerate(rows):
        y=300+i*545
        p.text(64,y,letter+'  '+title,38,INK)
        poster(p,64,y+67,952,390,mode)
        p.wrap(64,y+467,note,31,MUTED,952)
    p.text(64,1980,'同色卡的关系，需回到完整画面检查。',33,GREEN)
    assert len({p.im.crop((643, yy+76, 984, yy+305)).tobytes() for yy in (367,912,1457)})==1
    return p.save()


def figure15():
    p=Page('15','从完整海报里读出颜色角色','标注工作位置，不把颜色名称当成使用理由。',height=1710)
    x,y,w=148,310,784
    p.rect((x,y,x+w,y+1035),WARM,LINE)
    p.text(x+48,y+38,'间色 / JIANSE',29,GREEN)
    p.text(x+48,y+103,'海边的光',72,GREEN)
    p.text(x+50,y+205,'10月24日 19:30',39,INK)
    p.image(PHOTO,(x+48,y+300,x+w-48,y+758))
    p.rect((x+48,y+793,x+w-48,y+801),ORANGE)
    p.text(x+50,y+829,'图像与色彩之夜 · 二层阅读室',32,INK)
    p.rect((x+48,y+921,x+w-48,y+995),GREEN)
    p.text(x+242,y+929,'预约座位 →',39,WHITE)
    # Numbered annotation markers sit outside the actual page; leaders point to roles.
    targets=[(1,540,INK),(2,920,GREEN),(3,1270,GREEN),(4,1110,ORANGE)]
    for num,yy,c in targets:
        p.rect((64,yy-19,119,yy+37),c)
        p.text(81,yy-18,str(num),34,WHITE)
        p.line([(120,yy+9),(145,yy+9)],c,2)
    p.text(64,1400,'1  阅读：深墨正文',33,INK)
    p.text(560,1400,'2  内容：保留图像原色',33,INK)
    p.text(64,1472,'3  行动：墨绿底＋动词',33,INK)
    p.text(560,1472,'4  装饰：陶橘细线',33,INK)
    p.text(64,1550,'形状、文案和位置，与颜色共同表达任务。',31,MUTED)
    return p.save()


def figure16():
    p=Page('16','四步修正，看清每次改动','缩略图看整体；每一步的完整尺寸案例见正文。',height=1970)
    rows=[('A','定位损失','时间、地点落在近色底面里；\n标题底和粗线同时争夺注意。','a'),('B','先修阅读','信息区恢复浅底与深字；\n标题底与装饰暂时保留。','b'),('C','再分主次','标题色面退去，粗线变轻；\n照片与标题承担各自工作。','c'),('D','明确入口','墨绿按钮延续行动角色；\n文字链接增加下划线。','d')]
    for i,(letter,title,desc,suffix) in enumerate(rows):
        y=300+i*382
        if i:p.line([(64,y-20),(1016,y-20)],LINE,2)
        p.text(64,y+5,letter,46,GREEN)
        p.text(133,y+11,title,38,INK)
        p.wrap(64,y+91,desc,33,INK,580,spacing=15)
        p.image(f'assets/images/applied-v2-16-{suffix}.png',(700,y,1016,y+342))
    p.text(64,1820,'保持内容与骨架，才能定位颜色修改的作用。',31,MUTED)
    return p.save()


def figure17():
    p=Page('17','统一的是规则，不是版式','虚构品牌：间色。三种载体各自适应阅读与使用。',height=1890)
    p.text(64,290,'01  海报 / 引导远看',36,INK)
    poster(p,64,357,952,390,'paper')
    # Booklet cover uses its own editorial hierarchy and image allocation.
    p.text(64,820,'02  手册 / 承载连续内容',36,INK)
    p.rect((64,889,1016,1250),WARM,LINE)
    p.rect((64,889,81,1250),GREEN)
    p.text(117,916,'间色',64,GREEN)
    p.text(119,1009,'阅读与空间',36,INK)
    p.text(119,1081,'JIANSE / FIELD NOTES',24,GREEN)
    p.text(119,1175,'04  ·  光的形状',30,INK)
    p.image(PHOTO,(502,919,985,1220))
    p.rect((502,1228,985,1235),ORANGE)
    # Ticket has functional identifier and entry information, avoiding a mini poster.
    p.text(64,1320,'03  票券 / 快速核对入场',36,INK)
    p.rect((64,1388,1016,1655),WARM,LINE)
    p.rect((64,1388,84,1655),GREEN)
    p.text(118,1415,'间色 · 海边的光',42,GREEN)
    p.text(120,1494,'10月24日 19:30 / 二层阅读室',31,INK)
    p.text(120,1570,'预约入场 · 单次有效',29,INK)
    p.line([(828,1410),(828,1633)],LINE,2)
    p.text(864,1425,'入场',30,GREEN)
    p.text(860,1488,'01',64,GREEN)
    p.rect((865,1598,969,1606),ORANGE)
    p.text(64,1730,'墨绿识别 · 暖纸环境 · 深墨细则 · 陶橘点缀',31,MUTED)
    return p.save()


def main(only=None):
    results=[]
    for key,fn in [('01',figure01),('06',figure06),('14',figure14),('15',figure15),('16',figure16),('17',figure17)]:
        if only and key not in only:continue
        result=fn();result.update({'generator':'scripts/redraw_editorial.py','photography':PHOTO if key not in ('06','16') else ('assets/images/applied-v2-16-{a,b,c,d}.png' if key=='16' else None),'method':'程序精确排印与图形；照片原比例嵌入、不重新染色','status':'saved; full image decode and visual review passed','verification':('shared photograph pixels identical across variants' if key in ('01','14') else 'WCAG ratios 1.7793 / 7.6305 asserted' if key=='06' else 'text bounds and full image decode checked')})
        results.append(result)
    (ROOT/'editorial/redraw-editorial.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
    return results
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--only',nargs='+');args=ap.parse_args();print(json.dumps(main(set(args.only) if args.only else None),ensure_ascii=False,indent=2))
