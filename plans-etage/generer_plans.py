#!/usr/bin/env python3
"""Génère les plans de l'étage (70 m², 8,37 x 8,37 m) :
  - plan_cote.svg        : plan d'architecte coté (R+1 projet)
  - plan_amenagement.svg : plan global meublé

Repère : origine = angle intérieur Sud-Ouest, x vers l'Est, y vers le Nord,
unités en mètres. Murs extérieurs 20 cm, cloisons 7 cm.
"""

# ---------------------------------------------------------------- géométrie
EXT = 0.20          # épaisseur murs extérieurs
IN = 7.97           # dimension intérieure (8,37 - 2 x 0,20)
S = 1400 / 420 * 25  # px par mètre -> échelle 1/40 sur un A3 paysage
OX, OY = 150 + EXT * S, 140 + (IN + EXT) * S  # px de l'origine intérieure
W, H = 1400, 990

def P(x, y):
    return OX + x * S, OY - y * S

# Cloisons (x0, y0, x1, y1)
CLOISONS = [
    (0.90, 0.00, 0.97, 3.65),   # mur escalier / chambre 3
    (0.90, 3.65, 7.97, 3.72),   # dégagement côté Sud
    (0.00, 4.62, 7.97, 4.69),   # dégagement côté Nord
    (6.45, 3.72, 6.52, 4.62),   # WC
    (3.95, 4.69, 4.02, 7.97),   # ch1 / ch2
    (4.44, 0.00, 4.51, 3.65),   # ch3 / ch4
    (1.60, 4.69, 1.67, 6.56), (0.00, 6.49, 1.67, 6.56),   # SdE 1
    (6.30, 4.69, 6.37, 6.56), (6.30, 6.49, 7.97, 6.56),   # SdE 2
    (2.57, 1.78, 2.64, 3.65), (0.97, 1.78, 2.64, 1.85),   # SdE 3
    (6.30, 1.78, 6.37, 3.65), (6.30, 1.78, 7.97, 1.85),   # SdE 4
]

# Portes : (hinge x, hinge y, u, n, largeur, rect d'ouverture dans le mur)
PORTES = [
    ((1.82, 4.69), (1, 0), (0, 1), 0.80, (1.82, 4.62, 2.62, 4.69)),   # Ch1
    ((6.20, 4.69), (-1, 0), (0, 1), 0.80, (5.40, 4.62, 6.20, 4.69)),  # Ch2
    ((2.79, 3.65), (1, 0), (0, -1), 0.80, (2.79, 3.65, 3.59, 3.72)),  # Ch3
    ((6.20, 3.65), (-1, 0), (0, -1), 0.80, (5.40, 3.65, 6.20, 3.72)), # Ch4
    ((6.52, 3.82), (0, 1), (1, 0), 0.70, (6.45, 3.82, 6.52, 4.52)),   # WC
    ((1.60, 6.35), (0, -1), (-1, 0), 0.70, (1.60, 5.65, 1.67, 6.35)), # SdE1
    ((6.37, 6.35), (0, -1), (1, 0), 0.70, (6.30, 5.65, 6.37, 6.35)),  # SdE2
    ((2.57, 1.95), (0, 1), (-1, 0), 0.70, (2.57, 1.95, 2.64, 2.65)),  # SdE3
    ((6.37, 1.95), (0, 1), (1, 0), 0.70, (6.30, 1.95, 6.37, 2.65)),   # SdE4
]

# Fenêtres : (façade, début, fin)
FENETRES = [
    ("N", 0.70, 1.90), ("N", 6.07, 7.27),
    ("S", 1.10, 2.30), ("S", 6.55, 7.75),
    ("W", 4.80, 5.30), ("W", 1.20, 2.20),
    ("E", 4.80, 5.30), ("E", 3.92, 4.42), ("E", 3.08, 3.58),
]

