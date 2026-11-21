"""Render the owner's positioning discussion sheet; requires Pillow only."""
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont
import base64
import html
import re

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
ASSET = ROOT / 'docs/images/electrical-positioning-20261121'
ASSET.mkdir(parents=True, exist_ok=True)
SOURCE = ROOT / 'docs/electrical-network-positioning-draft-20261121.md'
FONT = 'C:/Windows/Fonts/msyh.ttc'
BOLD = 'C:/Windows/Fonts/msyhbd.ttc'

def font(size, bold=False):
    return ImageFont.truetype(BOLD if bold else FONT, size)

# Coordinates locate discussion groups on the supplied image, not construction points.
groups = [
    ('01', 729, 650, '入户左手开关、原门禁屏'),
    ('02', 715, 680, '核心 C0：入户左侧候选区'),
    ('03', 255, 309, '电视 / 大厅交换机 H0'),
    ('04', 356, 510, '沙发两侧、边几电源'),
    ('05', 402, 294, '电视同面H1M/S100；大厅其余面板分组'),
    ('06', 335, 395, '顶面 AP / M200 / E1（分开布点）'),
    ('07', 481, 475, 'FP400顶装：视场与USB电源候选'),
    ('08', 570, 318, '水吧台面与柜灯'),
    ('09', 779, 483, '餐边柜台面与柜灯'),
    ('10', 708, 415, '厨房入口灯控、台面电源'),
    ('11', 861, 561, '冰箱 / 嵌电 / 净水：位置待核'),
    ('12', 395, 245, '主卧门口开关 / 面板 AP'),
    ('13', 76, 79, '主卧左床头：柜子右侧墙面'),
    ('14', 253, 81, '主卧右床头'),
    ('15', 33, 100, '主卧窗帘电机/常电：候选端待核'),
    ('16', 625, 249, '次卧门口开关 / 面板 AP'),
    ('17', 688, 66, '次卧书桌插座与网口'),
    ('18', 819, 110, '次卧床头：朝向随实物核'),
    ('19', 391, 604, '电竞房门口开关 / 面板 AP'),
    ('20', 271, 744, '电竞双桌：左右分组'),
    ('21', 362, 679, '电竞交换机 S0 / 主机架'),
    ('22', 203, 609, '投影 / 影音：仅候选区域'),
    ('23', 541, 177, '主卫 A：镜柜、奥普、马桶'),
    ('24', 478, 747, '公卫 B：镜柜、奥普、马桶'),
    ('25', 640, 620, '洗衣 / 清洁家电'),
    ('26', 40, 373, '阳台窗帘电机/常电：候选端待核'),
]

base = Image.open(ROOT / 'docs/images/floorplan-20261020/装修布置图.jpg').convert('L')
base = ImageOps.invert(base).point(lambda p: min(255, round(p * 0.9 + 25)))
base = base.convert('RGB')
COLORS = {'S': '#c52e42', 'P': '#146cb6', 'AW': '#138152', 'AC': '#138152',
          'E': '#b56b0a', 'N': '#7846ad', 'D': '#57646c'}
CAPTIONS = {'S05A':'S05A H1M', 'S05B':'S05B H1M', 'S05D':'S05D S100',
            'E15':'E15 主卧窗帘', 'E26':'E26 阳台窗帘',
            'D06M':'D06M M200 顶装', 'D07F':'D07F FP400 顶装',
            'D12M':'D12M M1S', 'E12M':'E12M M1S常电'}
CURTAIN_CODES = ('E15', 'E26')

