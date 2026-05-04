import svgwrite
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

SKIN = "#FCDEC0"
SKIN_SHADOW = "#EABC98"
SKIN_HIGHLIGHT = "#FFF0E0"
HAIR = "#1C1C1C"
HAIR_HIGHLIGHT = "#3A3A3A"
HAIR_EDGE = "#4A4A4A"
EYE_DARK = "#1A0E00"
EYE_WHITE = "#FFFFFF"
EYE_IRIS = "#3D2B10"
GLASSES_FRAME = "#C09898"
GLASSES_LENS = "#E8E0E0"  # unused — lens fill removed for eye visibility
LIP = "#D4908A"
LIP_LINE = "#C07878"
SHIRT = "#A8D0E0"
SHIRT_LIGHT = "#C0DEE8"
SHIRT_DARK = "#88B8CC"
COLLAR_TRIM = "#4A6A6A"
BLUSH = "#F0B0A0"

CX, CY = 200, 180


def _front(dwg, expression="smile"):
    cx, cy = CX, CY

    # === hair_back ===
    hb = dwg.g(id="hair_back")
    hb.add(dwg.ellipse(center=(cx, cy - 5), r=(88, 88), fill=HAIR))
    hb.add(dwg.ellipse(center=(cx - 15, cy - 30), r=(50, 40),
                        fill=HAIR_HIGHLIGHT, opacity="0.3"))
    for s in [-1, 1]:
        hb.add(dwg.ellipse(center=(cx + s * 58, cy + 30), r=(35, 65), fill=HAIR))
    dwg.add(hb)

    # === neck ===
    nk = dwg.g(id="neck")
    nk.add(dwg.rect(insert=(cx - 18, cy + 72), size=(36, 35), rx=8, fill=SKIN))
    nk.add(dwg.rect(insert=(cx - 18, cy + 72), size=(36, 12), rx=4,
                      fill=SKIN_SHADOW, opacity="0.3"))
    dwg.add(nk)

    # === body ===
    bd = dwg.g(id="body")
    bp = dwg.path(fill=SHIRT)
    bp.push(f"M {cx-95},{cy+200}")
    bp.push(f"Q {cx-98},{cy+140} {cx-58},{cy+105}")
    bp.push(f"L {cx-18},{cy+95}")
    bp.push(f"L {cx+18},{cy+95}")
    bp.push(f"L {cx+58},{cy+105}")
    bp.push(f"Q {cx+98},{cy+140} {cx+95},{cy+200}")
    bp.push("Z")
    bd.add(bp)
    # shirt highlight
    hl = dwg.path(fill=SHIRT_LIGHT, opacity="0.5")
    hl.push(f"M {cx-40},{cy+105}")
    hl.push(f"Q {cx-35},{cy+130} {cx-20},{cy+200}")
    hl.push(f"L {cx+10},{cy+200}")
    hl.push(f"Q {cx},{cy+130} {cx-10},{cy+105}")
    hl.push("Z")
    bd.add(hl)
    dwg.add(bd)

    # === collar ===
    co = dwg.g(id="collar")
    for s in [-1, 1]:
        cp = dwg.path(fill=SHIRT_LIGHT, stroke=COLLAR_TRIM, stroke_width=1.5)
        cp.push(f"M {cx + s*18},{cy+95}")
        cp.push(f"L {cx + s*5},{cy+91}")
        cp.push(f"L {cx + s*2},{cy+115}")
        cp.push(f"L {cx + s*20},{cy+113}")
        cp.push("Z")
        co.add(cp)
    dwg.add(co)

    # === face ===
    fc = dwg.g(id="face")
    fc.add(dwg.ellipse(center=(cx, cy + 5), r=(70, 73), fill=SKIN))
    # cheek shadow
    fc.add(dwg.ellipse(center=(cx - 45, cy + 25), r=(20, 35),
                        fill=SKIN_SHADOW, opacity="0.2"))
    fc.add(dwg.ellipse(center=(cx + 45, cy + 25), r=(20, 35),
                        fill=SKIN_SHADOW, opacity="0.2"))
    # forehead highlight
    fc.add(dwg.ellipse(center=(cx, cy - 15), r=(35, 20),
                        fill=SKIN_HIGHLIGHT, opacity="0.3"))
    # blush
    for s in [-1, 1]:
        fc.add(dwg.ellipse(center=(cx + s * 28, cy + 30), r=(12, 7),
                            fill=BLUSH, opacity="0.2"))
    dwg.add(fc)

    # === ears ===
    ea = dwg.g(id="ears")
    for s in [-1, 1]:
        ea.add(dwg.ellipse(center=(cx + s * 63, cy + 12), r=(9, 14), fill=SKIN))
        ea.add(dwg.ellipse(center=(cx + s * 63, cy + 12), r=(5, 8),
                            fill=SKIN_SHADOW, opacity="0.25"))
    dwg.add(ea)

    # === hair_front (bangs + bob sides) ===
    hf = dwg.g(id="hair_front")
    bangs = dwg.path(fill=HAIR)
    bangs.push(f"M {cx-82},{cy}")
    bangs.push(f"Q {cx-70},{cy-50} {cx-20},{cy-65}")
    bangs.push(f"Q {cx+5},{cy-48} {cx+15},{cy-60}")
    bangs.push(f"Q {cx+50},{cy-70} {cx+70},{cy-45}")
    bangs.push(f"Q {cx+85},{cy-15} {cx+82},{cy}")
    bangs.push(f"Q {cx+72},{cy-22} {cx+45},{cy-32}")
    bangs.push(f"Q {cx+15},{cy-28} {cx},{cy-22}")
    bangs.push(f"Q {cx-25},{cy-28} {cx-50},{cy-32}")
    bangs.push(f"Q {cx-72},{cy-22} {cx-82},{cy}")
    bangs.push("Z")
    hf.add(bangs)
    # bangs highlight
    bh = dwg.path(fill=HAIR_HIGHLIGHT, opacity="0.35")
    bh.push(f"M {cx-50},{cy-15}")
    bh.push(f"Q {cx-30},{cy-55} {cx},{cy-50}")
    bh.push(f"Q {cx+20},{cy-48} {cx+35},{cy-52}")
    bh.push(f"Q {cx+15},{cy-35} {cx},{cy-30}")
    bh.push(f"Q {cx-25},{cy-32} {cx-50},{cy-15}")
    bh.push("Z")
    hf.add(bh)
    # bob side strands (left side longer for asymmetric cut)
    for s in [-1, 1]:
        bottom_y = cy + 82 if s == -1 else cy + 70
        tip_y = bottom_y + 6
        inner_y = bottom_y - 2
        st = dwg.path(fill=HAIR)
        sx = cx + s * 82
        st.push(f"M {sx},{cy}")
        st.push(f"Q {sx + s*6},{cy+35} {sx + s*3},{bottom_y}")
        st.push(f"Q {sx + s*1},{tip_y} {sx - s*10},{inner_y}")
        st.push(f"Q {sx - s*6},{cy+40} {sx - s*3},{cy+5}")
        st.push("Z")
        hf.add(st)
    dwg.add(hf)

    # === eyebrows ===
    eb = dwg.g(id="eyebrows")
    for dx in [-26, 26]:
        bx, by = cx + dx, cy - 18
        b = dwg.path(fill=HAIR)
        if expression == "thinking" and dx > 0:
            b.push(f"M {bx-14},{by+2}")
            b.push(f"Q {bx},{by-3} {bx+14},{by+1}")
            b.push(f"Q {bx},{by+1} {bx-14},{by+4}")
        else:
            b.push(f"M {bx-14},{by}")
            b.push(f"Q {bx},{by-5} {bx+14},{by}")
            b.push(f"Q {bx},{by-1} {bx-14},{by+3}")
        b.push("Z")
        eb.add(b)
    dwg.add(eb)

    # === glasses (before eyes so eyes paint on top) ===
    gl = dwg.g(id="glasses")
    for dx in [-26, 26]:
        gx, gy = cx + dx, cy - 5
        gl.add(dwg.ellipse(center=(gx, gy), r=(20, 14),
                            fill="none",
                            stroke=GLASSES_FRAME, stroke_width=2.5))
    br = dwg.path(fill="none", stroke=GLASSES_FRAME, stroke_width=1.8)
    br.push(f"M {cx-7},{cy-7}")
    br.push(f"Q {cx},{cy-11} {cx+7},{cy-7}")
    gl.add(br)
    for s in [-1, 1]:
        t = dwg.path(fill="none", stroke=GLASSES_FRAME, stroke_width=1.8)
        t.push(f"M {cx + s*46},{cy-6}")
        t.push(f"L {cx + s*60},{cy-2}")
        gl.add(t)
    dwg.add(gl)

    # === eyes ===
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

    # === nose ===
    ns = dwg.g(id="nose")
    n = dwg.path(fill="none", stroke=SKIN_SHADOW, stroke_width=1.2, stroke_linecap="round")
    n.push(f"M {cx-3},{cy+18}")
    n.push(f"Q {cx},{cy+27} {cx+3},{cy+18}")
    ns.add(n)
    dwg.add(ns)

    # === mouth ===
    mo = dwg.g(id="mouth")
    if expression == "smile":
        m = dwg.path(fill=LIP, stroke=LIP_LINE, stroke_width=0.7)
        m.push(f"M {cx-12},{cy+38}")
        m.push(f"Q {cx},{cy+48} {cx+12},{cy+38}")
        m.push(f"Q {cx},{cy+42} {cx-12},{cy+38}")
        mo.add(m)
    elif expression == "smile_bright":
        m = dwg.path(fill=LIP, stroke=LIP_LINE, stroke_width=0.7)
        m.push(f"M {cx-14},{cy+36}")
        m.push(f"Q {cx},{cy+50} {cx+14},{cy+36}")
        m.push(f"Q {cx},{cy+43} {cx-14},{cy+36}")
        mo.add(m)
    else:
        m = dwg.path(fill="none", stroke=LIP, stroke_width=1.6, stroke_linecap="round")
        m.push(f"M {cx-7},{cy+40}")
        m.push(f"Q {cx},{cy+38} {cx+7},{cy+40}")
        mo.add(m)
    dwg.add(mo)