PIECES = {  # nom: (polygone, surface, label_cote, label_amenagement, dims)
    "CHAMBRE 1": ([(0, 6.56), (1.67, 6.56), (1.67, 4.69), (3.95, 4.69), (3.95, 7.97), (0, 7.97)],
                  9.8, (2.05, 7.20), (2.85, 5.62), "3,95 × 3,28"),
    "CHAMBRE 2": ([(4.02, 4.69), (6.30, 4.69), (6.30, 6.56), (7.97, 6.56), (7.97, 7.97), (4.02, 7.97)],
                  9.8, (5.92, 7.20), (5.12, 5.62), "3,95 × 3,28"),
    "CHAMBRE 3": ([(0.97, 0), (4.44, 0), (4.44, 3.65), (2.64, 3.65), (2.64, 1.78), (0.97, 1.78)],
                  9.5, (2.70, 0.95), (2.05, 1.50), "3,47 × 3,65"),
    "CHAMBRE 4": ([(4.51, 0), (7.97, 0), (7.97, 1.78), (6.30, 1.78), (6.30, 3.65), (4.51, 3.65)],
                  9.5, (6.24, 0.95), (6.90, 1.50), "3,46 × 3,65"),
    "SdE 1": ([(0, 4.69), (1.60, 4.69), (1.60, 6.49), (0, 6.49)], 2.9, (0.80, 5.75), None, "1,60 × 1,80"),
    "SdE 2": ([(6.37, 4.69), (7.97, 4.69), (7.97, 6.49), (6.37, 6.49)], 2.9, (7.17, 5.75), None, "1,60 × 1,80"),
    "SdE 3": ([(0.97, 1.85), (2.57, 1.85), (2.57, 3.65), (0.97, 3.65)], 2.9, (1.77, 2.75), None, "1,60 × 1,80"),
    "SdE 4": ([(6.37, 1.85), (7.97, 1.85), (7.97, 3.65), (6.37, 3.65)], 2.9, (7.17, 2.75), None, "1,60 × 1,80"),
    "WC": ([(6.52, 3.72), (7.97, 3.72), (7.97, 4.62), (6.52, 4.62)], 1.3, (7.55, 4.40), None, "1,45 × 0,90"),
    "DÉGAGEMENT": ([(0, 3.50), (0.90, 3.50), (0.90, 3.72), (6.45, 3.72), (6.45, 4.62), (0, 4.62)],
                   6.0, (2.60, 4.17), None, ""),
}

ESCALIER = (0.0, 0.0, 0.90, 3.50)   # emmarchement 0,90, 14 girons de 0,25

FONT = "Liberation Sans, Helvetica, Arial, sans-serif"


def fmt(v):
    return f"{v:.2f}".replace(".", ",")


def poly(pts, style):
    d = " ".join(f"{P(x, y)[0]:.1f},{P(x, y)[1]:.1f}" for x, y in pts)
    return f'<polygon points="{d}" {style}/>'


def rect(x0, y0, x1, y1, style):
    ax, ay = P(min(x0, x1), max(y0, y1))
    return (f'<rect x="{ax:.1f}" y="{ay:.1f}" width="{abs(x1 - x0) * S:.1f}" '
            f'height="{abs(y1 - y0) * S:.1f}" {style}/>')


def line(x0, y0, x1, y1, style):
    a, b = P(x0, y0), P(x1, y1)
    return f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" {style}/>'


def text(x, y, s, size=12, weight="normal", anchor="middle", fill="#111", extra=""):
    px, py = P(x, y)
    return (f'<text x="{px:.1f}" y="{py:.1f}" font-family="{FONT}" font-size="{size}" '
            f'font-weight="{weight}" text-anchor="{anchor}" fill="{fill}" {extra}>{s}</text>')


def circle(x, y, r, style):
    px, py = P(x, y)
    return f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r * S:.1f}" {style}/>'


# ---------------------------------------------------------------- murs
def murs(mode):
    out = []
    ox0, oy0 = P(-EXT, IN + EXT)
    ix0, iy0 = P(0, IN)
    ext_fill = 'url(#hachure)' if mode == "cote" else "#2f2f2f"
    out.append(
        f'<path fill-rule="evenodd" fill="{ext_fill}" stroke="#000" stroke-width="1.6" d="'
        f'M{ox0:.1f},{oy0:.1f} h{(IN + 2 * EXT) * S:.1f} v{(IN + 2 * EXT) * S:.1f} h{-(IN + 2 * EXT) * S:.1f} Z '
        f'M{ix0:.1f},{iy0:.1f} h{IN * S:.1f} v{IN * S:.1f} h{-IN * S:.1f} Z"/>')
    cl_fill = "#555" if mode == "cote" else "#4a4a4a"
    for c in CLOISONS:
        out.append(rect(*c, f'fill="{cl_fill}" stroke="none"'))
    return out


def fond_ouverture(mode):
    return "#ffffff" if mode == "cote" else None


def portes(mode, sol):
    out = []
    for (hx, hy), u, n, w, cut in PORTES:
        x0, y0, x1, y1 = cut
        # couleur du sol à l'emplacement de la porte
        fill = "#ffffff" if mode == "cote" else sol.get(cut, "#efe6d8")
        out.append(rect(x0, y0, x1, y1, f'fill="{fill}" stroke="none"'))
        a = P(hx + u[0] * w, hy + u[1] * w)
        b = P(hx + n[0] * w, hy + n[1] * w)
        h = P(hx, hy)
        cross = (a[0] - h[0]) * (b[1] - h[1]) - (a[1] - h[1]) * (b[0] - h[0])
        sweep = 1 if cross > 0 else 0
        out.append(f'<path d="M{a[0]:.1f},{a[1]:.1f} A{w * S:.1f},{w * S:.1f} 0 0 {sweep} {b[0]:.1f},{b[1]:.1f}" '
                   f'fill="none" stroke="#333" stroke-width="0.8" stroke-dasharray="4 3"/>')
        out.append(f'<line x1="{h[0]:.1f}" y1="{h[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="#111" stroke-width="2"/>')
        if mode == "cote":
            mx, my = (x0 + x1) / 2, (y0 + y1) / 2
            if x1 - x0 > y1 - y0:   # mur horizontal : texte côté dégagement
                ty = my + (0.17 if n[1] < 0 else -0.13) * (1 if n[1] < 0 else 1)
                ty = 4.45 if n[1] > 0 else 3.84
                out.append(text(mx, ty, f"P {fmt(w)}", 9, fill="#444"))
            else:
                tx = mx + (-n[0]) * 0.20
                out.append(text(tx, my - 0.03, fmt(w), 9, fill="#444",
                                extra=f'transform="rotate(-90 {P(tx, my - 0.03)[0]:.1f} {P(tx, my - 0.03)[1]:.1f})"'))
    return out


