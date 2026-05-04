import os
from pathlib import Path
from typing import Optional

import svgwrite
import yaml

from core import CHARACTER_DIR, CONTENT_DIR

CX, CY = 200, 180


def load_character_config(path: Optional[Path] = None) -> dict:
    if path is None:
        path = CONTENT_DIR / "character.yml"
    with open(path) as f:
        return yaml.safe_load(f)


def _front(dwg: svgwrite.Drawing, cfg: dict, expression: str = "smile") -> None:
    cx, cy = CX, CY
    SKIN = cfg["skin"]
    SKIN_SHADOW = cfg["skin_shadow"]
    SKIN_HIGHLIGHT = cfg["skin_highlight"]
    HAIR = cfg["hair"]
    HAIR_HIGHLIGHT = cfg["hair_highlight"]
    EYE_DARK = cfg["eye_dark"]
    EYE_WHITE = cfg["eye_white"]
    EYE_IRIS = cfg["eye_iris"]
    GLASSES_FRAME = cfg["glasses_frame"]
    LIP = cfg["lip"]
    LIP_LINE = cfg["lip_line"]
    SHIRT = cfg["shirt"]
    SHIRT_LIGHT = cfg["shirt_light"]
    COLLAR_TRIM = cfg["collar_trim"]
    BLUSH = cfg["blush"]

    hb = dwg.g(id="hair_back")
    hb.add(dwg.ellipse(center=(cx, cy - 5), r=(88, 88), fill=HAIR))
    hb.add(dwg.ellipse(center=(cx - 15, cy - 30), r=(50, 40), fill=HAIR_HIGHLIGHT, opacity="0.3"))
    for s in [-1, 1]:
        hb.add(dwg.ellipse(center=(cx + s * 58, cy + 30), r=(35, 65), fill=HAIR))
    dwg.add(hb)

    nk = dwg.g(id="neck")
    nk.add(dwg.rect(insert=(cx - 18, cy + 72), size=(36, 35), rx=8, fill=SKIN))
    nk.add(dwg.rect(insert=(cx - 18, cy + 72), size=(36, 12), rx=4, fill=SKIN_SHADOW, opacity="0.3"))
    dwg.add(nk)

    bd = dwg.g(id="body")
    bp = dwg.path(fill=SHIRT)
    bp.push(f"M {cx-95},{cy+200} Q {cx-98},{cy+140} {cx-58},{cy+105} L {cx-18},{cy+95} L {cx+18},{cy+95} L {cx+58},{cy+105} Q {cx+98},{cy+140} {cx+95},{cy+200} Z")
    bd.add(bp)
    hl = dwg.path(fill=SHIRT_LIGHT, opacity="0.5")
    hl.push(f"M {cx-40},{cy+105} Q {cx-35},{cy+130} {cx-20},{cy+200} L {cx+10},{cy+200} Q {cx},{cy+130} {cx-10},{cy+105} Z")
    bd.add(hl)
    dwg.add(bd)

    co = dwg.g(id="collar")
    for s in [-1, 1]:
        cp = dwg.path(fill=SHIRT_LIGHT, stroke=COLLAR_TRIM, stroke_width=1.5)
        cp.push(f"M {cx + s*18},{cy+95} L {cx + s*5},{cy+91} L {cx + s*2},{cy+115} L {cx + s*20},{cy+113} Z")
        co.add(cp)
    dwg.add(co)

    fc = dwg.g(id="face")
    fc.add(dwg.ellipse(center=(cx, cy + 5), r=(70, 73), fill=SKIN))
    fc.add(dwg.ellipse(center=(cx - 45, cy + 25), r=(20, 35), fill=SKIN_SHADOW, opacity="0.2"))
    fc.add(dwg.ellipse(center=(cx + 45, cy + 25), r=(20, 35), fill=SKIN_SHADOW, opacity="0.2"))
    fc.add(dwg.ellipse(center=(cx, cy - 15), r=(35, 20), fill=SKIN_HIGHLIGHT, opacity="0.3"))
    for s in [-1, 1]:
        fc.add(dwg.ellipse(center=(cx + s * 28, cy + 30), r=(12, 7), fill=BLUSH, opacity="0.2"))
    dwg.add(fc)

    ea = dwg.g(id="ears")
    for s in [-1, 1]:
        ea.add(dwg.ellipse(center=(cx + s * 63, cy + 12), r=(9, 14), fill=SKIN))
        ea.add(dwg.ellipse(center=(cx + s * 63, cy + 12), r=(5, 8), fill=SKIN_SHADOW, opacity="0.25"))
    dwg.add(ea)

    hf = dwg.g(id="hair_front")
    bangs = dwg.path(fill=HAIR)
    bangs.push(f"M {cx-82},{cy} Q {cx-70},{cy-50} {cx-20},{cy-65} Q {cx+5},{cy-48} {cx+15},{cy-60} Q {cx+50},{cy-70} {cx+70},{cy-45} Q {cx+85},{cy-15} {cx+82},{cy} Q {cx+72},{cy-22} {cx+45},{cy-32} Q {cx+15},{cy-28} {cx},{cy-22} Q {cx-25},{cy-28} {cx-50},{cy-32} Q {cx-72},{cy-22} {cx-82},{cy} Z")
    hf.add(bangs)
    bh = dwg.path(fill=HAIR_HIGHLIGHT, opacity="0.35")
    bh.push(f"M {cx-50},{cy-15} Q {cx-30},{cy-55} {cx},{cy-50} Q {cx+20},{cy-48} {cx+35},{cy-52} Q {cx+15},{cy-35} {cx},{cy-30} Q {cx-25},{cy-32} {cx-50},{cy-15} Z")
    hf.add(bh)
    for s in [-1, 1]:
        bottom_y = cy + 82 if s == -1 else cy + 70
        tip_y = bottom_y + 6
        inner_y = bottom_y - 2
        st = dwg.path(fill=HAIR)
        sx = cx + s * 82
        st.push(f"M {sx},{cy} Q {sx + s*6},{cy+35} {sx + s*3},{bottom_y} Q {sx + s*1},{tip_y} {sx - s*10},{inner_y} Q {sx - s*6},{cy+40} {sx - s*3},{cy+5} Z")
        hf.add(st)
    dwg.add(hf)

    eb = dwg.g(id="eyebrows")
    for dx in [-26, 26]:
        bx, by = cx + dx, cy - 18
        b = dwg.path(fill=HAIR)
        if expression == "thinking" and dx > 0:
            b.push(f"M {bx-14},{by+2} Q {bx},{by-3} {bx+14},{by+1} Q {bx},{by+1} {bx-14},{by+4} Z")
        else:
            b.push(f"M {bx-14},{by} Q {bx},{by-5} {bx+14},{by} Q {bx},{by-1} {bx-14},{by+3} Z")
        eb.add(b)
    dwg.add(eb)

    gl = dwg.g(id="glasses")
    for dx in [-26, 26]:
        gx, gy = cx + dx, cy - 5
        gl.add(dwg.ellipse(center=(gx, gy), r=(20, 14), fill="none", stroke=GLASSES_FRAME, stroke_width=2.5))
    br = dwg.path(fill="none", stroke=GLASSES_FRAME, stroke_width=1.8)
    br.push(f"M {cx-7},{cy-7} Q {cx},{cy-11} {cx+7},{cy-7}")
    gl.add(br)
    for s in [-1, 1]:
        t = dwg.path(fill="none", stroke=GLASSES_FRAME, stroke_width=1.8)
        t.push(f"M {cx + s*46},{cy-6} L {cx + s*60},{cy-2}")
        gl.add(t)
    dwg.add(gl)

    eg = dwg.g(id="eyes")
    for dx in [-26, 26]:
        ex, ey = cx + dx, cy - 5
        pd = 2 if expression == "thinking" else 0
        eg.add(dwg.ellipse(center=(ex, ey), r=(14, 11), fill=EYE_WHITE))
        eg.add(dwg.ellipse(center=(ex + pd, ey), r=(8, 9), fill=EYE_IRIS))
        eg.add(dwg.circle(center=(ex + pd, ey), r=4.5, fill=EYE_DARK))
        eg.add(dwg.circle(center=(ex - 2, ey - 3), r=2.5, fill="#FFF", opacity="0.85"))
        eg.add(dwg.circle(center=(ex + 3, ey + 1), r=1.1, fill="#FFF", opacity="0.4"))
    dwg.add(eg)

    ns = dwg.g(id="nose")
    n = dwg.path(fill="none", stroke=SKIN_SHADOW, stroke_width=1.2, stroke_linecap="round")
    n.push(f"M {cx-3},{cy+18} Q {cx},{cy+27} {cx+3},{cy+18}")
    ns.add(n)
    dwg.add(ns)

    mo = dwg.g(id="mouth")
    if expression == "smile":
        m = dwg.path(fill=LIP, stroke=LIP_LINE, stroke_width=0.7)
        m.push(f"M {cx-12},{cy+38} Q {cx},{cy+48} {cx+12},{cy+38} Q {cx},{cy+42} {cx-12},{cy+38} Z")
        mo.add(m)
    elif expression == "smile_bright":
        m = dwg.path(fill=LIP, stroke=LIP_LINE, stroke_width=0.7)
        m.push(f"M {cx-14},{cy+36} Q {cx},{cy+50} {cx+14},{cy+36} Q {cx},{cy+43} {cx-14},{cy+36} Z")
        mo.add(m)
    else:
        m = dwg.path(fill="none", stroke=LIP, stroke_width=1.6, stroke_linecap="round")
        m.push(f"M {cx-7},{cy+40} Q {cx},{cy+38} {cx+7},{cy+40}")
        mo.add(m)
    dwg.add(mo)