# x/y point to a candidate wall or equipment area; lx/ly offset only the label.
# These source-image coordinates are deliberately NOT millimetre coordinates.
power = [
    ('S01',729,650,755,698), ('D01',690,650,674,700),
    ('P01',868,590,849,600), ('P02',620,650,595,684),
    ('P03A/B',255,294,255,330),
    ('P04A',170,551,144,512), ('P04B',390,552,412,519),
    ('S05A',392,294,360,345), ('S05B',520,280,546,251),
    ('S05C',599,275,583,226), ('S05D',411,294,456,375),
    ('S10',708,415,659,390),
    ('P08',578,295,556,341), ('P09',775,499,775,525),
    ('P09H',710,455,650,485),
    ('P10',751,294,746,352), ('P10H',810,295,825,268),
    ('P10U',883,392,843,434), ('P10R',850,417,828,474),
    ('P11',885,559,852,560),
    ('S12',420,271,389,202), ('P12',385,274,344,249),
    ('S13',71,79,110,114), ('P13',81,79,107,153),
    ('S14',253,47,255,78), ('P14',252,47,258,120),
    ('S16',613,271,650,238), ('P16',655,272,690,271),
    ('P17',698,48,695,100), ('S18',851,87,784,125), ('P18',857,87,831,167),
    ('S19',398,643,362,622), ('P19',398,651,395,685),
    ('P20A',236,772,227,739), ('P20B',344,772,325,739),
    ('P21',145,738,180,691), ('P22',144,615,185,606),
    ('S23',491,203,515,230), ('P23M',585,155,549,133),
    ('P23T',489,62,515,76), ('S24',465,651,491,679),
    ('P24M',504,611,464,589), ('P24T',422,756,454,734),
    ('P25',650,596,624,561),
]
wiring = [
    ('AW12',385,269,354,239), ('AW16',648,269,679,239),
    ('AW19',390,648,356,619), ('AC06',338,389,355,422),
    ('D06M',462,305,499,340), ('D06C',64,324,105,363),
    ('D07F',481,475,505,440), ('D12M',365,272,318,196),
    ('N02',619,650,590,685), ('N03',271,298,269,334),
    ('N21',145,738,182,700), ('N17',691,49,691,101),
    ('N20A',237,772,228,739), ('N20B',344,772,326,739),
    ('N22',143,615,184,615), ('N01',710,651,741,690),
    ('N07',487,475,554,495), ('N05G',408,310,410,365),
    ('E06C',65,324,102,307), ('E06L',308,305,322,274),
    ('E07',481,475,432,503), ('E12M',365,272,250,228),
    ('E08',577,294,625,332),
    ('E09',780,499,783,528), ('E15',33,100,78,205),
    ('E26',40,373,73,449), ('E22',145,615,168,570),
    ('E23',518,97,553,65), ('E24',486,707,508,745),
    ('E10',869,300,849,337),
]

# Both overview sheets and enlarged details use the same physical anchors.
# Curtain ends are candidates only; neither the side nor rail route is confirmed.
points_by_code = {item[0]: item for item in power + wiring}
curtain_points = [points_by_code[code] for code in CURTAIN_CODES]

def detail_point(code, lx, ly):
    return (*points_by_code[code][:3], lx, ly)

def kind(code):
    return 'AW' if code.startswith('AW') else 'AC' if code.startswith('AC') else code[0]

def marker(draw, item, transform, size=38, caption=None, phase='all'):
    code,x,y,lx,ly = item
    color = COLORS[kind(code)]
    x,y = transform(x,y)
    lx,ly = transform(lx,ly)
    if phase in ('all','line'):
        draw.line((x,y,lx,ly), fill=color, width=3)
        if code in CURTAIN_CODES:
            draw.rounded_rectangle((x-11,y-18,x+11,y+18),radius=4,
                                   fill='white',outline=color,width=3)
            draw.text((x,y),'M',font=font(14,True),fill=color,anchor='mm')
        else:
            draw.ellipse((x-6,y-6,x+6,y+6), fill=color)
    if phase == 'line':
        return
    title = caption or CAPTIONS.get(code,code)
    box = draw.textbbox((0,0), title, font=font(size,True))
    width = box[2]-box[0]+28
    height = size+20
    bounds = (lx-width/2,ly-height/2,lx+width/2,ly+height/2)
    if kind(code) == 'AC':
        draw.rounded_rectangle(bounds, radius=height/2, fill='white', outline=color,width=4)
    else:
        draw.rounded_rectangle(bounds, radius=7, fill='white', outline=color,width=4)
    draw.text((lx,ly-2),title,font=font(size,True),fill=color,anchor='mm')

