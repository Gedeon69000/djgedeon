#!/usr/bin/env python3
"""Génère les plans de l'étage (plateau 8,70 x 8,90 m murs nus = 77,43 m²) :
  - plan_cote.svg        : plan d'architecte coté (R+1 projet)
  - plan_amenagement.svg : plan global meublé

Repère : origine = angle intérieur FINI Sud-Ouest (après doublage),
x vers l'Est, y vers le Nord, unités en mètres.
Murs en pisé (épaisseur indicative), doublage 15 cm avec lame d'air,
cloisons 7 cm.
"""

# ---------------------------------------------------------------- géométrie
NU_X, NU_Y = 8.70, 8.90      # plateau entre murs nus (pisé brut)
DBL = 0.15                   # doublage : lame d'air 3 + isolant 10,5 + placo 1,3 (+ ossature)
PISE = 0.50                  # épaisseur indicative du pisé (à relever)
IX, IY = NU_X - 2 * DBL, NU_Y - 2 * DBL   # intérieur fini : 8,40 x 8,60
EXT = DBL + PISE

S = 1400 / 420 * 20          # px par mètre -> échelle 1/50 sur un A3 paysage
OX = 150 + EXT * S
OY = 140 + (IY + EXT) * S
W, H = 1400, 990


def P(x, y):
    return OX + x * S, OY - y * S


# Niveaux en y
Y_CS = 4.05              # nu Sud du mur bas du dégagement
Y_C0, Y_C1 = 4.12, 5.02  # dégagement 0,90
Y_N = 5.09               # début zone Nord
X_WC = 6.60              # fin du dégagement / mur WC

# Cloisons (x0, y0, x1, y1)
CLOISONS = [
    (0.90, 0.00, 0.97, Y_CS),          # mur escalier / chambre 3
    (0.90, Y_CS, IX, Y_C0),            # dégagement côté Sud
    (0.00, Y_C1, IX, Y_N),             # dégagement côté Nord
    (X_WC, Y_C0, X_WC + 0.07, Y_C1),   # WC
    (4.17, Y_N, 4.24, IY),             # ch1 / ch2
    (4.65, 0.00, 4.72, Y_CS),          # ch3 / ch4
    # SdE 1 (en long, Nord-Ouest) + rangement sous rampant
    (1.25, Y_N, 1.35, 7.56), (0.00, 7.49, 1.25, 7.56),   # cloison 10 cm (galandage)
    # SdE 2 (en long, Nord-Est) + rangement
    (7.05, Y_N, 7.15, 7.56), (7.15, 7.49, IX, 7.56),     # cloison 10 cm (galandage)
    # SdE 3 (en long, le long du dégagement)
    (0.97, 2.73, 3.44, 2.80), (3.37, 2.80, 3.44, Y_CS),
    # SdE 4
    (5.93, 2.73, IX, 2.80), (5.93, 2.80, 6.00, Y_CS),
]

# Portes : (charnière, u, n, largeur, rect d'ouverture dans le mur)
# Portes à galandage : (x0, x1 du mur, y début ouverture, y fin ouverture, y fin du caisson)
GALANDAGES = [(1.25, 1.35, 5.25, 5.98, 6.71),   # SdE1
              (7.05, 7.15, 5.25, 5.98, 6.71)]   # SdE2

PORTES = [
    ((1.47, Y_N), (1, 0), (0, 1), 0.80, (1.47, Y_C1, 2.27, Y_N)),        # Ch1
    ((6.53, Y_N), (-1, 0), (0, 1), 0.80, (5.73, Y_C1, 6.53, Y_N)),       # Ch2
    ((3.62, Y_CS), (1, 0), (0, -1), 0.80, (3.62, Y_CS, 4.42, Y_C0)),     # Ch3
    ((5.75, Y_CS), (-1, 0), (0, -1), 0.80, (4.95, Y_CS, 5.75, Y_C0)),    # Ch4
    ((X_WC + 0.07, 4.22), (0, 1), (1, 0), 0.70, (X_WC, 4.22, X_WC + 0.07, 4.92)),  # WC
    ((3.37, 2.95), (0, 1), (-1, 0), 0.70, (3.37, 2.95, 3.44, 3.65)),     # SdE3
    ((6.00, 2.95), (0, 1), (1, 0), 0.70, (5.93, 2.95, 6.00, 3.65)),      # SdE4
]

# Velux (projection en plan) : chambres + dégagement uniquement
# Velux disposés « en dé de 5 » : 4 chambres alignées deux à deux,
# symétriques par rapport à l'axe Nord-Sud (x = 4,20) et au faîtage (±2,20),
# celui du dégagement sur l'axe central, juste au Nord du faîtage.
VX_AXE, VX_D, VY_D = IX / 2, 1.46, 2.20
_v78 = lambda cx, cy: (cx - 0.39, cy - 0.375, cx + 0.39, cy + 0.375, "78×98")
VELUX = [
    _v78(VX_AXE - VX_D, IY / 2 + VY_D),   # Ch1
    _v78(VX_AXE + VX_D, IY / 2 + VY_D),   # Ch2
    _v78(VX_AXE - VX_D, IY / 2 - VY_D),   # Ch3
    _v78(VX_AXE + VX_D, IY / 2 - VY_D),   # Ch4
    (VX_AXE - 0.275, 4.38, VX_AXE + 0.275, 4.95, "55×78"),   # dégagement (centre)
]
FAITAGE = IY / 2  # hypothèse : faîtage Est-Ouest au milieu