def _side(dwg: svgwrite.Drawing, cfg: dict, direction: str = "right", expression: str = "neutral") -> None:
    cx = 210 if direction == "right" else 190
    cy = CY
    f = 1 if direction == "right" else -1
    SKIN = cfg["skin"]
    SKIN_SHADOW = cfg["skin_shadow"]
    SKIN_HIGHLIGHT = cfg["skin_highlight"]
    HAIR = cfg["hair"]
    HAIR_HIGHLIGHT = cfg["hair_highlight"]
    EYE_DARK = cfg["eye_dark"]
    EYE_WHITE = cfg["eye_white"]
    EYE_IRIS = cfg["eye_iris"]
    GLASSES_FRAME = cfg["glasses_frame"]
    LIP = cfg["lip"]
    SHIRT = cfg["shirt"]
    SHIRT_LIGHT = cfg["shirt_light"]
    COLLAR_TRIM = cfg["collar_trim"]
    BLUSH = cfg["blush"]

    hb = dwg.g(id="hair_back")
    hb.add(dwg.ellipse(center=(cx - f * 5, cy - 5), r=(82, 85), fill=HAIR))
    hb.add(dwg.ellipse(center=(cx - f * 15, cy - 30), r=(40, 35), fill=HAIR_HIGHLIGHT, opacity="0.25"))
    hb.add(dwg.ellipse(center=(cx - f * 42, cy + 30), r=(32, 60), fill=HAIR))
    dwg.add(hb)

    nk = dwg.g(id="neck")
    nk.add(dwg.rect(insert=(cx - 14, cy + 72), size=(28, 35), rx=6, fill=SKIN))
    dwg.add(nk)

    bd = dwg.g(id="body")
    bp = dwg.path(fill=SHIRT)
    bp.push(f"M {cx-85},{cy+195} Q {cx-88},{cy+135} {cx-50},{cy+105} L {cx-14},{cy+95} L {cx+14},{cy+95} L {cx+50},{cy+105} Q {cx+88},{cy+135} {cx+85},{cy+195} Z")
    bd.add(bp)
    hl = dwg.path(fill=SHIRT_LIGHT, opacity="0.4")
    hl.push(f"M {cx-30},{cy+108} Q {cx-25},{cy+135} {cx-15},{cy+195} L {cx+5},{cy+195} Q {cx-5},{cy+135} {cx-10},{cy+108} Z")
    bd.add(hl)
    dwg.add(bd)

    co = dwg.g(id="collar")
    for s in [-1, 1]:
        cp = dwg.path(fill=SHIRT_LIGHT, stroke=COLLAR_TRIM, stroke_width=1.5)
        cp.push(f"M {cx + s*14},{cy+95} L {cx + s*4},{cy+91} L {cx + s*2},{cy+113} L {cx + s*16},{cy+111} Z")
        co.add(cp)
    dwg.add(co)

    fc = dwg.g(id="face")
    fc.add(dwg.ellipse(center=(cx + f * 8, cy + 8), r=(60, 74), fill=SKIN))
    fc.add(dwg.ellipse(center=(cx + f * 30, cy + 5), r=(25, 30), fill=SKIN_HIGHLIGHT, opacity="0.25"))
    fc.add(dwg.ellipse(center=(cx + f * 32, cy + 30), r=(10, 7), fill=BLUSH, opacity="0.2"))
    dwg.add(fc)

    ea = dwg.g(id="ears")
    ea.add(dwg.ellipse(center=(cx - f * 50, cy + 10), r=(8, 13), fill=SKIN))
    dwg.add(ea)

    hf = dwg.g(id="hair_front")
    b = dwg.path(fill=HAIR)
    b.push(f"M {cx - f*75},{cy} Q {cx - f*50},{cy-50} {cx + f*15},{cy-62} Q {cx + f*50},{cy-65} {cx + f*72},{cy-38} Q {cx + f*60},{cy-28} {cx + f*25},{cy-28} Q {cx},{cy-22} {cx - f*35},{cy-25} Q {cx - f*60},{cy-18} {cx - f*75},{cy} Z")
    hf.add(b)
    bhl = dwg.path(fill=HAIR_HIGHLIGHT, opacity="0.3")
    bhl.push(f"M {cx - f*40},{cy-10} Q {cx - f*20},{cy-45} {cx + f*10},{cy-50} Q {cx + f*5},{cy-35} {cx - f*10},{cy-28} Q {cx - f*30},{cy-20} {cx - f*40},{cy-10} Z")
    hf.add(bhl)
    st = dwg.path(fill=HAIR)
    sx = cx - f * 75
    st.push(f"M {sx},{cy} Q {sx - f*5},{cy+35} {sx - f*3},{cy+68} Q {sx - f*1},{cy+75} {sx + f*10},{cy+70} Q {sx + f*5},{cy+38} {sx + f*2},{cy+5} Z")
    hf.add(st)
    dwg.add(hf)

    ex_p = cx + f * 16
    ey_p = cy - 5

    eb = dwg.g(id="eyebrows")
    bw = dwg.path(fill=HAIR)
    bw.push(f"M {ex_p-12},{ey_p-14} Q {ex_p},{ey_p-19} {ex_p+12},{ey_p-14} Q {ex_p},{ey_p-15} {ex_p-12},{ey_p-11} Z")
    eb.add(bw)
    dwg.add(eb)

    gl = dwg.g(id="glasses")
    gl.add(dwg.ellipse(center=(ex_p, ey_p), r=(17, 13), fill="none", stroke=GLASSES_FRAME, stroke_width=2.5))
    t = dwg.path(fill="none", stroke=GLASSES_FRAME, stroke_width=1.8)
    t.push(f"M {ex_p - f*17},{ey_p} L {ex_p - f*38},{ey_p+3}")
    gl.add(t)
    dwg.add(gl)

    eg = dwg.g(id="eyes")
    eg.add(dwg.ellipse(center=(ex_p, ey_p), r=(12, 10), fill=EYE_WHITE))
    eg.add(dwg.ellipse(center=(ex_p + f * 2, ey_p), r=(7, 8), fill=EYE_IRIS))
    eg.add(dwg.circle(center=(ex_p + f * 2, ey_p), r=4, fill=EYE_DARK))
    eg.add(dwg.circle(center=(ex_p - 1, ey_p - 2.5), r=2, fill="#FFF", opacity="0.85"))
    dwg.add(eg)

    ns = dwg.g(id="nose")
    np_ = dwg.path(fill="none", stroke=SKIN_SHADOW, stroke_width=1.1, stroke_linecap="round")
    np_.push(f"M {cx + f*20},{cy+16} Q {cx + f*26},{cy+24} {cx + f*22},{cy+28}")
    ns.add(np_)
    dwg.add(ns)

    mo = dwg.g(id="mouth")
    mp = dwg.path(fill="none", stroke=LIP, stroke_width=1.6, stroke_linecap="round")
    mp.push(f"M {cx + f*6},{cy+42} Q {cx + f*16},{cy+47} {cx + f*22},{cy+42}")
    mo.add(mp)
    dwg.add(mo)


def generate_all_poses(config_path: Optional[Path] = None, output_dir: Optional[Path] = None) -> None:
    if output_dir is None:
        output_dir = CHARACTER_DIR
    output_dir.mkdir(parents=True, exist_ok=True)
    cfg = load_character_config(config_path)

    poses = [
        ("fu_yao_front.svg", "front", "smile", "right"),
        ("fu_yao_thinking.svg", "front", "thinking", "right"),
        ("fu_yao_confident.svg", "front", "smile_bright", "right"),
        ("fu_yao_side_right.svg", "side", "neutral", "right"),
        ("fu_yao_side_left.svg", "side", "neutral", "left"),
    ]
    for filename, pose, expression, direction in poses:
        dwg = svgwrite.Drawing(str(output_dir / filename), size=("400px", "500px"), viewBox="0 0 400 500")
        if pose == "front":
            _front(dwg, cfg, expression)
        else:
            _side(dwg, cfg, direction, expression)
        dwg.save()
        print(f"  {filename}")

    print("Done.")