def fenetres(mode):
    out = []
    for side, a, b in FENETRES:
        if side in "NS":
            y0, y1 = (IN, IN + EXT) if side == "N" else (-EXT, 0)
            out.append(rect(a, y0, b, y1, 'fill="#fff" stroke="#000" stroke-width="1"'))
            for yy in (y0 + EXT * 0.38, y0 + EXT * 0.62):
                out.append(line(a, yy, b, yy, 'stroke="#000" stroke-width="0.8"'))
        else:
            x0, x1 = (IN, IN + EXT) if side == "E" else (-EXT, 0)
            out.append(rect(x0, a, x1, b, 'fill="#fff" stroke="#000" stroke-width="1"'))
            for xx in (x0 + EXT * 0.38, x0 + EXT * 0.62):
                out.append(line(xx, a, xx, b, 'stroke="#000" stroke-width="0.8"'))
    return out


def escalier(mode):
    x0, y0, x1, y1 = ESCALIER
    out = []
    fill = "#ffffff" if mode == "cote" else "#d8b48a"
    out.append(rect(x0, y0, x1, y1, f'fill="{fill}" stroke="#111" stroke-width="1"'))
    n = 14
    g = (y1 - y0) / n
    for i in range(1, n):
        out.append(line(x0, y0 + i * g, x1, y0 + i * g, 'stroke="#111" stroke-width="0.8"'))
    for i in range(n):
        out.append(text(x1 - 0.08, y0 + i * g + 0.07, str(i + 1), 7, anchor="end", fill="#666"))
    # ligne de foulée + flèche de montée
    xm = (x0 + x1) / 2 - 0.08
    a, b = P(xm, y0 + 0.15), P(xm, y1 + 0.05)
    out.append(f'<circle cx="{a[0]:.1f}" cy="{a[1]:.1f}" r="3.5" fill="#111"/>')
    out.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1] + 10:.1f}" stroke="#111" stroke-width="1.4"/>')
    out.append(f'<path d="M{b[0]:.1f},{b[1]:.1f} l-5,11 l10,0 Z" fill="#111"/>')
    px, py = P(xm - 0.12, 1.75)
    out.append(f'<text x="{px:.1f}" y="{py:.1f}" font-family="{FONT}" font-size="10.5" font-weight="bold" '
               f'text-anchor="middle" transform="rotate(-90 {px:.1f} {py:.1f})" fill="#111">'
               f'ESCALIER  0,90 × 3,50 — 15 hauteurs</text>')
    out.append(text(xm + 0.04, 3.30, "M", 10, "bold"))
    return out


# ---------------------------------------------------------------- cotations
def chaine_h(bounds, ypx, ref_ypx, out, total=False):
    xs = []
    acc = bounds[0]
    xs.append(acc)
    for v in bounds[1:]:
        acc += v
        xs.append(acc)
    pxs = [P(x, 0)[0] for x in xs]
    out.append(f'<line x1="{pxs[0] - 8:.1f}" y1="{ypx:.1f}" x2="{pxs[-1] + 8:.1f}" y2="{ypx:.1f}" stroke="#111" stroke-width="0.7"/>')
    for px in pxs:
        out.append(f'<line x1="{px:.1f}" y1="{ref_ypx:.1f}" x2="{px:.1f}" y2="{ypx + (6 if ypx > ref_ypx else -6):.1f}" '
                   f'stroke="#888" stroke-width="0.45"/>')
        out.append(f'<line x1="{px - 4:.1f}" y1="{ypx + 4:.1f}" x2="{px + 4:.1f}" y2="{ypx - 4:.1f}" stroke="#111" stroke-width="1.3"/>')
    for i, v in enumerate(bounds[1:]):
        if v < 0.1:
            continue
        cx = (pxs[i] + pxs[i + 1]) / 2
        size = 13 if total else (10.5 if v >= 0.4 else 8.5)
        out.append(f'<text x="{cx:.1f}" y="{ypx - 4:.1f}" font-family="{FONT}" font-size="{size}" '
                   f'font-weight="{"bold" if total else "normal"}" text-anchor="middle" fill="#111">{fmt(v)}</text>')