def legend(draw, y, entries):
    for i,(prefix,title) in enumerate(entries):
        x=110+i*465
        draw.rounded_rectangle((x,y,x+100,y+56),radius=8,fill=COLORS[prefix])
        draw.text((x+50,y+26),prefix,font=font(30,True),fill='white',anchor='mm')
        draw.text((x+115,y+5),title,font=font(32),fill='#24343d')

def full_map(filename,title,subtitle,points,notes):
    canvas=Image.new('RGB',(3000,3090),'white')
    draw=ImageDraw.Draw(canvas)
    draw.text((110,40),title,font=font(66,True),fill='#183a47')
    draw.text((112,130),subtitle,font=font(34),fill='#51606a')
    canvas.paste(base.resize((2718,2400),Image.Resampling.LANCZOS),(141,220))
    transform=lambda x,y:(141+x*3,220+y*3)
    for phase in ('line','label'):
        for item in points:
            marker(draw,item,transform,phase=phase)
    draw.line((110,2660,2890,2660),fill='#cbd3d7',width=3)
    legend(draw,2690,[('S','开关 / 控制屏'),('P','插座组'),('AW','面板AP'),('AC','吊顶AP'),('E','预留电源'),('N','网线 / 弱电')])
    for i,note in enumerate(notes):
        draw.text((110,2795+i*62),note,font=font(33),fill='#24343d')
    canvas.save(ASSET/filename,optimize=True)

full_map('position-groups.png','01 / 开关、插座与窗帘 · 分色点位图',
    '2026-11-21 修订：主卧点位移至柜子右侧、次卧恢复原点；H1M/S100移到电视同面。',power+curtain_points,[
    'S01：左手开灯；D01：已有门禁屏（灰色参照，坐标待量尺）；P01：鞋柜插座另定位。',
    'S05A＝H1M、S05D＝S100屏，均在电视墙同面；S05B/C为其余H1M，S16/S18为普通开关。',
    'P03A/B为电视背后与柜内上下分层；P10U厨下、P10R水槽右侧、P09H餐桌火锅取电。',
    'S13/P13在柜子右侧墙面；S18/P18恢复此前偏左位置；橙色M为E15主卧/E26阳台电机候选端。'])
full_map('ap-wiring-points.png','02 / AP、网口与电源预留 · 分色图',
    '大厅M200网关、FP400传感器顶装；另一台M1S网关在主卧，使用开放常电插座。',wiring,[
    'N02 / C0 → AW12主卧、AW16次卧、N03 / H0大厅、N21 / S0电竞：四条中央主干。',
    'M200：H0供PoE，布2根Cat6A（1用1备）；E1独立供电；主卧M1S走Wi-Fi＋E12M常电。',
    'FP400顶装：E07供USB-C 5V1A，N07仅备用；官方推荐顶装3–4m，现场核吊顶高度与视场。',
    'E15主卧/E26阳台：M为电机候选端，均需常电；E23/E24奥普；E10燃气报警条件位。'])

# Two enlarged details distinguish actual door-hand information from approximate scale.
detail=Image.new('RGB',(1880,2250),'white')
dd=ImageDraw.Draw(detail)
dd.text((65,35),'03 / 入户与厨房开关 · 放大讨论图',font=font(51,True),fill='#183a47')
dd.text((65,110),'红色S开关 · 蓝色P插座 · 灰色D已有设备；示意门向，不代表实测门宽。',font=font(27),fill='#51606a')
dd.text((65,185),'A  入户：内开、右铰链，左手侧安排 S01',font=font(38,True),fill=COLORS['S'])
crop=(550,500,906,720)
detail.paste(base.crop(crop).resize((1068,660),Image.Resampling.LANCZOS),(65,260))
t=lambda x,y:(65+(x-550)*3,260+(y-500)*3)
# Dashed door swing is schematic; the user confirmed orientation, not exact endpoints.
hx,hy=t(824,650)
r=80*3
dd.arc((hx-r,hy-r,hx+r,hy+r),180,270,fill='#828e96',width=3)
for y in range(int(hy-r),int(hy),21):
    dd.line((hx,y,hx,min(y+10,hy)),fill='#828e96',width=4)