PIECES = {  # nom: (polygone, surface, label_cote, label_amenagement, dims)
    "CHAMBRE 1": ([(1.35, Y_N), (4.17, Y_N), (4.17, IY), (0, IY), (0, 7.56), (1.35, 7.56)],
                  11.2, (2.76, 7.95), (2.74, 6.42), "2,82 × 3,51"),
    "CHAMBRE 2": ([(4.24, Y_N), (7.05, Y_N), (7.05, 7.56), (IX, 7.56), (IX, IY), (4.24, IY)],
                  11.2, (5.64, 7.95), (5.66, 6.42), "2,81 × 3,51"),
    "CHAMBRE 3": ([(0.97, 0), (4.65, 0), (4.65, Y_CS), (3.44, Y_CS), (3.44, 2.73), (0.97, 2.73)],
                  11.6, (2.30, 1.10), (3.50, 1.30), "3,68 × 2,73"),
    "CHAMBRE 4": ([(4.72, 0), (IX, 0), (IX, 2.73), (5.93, 2.73), (5.93, Y_CS), (4.72, Y_CS)],
                  11.6, (6.85, 1.10), (5.87, 1.30), "3,68 × 2,73"),
    "SdE 1": ([(0, Y_N), (1.25, Y_N), (1.25, 7.49), (0, 7.49)], 3.0, (0.62, 6.45), (0.62, 5.55), "1,25 × 2,40"),
    "SdE 2": ([(7.15, Y_N), (IX, Y_N), (IX, 7.49), (7.15, 7.49)], 3.0, (7.77, 6.45), (7.77, 5.55), "1,25 × 2,40"),
    "SdE 3": ([(0.97, 2.80), (3.37, 2.80), (3.37, Y_CS), (0.97, Y_CS)], 3.0, (2.30, 3.45), (2.30, 3.35), "2,40 × 1,25"),
    "SdE 4": ([(6.00, 2.80), (IX, 2.80), (IX, Y_CS), (6.00, Y_CS)], 3.0, (7.10, 3.45), (7.10, 3.35), "2,40 × 1,25"),
    "WC": ([(X_WC + 0.07, Y_C0), (IX, Y_C0), (IX, Y_C1), (X_WC + 0.07, Y_C1)], 1.6, (7.85, 4.62), (7.55, 4.66), "1,73 × 0,90"),
    "DÉGAGEMENT": ([(0, 3.70), (0.90, 3.70), (0.90, Y_C0), (X_WC, Y_C0), (X_WC, Y_C1), (0, Y_C1)],
                   6.3, (2.75, 4.62), (2.75, 4.62), ""),
}
RANGEMENTS = [(0.0, 7.56, 1.25, IY), (7.15, 7.56, IX, IY)]

# Escalier quart tournant bas : départ vers l'Ouest le long du mur Sud,
# marches balancées dans l'angle Sud-Ouest, puis volée droite vers le Nord.
# Lignes de nez de marche : (point côté mur, point côté jour)
ESC_ARRIVEE = 3.70
ESC_LIGNES = [((0.90, 0.0), (0.90, 0.90)), ((0.42, 0.0), (0.90, 0.98)), ((0.0, 0.0), (0.90, 1.10)),
              ((0.0, 0.42), (0.90, 1.24)), ((0.0, 0.80), (0.90, 1.40)), ((0.0, 1.12), (0.90, 1.55)),
              ((0.0, 1.42), (0.90, 1.70))]
ESC_LIGNES += [((0.0, 1.81 + k * (ESC_ARRIVEE - 1.81) / 7), (0.90, 1.81 + k * (ESC_ARRIVEE - 1.81) / 7))
               for k in range(8)]

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


def anneau(e_ext, e_int, fill, stroke='stroke="none"'):
    """Anneau rectangulaire entre les décalages e_ext (extérieur) et e_int (intérieur)."""
    a0, a1 = P(-e_ext, IY + e_ext)
    b0, b1 = P(-e_int, IY + e_int)
    we, he = (IX + 2 * e_ext) * S, (IY + 2 * e_ext) * S
    wi, hi = (IX + 2 * e_int) * S, (IY + 2 * e_int) * S
    return (f'<path fill-rule="evenodd" fill="{fill}" {stroke} d="M{a0:.1f},{a1:.1f} h{we:.1f} v{he:.1f} h{-we:.1f} Z '
            f'M{b0:.1f},{b1:.1f} h{wi:.1f} v{hi:.1f} h{-wi:.1f} Z"/>')


# ---------------------------------------------------------------- murs
def murs(mode):
    out = []
    pise = "url(#pise)" if mode == "cote" else "#a88a66"
    out.append(anneau(EXT, DBL, pise, 'stroke="#000" stroke-width="1.4"'))
    # doublage : lame d'air (blanc), isolant, placo
    out.append(anneau(DBL, DBL - 0.03, "#ffffff"))
    out.append(anneau(DBL - 0.03, 0.013, "url(#isolant)" if mode == "cote" else "#f1e3a6"))
    out.append(anneau(0.013, 0.0, "#777"))
    cl_fill = "#555" if mode == "cote" else "#4a4a4a"
    for c in CLOISONS:
        out.append(rect(*c, f'fill="{cl_fill}" stroke="none"'))
    return out