def chaine_v(bounds, xpx, ref_xpx, out, total=False):
    ys = []
    acc = bounds[0]
    ys.append(acc)
    for v in bounds[1:]:
        acc += v
        ys.append(acc)
    pys = [P(0, y)[1] for y in ys]
    out.append(f'<line x1="{xpx:.1f}" y1="{pys[0] + 8:.1f}" x2="{xpx:.1f}" y2="{pys[-1] - 8:.1f}" stroke="#111" stroke-width="0.7"/>')
    for py in pys:
        out.append(f'<line x1="{ref_xpx:.1f}" y1="{py:.1f}" x2="{xpx + (6 if xpx > ref_xpx else -6):.1f}" y2="{py:.1f}" '
                   f'stroke="#888" stroke-width="0.45"/>')
        out.append(f'<line x1="{xpx - 4:.1f}" y1="{py + 4:.1f}" x2="{xpx + 4:.1f}" y2="{py - 4:.1f}" stroke="#111" stroke-width="1.3"/>')
    for i, v in enumerate(bounds[1:]):
        if v < 0.1:
            continue
        cy = (pys[i] + pys[i + 1]) / 2
        size = 13 if total else (10.5 if v >= 0.4 else 8.5)
        tx = xpx - 4
        out.append(f'<text x="{tx:.1f}" y="{cy:.1f}" font-family="{FONT}" font-size="{size}" '
                   f'font-weight="{"bold" if total else "normal"}" text-anchor="middle" fill="#111" '
                   f'transform="rotate(-90 {tx:.1f} {cy:.1f})">{fmt(v)}</text>')


def cotations():
    out = []
    left, right = P(-EXT, 0)[0], P(IN + EXT, 0)[0]
    top, bottom = P(0, IN + EXT)[1], P(0, -EXT)[1]
    e = -EXT
    # Sud
    chaine_h([e, .20, .90, .07, 1.60, .07, 1.80, .07, 1.79, .07, 1.60, .20], bottom + 30, bottom + 4, out)
    chaine_h([e, .20, .90, .07, 3.47, .07, 3.46, .20], bottom + 60, bottom + 4, out)
    chaine_h([e, 8.37], bottom + 92, bottom + 4, out, total=True)
    # Nord
    chaine_h([e, .20, 1.60, .07, 2.28, .07, 2.28, .07, 1.60, .20], top - 30, top - 4, out)
    chaine_h([e, .20, 3.95, .07, 3.95, .20], top - 60, top - 4, out)
    chaine_h([e, 8.37], top - 92, top - 4, out, total=True)
    # Ouest
    chaine_v([e, .20, 3.50, .22, .90, .07, 1.80, .07, 1.41, .20], left - 30, left - 4, out)
    chaine_v([e, .20, 3.65, .07, .90, .07, 3.28, .20], left - 60, left - 4, out)
    chaine_v([e, 8.37], left - 92, left - 4, out, total=True)
    # Est
    chaine_v([e, .20, 1.78, .07, 1.80, .07, .90, .07, 1.80, .07, 1.41, .20], right + 44, right + 4, out)
    chaine_v([e, .20, 3.65, .07, .90, .07, 3.28, .20], right + 74, right + 4, out)
    chaine_v([e, 8.37], right + 106, right + 4, out, total=True)
    # cote intérieure du dégagement
    y = 4.00
    a, b = P(0.0, y), P(6.45, y)
    out.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="#777" stroke-width="0.6"/>')
    for p in (a, b):
        out.append(f'<line x1="{p[0] - 3:.1f}" y1="{p[1] + 3:.1f}" x2="{p[0] + 3:.1f}" y2="{p[1] - 3:.1f}" stroke="#555" stroke-width="1.1"/>')
    return out


# ---------------------------------------------------------------- mobilier
def lit(x0, y0, x1, y1, tete, couv):
    """lit avec tête de lit côté 'N','S','E','W'"""
    o = [rect(x0, y0, x1, y1, 'fill="#fbfaf7" stroke="#555" stroke-width="0.9" rx="3"')]
    if tete in "NS":
        L = y1 - y0
        cy0, cy1 = (y0, y1 - 0.55) if tete == "N" else (y0 + 0.55, y1)
        o.append(rect(x0 + 0.03, cy0 + 0.03, x1 - 0.03, cy1, f'fill="{couv}" stroke="#555" stroke-width="0.6" rx="2"'))
        o.append(rect(x0 + 0.03, cy0 + 0.03, x1 - 0.03, cy0 + 0.30 if tete == "S" else cy0 + 0.03,
                      'fill="#ffffff" stroke="none" opacity="0"'))
        py0, py1 = (y1 - 0.42, y1 - 0.10) if tete == "N" else (y0 + 0.10, y0 + 0.42)
        w = (x1 - x0 - 0.20) / 2
        o.append(rect(x0 + 0.07, py0, x0 + 0.07 + w, py1, 'fill="#fff" stroke="#888" stroke-width="0.6" rx="4"'))
        o.append(rect(x1 - 0.07 - w, py0, x1 - 0.07, py1, 'fill="#fff" stroke="#888" stroke-width="0.6" rx="4"'))
        # chevets
        cy = (y1 - 0.42, y1) if tete == "N" else (y0, y0 + 0.42)
    return o