dd.ellipse((hx-8,hy-8,hx+8,hy+8),fill='#57646c')
dd.text((hx+12,hy+10),'右门轴',font=font(25),fill='#57646c')
marker(dd,('S01',729,650,739,695),t,32,'S01 左手灯控')
marker(dd,('D01',690,650,633,682),t,29,'D01 门禁屏')
marker(dd,('P01',868,590,852,553),t,29,'P01 鞋柜电源')
for i,line in enumerate(['左手墙段，开门即能摸到。','S01中心先按110–120cm讨论。','门禁屏保留原位；开关优先','在其下方可达处，或并排。','强电/楼宇线分管、分底盒。','屏幕与门轴坐标均待现场量尺。']):
    dd.text((1195,320+i*66),line,font=font(29),fill='#24343d')
dd.line((65,990,1815,990),fill='#cbd3d7',width=3)
dd.text((65,1030),'B  厨房：S10 在入口餐厅侧，先开灯再进去',font=font(38,True),fill=COLORS['S'])
crop=(510,270,906,520)
detail.paste(base.crop(crop).resize((1188,750),Image.Resampling.LANCZOS),(65,1130))
t=lambda x,y:(65+(x-510)*3,1130+(y-270)*3)
marker(dd,('S10',708,415,644,390),t,34,'S10 厨房灯控')
marker(dd,('P10',751,294,765,345),t,30,'P10 台面插座')
marker(dd,('P10U',883,392,846,375),t,27,'P10U 水槽下')
marker(dd,('P10R',850,417,844,442),t,27,'P10R 水槽右侧')
marker(dd,('P09H',710,455,637,486),t,27,'P09H 火锅取电')
marker(dd,('P09',775,499,785,478),t,28,'P09 餐边柜')
a=t(658,409); b=t(719,384)
dd.line((*a,*b),fill='#57646c',width=4)
dd.polygon([b,(b[0]-18,b[1]+3),(b[0]-10,b[1]+20)],fill='#57646c')
dd.text(t(610,448),'从餐厅进入厨房 →',font=font(27),fill='#57646c')
for i,line in enumerate(['S10：入口餐厅侧，原H1M。','P10U：水槽下约2个插位，','柜内干燥侧壁，可检修。','P10R：面对水槽右手侧；','图纸为下方台面端。','P09H：餐桌靠短墙一端，','电磁炉短线到桌，不跨走道。','电磁炉负载/插头需核回路。','短边界墙体/柜体先核可装性。']):
    dd.text((1290,1195+i*62),line,font=font(27),fill='#24343d')
dd.text((65,1970),'开关和插座分开定位：S10移到入口，P10仍按厨房台面设备使用位置安排。',font=font(32,True),fill='#183a47')
dd.text((65,2050),'颜色表示类别，不表示已定案。墙体、柜体、门宽、标高与具体间距明天现场签认。',font=font(30),fill='#51606a')
detail.save(ASSET/'entry-kitchen-detail.png',optimize=True)

# A compact detail sheet shows which face of each protrusion is intended.
bed=Image.new('RGB',(2400,2230),'white')
bd=ImageDraw.Draw(bed)
bd.text((65,35),'04 / 床头点位、主卫右手灯控与电视电源',font=font(54,True),fill='#183a47')
bd.text((65,112),'红色S＝开关；蓝色P＝插座；橙色E＝窗帘常电。俯视图不表达实际安装高度。',font=font(30),fill='#51606a')
bd.text((65,190),'A  主卧：S13/P13右移至柜子旁墙面',font=font(35,True),fill='#183a47')
crop=(0,15,130,190)
bed.paste(base.crop(crop).resize((520,700),Image.Resampling.LANCZOS),(65,250))
t=lambda x,y:(65+x*4,250+(y-15)*4)
bd.line((*t(66,79),*t(86,79)),fill='#183a47',width=7)
for phase in ('line','label'):
    marker(bd,detail_point('S13',195,78),t,31,'S13 床头开关',phase)
    marker(bd,detail_point('P13',195,115),t,31,'P13 床头插座',phase)
    marker(bd,detail_point('E15',195,145),t,31,'E15 电机/常电',phase)