def portes(mode):
    out = []
    for (hx, hy), u, n, w, cut in PORTES:
        x0, y0, x1, y1 = cut
        fill = "#ffffff" if mode == "cote" else "#efe6d8"
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
            if x1 - x0 > y1 - y0:
                ty = Y_C1 - 0.17 if n[1] > 0 else Y_C0 + 0.10
                out.append(text(mx, ty, f"P {fmt(w)}", 8, fill="#444"))
            else:
                tx = mx + (-n[0]) * 0.17
                px, py = P(tx, my)
                out.append(f'<text x="{px:.1f}" y="{py:.1f}" font-family="{FONT}" font-size="8" text-anchor="middle" '
                           f'fill="#444" transform="rotate(-90 {px:.1f} {py:.1f})">{fmt(w)}</text>')
    return out


def galandages(mode):
    out = []
    fill = "#ffffff" if mode == "cote" else "#efe6d8"
    for x0, x1, y0, y1, yc in GALANDAGES:
        out.append(rect(x0, y0, x1, y1, f'fill="{fill}" stroke="none"'))
        xm = (x0 + x1) / 2
        # caisson dans la cloison
        out.append(rect(x0 + 0.02, y1, x1 - 0.02, yc, 'fill="#fff" stroke="#111" stroke-width="0.6" stroke-dasharray="3 2"'))
        # vantail ouvert (dans le caisson) + position fermée en pointillés
        out.append(line(xm, y1 - 0.06, xm, yc - 0.02, 'stroke="#111" stroke-width="2.2"'))
        out.append(line(xm, y0, xm, y1, 'stroke="#555" stroke-width="0.8" stroke-dasharray="4 3"'))
        if mode == "cote":
            tx = x0 - 0.17 if x0 < 4 else x1 + 0.17
            px, py = P(tx, (y0 + y1) / 2)
            out.append(f'<text x="{px:.1f}" y="{py:.1f}" font-family="{FONT}" font-size="8" text-anchor="middle" '
                       f'fill="#444" transform="rotate(-90 {px:.1f} {py:.1f})">gal. 0,73</text>')
    return out


def escalier(mode):
    out = []
    fill = "#ffffff" if mode == "cote" else "#d8b48a"
    out.append(rect(0, 0, 0.90, ESC_ARRIVEE, f'fill="{fill}" stroke="#111" stroke-width="1"'))
    for (a, b) in ESC_LIGNES[1:-1]:
        out.append(line(a[0], a[1], b[0], b[1], 'stroke="#111" stroke-width="0.8"'))
    for i in range(len(ESC_LIGNES) - 1):
        (a0, b0), (a1, b1) = ESC_LIGNES[i], ESC_LIGNES[i + 1]
        cx = (a0[0] + b0[0] + a1[0] + b1[0]) / 4
        cy = (a0[1] + b0[1] + a1[1] + b1[1]) / 4
        if i >= 6:
            cx = 0.80
        out.append(text(cx, cy - 0.04, str(i + 1), 6.5, fill="#666"))
    a, c, d, b = P(0.86, 0.45), P(0.45, 0.45), P(0.45, 0.95), P(0.45, ESC_ARRIVEE - 0.05)
    out.append(f'<circle cx="{a[0]:.1f}" cy="{a[1]:.1f}" r="3" fill="#111"/>')
    out.append(f'<path d="M{a[0]:.1f},{a[1]:.1f} Q{c[0]:.1f},{c[1]:.1f} {d[0]:.1f},{d[1]:.1f} L{b[0]:.1f},{b[1] + 9:.1f}" '
               f'fill="none" stroke="#111" stroke-width="1.3"/>')
    out.append(f'<path d="M{b[0]:.1f},{b[1]:.1f} l-4.5,10 l9,0 Z" fill="#111"/>')
    px, py = P(0.20, 2.65)
    out.append(f'<text x="{px:.1f}" y="{py:.1f}" font-family="{FONT}" font-size="8.5" font-weight="bold" '
               f'text-anchor="middle" transform="rotate(-90 {px:.1f} {py:.1f})" fill="#111">'
               f'ESCALIER ¼ TOURNANT — 15 h</text>')
    out.append(text(0.60, ESC_ARRIVEE - 0.25, "M", 9, "bold"))
    return out


def velux(mode):
    out = []
    for x0, y0, x1, y1, lib in VELUX:
        st = 'fill="#dbe9f3" fill-opacity="0.35" stroke="#1f5f8b" stroke-width="1.1" stroke-dasharray="5 3"'
        out.append(rect(x0, y0, x1, y1, st))
        out.append(line(x0, y0, x1, y1, 'stroke="#1f5f8b" stroke-width="0.5" stroke-dasharray="3 3"'))
        out.append(line(x0, y1, x1, y0, 'stroke="#1f5f8b" stroke-width="0.5" stroke-dasharray="3 3"'))
        if mode == "cote":
            if lib == "55×78":
                out.append(text(x1 + 0.06, (y0 + y1) / 2 - 0.03, f"V {lib}", 7.5, anchor="start", fill="#1f5f8b"))
            else:
                out.append(text((x0 + x1) / 2, y0 - 0.15, f"V {lib}", 7.5, fill="#1f5f8b"))
    out.append(line(-EXT - 0.25, FAITAGE, IX + EXT + 0.25, FAITAGE,
                    'stroke="#1f5f8b" stroke-width="0.7" stroke-dasharray="14 4 2 4" opacity="0.7"'))
    if mode != "cote":
        out.append(text(IX + EXT + 0.30, FAITAGE - 0.04, "faîtage (hyp.)", 8, anchor="start", fill="#1f5f8b"))
    return out


