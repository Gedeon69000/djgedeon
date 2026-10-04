#!/usr/bin/env python3
"""Plans du rez-de-chaussée de La Marinka (même plateau que l'étage : 8,70 x 8,90 m murs nus).

Réutilise la géométrie et les outils de dessin de ../plans-etage/generer_plans.py
(même repère : origine = angle intérieur fini Sud-Ouest, x vers l'Est, y vers le Nord).
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "plans-etage"))
import generer_plans as gp  # noqa: E402
from generer_plans import P, S, rect, line, text, circle, poly, fmt, FONT, IX, IY, EXT, DBL, PISE  # noqa: E402

# ---------------------------------------------------------------- géométrie RDC
Y_BLOC0, Y_BLOC1 = 2.13, 3.77          # bloc WC + cellier (sous la SdE 3 de l'étage)
CLOISONS = [
    (0.90, 0.90, 0.97, 3.77),          # cloison escalier (pied de l'escalier ouvert)
    (0.97, 2.13, 3.61, 2.20), (0.97, 3.70, 3.61, 3.77),
    (1.97, 2.20, 2.04, 3.70), (3.54, 2.20, 3.61, 3.70),
]
# (charnière, u, n, largeur, rect d'ouverture)
PORTES = [
    ((1.10, 2.20), (1, 0), (0, 1), 0.70, (1.10, 2.13, 1.80, 2.20)),     # WC
    ((3.40, 2.20), (-1, 0), (0, 1), 0.80, (2.60, 2.13, 3.40, 2.20)),    # cellier
    ((2.50, 0.00), (-1, 0), (0, 1), 0.90, (1.60, -EXT, 2.50, 0.00)),    # porte d'entrée
]
BAIE = (2.30, 6.30)        # baie vitrée 4,00 m, mur Est
CAISSONS = [(0.30, 2.30), (6.30, 8.30)]

PIECES = {
    "SALON": (None, None, (6.10, 2.05), (6.10, 2.62), ""),
    "SALLE À MANGER": (None, None, (5.80, 6.20), (5.80, 7.25), "12 couverts"),
    "CUISINE": (None, None, (2.40, 5.30), (2.40, 5.30), "en L + îlot"),
    "ENTRÉE": ([(0.97, 0), (3.61, 0), (3.61, 2.13), (0.97, 2.13)], 5.6, (2.05, 1.45), (2.05, 1.45), ""),
    "WC": ([(0.97, 2.20), (1.97, 2.20), (1.97, 3.70), (0.97, 3.70)], 1.5, (1.47, 2.95), (1.47, 2.62), "1,00 × 1,50"),
    "CELLIER": ([(2.04, 2.20), (3.54, 2.20), (3.54, 3.70), (2.04, 3.70)], 2.3, (2.79, 2.95), (2.95, 2.62), "1,50 × 1,50"),
}
PIECE_DE_VIE = [(0, 3.70), (0.90, 3.70), (0.90, 3.77), (3.61, 3.77), (3.61, 0), (IX, 0), (IX, IY), (0, IY)]

SURFACES = [
    ("Pièce de vie (cuisine, séjour, salon)", "58,6"), ("Entrée (dont placard)", "5,6"),
    ("WC", "1,5"), ("Cellier / buanderie", "2,3"), ("Escalier (emprise)", "3,3"),
]
NOTES = [
    "Murs pisé ≈ 50 cm + doublage 15 cm (lame",
    "d'air + isolant perspirant), comme à l'étage.",
    "Baie vitrée 4,00 m à galandage, mur Est",
    "(jardin) : 2 vantaux de 2,00 m dans les murs.",
    "Ouverture 4 m dans le pisé : linteau béton ou",
    "acier, étude BET obligatoire. Repli : 3,00 m.",
    "Caissons : doublage épaissi local (≈ 20 cm).",
    "Escalier identique à l'étage (¼ tournant bas).",
    "Salon 10-12 pl. : canapés 3,60 + 3,20 + poufs.",
    "Table 3,40 × 1,05 : 12 couverts (5 + 5 + 2).",
    "Cuisine en L + îlot ; évier sous la chute Ouest.",
    "WC + cellier sous la SdE 3 (chute commune).",
    "Entrée au Sud (position à confirmer) ; autres",
    "ouvertures à reporter selon l'existant.",
]
LEGENDE = [("pise", "Mur pisé existant"), ("dbl", "Doublage 15 (lame d'air)"),
           ("cl", "Cloison neuve 7 cm"), ("baie", "Baie vitrée galandage"),
           ("porte", "Porte (P = passage)"), ("fen", "Caisson galandage")]


# ---------------------------------------------------------------- dessin
def murs(mode):
    gp.CLOISONS = CLOISONS
    return gp.murs(mode)


def portes(mode):
    out = []
    for (hx, hy), u, n, w, cut in PORTES:
        x0, y0, x1, y1 = cut
        out.append(rect(x0, y0, x1, y1, f'fill="{"#ffffff" if mode == "cote" else "#efe6d8"}" stroke="none"'))
        a, b, h = P(hx + u[0] * w, hy + u[1] * w), P(hx + n[0] * w, hy + n[1] * w), P(hx, hy)
        cross = (a[0] - h[0]) * (b[1] - h[1]) - (a[1] - h[1]) * (b[0] - h[0])
        out.append(f'<path d="M{a[0]:.1f},{a[1]:.1f} A{w * S:.1f},{w * S:.1f} 0 0 {1 if cross > 0 else 0} {b[0]:.1f},{b[1]:.1f}" '
                   f'fill="none" stroke="#333" stroke-width="0.8" stroke-dasharray="4 3"/>')
        out.append(f'<line x1="{h[0]:.1f}" y1="{h[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="#111" stroke-width="2"/>')
        if mode == "cote" and y0 > 0:
            out.append(text((x0 + x1) / 2, y0 - 0.17, f"P {fmt(w)}", 8, fill="#444"))
    # seuil de la porte d'entrée
    out.append(line(1.60, -EXT, 2.50, -EXT, 'stroke="#111" stroke-width="1.2"'))
    return out


def baie(mode):
    out = []
    y0, y1 = BAIE
    out.append(rect(IX, y0, IX + EXT, y1, 'fill="#ffffff" stroke="none"'))
    out.append(line(IX + EXT, y0, IX + EXT, y1, 'stroke="#111" stroke-width="0.8"'))
    # deux vantaux (position fermée) + rails
    xm = IX + 0.07
    for a, b in ((y0, (y0 + y1) / 2 + 0.03), ((y0 + y1) / 2 - 0.03, y1)):
        out.append(line(xm - 0.02, a, xm - 0.02, b, 'stroke="#2a6f97" stroke-width="1.6"'))
        out.append(line(xm + 0.02, a, xm + 0.02, b, 'stroke="#2a6f97" stroke-width="1.6"'))
    # caissons de galandage dans le doublage
    for c0, c1 in CAISSONS:
        out.append(rect(IX + 0.02, c0, IX + 0.12, c1, 'fill="#ffffff" stroke="#2a6f97" stroke-width="0.8" stroke-dasharray="4 3"'))
    # flèches de coulissement
    for yy, d in ((y0 + 0.55, -1), (y1 - 0.55, 1)):
        a, b = P(IX - 0.12, yy), P(IX - 0.12, yy + d * 0.45)
        out.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="#2a6f97" stroke-width="1"/>')
        out.append(f'<path d="M{b[0]:.1f},{b[1]:.1f} l-3.5,{5 * d:.1f} l7,0 Z" fill="#2a6f97"/>')
    lab = "BAIE VITRÉE GALANDAGE 4,00 m — JARDIN"
    px, py = P(IX + EXT + 0.30, (y0 + y1) / 2)
    out.append(f'<text x="{px:.1f}" y="{py:.1f}" font-family="{FONT}" font-size="10" font-weight="bold" fill="#2a6f97" '
               f'text-anchor="middle" transform="rotate(90 {px:.1f} {py:.1f})">{lab}</text>' if mode != "cote" else "")
    return out


def escalier(mode):
    out = gp.escalier(mode)
    # ligne de coupe conventionnelle du plan RDC
    a, b = P(0.0, 2.35), P(0.90, 2.75)
    out.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="#111" stroke-width="1.6"/>')
    a, b = P(0.0, 2.43), P(0.90, 2.83)
    out.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="#fff" stroke-width="3"/>')
    return out


# ---------------------------------------------------------------- mobilier
def canape(x0, y0, x1, y1, dossier, places, couleur="#b9b1a3"):
    o = [rect(x0, y0, x1, y1, f'fill="{couleur}" stroke="#6d665c" stroke-width="0.9" rx="5"')]
    e = 0.20
    if dossier == "S":
        o.append(rect(x0, y0, x1, y0 + e, 'fill="#9c9487" stroke="#6d665c" stroke-width="0.6" rx="3"'))
        sx0, sx1 = x0 + e, x1 - e
        o.append(rect(x0, y0, x0 + e, y1, 'fill="#9c9487" stroke="#6d665c" stroke-width="0.6" rx="3"'))
        o.append(rect(x1 - e, y0, x1, y1, 'fill="#9c9487" stroke="#6d665c" stroke-width="0.6" rx="3"'))
        for k in range(1, places):
            xx = sx0 + k * (sx1 - sx0) / places
            o.append(line(xx, y0 + e, xx, y1 - 0.05, 'stroke="#8b8378" stroke-width="0.7"'))
    else:  # dossier au Nord
        o.append(rect(x0, y1 - e, x1, y1, 'fill="#9c9487" stroke="#6d665c" stroke-width="0.6" rx="3"'))
        sx0, sx1 = x0 + e, x1 - e
        o.append(rect(x0, y0, x0 + e, y1, 'fill="#9c9487" stroke="#6d665c" stroke-width="0.6" rx="3"'))
        o.append(rect(x1 - e, y0, x1, y1, 'fill="#9c9487" stroke="#6d665c" stroke-width="0.6" rx="3"'))
        for k in range(1, places):
            xx = sx0 + k * (sx1 - sx0) / places
            o.append(line(xx, y0 + 0.05, xx, y1 - e, 'stroke="#8b8378" stroke-width="0.7"'))
    return o


def chaise(cx, cy, orient):
    w, d = 0.45, 0.45
    o = [rect(cx - w / 2, cy - d / 2, cx + w / 2, cy + d / 2, 'fill="#e7e2da" stroke="#666" stroke-width="0.8" rx="3"')]
    if orient == "N":   # dossier au Nord (l'assise regarde le Sud)
        o.append(rect(cx - w / 2, cy + d / 2 - 0.06, cx + w / 2, cy + d / 2, 'fill="#9a8f80" stroke="none"'))
    elif orient == "S":
        o.append(rect(cx - w / 2, cy - d / 2, cx + w / 2, cy - d / 2 + 0.06, 'fill="#9a8f80" stroke="none"'))
    elif orient == "W":
        o.append(rect(cx - w / 2, cy - d / 2, cx - w / 2 + 0.06, cy + d / 2, 'fill="#9a8f80" stroke="none"'))
    else:
        o.append(rect(cx + w / 2 - 0.06, cy - d / 2, cx + w / 2, cy + d / 2, 'fill="#9a8f80" stroke="none"'))
    return o


def mobilier():
    o = []
    # ---- Salon : 2 canapés face à face + table basse + poufs, sur tapis
    o.append(rect(4.75, 1.20, 7.65, 2.90, 'fill="#e9e1d3" stroke="#cbbfa9" stroke-width="0.8" rx="4"'))
    o += canape(4.40, 0.10, 8.00, 1.05, "S", 5, "#b9b1a3")
    o += canape(4.40, 3.00, 7.60, 3.95, "N", 4, "#a7b3a0")
    o.append(rect(5.40, 1.60, 6.80, 2.40, 'fill="#c99c6a" stroke="#6b4f2f" stroke-width="0.8" rx="4"'))
    o.append(circle(7.25, 1.65, 0.22, 'fill="#d9c7a7" stroke="#8a7a5f" stroke-width="0.8"'))
    o.append(circle(7.25, 2.40, 0.22, 'fill="#d9c7a7" stroke="#8a7a5f" stroke-width="0.8"'))
    o += gp.plante(8.15, 1.30)
    # ---- Salle à manger : table 3,40 x 1,05 — 12 couverts
    tx0, tx1, ty0, ty1 = 4.10, 7.50, 5.35, 6.40
    o.append(rect(tx0, ty0, tx1, ty1, 'fill="#c99c6a" stroke="#6b4f2f" stroke-width="1" rx="3"'))
    xs = [tx0 + 0.34 + k * (tx1 - tx0 - 0.68) / 4 for k in range(5)]
    for cx in xs:
        o += chaise(cx, ty1 + 0.25, "N")
        o += chaise(cx, ty0 - 0.25, "S")
    o += chaise(tx0 - 0.27, (ty0 + ty1) / 2, "W")
    o += chaise(tx1 + 0.27, (ty0 + ty1) / 2, "E")
    # suspension(s) au-dessus de la table
    for cx in (4.95, 5.80, 6.65):
        o.append(circle(cx, (ty0 + ty1) / 2, 0.12, 'fill="none" stroke="#b08d57" stroke-width="0.8" stroke-dasharray="2 2"'))
    # ---- Cuisine en L + îlot
    plan_t = 'fill="#d6d9dc" stroke="#555" stroke-width="0.9"'
    o.append(rect(0.0, 7.95, 3.60, IY, plan_t))                   # plan de travail Nord
    o.append(rect(0.0, 4.60, 0.65, 7.95, plan_t))                 # plan de travail Ouest
    o.append(rect(0.0, 4.60, 0.65, 5.25, 'fill="#eef0f2" stroke="#555" stroke-width="0.9"'))   # colonne frigo
    o.append(rect(0.0, 5.25, 0.65, 5.85, 'fill="#eef0f2" stroke="#555" stroke-width="0.9"'))   # colonne four
    o.append(text(0.33, 4.88, "frigo", 7, fill="#555"))
    o.append(text(0.33, 5.50, "four", 7, fill="#555"))
    # évier 2 bacs (mur Ouest, sous la chute de la SdE 1)
    o.append(rect(0.08, 6.20, 0.55, 6.60, 'fill="#fff" stroke="#555" stroke-width="0.7" rx="2"'))
    o.append(rect(0.08, 6.65, 0.55, 7.05, 'fill="#fff" stroke="#555" stroke-width="0.7" rx="2"'))
    # plaque de cuisson (mur Nord)
    o.append(rect(1.80, 8.02, 2.55, 8.53, 'fill="#333" stroke="#111" stroke-width="0.7" rx="2"'))
    for cx, cy in ((1.98, 8.40), (2.37, 8.40), (1.98, 8.15), (2.37, 8.15)):
        o.append(circle(cx, cy, 0.09, 'fill="none" stroke="#bbb" stroke-width="0.7"'))
    # îlot + tabourets
    o.append(rect(1.50, 6.15, 3.30, 7.00, 'fill="#e9e4dc" stroke="#555" stroke-width="1" rx="2"'))
    for cx in (1.85, 2.40, 2.95):
        o.append(circle(cx, 5.88, 0.17, 'fill="#c99c6a" stroke="#6b4f2f" stroke-width="0.7"'))
    # ---- Entrée : placard + banc
    o += gp.placard(3.01, 0.0, 3.61, 1.20)
    o.append(rect(0.97, 1.55, 1.80, 1.95, 'fill="#c99c6a" stroke="#6b4f2f" stroke-width="0.7"'))
    o.append(text(1.38, 1.70, "banc", 7, fill="#fff"))
    # ---- WC : cuvette suspendue mur Nord + lave-mains
    o.append(rect(1.25, 3.52, 1.69, 3.70, 'fill="#fff" stroke="#555" stroke-width="0.9"'))
    px, py = P(1.47, 3.33)
    o.append(f'<ellipse cx="{px:.1f}" cy="{py:.1f}" rx="{0.17 * S:.1f}" ry="{0.20 * S:.1f}" fill="#fff" stroke="#555" stroke-width="0.9"/>')
    o.append(rect(1.77, 2.95, 1.97, 3.30, 'fill="#fff" stroke="#555" stroke-width="0.8" rx="2"'))
    # ---- Cellier : lave-linge, sèche-linge, ballon
    for x0 in (2.10, 2.75):
        o.append(rect(x0, 3.08, x0 + 0.60, 3.68, 'fill="#fff" stroke="#555" stroke-width="0.9" rx="2"'))
        o.append(circle(x0 + 0.30, 3.38, 0.20, 'fill="#eef5f8" stroke="#777" stroke-width="0.7"'))
    o.append(circle(2.33, 2.50, 0.27, 'fill="#f4f4f4" stroke="#555" stroke-width="0.9"'))
    o.append(text(2.33, 2.47, "ECS", 7, fill="#555"))
    return o


# ---------------------------------------------------------------- cotations
def cotations():
    out = []
    left, right = P(-EXT, 0)[0], P(IX + EXT, 0)[0]
    top, bottom = P(0, IY + EXT)[1], P(0, -EXT)[1]
    pe, d = -EXT, DBL
    # Sud : porte d'entrée, puis cloisons
    gp.chaine_h([pe, PISE, d, 1.60, .90, 5.90, d, PISE], bottom + 28, bottom + 4, out)
    gp.chaine_h([-d, d, .90, .07, 1.00, .07, 1.50, .07, 4.79, d], bottom + 58, bottom + 4, out)
    gp.chaine_h([-d, gp.NU_X], bottom + 90, bottom + 4, out, total=True)
    # Nord : cuisine
    gp.chaine_h([pe, PISE, d, 3.60, 4.80, d, PISE], top - 28, top - 4, out)
    gp.chaine_h([-d, gp.NU_X], top - 60, top - 4, out, total=True)
    # Ouest : escalier, bloc WC/cellier
    gp.chaine_v([pe, PISE, d, .90, 2.80, 4.90, d, PISE], left - 28, left - 4, out)
    gp.chaine_v([-d, d, 2.13, .07, 1.50, .07, 4.83, d], left - 58, left - 4, out)
    gp.chaine_v([-d, gp.NU_Y], left - 90, left - 4, out, total=True)
    # Est : baie et caissons
    gp.chaine_v([pe, PISE, d + .30, 2.00, 4.00, 2.00, d + .30, PISE], right + 40, right + 4, out)
    gp.chaine_v([-d, gp.NU_Y], right + 72, right + 4, out, total=True)
    # cotes intérieures table / salon
    return out


# ---------------------------------------------------------------- planche
def plan(mode):
    W, H = gp.W, gp.H
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
         gp.defs(), f'<rect width="{W}" height="{H}" fill="#fff"/>',
         f'<rect x="12" y="12" width="{W - 24}" height="{H - 24}" fill="none" stroke="#111" stroke-width="1.5"/>']
    titre = "PLAN RDC — PROJET COTÉ" if mode == "cote" else "PLAN RDC — AMÉNAGEMENT"
    o.append(f'<text x="40" y="44" font-family="{FONT}" font-size="20" font-weight="bold">{titre}</text>')
    if mode == "amenagement":
        o.append(poly(PIECE_DE_VIE, 'fill="url(#parquet)" stroke="none"'))
        o.append(poly(PIECES["ENTRÉE"][0], 'fill="#e6dccb" stroke="none"'))
        for nom in ("WC", "CELLIER"):
            o.append(poly(PIECES[nom][0], 'fill="url(#carrelage)" stroke="none"'))
        # zone cuisine carrelée
        o.append(rect(0, 3.77, 3.61, IY, 'fill="#e9e4dc" stroke="none" opacity="0.55"'))
    o += escalier(mode)
    o += murs(mode)
    o += portes(mode)
    o += baie(mode)
    if mode == "amenagement":
        o += mobilier()
    halo = 'paint-order="stroke" stroke="#ffffff" stroke-width="3" stroke-linejoin="round"'
    for nom, (pts, surf, lc, la, dims) in PIECES.items():
        x, y = lc if mode == "cote" else la
        petit = nom in ("WC", "CELLIER")
        o.append(text(x, y, nom, 9.5 if petit else 12, "bold", extra=halo))
        if surf:
            o.append(text(x, y - 0.20, f"{surf:.1f}".replace(".", ",") + " m²", 9 if petit else 11, extra=halo))
        if dims and (mode == "cote" or not petit):
            o.append(text(x, y - (0.38 if surf else 0.22), dims, 9, fill="#555", extra=halo))
    if mode == "cote":
        o.append(text(5.80, 4.30, "PIÈCE DE VIE 58,6 m²", 13, "bold", extra=halo))
        o += cotations()
        lab = "BAIE VITRÉE 4,00 m À GALANDAGE"
        px, py = P(IX - 0.30, (BAIE[0] + BAIE[1]) / 2)
        o.append(f'<text x="{px:.1f}" y="{py:.1f}" font-family="{FONT}" font-size="9.5" font-weight="bold" fill="#2a6f97" '
                 f'text-anchor="middle" transform="rotate(-90 {px:.1f} {py:.1f})">{lab}</text>')
        o.append(text(IX - 0.30, 1.30, "caisson", 8, fill="#2a6f97", extra=f'transform="rotate(-90 {P(IX - 0.30, 1.30)[0]:.1f} {P(IX - 0.30, 1.30)[1]:.1f})"'))
        o.append(text(IX - 0.30, 7.30, "caisson", 8, fill="#2a6f97", extra=f'transform="rotate(-90 {P(IX - 0.30, 7.30)[0]:.1f} {P(IX - 0.30, 7.30)[1]:.1f})"'))
    else:
        out = []
        left, bottom = P(-EXT, 0)[0], P(0, -EXT)[1]
        gp.chaine_h([-DBL, gp.NU_X], bottom + 40, bottom + 4, out, total=True)
        gp.chaine_v([-DBL, gp.NU_Y], left - 40, left - 4, out, total=True)
        o += out
        o.append(text(2.05, -EXT - 0.32, "Entrée ↑", 9.5, "bold", fill="#444"))
        o.append(text(IX + EXT + 0.35, 8.90, "JARDIN", 12, "bold", anchor="start", fill="#5d7f4f"))
    o.append(gp.nord(965, 90))
    o.append(gp.echelle_graphique(150, 960 - 22))
    o += gp.panneau(titre, surfaces=SURFACES, notes=NOTES, total="71,3 m²",
                    projet="La Marinka — Rez-de-chaussée (77 m²)",
                    sous_titre="Séjour 12 pers. + cuisine + baie jardin", indice="A — esquisse")
    o += gp.legende(mode, LEGENDE)
    o.append('</svg>')
    return "\n".join(o)


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    for mode, nom in (("cote", "plan_rdc_cote.svg"), ("amenagement", "plan_rdc_amenagement.svg")):
        with open(os.path.join(here, nom), "w", encoding="utf-8") as f:
            f.write(plan(mode))
    print("ok")