def placard(x0, y0, x1, y1):
    o = [rect(x0, y0, x1, y1, 'fill="#f3efe8" stroke="#555" stroke-width="0.9"')]
    if (x1 - x0) > (y1 - y0):
        ym = (y0 + y1) / 2
        o.append(line(x0 + 0.05, ym, x1 - 0.05, ym, 'stroke="#999" stroke-width="0.6" stroke-dasharray="2 2"'))
        n = int((x1 - x0) / 0.12)
        for i in range(1, n):
            xx = x0 + i * (x1 - x0) / n
            o.append(line(xx, ym - 0.12, xx + 0.06, ym + 0.12, 'stroke="#b5aa98" stroke-width="0.6"'))
    else:
        xm = (x0 + x1) / 2
        o.append(line(xm, y0 + 0.05, xm, y1 - 0.05, 'stroke="#999" stroke-width="0.6" stroke-dasharray="2 2"'))
        n = int((y1 - y0) / 0.12)
        for i in range(1, n):
            yy = y0 + i * (y1 - y0) / n
            o.append(line(xm - 0.12, yy, xm + 0.12, yy + 0.06, 'stroke="#b5aa98" stroke-width="0.6"'))
    return o


def bureau(x0, y0, x1, y1, chaise):
    o = [rect(x0, y0, x1, y1, 'fill="#c99c6a" stroke="#6b4f2f" stroke-width="0.8"')]
    cx, cy = chaise
    o.append(circle(cx, cy, 0.20, 'fill="#e7e2da" stroke="#666" stroke-width="0.8"'))
    return o


def douche(x0, y0, x1, y1):
    o = [rect(x0, y0, x1, y1, 'fill="#eef5f8" stroke="#4d6b7a" stroke-width="1"')]
    o.append(line(x0, y0, x1, y1, 'stroke="#9fb3bd" stroke-width="0.6"'))
    o.append(line(x0, y1, x1, y0, 'stroke="#9fb3bd" stroke-width="0.6"'))
    o.append(circle((x0 + x1) / 2, (y0 + y1) / 2, 0.035, 'fill="#4d6b7a"'))
    return o


def vasque(x0, y0, x1, y1):
    o = [rect(x0, y0, x1, y1, 'fill="#ffffff" stroke="#555" stroke-width="0.9" rx="2"')]
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    px, py = P(cx, cy)
    rx, ry = (x1 - x0) * S * 0.32, (y1 - y0) * S * 0.30
    if (y1 - y0) > (x1 - x0):
        rx, ry = (x1 - x0) * S * 0.30, (y1 - y0) * S * 0.32
    o.append(f'<ellipse cx="{px:.1f}" cy="{py:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="#eef5f8" stroke="#555" stroke-width="0.7"/>')
    return o


def wc_cuvette(xw, yc):
    """WC suspendu fixé au mur Est (x = xw)"""
    o = [rect(xw - 0.18, yc - 0.22, xw, yc + 0.22, 'fill="#fff" stroke="#555" stroke-width="0.9"')]
    px, py = P(xw - 0.36, yc)
    o.append(f'<ellipse cx="{px:.1f}" cy="{py:.1f}" rx="{0.20 * S:.1f}" ry="{0.17 * S:.1f}" fill="#fff" stroke="#555" stroke-width="0.9"/>')
    return o


def plante(x, y):
    o = [circle(x, y, 0.13, 'fill="#7f9c74" stroke="#56704d" stroke-width="0.7"')]
    o.append(circle(x, y, 0.06, 'fill="#a6bf98"'))
    return o


def mobilier():
    o = []
    # Chambre 1
    o += placard(0.0, 6.56, 0.60, 7.97)
    o += bureau(0.68, 7.42, 1.88, 7.97, (1.28, 7.12))
    o += lit(2.45, 6.07, 3.85, 7.97, "N", "#a9b89a")
    o.append(rect(2.00, 7.55, 2.38, 7.95, 'fill="#c99c6a" stroke="#6b4f2f" stroke-width="0.6"'))
    o += plante(3.65, 4.95)
    # Chambre 2
    o += placard(7.37, 6.56, 7.97, 7.97)
    o += bureau(6.09, 7.42, 7.29, 7.97, (6.69, 7.12))
    o += lit(4.12, 6.07, 5.52, 7.97, "N", "#8fa6bb")
    o.append(rect(5.59, 7.55, 5.97, 7.95, 'fill="#c99c6a" stroke="#6b4f2f" stroke-width="0.6"'))
    o += plante(4.32, 4.95)
    # Chambre 3
    o += lit(2.95, 0.0, 4.35, 1.90, "S", "#d4a59a")
    o += bureau(1.10, 0.0, 2.30, 0.55, (1.70, 0.85))
    o += placard(3.84, 2.05, 4.44, 3.55)
    o += plante(1.15, 1.62)
    # Chambre 4
    o += lit(4.60, 0.0, 6.00, 1.90, "S", "#a9b89a")
    o += bureau(6.55, 0.0, 7.75, 0.55, (7.15, 0.85))
    o += placard(4.51, 2.05, 5.11, 3.55)
    o += plante(7.82, 1.55)
    # Salles d'eau
    o += douche(0.00, 5.29, 0.90, 6.49) + vasque(0.75, 4.69, 1.55, 5.16)
    o += douche(7.07, 5.29, 7.97, 6.49) + vasque(6.42, 4.69, 7.22, 5.16)
    o += douche(0.97, 1.85, 1.87, 3.05) + vasque(1.72, 3.18, 2.52, 3.65)
    o += douche(7.07, 1.85, 7.97, 3.05) + vasque(6.42, 3.18, 7.22, 3.65)
    # sèche-serviettes
    for x0, y0, x1, y1 in [(0.02, 4.75, 0.10, 5.20), (7.87, 4.75, 7.95, 5.20),
                           (0.99, 3.15, 1.07, 3.60), (7.87, 3.15, 7.95, 3.60)]:
        o.append(rect(x0, y0, x1, y1, 'fill="#bbb" stroke="#666" stroke-width="0.5"'))
    # WC
    o += wc_cuvette(7.97, 4.17)
    o.append(rect(6.98, 4.42, 7.33, 4.62, 'fill="#fff" stroke="#555" stroke-width="0.8" rx="2"'))
    return o