# ---------------------------------------------------------------- cotations
def _cumul(bounds):
    xs = [bounds[0]]
    for v in bounds[1:]:
        xs.append(xs[-1] + v)
    return xs


def _label(v, total):
    return fmt(v)


def chaine_h(bounds, ypx, ref_ypx, out, total=False):
    pxs = [P(x, 0)[0] for x in _cumul(bounds)]
    out.append(f'<line x1="{pxs[0] - 8:.1f}" y1="{ypx:.1f}" x2="{pxs[-1] + 8:.1f}" y2="{ypx:.1f}" stroke="#111" stroke-width="0.7"/>')
    for px in pxs:
        out.append(f'<line x1="{px:.1f}" y1="{ref_ypx:.1f}" x2="{px:.1f}" y2="{ypx + (6 if ypx > ref_ypx else -6):.1f}" '
                   f'stroke="#999" stroke-width="0.4"/>')
        out.append(f'<line x1="{px - 4:.1f}" y1="{ypx + 4:.1f}" x2="{px + 4:.1f}" y2="{ypx - 4:.1f}" stroke="#111" stroke-width="1.2"/>')
    for i, v in enumerate(bounds[1:]):
        if v < 0.12:
            continue
        cx = (pxs[i] + pxs[i + 1]) / 2
        size = 12 if total else (10 if v >= 0.6 else 7.5)
        out.append(f'<text x="{cx:.1f}" y="{ypx - 4:.1f}" font-family="{FONT}" font-size="{size}" '
                   f'font-weight="{"bold" if total else "normal"}" text-anchor="middle" fill="#111">{_label(v, total)}</text>')


def chaine_v(bounds, xpx, ref_xpx, out, total=False):
    pys = [P(0, y)[1] for y in _cumul(bounds)]
    out.append(f'<line x1="{xpx:.1f}" y1="{pys[0] + 8:.1f}" x2="{xpx:.1f}" y2="{pys[-1] - 8:.1f}" stroke="#111" stroke-width="0.7"/>')
    for py in pys:
        out.append(f'<line x1="{ref_xpx:.1f}" y1="{py:.1f}" x2="{xpx + (6 if xpx > ref_xpx else -6):.1f}" y2="{py:.1f}" '
                   f'stroke="#999" stroke-width="0.4"/>')
        out.append(f'<line x1="{xpx - 4:.1f}" y1="{py + 4:.1f}" x2="{xpx + 4:.1f}" y2="{py - 4:.1f}" stroke="#111" stroke-width="1.2"/>')
    for i, v in enumerate(bounds[1:]):
        if v < 0.12:
            continue
        cy = (pys[i] + pys[i + 1]) / 2
        size = 12 if total else (10 if v >= 0.6 else 7.5)
        tx = xpx - 4
        out.append(f'<text x="{tx:.1f}" y="{cy:.1f}" font-family="{FONT}" font-size="{size}" '
                   f'font-weight="{"bold" if total else "normal"}" text-anchor="middle" fill="#111" '
                   f'transform="rotate(-90 {tx:.1f} {cy:.1f})">{_label(v, total)}</text>')


def cotations():
    out = []
    left, right = P(-EXT, 0)[0], P(IX + EXT, 0)[0]
    top, bottom = P(0, IY + EXT)[1], P(0, -EXT)[1]
    pe, d = -EXT, DBL
    # Sud
    chaine_h([pe, PISE, d, .90, .07, 2.40, .07, 1.21, .07, 1.21, .07, 2.40, d, PISE], bottom + 28, bottom + 4, out)
    chaine_h([-d, d, .90, .07, 3.68, .07, 3.68, d], bottom + 58, bottom + 4, out)
    chaine_h([-d, NU_X], bottom + 90, bottom + 4, out, total=True)
    # Nord
    chaine_h([pe, PISE, d, 1.25, .10, 2.82, .07, 2.81, .10, 1.25, d, PISE], top - 28, top - 4, out)
    chaine_h([-d, d, 4.17, .07, 4.16, d], top - 58, top - 4, out)
    chaine_h([-d, NU_X], top - 90, top - 4, out, total=True)
    # Ouest
    chaine_v([pe, PISE, d, .90, 2.80, .42, .90, .07, 2.40, .07, 1.04, d, PISE], left - 28, left - 4, out)
    chaine_v([-d, d, 4.05, .07, .90, .07, 3.51, d], left - 58, left - 4, out)
    chaine_v([-d, NU_Y], left - 90, left - 4, out, total=True)
    # Est
    chaine_v([pe, PISE, d, 2.73, .07, 1.25, .07, .90, .07, 2.40, .07, 1.04, d, PISE], right + 40, right + 4, out)
    chaine_v([-d, d, 4.05, .07, .90, .07, 3.51, d], right + 70, right + 4, out)
    chaine_v([-d, NU_Y], right + 102, right + 4, out, total=True)
    # cote intérieure du dégagement
    y = 4.17
    a, b = P(0.0, y), P(X_WC, y)
    out.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="#777" stroke-width="0.6"/>')
    for p in (a, b):
        out.append(f'<line x1="{p[0] - 3:.1f}" y1="{p[1] + 3:.1f}" x2="{p[0] + 3:.1f}" y2="{p[1] - 3:.1f}" stroke="#555" stroke-width="1.1"/>')
    out.append(text(1.20, y + 0.04, "6,60", 8.5, fill="#444"))
    return out


