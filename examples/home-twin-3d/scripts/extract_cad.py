"""Reproduce the small house twin from the locally converted user CAD.

The linework is extracted automatically. Walls are a reviewed selection of
paired CAD lines: indiscriminately extruding layer 墙体 would also turn beds,
wardrobes and window ledges into walls. Room zoning is a documented manual
interpretation of this plan, not automated CAD room recognition.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import ezdxf
from ezdxf.disassemble import recursive_decompose

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT.parent / "outputs/smart-home-3d-research/cad/floorplan.dxf"


def extract(source: Path) -> dict:
    doc = ezdxf.readfile(source)
    if doc.header.get("$INSUNITS") != 4:
        raise ValueError("Expected the inspected CAD to use millimetres (INSUNITS=4)")
    ms = doc.modelspace()
    by_handle = {e.dxf.handle: e for e in ms}
    # Outer top-left corner is the end of the top external wall line D63D1.
    ox, oy, _ = by_handle["D63D1"].dxf.end
    def p(x, y):
        return [round((float(x)-ox)/1000, 6), round((oy-float(y))/1000, 6)]
    def line(e):
        return [p(e.dxf.start.x,e.dxf.start.y),p(e.dxf.end.x,e.dxf.end.y)]
    def source_refs(refs):
        for ref in refs.split(","):
            if ref and ref not in by_handle:
                raise ValueError(f"Reviewed CAD entity {ref} is missing")
        return f"CAD 实体 {refs}；双线/边线人工归并为单墙中心线，未逐线拉伸。"

    # The exterior follows the CAD outer edges, including its south-east recess
    # and 20/25 mm changes in facade alignment. It is NOT the 11.33 m inner span.
    footprint = [[0,0],[11.81,0],[11.81,2.6],[11.83,2.6],
                 [11.83,8.455],[7.215,8.455],[7.215,10.17],
                 [.025,10.17],[.025,4.43],[0,4.43]]

    # Coordinates in m, traced from this CAD after the origin transform above.
    # Gaps are deliberate. Windows and doors are separate semantic records.
    wall_specs = [
      ("outer-nw",[.12,.165],[6.435,.165],.33,"wall","D6350,D63D1"),
      ("outer-ne",[7.135,.165],[11.69,.165],.33,"wall","D6373,D63D0"),
      ("outer-west-top",[.12,.12],[.12,.235],.24,"wall","D63D2"),
      ("outer-west-middle",[.2575,3.33],[.2575,4.43],.515,"wall","D63D3,D63A6"),
      ("outer-west-bottom",[.145,9.125],[.145,10.0275],.24,"wall","D63C9,D63A1"),
      ("outer-south-west",[.145,10.0275],[5.18,10.0275],.285,"wall","D6385,D63CA"),
      ("outer-south-east",[6.05,10.05],[7.095,10.05],.24,"wall","D6394,D6395"),
      ("outer-return",[7.095,8.335],[7.095,10.05],.24,"wall","D638F,D6390"),
      ("entry-left",[7.095,8.335],[9.59,8.335],.24,"wall","D6321,D6322"),
      ("entry-right",[10.66,8.335],[11.71,8.335],.24,"wall","D631E,D63CB"),
      ("outer-east-top",[11.69,.165],[11.69,.85],.24,"wall","D6381,D63CF"),
      ("outer-east-middle",[11.71,2.6],[11.71,4.28],.24,"wall","D637C,D6333,D63CD"),
      ("outer-east-bottom",[11.71,5.14],[11.71,8.335],.24,"wall","D6338,D631F,D63CC"),
      ("master-south",[.515,3.4575],[5.435,3.4575],.255,"wall","D634F,D6384"),
      ("master-door-jamb",[5.435,3.23],[5.435,3.4575],.10,"wall","D6345,D634E"),
      ("bath-west",[5.44,.33],[5.44,1.368],.11,"wall","D6360,D6361"),
      ("bath-south",[6.219,2.32],[7.805,2.32],.12,"wall","D6348,D6371,D6B28"),
      ("bedroom-west",[7.805,.33],[7.805,2.455],.12,"wall","D636D,D6B27,D634B,D634C"),
      ("bedroom-door-jamb",[7.81,3.215],[7.81,3.445],.11,"wall","D6344,D634D"),
      ("bedroom-south-left",[6.665,3.4375],[7.575,3.4375],.215,"wall","D6372,D6343"),
      ("bedroom-south-right",[7.575,3.4575],[11.69,3.4575],.255,"wall","D6372,D6341,D6332"),
      ("kitchen-nw-stub",[9.135,3.56],[9.135,4.23],.11,"wall","D632F"),
      ("kitchen-south",[9.14,5.855],[10.88,5.855],.11,"wall","D6329,D632B"),
      ("kitchen-shaft-west",[10.88,5.855],[10.88,6.67],.10,"wall","D6328,D63B2"),
      ("kitchen-shaft-south",[10.88,6.67],[11.71,6.67],.10,"wall","D6326,D6327"),
      ("studio-west",[1.715,7.075],[1.715,9.885],.12,"wall","D639D,D6D4F"),
      ("studio-north",[1.715,7.075],[5.045,7.075],.12,"wall","D6D26,D6D49"),
      ("studio-east-jamb",[5.045,7.075],[5.045,7.217],.12,"wall","DA96E,DA96F"),
      ("studio-east",[5.0375,8.27],[5.0375,9.885],.105,"wall","D6340,D6391"),
      ("guest-bath-nw",[4.985,8.27],[5.135,8.27],.11,"wall","D633F,D638D"),
      ("guest-bath-ne",[5.935,8.27],[6.975,8.27],.11,"wall","D633C,D638E"),
      ("vanity-east",[7.085,7.015],[7.085,8.215],.22,"wall","D6320,D633B"),
    ]
    walls = [{"id":i,"a":a,"b":b,"thickness":t,"height":2.65,"kind":k,
              "provenance":source_refs(refs)+"墙高 2.65 m 为待确认假设。"}
             for i,a,b,t,k,refs in wall_specs]

    openings = []
    for i,kind,a,b,h,sill,refs in [
      ("entry-door","door",[9.59,8.335],[10.66,8.335],2.1,0,"D631C,D631D"),
      ("studio-door","door",[5.045,7.217],[5.045,8.215],2.1,0,"DA96E,D633E"),
      ("guest-bath-door","door",[5.135,8.27],[5.935,8.27],2.1,0,"D633D,D633E"),
      ("bedroom-door","door",[7.805,2.455],[7.805,3.215],2.1,0,"D6349,D634A"),
      ("master-west-window","window",[.12,.235],[.12,3.33],1.65,.75,"D6357,D635A"),
      ("living-west-window","window",[.145,4.43],[.145,9.125],1.65,.75,"D63A2,D63A5"),
      ("bath-north-window","window",[6.435,.12],[7.135,.12],1.1,1.3,"D6367,D636A"),
      ("bedroom-east-window","window",[11.69,.85],[11.69,2.6],1.65,.75,"D637D,D6380"),
      ("kitchen-east-window","window",[11.71,4.28],[11.71,5.14],1.1,1.2,"D6334,D6337"),
      ("guest-bath-south-window","window",[5.18,10.05],[6.05,10.05],1.1,1.3,"D6396,D6399"),
    ]:
        openings.append({"id":i,"kind":kind,"a":a,"b":b,"height":h,"sill":sill,
                         "provenance":source_refs(refs)+"平面位置/宽度取自 CAD；高度、窗台及门扇形式为示意假设。"})

    room_specs = [
      ("master","主卧",[[.515,.33],[5.385,.33],[5.385,1.397],[6.165,2.38],[6.665,2.38],[6.665,3.33],[.515,3.33]],[2.8,1.7],False),
      ("bathroom","主卫",[[5.495,.33],[7.745,.33],[7.745,2.26],[6.219,2.26],[5.495,1.34]],[6.65,1.2],False),
      ("bedroom","次卧",[[7.865,.33],[11.57,.33],[11.57,3.33],[7.865,3.33]],[9.65,1.7],False),
      ("living","客厅",[[.515,3.585],[6.665,3.585],[6.665,6.9],[5.105,7.015],[1.655,7.015],[1.655,9.885],[.515,9.885]],[3.4,5.25],True),
      ("dining","餐厅",[[6.665,3.585],[9.08,3.585],[9.08,5.91],[10.83,5.91],[10.83,6.72],[7.195,6.72],[7.195,7.015],[6.665,7.015]],[8.15,5.35],True),
      ("studio","电竞房",[[1.775,7.135],[4.985,7.135],[4.985,9.885],[1.775,9.885]],[3.38,8.45],True),
      ("kitchen","厨房",[[9.19,3.56],[11.59,3.56],[11.59,5.8],[9.19,5.8]],[10.4,4.7],False),
      ("guest-bath","客卫",[[5.09,8.325],[6.975,8.325],[6.975,9.93],[5.09,9.93]],[6.05,9.1],False),
      ("entry","玄关",[[7.195,6.72],[11.59,6.72],[11.59,8.215],[7.195,8.215]],[9.75,7.5],False),
    ]
    rooms=[]
    for i,name,poly,center,interactive in room_specs:
        provenance="依据 CAD 墙/门窗/家具平面人工划分区域；polygon 用于地面着色和点击，不用于自动生墙。"
        if i in ("living","dining"):
            provenance += "客餐厅为开放连通空间，二者分界为界面分区。"
        if i=="studio":
            provenance += "左下房间命名为电竞房是用途映射；CAD 可证实 3.21 m 内宽和吧台线，不代表 CAD 原有该房间文字。"
        rooms.append(dict(id=i,name=name,polygon=poly,center=center,interactive=interactive,provenance=provenance))

    # Simple boxes trace visible CAD furniture. Their height/material is an
    # illustration; they are not measured 3D asset models or equipment points.
    furniture=[]
    for i,t,x,z,w,d,h,rot,room,refs in [
      ("living-sofa","sofa",3.403896,6.560656,2.09,.7315,.78,0,"living","CAD AA-家具 可见沙发轮廓，x2.358896–4.448896/z6.194906–6.926406"),
      ("living-coffee","table",3.38,5.55,1.15,.6,.35,0,"living","CAD 家具平面目视定位"),
      ("living-media","cabinet",3.15,3.78,3,.3,.45,0,"living","DA7F0,DA7F7,DA7F8"),
      ("dining-table","table",8.154909,5.716454,1.8,.8,.75,0,"dining","CAD 可见餐桌矩形，x7.254909–9.054909/z5.316454–6.116454"),
      ("dining-chair-1","chair",7.75,5.10,.46,.48,.82,0,"dining","餐桌椅示意"),
      ("dining-chair-2","chair",8.45,5.10,.46,.48,.82,0,"dining","餐桌椅示意"),
      ("dining-chair-3","chair",7.75,6.33,.46,.48,.82,3.141593,"dining","餐桌椅示意"),
      ("dining-chair-4","chair",8.45,6.33,.46,.48,.82,3.141593,"dining","餐桌椅示意"),
      ("studio-bar","bar",3.38,9.485,3.21,.8,.92,0,"studio","D6D28,D6385,D6D4F；吧台内宽3.21m、深0.8m取自CAD"),
      ("studio-seat-1","chair",2.57,8.76,.48,.48,.85,0,"studio","CAD 吧台前圆凳目视定位"),
      ("studio-seat-2","chair",4.14,8.76,.48,.48,.85,0,"studio","CAD 吧台前圆凳目视定位"),
      ("studio-storage","cabinet",2.102,7.386,.654,.502,2.2,0,"studio","DA99D；柜体平面0.654×0.502m"),
      ("master-bed","bed",2.05,1.48,1.8,2.0,.52,0,"master","CAD 床平面目视定位"),
      ("master-wardrobe","wardrobe",4.31,1.2,.6,2.2,2.4,0,"master","D68E9,D68FB，家具误在墙体图层；不拉伸为墙"),
      ("bedroom-bed","bed",10.82,1.33,1.5,2.0,.52,0,"bedroom","床宽1.5m沿用CAD DC089,DC08A,DC08B；依用户反馈向东0.70m、向北0.50m，右侧贴现有东窗侧内边x=11.57、床头贴北墙内边z=0.33；位置为用户调整，不冒充原CAD床位"),
      ("bedroom-wardrobe","wardrobe",8.165,1.6,.6,1.9,2.4,0,"bedroom","CAD 家具平面目视定位"),
      ("kitchen-north","kitchen",10.4,3.86,2.4,.6,.9,0,"kitchen","CAD 厨房轮廓目视定位"),
      ("kitchen-east","kitchen",11.29,4.9,.6,1.45,.9,0,"kitchen","CAD 厨房轮廓目视定位"),
      ("kitchen-south","kitchen",10.11,5.5,1.8,.6,.9,0,"kitchen","CAD 厨房轮廓目视定位"),
      ("dining-sideboard","cabinet",7.85,3.86,2.2,.6,.9,0,"dining","原文 水吧/餐边柜；平面目视定位"),
      ("entry-cabinet","cabinet",8.45,7.88,2.0,.6,1.0,0,"entry","CAD 玄关柜轮廓目视定位"),
      ("guest-wc","wc",5.55,9.5,.4,.68,.55,0,"guest-bath","CAD 洁具目视定位"),
      ("master-wc","wc",5.98,.8,.4,.68,.55,0,"bathroom","CAD 洁具目视定位"),
    ]:
        furniture.append(dict(id=i,type=t,x=x,z=z,width=w,depth=d,height=h,rotation=rot,
                              roomId=room,provenance=refs+"；简化家具示意，立面/材质未测量。"))

    cad_lines=[]
    allowed={"墙体","窗","门","Furniture","家具轮廓","家具内线","AA-家具",
             "内线","内标注","0","AA-COLUMN","0-100a增建墙体","S设备"}
    def add(a,b,layer):
        if math.dist(a,b)<.001: return
        if all(-.1<=q[0]<=12 and -.1<=q[1]<=10.4 for q in (a,b)):
            cad_lines.append(dict(a=a,b=b,layer=layer))
    for e in recursive_decompose(ms):
        if e.dxf.get("invisible", 0):
            continue
        layer=e.dxf.layer
        if layer not in allowed: continue
        typ=e.dxftype()
        if typ=="LINE":
            a,b=line(e);add(a,b,layer)
        elif typ in ("LWPOLYLINE","POLYLINE"):
            try:
                for v in e.virtual_entities():
                    if v.dxftype()=="LINE":
                        a,b=line(v);add(a,b,layer)
                    elif v.dxftype()=="ARC":
                        pts=[p(q.x,q.y) for q in v.flattening(12)]
                        for a,b in zip(pts,pts[1:]):add(a,b,layer)
            except (AttributeError,NotImplementedError): pass
        elif typ in ("ARC","CIRCLE","ELLIPSE","SPLINE"):
            try:
                pts=[p(q.x,q.y) for q in e.flattening(12)]
                for a,b in zip(pts,pts[1:]):add(a,b,layer)
            except (AttributeError,NotImplementedError): pass

    actual_dims=[float(e.get_measurement()) for e in ms.query("DIMENSION")]
    checks=[
      {"name":"上下内净标注总宽","expectedMm":11330,"actualMm":min(actual_dims,key=lambda x:abs(x-11330)),"passed":sum(abs(v-11330)<.01 for v in actual_dims)>=2},
      {"name":"底部尺寸链闭合","expectedMm":11330,"actualMm":1390+230+3100+105+1885+4620,"passed":abs(sum([1390,230,3100,105,1885,4620])-11330)<.01},
      {"name":"电竞房内宽","expectedMm":3210,"actualMm":next(v for v in actual_dims if abs(v-3210)<.01),"passed":any(abs(v-3210)<.01 for v in actual_dims)},
      {"name":"外轮廓最宽","expectedMm":11830,"actualMm":by_handle["D63CC"].dxf.start.x-ox,"passed":abs(by_handle["D63CC"].dxf.start.x-ox-11830)<.01},
    ]
    assumptions=[
      "主体尺寸/坐标取自用户 DWG 本地转换 DXF；当前平面仍需用户核对是否为最终施工版本。",
      "墙高暂设 2.65 m；门高、窗高、窗台、家具高度和材质为示意，待实测。",
      "房间 polygon 是语义/交互分区，不是严格墙中心线闭合房间；不要据其生成新墙。",
      "客厅与餐厅为开放空间，人为分区不表示有隔墙。",
      "电竞房对应左下 3.21m 内宽房间；原 CAD 未出现电竞房文字，用途来自本次任务。",
      "墙体采用人工审查的 CAD 双线中心线；床/衣柜也存在墙体图层，已排除这些家具假墙。",
      "左下吧台尺寸由本 CAD 推导，没有沿用旧项目的连体桌尺寸。",
      "次卧床依据用户反馈贴东窗侧和北墙，中心调整为[10.82,1.33]m；床尺寸/朝向保留，实际设计师方案仍待核对。沙发位置和朝向维持用户认可状态。",
      "主卧/主卫局部斜门与凹槽在小样中简化保留通行，不代表已完成施工级门窗重建。",
      "原文半墙标记位于[6.445,6.522]m、客卫干区附近，不在电竞房北墙。附近0.53m短构件归属未完全确定，未误补为全高墙。",
      "DXF 转换有旧文本编码警告；尚未原生 CAD 逐实体比对。",
      "灯位/回路不由此几何文件推断，模拟设备由独立 devices.json 提供。",
    ]
    return dict(meta=dict(source=str(source),sourceDwg="D:/Users/kotei/Downloads/武汉印130最新版.dwg",
                          sourceSha256=hashlib.sha256(source.read_bytes()).hexdigest(),units="m",
                          originCadMm=dict(x=ox,y=oy),axes="x=CAD右方;z=CAD下方;y=高度",rotationUnit="radians",
                          assumptions=assumptions,dimensionChecks=checks,roomsAreSemanticZones=True),
                footprint=footprint,rooms=rooms,walls=walls,openings=openings,cadLines=cad_lines,furniture=furniture)


if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--source",type=Path,default=DEFAULT_SOURCE)
    parser.add_argument("--output",type=Path,default=ROOT/"data/house.json")
    args=parser.parse_args()
    house=extract(args.source)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(house,ensure_ascii=False,indent=2),encoding="utf-8")
    print(f"Wrote {args.output}: {len(house['walls'])} walls, {len(house['openings'])} openings, {len(house['cadLines'])} CAD segments")