bd.text((640,300),'深色短线＝柜子右侧墙面',font=font(27),fill='#183a47')
bd.text((640,830),'E15仅示候选端，高度随电机复尺。',font=font(26),fill='#51606a')
bd.text((640,880),'窗帘常电独立于床头灯控。',font=font(27),fill='#51606a')
bd.text((1240,190),'B  次卧：S18/P18向左恢复原位',font=font(35,True),fill='#183a47')
crop=(700,15,906,220)
bed.paste(base.crop(crop).resize((618,615),Image.Resampling.LANCZOS),(1240,250))
t=lambda x,y:(1240+(x-700)*3,250+(y-15)*3)
bd.line((*t(844,87),*t(861,87)),fill='#183a47',width=7)
for phase in ('line','label'):
    marker(bd,detail_point('S18',1005,90),t,31,'S18 普通床头开关',phase)
    marker(bd,detail_point('P18',1005,145),t,31,'P18 床头插座',phase)
bd.text((1240,920),'与S16门口灯控是否做普通双控，由电工按灯路接线。',font=font(28),fill='#51606a')
bd.line((65,1010,2335,1010),fill='#cbd3d7',width=3)
bd.text((65,1060),'C  主卫：进入卫生间前，右手开灯',font=font(35,True),fill='#183a47')
crop=(360,70,630,260)
bed.paste(base.crop(crop).resize((1080,760),Image.Resampling.LANCZOS),(65,1130))
t=lambda x,y:(65+(x-360)*4,1130+(y-70)*4)
marker(bd,('S23',491,203,552,234),t,34,'S23 右手灯控')
a=t(437,233); b=t(474,167)
bd.line((*a,*b),fill='#57646c',width=4)
bd.polygon([b,(b[0]-15,b[1]+25),(b[0]+10,b[1]+22)],fill='#57646c')
bd.text(t(375,239),'从主卧入主卫',font=font(28),fill='#57646c')
bd.text((1240,1060),'D  电视区：上下分层，不是左右加两组',font=font(35,True),fill='#183a47')
bd.rectangle((1320,1190,2120,1530),outline='#62727b',width=5)
bd.text((1720,1235),'电视 / 挂架范围',font=font(32),fill='#62727b',anchor='mm')
bd.rounded_rectangle((1570,1350,1905,1412),radius=7,fill='white',outline=COLORS['P'],width=4)
bd.text((1737,1380),'P03A 电视背后电源',font=font(28,True),fill=COLORS['P'],anchor='mm')
bd.rectangle((1290,1645,2175,1850),outline='#62727b',width=5)
bd.text((1733,1690),'电视柜：设备 / 通风格',font=font(31),fill='#62727b',anchor='mm')
bd.rounded_rectangle((1565,1740,1910,1805),radius=7,fill='white',outline=COLORS['P'],width=4)
bd.text((1737,1772),'P03B 柜内设备电源',font=font(28,True),fill=COLORS['P'],anchor='mm')
bd.line((1490,1530,1490,1645),fill=COLORS['N'],width=5)
bd.text((1520,1573),'柜到电视的可抽换弱电通道',font=font(27),fill=COLORS['N'])
bd.text((1240,1920),'全电视区仍合计约6–8插位，A/B不各算一份。',font=font(29),fill='#51606a')
bd.text((1240,1970),'电视放柜上时可合并柜内；高位按挂架避让。',font=font(29),fill='#51606a')
bd.text((1240,2020),'S05A H1M / S05D S100已移到电视同面，见总图。',font=font(27),fill='#183a47')
bd.text((65,2110),'凸墙若为结构柱/承重构件，采用获准的饰面层或浅盒安装，不为底盒深凿、切筋。',font=font(31),fill='#183a47')
bed.save(ASSET/'bedroom-tv-detail.png',optimize=True)