# ---------------------------------------------------------------- mobilier
def lit(x0, y0, x1, y1, tete, couv):
    o = [rect(x0, y0, x1, y1, 'fill="#fbfaf7" stroke="#555" stroke-width="0.9" rx="3"')]
    oreiller = 'fill="#fff" stroke="#888" stroke-width="0.6" rx="3"'
    if tete in "NS":
        cy0, cy1 = (y0 + 0.03, y1 - 0.50) if tete == "N" else (y0 + 0.50, y1 - 0.03)
        o.append(rect(x0 + 0.03, cy0, x1 - 0.03, cy1, f'fill="{couv}" stroke="#555" stroke-width="0.6" rx="2"'))
        py0, py1 = (y1 - 0.40, y1 - 0.10) if tete == "N" else (y0 + 0.10, y0 + 0.40)
        w = (x1 - x0 - 0.20) / 2
        o.append(rect(x0 + 0.07, py0, x0 + 0.07 + w, py1, oreiller))
        o.append(rect(x1 - 0.07 - w, py0, x1 - 0.07, py1, oreiller))
    else:
        cx0, cx1 = (x0 + 0.50, x1 - 0.03) if tete == "W" else (x0 + 0.03, x1 - 0.50)
        o.append(rect(cx0, y0 + 0.03, cx1, y1 - 0.03, f'fill="{couv}" stroke="#555" stroke-width="0.6" rx="2"'))
        px0, px1 = (x0 + 0.10, x0 + 0.40) if tete == "W" else (x1 - 0.40, x1 - 0.10)
        h = (y1 - y0 - 0.20) / 2
        o.append(rect(px0, y0 + 0.07, px1, y0 + 0.07 + h, oreiller))
        o.append(rect(px0, y1 - 0.07 - h, px1, y1 - 0.07, oreiller))
    return o


def chevet(x0, y0):
    return [rect(x0, y0, x0 + 0.38, y0 + 0.38, 'fill="#c99c6a" stroke="#6b4f2f" stroke-width="0.6"')]


def placard(x0, y0, x1, y1, ouverture=None):
    o = [rect(x0, y0, x1, y1, 'fill="#f3efe8" stroke="#555" stroke-width="0.9"')]
    horiz = (x1 - x0) > (y1 - y0)
    if horiz:
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


def rangement(x0, y0, x1, y1, cote_portes):
    """Rangement sous rampant avec portes coulissantes côté chambre."""
    o = [rect(x0, y0, x1, y1, 'fill="#efe9df" stroke="none"')]
    for k in range(1, 5):
        yy = y0 + k * (y1 - y0) / 5
        o.append(line(x0 + 0.08, yy, x1 - 0.08, yy, 'stroke="#c9bfae" stroke-width="0.6" stroke-dasharray="3 3"'))
    xp = x1 if cote_portes == "E" else x0
    d = -0.04 if cote_portes == "E" else 0.04
    ym = (y0 + y1) / 2
    o.append(line(xp, y0 + 0.02, xp, ym + 0.05, 'stroke="#444" stroke-width="2"'))
    o.append(line(xp + d, ym - 0.05, xp + d, y1 - 0.02, 'stroke="#444" stroke-width="2"'))
    return o


def bureau(x0, y0, x1, y1, chaise):
    o = [rect(x0, y0, x1, y1, 'fill="#c99c6a" stroke="#6b4f2f" stroke-width="0.8"')]
    o.append(circle(chaise[0], chaise[1], 0.20, 'fill="#e7e2da" stroke="#666" stroke-width="0.8"'))
    return o


def douche(x0, y0, x1, y1):
    o = [rect(x0, y0, x1, y1, 'fill="#eef5f8" stroke="#4d6b7a" stroke-width="1"')]
    o.append(line(x0, y0, x1, y1, 'stroke="#9fb3bd" stroke-width="0.6"'))
    o.append(line(x0, y1, x1, y0, 'stroke="#9fb3bd" stroke-width="0.6"'))
    o.append(circle((x0 + x1) / 2, (y0 + y1) / 2, 0.035, 'fill="#4d6b7a"'))
    return o


def paroi(x0, y0, x1, y1):
    return [line(x0, y0, x1, y1, 'stroke="#4d6b7a" stroke-width="2.2"')]


def vasque(x0, y0, x1, y1):
    o = [rect(x0, y0, x1, y1, 'fill="#ffffff" stroke="#555" stroke-width="0.9" rx="2"')]
    px, py = P((x0 + x1) / 2, (y0 + y1) / 2)
    w, h = (x1 - x0) * S, (y1 - y0) * S
    o.append(f'<ellipse cx="{px:.1f}" cy="{py:.1f}" rx="{w * 0.32:.1f}" ry="{h * 0.32:.1f}" fill="#eef5f8" stroke="#555" stroke-width="0.7"/>')
    return o


def seche_serviettes(x0, y0, x1, y1):
    return [rect(x0, y0, x1, y1, 'fill="#bbb" stroke="#666" stroke-width="0.5"')]


def wc_cuvette(xw, yc):
    o = [rect(xw - 0.18, yc - 0.22, xw, yc + 0.22, 'fill="#fff" stroke="#555" stroke-width="0.9"')]
    px, py = P(xw - 0.36, yc)
    o.append(f'<ellipse cx="{px:.1f}" cy="{py:.1f}" rx="{0.20 * S:.1f}" ry="{0.17 * S:.1f}" fill="#fff" stroke="#555" stroke-width="0.9"/>')
    return o