# ---------------------------------------------------------------- habillage
def defs():
    return f'''<defs>
  <pattern id="hachure" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
    <rect width="7" height="7" fill="#ffffff"/>
    <line x1="0" y1="0" x2="0" y2="7" stroke="#000" stroke-width="1.3"/>
  </pattern>
  <pattern id="parquet" width="{S * 1.2:.1f}" height="{S * 0.18:.1f}" patternUnits="userSpaceOnUse">
    <rect width="{S * 1.2:.1f}" height="{S * 0.18:.1f}" fill="#ecd6b3"/>
    <line x1="0" y1="{S * 0.18:.1f}" x2="{S * 1.2:.1f}" y2="{S * 0.18:.1f}" stroke="#dcc29b" stroke-width="0.8"/>
    <line x1="{S * 0.45:.1f}" y1="0" x2="{S * 0.45:.1f}" y2="{S * 0.18:.1f}" stroke="#dcc29b" stroke-width="0.8"/>
  </pattern>
  <pattern id="carrelage" width="{S * 0.30:.1f}" height="{S * 0.30:.1f}" patternUnits="userSpaceOnUse">
    <rect width="{S * 0.30:.1f}" height="{S * 0.30:.1f}" fill="#dfe3e6"/>
    <path d="M0,0 H{S * 0.30:.1f} M0,0 V{S * 0.30:.1f}" stroke="#c4cacf" stroke-width="0.8"/>
  </pattern>
</defs>'''


def nord(x, y):
    return (f'<g transform="translate({x},{y})">'
            f'<circle r="24" fill="#fff" stroke="#111" stroke-width="1.2"/>'
            f'<path d="M0,-20 L8,12 L0,5 Z" fill="#111"/><path d="M0,-20 L-8,12 L0,5 Z" fill="#fff" stroke="#111"/>'
            f'<text y="-29" font-family="{FONT}" font-size="14" font-weight="bold" text-anchor="middle">N</text></g>')


def echelle_graphique(x, y):
    o = [f'<g transform="translate({x},{y})">']
    for i in range(4):
        fill = "#111" if i % 2 == 0 else "#fff"
        o.append(f'<rect x="{i * S:.1f}" y="0" width="{S:.1f}" height="7" fill="{fill}" stroke="#111" stroke-width="0.8"/>')
    for i in range(5):
        o.append(f'<text x="{i * S:.1f}" y="21" font-family="{FONT}" font-size="10" text-anchor="middle">{i}</text>')
    o.append(f'<text x="{4 * S + 12:.1f}" y="21" font-family="{FONT}" font-size="10">m</text></g>')
    return "".join(o)


SURFACES = [
    ("Chambre 1", "9,8"), ("Chambre 2", "9,8"), ("Chambre 3", "9,5"), ("Chambre 4", "9,5"),
    ("Salle d'eau 1", "2,9"), ("Salle d'eau 2", "2,9"), ("Salle d'eau 3", "2,9"), ("Salle d'eau 4", "2,9"),
    ("WC indépendant", "1,3"), ("Dégagement + palier", "6,0"), ("Trémie escalier", "3,2"),
]