def _side(dwg, direction="right", expression="neutral"):
    cx = 210 if direction == "right" else 190
    cy = CY
    f = 1 if direction == "right" else -1

    hb = dwg.g(id="hair_back")
    hb.add(dwg.ellipse(center=(cx - f * 5, cy - 5), r=(82, 85), fill=HAIR))
    hb.add(dwg.ellipse(center=(cx - f * 15, cy - 30), r=(40, 35),
                        fill=HAIR_HIGHLIGHT, opacity="0.25"))
    hb.add(dwg.ellipse(center=(cx - f * 42, cy + 30), r=(32, 60), fill=HAIR))
    dwg.add(hb)

    nk = dwg.g(id="neck")
    nk.add(dwg.rect(insert=(cx - 14, cy + 72), size=(28, 35), rx=6, fill=SKIN))
    dwg.add(nk)

    bd = dwg.g(id="body")
    bp = dwg.path(fill=SHIRT)
    bp.push(f"M {cx-85},{cy+195}")
    bp.push(f"Q {cx-88},{cy+135} {cx-50},{cy+105}")
    bp.push(f"L {cx-14},{cy+95}")
    bp.push(f"L {cx+14},{cy+95}")
    bp.push(f"L {cx+50},{cy+105}")
    bp.push(f"Q {cx+88},{cy+135} {cx+85},{cy+195}")
    bp.push("Z")
    bd.add(bp)
    hl = dwg.path(fill=SHIRT_LIGHT, opacity="0.4")
    hl.push(f"M {cx-30},{cy+108}")
    hl.push(f"Q {cx-25},{cy+135} {cx-15},{cy+195}")
    hl.push(f"L {cx+5},{cy+195}")
    hl.push(f"Q {cx-5},{cy+135} {cx-10},{cy+108}")
    hl.push("Z")
    bd.add(hl)
    dwg.add(bd)

    co = dwg.g(id="collar")
    for s in [-1, 1]:
        cp = dwg.path(fill=SHIRT_LIGHT, stroke=COLLAR_TRIM, stroke_width=1.5)
        cp.push(f"M {cx + s*14},{cy+95}")
        cp.push(f"L {cx + s*4},{cy+91}")
        cp.push(f"L {cx + s*2},{cy+113}")
        cp.push(f"L {cx + s*16},{cy+111}")
        cp.push("Z")
        co.add(cp)
    dwg.add(co)

    fc = dwg.g(id="face")
    fc.add(dwg.ellipse(center=(cx + f * 8, cy + 8), r=(60, 74), fill=SKIN))
    fc.add(dwg.ellipse(center=(cx + f * 30, cy + 5), r=(25, 30),
                        fill=SKIN_HIGHLIGHT, opacity="0.25"))
    fc.add(dwg.ellipse(center=(cx + f * 32, cy + 30), r=(10, 7),
                        fill=BLUSH, opacity="0.2"))
    dwg.add(fc)

    ea = dwg.g(id="ears")
    ea.add(dwg.ellipse(center=(cx - f * 50, cy + 10), r=(8, 13), fill=SKIN))
    dwg.add(ea)

    hf = dwg.g(id="hair_front")
    b = dwg.path(fill=HAIR)
    b.push(f"M {cx - f*75},{cy}")
    b.push(f"Q {cx - f*50},{cy-50} {cx + f*15},{cy-62}")
    b.push(f"Q {cx + f*50},{cy-65} {cx + f*72},{cy-38}")
    b.push(f"Q {cx + f*60},{cy-28} {cx + f*25},{cy-28}")
    b.push(f"Q {cx},{cy-22} {cx - f*35},{cy-25}")
    b.push(f"Q {cx - f*60},{cy-18} {cx - f*75},{cy}")
    b.push("Z")
    hf.add(b)
    bhl = dwg.path(fill=HAIR_HIGHLIGHT, opacity="0.3")
    bhl.push(f"M {cx - f*40},{cy-10}")
    bhl.push(f"Q {cx - f*20},{cy-45} {cx + f*10},{cy-50}")
    bhl.push(f"Q {cx + f*5},{cy-35} {cx - f*10},{cy-28}")
    bhl.push(f"Q {cx - f*30},{cy-20} {cx - f*40},{cy-10}")
    bhl.push("Z")
    hf.add(bhl)
    st = dwg.path(fill=HAIR)
    sx = cx - f * 75
    st.push(f"M {sx},{cy}")
    st.push(f"Q {sx - f*5},{cy+35} {sx - f*3},{cy+68}")
    st.push(f"Q {sx - f*1},{cy+75} {sx + f*10},{cy+70}")
    st.push(f"Q {sx + f*5},{cy+38} {sx + f*2},{cy+5}")
    st.push("Z")
    hf.add(st)
    dwg.add(hf)

    ex_p = cx + f * 16
    ey_p = cy - 5

    eb = dwg.g(id="eyebrows")
    bw = dwg.path(fill=HAIR)
    bw.push(f"M {ex_p-12},{ey_p-14}")
    bw.push(f"Q {ex_p},{ey_p-19} {ex_p+12},{ey_p-14}")
    bw.push(f"Q {ex_p},{ey_p-15} {ex_p-12},{ey_p-11}")
    bw.push("Z")
    eb.add(bw)
    dwg.add(eb)

    # glasses before eyes (so eyes paint on top)
    gl = dwg.g(id="glasses")
    gl.add(dwg.ellipse(center=(ex_p, ey_p), r=(17, 13),
                        fill="none",
                        stroke=GLASSES_FRAME, stroke_width=2.5))
    t = dwg.path(fill="none", stroke=GLASSES_FRAME, stroke_width=1.8)
    t.push(f"M {ex_p - f*17},{ey_p}")
    t.push(f"L {ex_p - f*38},{ey_p+3}")
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
    np_.push(f"M {cx + f*20},{cy+16}")
    np_.push(f"Q {cx + f*26},{cy+24} {cx + f*22},{cy+28}")
    ns.add(np_)
    dwg.add(ns)

    mo = dwg.g(id="mouth")
    mp = dwg.path(fill="none", stroke=LIP, stroke_width=1.6, stroke_linecap="round")
    mp.push(f"M {cx + f*6},{cy+42}")
    mp.push(f"Q {cx + f*16},{cy+47} {cx + f*22},{cy+42}")
    mo.add(mp)
    dwg.add(mo)


def generate(filename, pose="front", expression="smile", direction="right"):
    dwg = svgwrite.Drawing(os.path.join(OUTPUT_DIR, filename),
                            size=("400px", "500px"), viewBox="0 0 400 500")
    if pose == "front":
        _front(dwg, expression)
    else:
        _side(dwg, direction, expression)
    dwg.save()
    print(f"  {filename}")


if __name__ == "__main__":
    generate("fu_yao_front.svg", "front", "smile")
    generate("fu_yao_thinking.svg", "front", "thinking")
    generate("fu_yao_confident.svg", "front", "smile_bright")
    generate("fu_yao_side_right.svg", "side", direction="right")
    generate("fu_yao_side_left.svg", "side", direction="left")
    print("Done.")