def plante(x, y):
    return [circle(x, y, 0.13, 'fill="#7f9c74" stroke="#56704d" stroke-width="0.7"'), circle(x, y, 0.06, 'fill="#a6bf98"')]


def mobilier():
    o = []
    # Chambre 1 : lit tête au Nord, bureau contre la cloison, rangement sous rampant
    o += lit(2.05, 6.70, 3.45, IY, "N", "#a9b89a")
    o += chevet(1.60, 8.17) + chevet(3.52, 8.17)
    o += bureau(3.62, 5.25, 4.17, 6.45, (3.38, 5.85))
    o += rangement(*RANGEMENTS[0], "E")
    o += plante(1.55, 6.30)
    # Chambre 2
    o += lit(4.96, 6.70, 6.36, IY, "N", "#8fa6bb")
    o += chevet(4.51, 8.17) + chevet(6.43, 8.17)
    o += bureau(4.24, 5.25, 4.79, 6.45, (5.03, 5.85))
    o += rangement(*RANGEMENTS[1], "W")
    o += plante(6.85, 6.30)
    # Chambre 3 : lit tête contre la SdE, armoire contre la cloison, bureau
    o += lit(1.55, 0.83, 2.95, 2.73, "N", "#d4a59a")
    o += chevet(1.12, 2.32) + chevet(3.00, 2.32)
    o += placard(4.05, 0.20, 4.65, 1.75)
    o += bureau(3.05, 0.0, 4.00, 0.50, (3.52, 0.70))
    # Chambre 4
    o += lit(6.42, 0.83, 7.82, 2.73, "N", "#a9b89a")
    o += chevet(5.99, 2.32) + chevet(7.87, 2.32)
    o += placard(4.72, 0.20, 5.32, 1.75)
    o += bureau(5.37, 0.0, 6.32, 0.50, (5.85, 0.70))
    # Salles d'eau en longueur : douche 120x80 au fond, vasque, sèche-serviettes
    o += douche(0.03, 6.69, 1.22, 7.49) + paroi(0.03, 6.69, 0.80, 6.69)
    o += vasque(0.0, 5.92, 0.48, 6.62) + seche_serviettes(0.10, Y_N, 0.60, Y_N + 0.08)
    o += douche(7.18, 6.69, IX - 0.03, 7.49) + paroi(7.60, 6.69, IX - 0.03, 6.69)
    o += vasque(IX - 0.48, 5.92, IX, 6.62) + seche_serviettes(7.80, Y_N, 8.30, Y_N + 0.08)
    o += douche(0.97, 2.83, 1.77, Y_CS - 0.03) + paroi(1.77, 2.83, 1.77, 3.60)
    o += vasque(1.95, Y_CS - 0.48, 2.70, Y_CS) + seche_serviettes(2.00, 2.80, 2.50, 2.88)
    o += douche(7.60, 2.83, IX, Y_CS - 0.03) + paroi(7.60, 2.83, 7.60, 3.60)
    o += vasque(6.70, Y_CS - 0.48, 7.45, Y_CS) + seche_serviettes(6.85, 2.80, 7.35, 2.88)
    # WC suspendu + lave-mains
    o += wc_cuvette(IX, 4.47)
    o.append(rect(7.45, Y_C1 - 0.20, 7.80, Y_C1, 'fill="#fff" stroke="#555" stroke-width="0.8" rx="2"'))
    return o