curtains=Image.new('RGB',(2400,1680),'white')
cd=ImageDraw.Draw(curtains)
cd.text((65,35),'05 / 主卧与阳台 · 窗帘电机、常电放大图',font=font(54,True),fill='#183a47')
cd.text((65,112),'橙色M＝电机候选位置，E＝该电机的常电接口；两张总图与此图使用同一落点。',font=font(30),fill='#51606a')
cd.text((65,190),'A  E15 主卧：已签 C200 ×1',font=font(37,True),fill='#183a47')
curtains.paste(base.crop((0,20,130,280)).resize((520,1040),Image.Resampling.LANCZOS),(65,265))
t=lambda x,y:(65+x*4,265+(y-20)*4)
marker(cd,detail_point('E15',190,115),t,34,'E15 电机＋常电')
for i,line in enumerate(['候选：靠窗上端、柜体外侧。','图中“上端”仅指图纸方向。','不是S13/P13床头用电位。','按电机/轨道确定实际端头，','接口留高位并可检修。','纱帘第二电机仍为可选项。']):
    cd.text((640,770+i*60),line,font=font(27),fill='#24343d')
cd.line((1195,185,1195,1320),fill='#cbd3d7',width=3)
cd.text((1240,190),'B  E26 阳台：已签 C200 ×1',font=font(37,True),fill='#183a47')
curtains.paste(base.crop((0,275,160,780)).resize((320,1010),Image.Resampling.LANCZOS),(1240,265))
t=lambda x,y:(1240+x*2,265+(y-275)*2)
marker(cd,detail_point('E26',365,390),t,34,'E26 电机＋常电')
for i,line in enumerate(['候选：图纸左侧长窗上端。','阳台名称依据原签字单；','原图未独立标出阳台边界。','窗帘实际位置及电机端头','均需现场核对后定位。','原单7m不是轨道下料尺寸。','原“公共窗帘”即本组，','此次不新增第三台电机。']):
    cd.text((1660,770+i*60),line,font=font(27),fill='#24343d')
cd.line((65,1350,2335,1350),fill='#cbd3d7',width=3)
for i,line in enumerate(['两处均为窗帘专用常电，不由床头灯开关、普通照明开关或离家全断电场景切断。',
                         '电机端、轨道走向与安装高度未定案；按窗帘盒、梁、厂家安装图和拆换空间现场复尺。',
                         'M/E是同一台电机及其接口，不重复计设备或电源数量；原签C200合计2套。']):
    cd.text((65,1395+i*75),line,font=font(32),fill='#24343d')
curtains.save(ASSET/'curtain-motor-detail.png',optimize=True)
PNG = ASSET / 'position-groups.png'

def inline(text):
    text = html.escape(text)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    def link(match):
        title, target = match.groups()
        if target.startswith(('https://', 'http://')):
            return f'<a href="{target}">{title}</a>'
        # Standalone print copy: the complete source bibliography stays in Markdown.
        return title
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', link, text)
    return text

def render_markdown(source):
    lines = source.splitlines()
    result = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if line.startswith('!['):
            match = re.fullmatch(r'!\[([^\]]*)\]\(([^)]+)\)',line)
            image_path = SOURCE.parent / match.group(2)
            data = base64.b64encode(image_path.read_bytes()).decode()
            result.append(f'<figure><img src="data:image/png;base64,{data}" alt="{html.escape(match.group(1),quote=True)}"></figure>')
        elif line.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                cells = [s.strip() for s in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r':?-+:?', c) for c in cells):
                    rows.append(cells)
                i += 1
            result.append('<div class="table-wrap"><table><thead><tr>' + ''.join('<th>'+inline(c)+'</th>' for c in rows[0]) + '</tr></thead><tbody>')
            for cells in rows[1:]:
                result.append('<tr>' + ''.join('<td data-label="'+html.escape(rows[0][j], quote=True)+'">'+inline(c)+'</td>' for j, c in enumerate(cells)) + '</tr>')
            result.append('</tbody></table></div>')
            continue
        elif line.startswith('#'):
            level = len(line) - len(line.lstrip('#'))
            result.append(f'<h{level}>{inline(line[level:].strip())}</h{level}>')
        elif line.startswith('>'):
            result.append('<p class="context">'+inline(line[1:].strip())+'</p>')
        elif re.match(r'^(\d+\. |\- )', line):
            ordered = bool(re.match(r'^\d+\. ', line))
            tag = 'ol' if ordered else 'ul'
            pattern = r'^\d+\. ' if ordered else r'^\- '
            result.append(f'<{tag}>')
            while i < len(lines) and re.match(pattern, lines[i].strip()):
                item = re.sub(pattern, '', lines[i].strip())
                item = item.replace('[ ]', '□')
                result.append('<li>'+inline(item)+'</li>')
                i += 1
            result.append(f'</{tag}>')
            continue
        else:
            result.append('<p>'+inline(line)+'</p>')
        i += 1
    return '\n'.join(result)