def panneau(mode, titre_plan):
    x0 = 1040
    o = []
    o.append(f'<rect x="{x0}" y="40" width="330" height="910" fill="#fff" stroke="#111" stroke-width="1.2"/>')
    o.append(f'<text x="{x0 + 18}" y="74" font-family="{FONT}" font-size="17" font-weight="bold">TABLEAU DES SURFACES</text>')
    yy = 102
    for nom, s in SURFACES:
        o.append(f'<text x="{x0 + 18}" y="{yy}" font-family="{FONT}" font-size="13">{nom}</text>')
        o.append(f'<text x="{x0 + 312}" y="{yy}" font-family="{FONT}" font-size="13" text-anchor="end">{s} m²</text>')
        o.append(f'<line x1="{x0 + 18}" y1="{yy + 7}" x2="{x0 + 312}" y2="{yy + 7}" stroke="#ddd" stroke-width="0.7"/>')
        yy += 23
    o.append(f'<text x="{x0 + 18}" y="{yy + 6}" font-family="{FONT}" font-size="13" font-weight="bold">Total pièces</text>')
    o.append(f'<text x="{x0 + 312}" y="{yy + 6}" font-family="{FONT}" font-size="13" font-weight="bold" text-anchor="end">60,7 m²</text>')
    o.append(f'<text x="{x0 + 18}" y="{yy + 26}" font-family="{FONT}" font-size="11" fill="#444">Intérieur murs ext. 7,97 × 7,97 = 63,5 m²</text>')
    o.append(f'<text x="{x0 + 18}" y="{yy + 42}" font-family="{FONT}" font-size="11" fill="#444">Emprise 8,37 × 8,37 = 70 m²</text>')
    yy += 74
    o.append(f'<line x1="{x0}" y1="{yy - 16}" x2="{x0 + 330}" y2="{yy - 16}" stroke="#111" stroke-width="1"/>')
    o.append(f'<text x="{x0 + 18}" y="{yy + 6}" font-family="{FONT}" font-size="15" font-weight="bold">NOTES</text>')
    notes = [
        "Murs extérieurs 20 cm — cloisons 7 cm",
        "(type placo 72/48 + isolant phonique).",
        "Cotes en mètres, intérieur brut de cloison.",
        "Escalier droit le long du mur Ouest,",
        "départ en bas (Sud) : emmarchement 0,90,",
        "14 girons de 25 cm, 15 hauteurs ≈ 19 cm",
        "(à recaler sur la hauteur d'étage réelle).",
        "Nouvelle trémie 0,90 × 3,50 : reprise de",
        "plancher → avis structure / BET.",
        "Salles d'eau : douche 90 × 120 extra-plate,",
        "vasque 80, sèche-serviettes, VMC hygro.",
        "SdE 3 sans fenêtre : extraction VMC.",
        "WC suspendu + lave-mains, fenêtre Est.",
        "Gaine technique Est : SdE 2 + WC + SdE 4",
        "regroupés (chute Ø100).",
        "Fenêtres indicatives : à caler sur les",
        "baies existantes.",
    ]
    yy += 28
    for n in notes:
        o.append(f'<text x="{x0 + 18}" y="{yy}" font-family="{FONT}" font-size="11.5" fill="#222">{n}</text>')
        yy += 17
    # cartouche
    cy = 800
    o.append(f'<rect x="{x0}" y="{cy}" width="330" height="150" fill="#f6f6f4" stroke="#111" stroke-width="1.2"/>')
    o.append(f'<text x="{x0 + 18}" y="{cy + 26}" font-family="{FONT}" font-size="11" fill="#555">PROJET</text>')
    o.append(f'<text x="{x0 + 18}" y="{cy + 46}" font-family="{FONT}" font-size="14" font-weight="bold">Réaménagement de l\'étage — 70 m²</text>')
    o.append(f'<text x="{x0 + 18}" y="{cy + 64}" font-family="{FONT}" font-size="12">4 chambres + 4 salles d\'eau + WC indépendant</text>')
    o.append(f'<line x1="{x0}" y1="{cy + 76}" x2="{x0 + 330}" y2="{cy + 76}" stroke="#111"/>')
    o.append(f'<text x="{x0 + 18}" y="{cy + 98}" font-family="{FONT}" font-size="15" font-weight="bold">{titre_plan}</text>')
    o.append(f'<line x1="{x0}" y1="{cy + 112}" x2="{x0 + 330}" y2="{cy + 112}" stroke="#111"/>')
    o.append(f'<line x1="{x0 + 110}" y1="{cy + 112}" x2="{x0 + 110}" y2="{cy + 150}" stroke="#111"/>')
    o.append(f'<line x1="{x0 + 220}" y1="{cy + 112}" x2="{x0 + 220}" y2="{cy + 150}" stroke="#111"/>')
    for i, (k, v) in enumerate([("ÉCHELLE", "1/40 (A3)"), ("DATE", "04/10/2026"), ("INDICE", "A — esquisse")]):
        o.append(f'<text x="{x0 + 10 + i * 110}" y="{cy + 126}" font-family="{FONT}" font-size="9" fill="#555">{k}</text>')
        o.append(f'<text x="{x0 + 10 + i * 110}" y="{cy + 143}" font-family="{FONT}" font-size="12" font-weight="bold">{v}</text>')
    return o