# ---------------------------------------------------------------- habillage
def defs():
    return f'''<defs>
  <pattern id="pise" width="9" height="9" patternUnits="userSpaceOnUse">
    <rect width="9" height="9" fill="#e8d9c2"/>
    <circle cx="2" cy="2" r="0.9" fill="#8a6d4a"/><circle cx="6.5" cy="5" r="0.7" fill="#8a6d4a"/>
    <circle cx="3.5" cy="7.5" r="0.6" fill="#8a6d4a"/>
  </pattern>
  <pattern id="isolant" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
    <rect width="6" height="6" fill="#fdf6d8"/>
    <line x1="0" y1="0" x2="0" y2="6" stroke="#c9b45e" stroke-width="0.8"/>
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
    for i in range(5):
        fill = "#111" if i % 2 == 0 else "#fff"
        o.append(f'<rect x="{i * S:.1f}" y="0" width="{S:.1f}" height="7" fill="{fill}" stroke="#111" stroke-width="0.8"/>')
    for i in range(6):
        o.append(f'<text x="{i * S:.1f}" y="21" font-family="{FONT}" font-size="10" text-anchor="middle">{i}</text>')
    o.append(f'<text x="{5 * S + 12:.1f}" y="21" font-family="{FONT}" font-size="10">m</text></g>')
    return "".join(o)


SURFACES = [
    ("Chambre 1 (dont rangement 1,3)", "11,2"), ("Chambre 2 (dont rangement 1,3)", "11,2"),
    ("Chambre 3", "11,6"), ("Chambre 4", "11,6"),
    ("Salles d'eau 1 à 4 (4 × 3,0)", "12,0"), ("WC indépendant", "1,6"),
    ("Dégagement + palier", "6,3"), ("Trémie escalier", "3,3"),
]


def panneau(titre_plan):
    x0 = 1040
    o = []
    o.append(f'<rect x="{x0}" y="40" width="330" height="910" fill="#fff" stroke="#111" stroke-width="1.2"/>')
    o.append(f'<text x="{x0 + 18}" y="72" font-family="{FONT}" font-size="17" font-weight="bold">TABLEAU DES SURFACES</text>')
    yy = 100
    for nom, s in SURFACES:
        o.append(f'<text x="{x0 + 18}" y="{yy}" font-family="{FONT}" font-size="12.5">{nom}</text>')
        o.append(f'<text x="{x0 + 312}" y="{yy}" font-family="{FONT}" font-size="12.5" text-anchor="end">{s} m²</text>')
        o.append(f'<line x1="{x0 + 18}" y1="{yy + 7}" x2="{x0 + 312}" y2="{yy + 7}" stroke="#ddd" stroke-width="0.7"/>')
        yy += 23
    o.append(f'<text x="{x0 + 18}" y="{yy + 4}" font-family="{FONT}" font-size="13" font-weight="bold">Total pièces (fini)</text>')
    o.append(f'<text x="{x0 + 312}" y="{yy + 4}" font-family="{FONT}" font-size="13" font-weight="bold" text-anchor="end">68,8 m²</text>')
    o.append(f'<text x="{x0 + 18}" y="{yy + 24}" font-family="{FONT}" font-size="11" fill="#444">Plateau murs nus 8,70 × 8,90 = 77,4 m²</text>')
    o.append(f'<text x="{x0 + 18}" y="{yy + 40}" font-family="{FONT}" font-size="11" fill="#444">Intérieur fini (doublage 15) 8,40 × 8,60 = 72,2 m²</text>')
    yy += 70
    o.append(f'<line x1="{x0}" y1="{yy - 14}" x2="{x0 + 330}" y2="{yy - 14}" stroke="#111" stroke-width="1"/>')
    o.append(f'<text x="{x0 + 18}" y="{yy + 8}" font-family="{FONT}" font-size="15" font-weight="bold">NOTES</text>')
    notes = [
        "Murs en pisé ≈ 50 cm (épaisseur à relever).",
        "Doublage 15 cm : lame d'air 3 cm + isolant",
        "perspirant (fibre de bois) 10 cm + frein-vapeur",
        "hygrovariable + placo 13 mm. Pas de pare-",
        "vapeur étanche : le pisé doit respirer.",
        "Cloisons 7 cm (placo 72/48 + laine).",
        "Escalier ¼ tournant bas le long du mur Ouest :",
        "15 h ≈ 19 cm, giron 27 cm, emmarchement 0,90.",
        "Trémie 0,90 × 3,70 : avis structure / BET.",
        "Velux : chambres + dégagement uniquement.",
        "SdE et WC sans Velux : VMC hygro obligatoire.",
        "SdE en longueur 1,25 × 2,40 : douche 120×80",
        "au fond, vasque 75, sèche-serviettes.",
        "SdE 1 et 2 : portes à galandage (cloison 10).",
        "Velux en « dé de 5 », alignés et symétriques.",
        "Faîtage E-O ; zones < 1,80 m hors Carrez.",
    ]
    yy += 30
    for n in notes:
        o.append(f'<text x="{x0 + 18}" y="{yy}" font-family="{FONT}" font-size="11" fill="#222">{n}</text>')
        yy += 16
    cy = 800
    o.append(f'<rect x="{x0}" y="{cy}" width="330" height="150" fill="#f6f6f4" stroke="#111" stroke-width="1.2"/>')
    o.append(f'<text x="{x0 + 18}" y="{cy + 26}" font-family="{FONT}" font-size="11" fill="#555">PROJET</text>')
    o.append(f'<text x="{x0 + 18}" y="{cy + 46}" font-family="{FONT}" font-size="14" font-weight="bold">Réaménagement de l\'étage — 77 m²</text>')
    o.append(f'<text x="{x0 + 18}" y="{cy + 64}" font-family="{FONT}" font-size="12">4 chambres + 4 salles d\'eau + WC indépendant</text>')
    o.append(f'<line x1="{x0}" y1="{cy + 76}" x2="{x0 + 330}" y2="{cy + 76}" stroke="#111"/>')
    o.append(f'<text x="{x0 + 18}" y="{cy + 98}" font-family="{FONT}" font-size="15" font-weight="bold">{titre_plan}</text>')
    o.append(f'<line x1="{x0}" y1="{cy + 112}" x2="{x0 + 330}" y2="{cy + 112}" stroke="#111"/>')
    o.append(f'<line x1="{x0 + 110}" y1="{cy + 112}" x2="{x0 + 110}" y2="{cy + 150}" stroke="#111"/>')
    o.append(f'<line x1="{x0 + 220}" y1="{cy + 112}" x2="{x0 + 220}" y2="{cy + 150}" stroke="#111"/>')
    for i, (k, v) in enumerate([("ÉCHELLE", "1/50 (A3)"), ("DATE", "04/10/2026"), ("INDICE", "E — esquisse")]):
        o.append(f'<text x="{x0 + 10 + i * 110}" y="{cy + 126}" font-family="{FONT}" font-size="9" fill="#555">{k}</text>')
        o.append(f'<text x="{x0 + 10 + i * 110}" y="{cy + 143}" font-family="{FONT}" font-size="12" font-weight="bold">{v}</text>')
    return o


def legende(mode):
    o = []
    x0, y = 1058, 718
    o.append(f'<line x1="1040" y1="{y - 16}" x2="1370" y2="{y - 16}" stroke="#111" stroke-width="1"/>')
    items = [("pise", "Mur pisé existant"), ("dbl", "Doublage 15 (lame d'air)"),
             ("cl", "Cloison neuve 7 cm"), ("vel", "Velux (projection)"),
             ("porte", "Porte (P = passage)"), ("faite", "Faîtage supposé")]
    for idx, (k, t) in enumerate(items):
        x = x0 + (idx % 2) * 158
        yy = y + (idx // 2) * 24
        if k == "pise":
            o.append(f'<rect x="{x}" y="{yy}" width="30" height="12" fill="{"url(#pise)" if mode == "cote" else "#a88a66"}" stroke="#000"/>')
        elif k == "dbl":
            o.append(f'<rect x="{x}" y="{yy}" width="30" height="12" fill="{"url(#isolant)" if mode == "cote" else "#f1e3a6"}" stroke="#777"/>'
                     f'<rect x="{x}" y="{yy}" width="5" height="12" fill="#fff" stroke="#777" stroke-width="0.5"/>')
        elif k == "cl":
            o.append(f'<rect x="{x}" y="{yy + 3}" width="30" height="6" fill="#555"/>')
        elif k == "vel":
            o.append(f'<rect x="{x}" y="{yy - 2}" width="30" height="16" fill="#dbe9f3" stroke="#1f5f8b" stroke-dasharray="5 3"/>'
                     f'<path d="M{x},{yy - 2} L{x + 30},{yy + 14} M{x},{yy + 14} L{x + 30},{yy - 2}" stroke="#1f5f8b" stroke-width="0.5" stroke-dasharray="3 3"/>')
        elif k == "porte":
            o.append(f'<line x1="{x}" y1="{yy + 14}" x2="{x}" y2="{yy - 4}" stroke="#111" stroke-width="2"/>'
                     f'<path d="M{x},{yy - 4} A18,18 0 0 1 {x + 18},{yy + 14}" fill="none" stroke="#333" stroke-dasharray="3 2"/>')
        else:
            o.append(f'<line x1="{x}" y1="{yy + 6}" x2="{x + 30}" y2="{yy + 6}" stroke="#1f5f8b" stroke-dasharray="8 3 2 3"/>')
        o.append(f'<text x="{x + 36}" y="{yy + 10}" font-family="{FONT}" font-size="10.5">{t}</text>')
    return o


LIB_AMENAGEMENT_PETITS = {"SdE 1", "SdE 2", "SdE 3", "SdE 4", "WC"}


def plan(mode):
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
         defs(), f'<rect width="{W}" height="{H}" fill="#fff"/>',
         f'<rect x="12" y="12" width="{W - 24}" height="{H - 24}" fill="none" stroke="#111" stroke-width="1.5"/>']
    titre = "PLAN R+1 — PROJET COTÉ" if mode == "cote" else "PLAN R+1 — AMÉNAGEMENT"
    o.append(f'<text x="40" y="44" font-family="{FONT}" font-size="20" font-weight="bold">{titre}</text>')

    if mode == "amenagement":
        for nom, (pts, *_r) in PIECES.items():
            if nom.startswith("CHAMBRE"):
                f = "url(#parquet)"
            elif nom.startswith("SdE") or nom == "WC":
                f = "url(#carrelage)"
            else:
                f = "#efe6d8"
            o.append(poly(pts, f'fill="{f}" stroke="none"'))
    o += escalier(mode)
    o += murs(mode)
    o += portes(mode)
    o += galandages(mode)
    if mode == "amenagement":
        o += mobilier()
    else:
        for r in RANGEMENTS:
            o += rangement(*r, "E" if r[0] < 1 else "W")
    o += velux(mode)
    for nom, (pts, surf, lc, la, dims) in PIECES.items():
        x, y = lc if mode == "cote" else la
        big = nom.startswith("CHAMBRE") or nom == "DÉGAGEMENT"
        halo = 'paint-order="stroke" stroke="#ffffff" stroke-width="3" stroke-linejoin="round"'
        surf_txt = f"{surf:.1f}".replace(".", ",") + " m²"
        if mode == "amenagement" and not big:
            o.append(text(x, y, nom, 9, "bold", extra=halo))
            o.append(text(x, y - 0.17, surf_txt, 8.5, extra=halo))
            continue
        o.append(text(x, y, nom, 12 if big else 10, "bold", extra=halo))
        o.append(text(x, y - 0.24, surf_txt, 11 if big else 9.5, extra=halo))
        if dims and mode == "cote":
            o.append(text(x, y - 0.45, dims, 9, fill="#555", extra=halo))
    if mode == "cote":
        o.append(text(0.62, 8.05, "Rgt", 8, fill="#666"))
        o.append(text(7.77, 8.05, "Rgt", 8, fill="#666"))
        o += cotations()
    else:
        out = []
        left = P(-EXT, 0)[0]
        bottom = P(0, -EXT)[1]
        chaine_h([-DBL, NU_X], bottom + 40, bottom + 4, out, total=True)
        chaine_v([-DBL, NU_Y], left - 40, left - 4, out, total=True)
        o += out
        o.append(text(0.95, -EXT - 0.28, "← Départ escalier (accès côté Est au RDC)", 9.5, anchor="start", fill="#444"))
        o.append(text(0.62, 8.05, "rangement", 7.5, fill="#777"))
        o.append(text(7.77, 8.05, "rangement", 7.5, fill="#777"))
    o.append(nord(965, 90))
    o.append(echelle_graphique(150, 960 - 22))
    o += panneau(titre)
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