body = render_markdown(SOURCE.read_text(encoding='utf-8'))
page = '''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>11月22日水电定位讨论稿</title>
<style>
*{box-sizing:border-box}body{margin:0;background:#f1f4f4;color:#24323a;font-family:"Microsoft YaHei","PingFang SC",sans-serif;font-size:15px;line-height:1.8}
main{max-width:1180px;margin:24px auto;background:#fff;padding:40px 48px}h1{font-size:29px;margin:0 0 18px;color:#183a47}h2{font-size:24px;margin:38px 0 15px;padding-top:12px;border-top:2px solid #16747c}h3{font-size:19px;margin:25px 0 12px;color:#16747c}
p{margin:12px 0}.context{background:#f1f6f6;padding:12px 18px}figure{margin:22px auto;max-width:860px}img{display:block;width:100%;height:auto}table{width:100%;border-collapse:collapse;font-size:14px;line-height:1.65;margin:12px 0 22px}th{background:#e9f1f1;text-align:left;color:#183a47}td,th{padding:10px 12px;border:1px solid #cdd8db;vertical-align:top}td:first-child{min-width:115px}tr:nth-child(even){background:#f8fafb}.table-wrap{overflow:auto}li{margin:8px 0}a{color:#176b76}code{font-size:.95em;background:#eef2f4;padding:1px 4px;overflow-wrap:anywhere}.toolbar{max-width:1180px;margin:18px auto;text-align:right}.toolbar button{font:inherit;border:0;background:#183a47;color:white;padding:10px 20px;cursor:pointer;border-radius:6px}
@media screen and (max-width:700px){main{padding:24px 16px;margin:0}h1{font-size:24px}h2{font-size:22px}.toolbar{padding:0 16px}.context{padding:10px}.table-wrap{overflow:visible}table,tbody,tr,td{display:block;width:100%}thead{display:none}tr{margin-bottom:18px;border:1px solid #cdd8db}td{border:0;border-bottom:1px solid #e7ecee;padding:10px 12px}td:first-child{font-weight:bold;background:#e9f1f1}td:not(:first-child)::before{content:attr(data-label);display:block;color:#16747c;font-size:12px;margin-bottom:4px}td:last-child{border-bottom:0}}
@page{size:A4;margin:13mm 12mm 15mm}
@media print{body{background:white;font-size:9.5pt;line-height:1.5}main{padding:0;margin:0;max-width:none}.toolbar{display:none}h1{font-size:19pt}h2{font-size:15pt;break-after:avoid;margin-top:20px}h3{font-size:11.5pt;break-after:avoid}p{orphans:3;widows:3}figure{max-width:165mm;break-inside:avoid}table{font-size:8.8pt;line-height:1.45;min-width:0}td,th{padding:6px}td:first-child{min-width:0}tr{break-inside:avoid}thead{display:table-header-group}.table-wrap{overflow:visible}a{color:inherit;text-decoration:none}li{margin:5px 0}}
</style></head><body><div class="toolbar"><button onclick="window.print()">打印 / 另存为 PDF</button></div><main>'''+body+'''</main></body></html>'''
(OUT / '水电定位讨论稿.html').write_text(page, encoding='utf-8')
assert len(groups) == 26 and len({g[0] for g in groups}) == 26
assert len(re.findall(r'<table>', page)) == len(re.findall(r'</table>', page))
print(PNG)
print(OUT / '水电定位讨论稿.html')