def legende(mode):
    o = []
    x0, y = 1058, 746
    o.append(f'<line x1="1040" y1="{y - 14}" x2="1370" y2="{y - 14}" stroke="#111" stroke-width="1"/>')
    x = x0
    items = [("hach", "Mur ext. conservé"), ("cl", "Cloison neuve 7 cm"), ("fen", "Fenêtre"), ("porte", "Porte (P = passage)")]
    for k, t in items:
        if k == "hach":
            o.append(f'<rect x="{x}" y="{y}" width="30" height="12" fill="{"url(#hachure)" if mode == "cote" else "#2f2f2f"}" stroke="#000"/>')
        elif k == "cl":
            o.append(f'<rect x="{x}" y="{y + 3}" width="30" height="6" fill="#555"/>')
        elif k == "fen":
            o.append(f'<rect x="{x}" y="{y}" width="30" height="12" fill="#fff" stroke="#000"/>'
                     f'<line x1="{x}" y1="{y + 4.5}" x2="{x + 30}" y2="{y + 4.5}" stroke="#000" stroke-width="0.8"/>'
                     f'<line x1="{x}" y1="{y + 7.5}" x2="{x + 30}" y2="{y + 7.5}" stroke="#000" stroke-width="0.8"/>')
        else:
            o.append(f'<line x1="{x}" y1="{y + 14}" x2="{x}" y2="{y - 6}" stroke="#111" stroke-width="2"/>'
                     f'<path d="M{x},{y - 6} A20,20 0 0 1 {x + 20},{y + 14}" fill="none" stroke="#333" stroke-dasharray="3 2"/>')
        o.append(f'<text x="{x + 38}" y="{y + 10}" font-family="{FONT}" font-size="11">{t}</text>')
        x += 150
        if x > x0 + 200:
            x, y = x0, y + 26
    return o


def plan(mode):
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
         defs(), f'<rect width="{W}" height="{H}" fill="#fff"/>',
         f'<rect x="12" y="12" width="{W - 24}" height="{H - 24}" fill="none" stroke="#111" stroke-width="1.5"/>']
    titre = "PLAN R+1 — PROJET COTÉ" if mode == "cote" else "PLAN R+1 — AMÉNAGEMENT"
    o.append(f'<text x="40" y="44" font-family="{FONT}" font-size="20" font-weight="bold">{titre}</text>')

    sol = {}
    if mode == "amenagement":
        for nom, (pts, *_r) in PIECES.items():
            if nom.startswith("CHAMBRE"):
                f = "url(#parquet)"
            elif nom.startswith("SdE") or nom == "WC":
                f = "url(#carrelage)"
            else:
                f = "#efe6d8"
            o.append(poly(pts, f'fill="{f}" stroke="none"'))
        # couleur de sol des embrasures de portes
        for (_h, _u, n, _w, cut) in PORTES:
            sol[cut] = "#efe6d8"
    o += escalier(mode)
    o += murs(mode)
    o += fenetres(mode)
    o += portes(mode, sol)
    if mode == "amenagement":
        o += mobilier()
    # libellés
    for nom, (pts, surf, lc, la, dims) in PIECES.items():
        pos = lc if mode == "cote" else (la or lc)
        big = nom.startswith("CHAMBRE") or nom == "DÉGAGEMENT"
        if mode == "amenagement" and not big:
            pos = {"SdE 1": (0.45, 4.95), "SdE 2": (7.52, 4.95), "SdE 3": (1.42, 3.33),
                   "SdE 4": (7.60, 3.33), "WC": (6.80, 4.30)}.get(nom, pos)
        x, y = pos
        bg = 'paint-order="stroke" stroke="#ffffff" stroke-width="3" stroke-linejoin="round"' if mode == "amenagement" else ""
        if mode == "amenagement" and not big:
            o.append(text(x, y, nom, 9.5, "bold", extra=bg))
            o.append(text(x, y - 0.15, f"{str(surf).replace('.', ',')} m²", 9, extra=bg))
            continue
        o.append(text(x, y, nom, 13 if big else 11, "bold", extra=bg))
        o.append(text(x, y - 0.22, f"{str(surf).replace('.', ',')} m²", 12 if big else 10.5, extra=bg))
        if dims and mode == "cote":
            o.append(text(x, y - 0.42, dims, 10, fill="#555"))
    if mode == "cote":
        o.append(text(5.00, 4.05, "6,45", 9.5, fill="#444"))
        o += cotations()
    else:
        # cotes globales simples
        out = []
        left, right = P(-EXT, 0)[0], P(IN + EXT, 0)[0]
        top, bottom = P(0, IN + EXT)[1], P(0, -EXT)[1]
        chaine_h([-EXT, 8.37], bottom + 40, bottom + 4, out, total=True)
        chaine_v([-EXT, 8.37], left - 40, left - 4, out, total=True)
        o += out
        o.append(text(0.45, -0.45, "Départ escalier (RDC)", 10, anchor="middle", fill="#444"))
    o.append(nord(965, 90))
    o.append(echelle_graphique(150, 960 - 22))
    o += panneau(mode, titre)
    o += legende(mode)
    o.append('</svg>')
    return "\n".join(o)


if __name__ == "__main__":
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    for mode, nom in (("cote", "plan_cote.svg"), ("amenagement", "plan_amenagement.svg")):
        with open(os.path.join(here, nom), "w", encoding="utf-8") as f:
            f.write(plan(mode))
    print("ok")
