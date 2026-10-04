"""Génère « La Marinka.xlsx » : budget estimatif de l'aménagement de l'étage."""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.comments import Comment
from openpyxl.worksheet.datavalidation import DataValidation

F = "Arial"
BLUE = Font(name=F, color="0000FF")
BLACK = Font(name=F)
BOLD = Font(name=F, bold=True)
GREEN = Font(name=F, color="008000")
TITLE = Font(name=F, bold=True, size=16)
HEAD = Font(name=F, bold=True, color="FFFFFF")
HEAD_FILL = PatternFill("solid", fgColor="5B4636")
LOT_FILL = PatternFill("solid", fgColor="EFE6D8")
YELLOW = PatternFill("solid", fgColor="FFFF00")
TOT_FILL = PatternFill("solid", fgColor="D9D2C5")
thin = Side(style="thin", color="BBBBBB")
BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
EUR = '#,##0 €;-#,##0 €;"-"'
PCT = '0%'

wb = Workbook()
ps = wb.active
ps.title = "Paramètres"
bs = wb.create_sheet("Budget étage", 0)

# ------------------------------------------------------------ Paramètres
ps["A1"] = "La Marinka — Paramètres et postes hors budget"; ps["A1"].font = TITLE
params = [
    ("Imprévus (% des travaux)", 0.10, "Usuel en rénovation de bâti ancien : 10 à 15 %."),
    ("Maîtrise d'œuvre / architecte (% des travaux)", 0.0, "0 % si vous pilotez vous-même ; 8 à 12 % avec un maître d'œuvre."),
]
ps["A3"], ps["B3"], ps["C3"] = "Paramètre", "Valeur", "Commentaire"
for c in "ABC":
    ps[f"{c}3"].font = HEAD; ps[f"{c}3"].fill = HEAD_FILL
for i, (lab, val, com) in enumerate(params, start=4):
    ps[f"A{i}"] = lab; ps[f"A{i}"].font = BLACK
    ps[f"B{i}"] = val; ps[f"B{i}"].font = BLUE; ps[f"B{i}"].fill = YELLOW; ps[f"B{i}"].number_format = PCT
    ps[f"C{i}"] = com; ps[f"C{i}"].font = BLACK
ps["A7"] = "TVA : prix affichés TTC à 20 % (création de surface habitable dans une grange : taux réduit en principe non applicable)."
ps["A7"].font = Font(name=F, italic=True)

ps["A9"] = "Postes HORS budget étage (à chiffrer séparément)"; ps["A9"].font = BOLD
ps["A10"], ps["B10"], ps["C10"], ps["D10"] = "Poste", "Min €", "Max €", "Commentaire"
for c in "ABCD":
    ps[f"{c}10"].font = HEAD; ps[f"{c}10"].fill = HEAD_FILL
hors = [
    ("Couverture / charpente (si à reprendre)", 15000, 40000, "À diagnostiquer en priorité."),
    ("Raccordements eau / électricité / assainissement individuel", 8000, 15000, "Selon raccordement existant de la grange."),
    ("Renfort du plancher / chape", 5000, 12000, "Si le plancher de l'étage est insuffisant."),
    ("Taxe d'aménagement + dossier changement de destination", 2000, 5000, "Selon taux communal et départemental."),
]
for i, (p, mn, mx, com) in enumerate(hors, start=11):
    ps[f"A{i}"] = p; ps[f"A{i}"].font = BLACK
    for c, v in (("B", mn), ("C", mx)):
        ps[f"{c}{i}"] = v; ps[f"{c}{i}"].font = BLUE; ps[f"{c}{i}"].number_format = EUR
    ps[f"D{i}"] = com; ps[f"D{i}"].font = BLACK
r = 11 + len(hors)
ps[f"A{r}"] = "Total hors budget"; ps[f"A{r}"].font = BOLD
for c in "BC":
    ps[f"{c}{r}"] = f"=SUM({c}11:{c}{r-1})"; ps[f"{c}{r}"].font = BOLD; ps[f"{c}{r}"].number_format = EUR
HORS_TOT = r
ps.column_dimensions["A"].width = 58; ps.column_dimensions["B"].width = 14
ps.column_dimensions["C"].width = 14; ps.column_dimensions["D"].width = 50

# ------------------------------------------------------------ Feuilles budget
HEADS = ["Lot", "Poste", "Unité", "Qté", "PU min €", "PU max €", "Total min €", "Total max €",
         "Faisable soi-même", "Part matériaux", "Auto min €", "Auto max €", "Devis reçu €", "Montant retenu €", "Commentaire"]
HR = 4
COLS = {7: "G", 8: "H", 11: "K", 12: "L", 14: "N"}

LIGNES_ETAGE = [
    ("Gros œuvre", [
        ("Nouvelle trémie, reprise solivage, rebouchage ancienne trémie", "forfait", 1, 3000, 8000, "Non", 0.5, "Avis BET structure."),
        ("Étude BET structure", "forfait", 1, 1000, 2000, "Non", 0.5, ""),
        ("Escalier bois ¼ tournant sur mesure, posé", "u", 1, 4000, 9000, "Non", 0.5, "Kit à poser soi-même : 1 500 – 3 000 €."),
    ]),
    ("Enveloppe / isolation", [
        ("Isolation rampants fibre de bois", "m²", 100, 120, 250, "Oui", 0.55, "Surface de rampants à métrer."),
        ("Velux 78×98 posés + raccords", "u", 4, 1000, 1600, "Non", 0.6, "Étanchéité : à confier à un pro."),
        ("Velux 55×78 posé (dégagement)", "u", 1, 800, 1300, "Non", 0.6, ""),
        ("Doublage murs pisé (lame d'air + isolant perspirant + placo)", "m²", 70, 75, 130, "Oui", 0.5, "Pas de pare-vapeur étanche."),
    ]),
    ("Cloisons / plafonds", [
        ("Cloisons placo 72/48 + laine (dont 2 en 10 cm galandage)", "m²", 75, 55, 90, "Oui", 0.45, ""),
        ("Finition plafonds / habillage sous rampant", "m²", 100, 40, 70, "Oui", 0.45, ""),
    ]),
    ("Plomberie", [
        ("Salle d'eau complète (douche 120×80, vasque, sèche-serviettes)", "u", 4, 5000, 9000, "Non", 0.5, "Poste le plus lourd."),
        ("WC suspendu + lave-mains", "u", 1, 1500, 3000, "Non", 0.5, ""),
        ("Réseaux alimentation / évacuations / chutes", "forfait", 1, 500, 1000, "Non", 0.5, "2 descentes (Est et Ouest)."),
        ("Production eau chaude (ballon 200-300 L)", "u", 1, 2000, 4000, "Non", 0.6, "Thermodynamique = haut de fourchette."),
    ]),
    ("Électricité / ventilation / chauffage", [
        ("Électricité neuve NF C 15-100", "m²", 77, 80, 130, "Non", 0.4, ""),
        ("VMC hygro B (4 SdE + WC)", "u", 1, 1500, 3000, "Non", 0.5, "Obligatoire : SdE et WC sans ouvrant."),
        ("Chauffage (radiateurs inertie ou PAC air/air)", "forfait", 1, 4000, 12000, "Non", 0.6, ""),
    ]),
    ("Menuiseries intérieures", [
        ("Portes battantes posées", "u", 7, 300, 550, "Oui", 0.6, "4 chambres, SdE 3-4, WC."),
        ("Portes à galandage (SdE 1-2) avec caisson", "u", 2, 700, 1200, "Oui", 0.6, ""),
        ("Façades rangements sous rampant", "u", 2, 300, 700, "Oui", 0.6, ""),
    ]),
    ("Revêtements / finitions", [
        ("Parquet chambres + dégagement", "m²", 51, 45, 90, "Oui", 0.6, ""),
        ("Carrelage sols SdE + WC", "m²", 14, 70, 130, "Oui", 0.5, ""),
        ("Faïence murale SdE", "m²", 40, 70, 130, "Oui", 0.5, ""),
        ("Peinture murs + plafonds", "m²", 300, 20, 33, "Oui", 0.25, ""),
    ]),
]

LIGNES_RDC = [
    ("Gros œuvre / structure", [
        ("Ouverture 4 m dans le pisé : étaiement, linteau béton ou acier, reprises", "forfait", 1, 6000, 15000, "Non", 0.4, "Intervention la plus lourde du RDC."),
        ("Étude BET structure (baie 4 m)", "forfait", 1, 1000, 2500, "Non", 0.5, "Obligatoire dans le pisé."),
        ("Sol : décaissement, hérisson ventilé, dalle isolée (chaux ou béton)", "m²", 72, 90, 180, "Non", 0.45, "Sol de grange brut ; dalle respirante conseillée avec le pisé."),
    ]),
    ("Menuiseries extérieures", [
        ("Baie vitrée 4,00 m à galandage, 2 vantaux, posée", "u", 1, 12000, 25000, "Non", 0.7, "Alu ou bois-alu, double vitrage ; caissons compris."),
        ("Seuil, bavette, raccords d'étanchéité baie", "forfait", 1, 800, 2000, "Non", 0.5, ""),
    ]),
    ("Isolation / doublage / plafond", [
        ("Doublage murs pisé (lame d'air + isolant perspirant + placo)", "m²", 79, 75, 130, "Oui", 0.5, "Périmètre 34 m × 2,60 m − baie."),
        ("Doublage épaissi au droit des caissons galandage", "ml", 4, 150, 300, "Oui", 0.5, "2 × 2 m."),
        ("Plafond sous plancher étage + isolation phonique", "m²", 72, 45, 80, "Oui", 0.45, "Ou poutres apparentes traitées."),
    ]),
    ("Électricité / chauffage", [
        ("Électricité séjour (prises, réseau, mur TV, éclairages table et billard)", "m²", 72, 70, 110, "Non", 0.4, ""),
        ("Chauffage (poêle à bois ou PAC air/air)", "forfait", 1, 4000, 12000, "Non", 0.6, "Poêle : conduit compris."),
    ]),
    ("Revêtements / finitions", [
        ("Revêtement de sol (parquet massif ou terre cuite)", "m²", 72, 50, 110, "Oui", 0.6, ""),
        ("Peinture / enduits murs + plafond", "m²", 150, 20, 35, "Oui", 0.25, "Enduit chaux possible."),
        ("Plinthes, finitions, habillage escalier", "forfait", 1, 600, 1500, "Oui", 0.5, "Escalier : compté dans l'onglet étage."),
    ]),
]


def feuille_budget(ws, titre, lignes, surface, libelle_total):
    ws["A1"] = titre; ws["A1"].font = TITLE
    ws["A2"] = ("Prix TTC indicatifs (marché France 2025-2026, entreprise), travaux seuls sans ameublement. "
                "Cellules en BLEU = à ajuster ; colonne JAUNE « Devis reçu » = à remplir au fil des devis.")
    ws["A2"].font = Font(name=F, italic=True, size=9)
    for j, h in enumerate(HEADS, start=1):
        c = ws.cell(HR, j, h); c.font = HEAD; c.fill = HEAD_FILL
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True); c.border = BOX
    ws.row_dimensions[HR].height = 32
    dv = DataValidation(type="list", formula1='"Oui,Non"', allow_blank=False)
    ws.add_data_validation(dv)
    r = HR + 1
    first = r
    for lot, items in lignes:
        ws.cell(r, 1, lot).font = BOLD
        for j in range(1, 16):
            ws.cell(r, j).fill = LOT_FILL; ws.cell(r, j).border = BOX
        r += 1
        for poste, unite, q, pmin, pmax, auto, mat, com in items:
            for j, v in {2: poste, 3: unite, 4: q, 5: pmin, 6: pmax, 9: auto, 10: mat, 15: com}.items():
                ws.cell(r, j, v)
            for j in (4, 5, 6, 9, 10):
                ws.cell(r, j).font = BLUE
            ws.cell(r, 7, f"=D{r}*E{r}"); ws.cell(r, 8, f"=D{r}*F{r}")
            ws.cell(r, 11, f'=IF(I{r}="Oui",G{r}*J{r},G{r})'); ws.cell(r, 12, f'=IF(I{r}="Oui",H{r}*J{r},H{r})')
            ws.cell(r, 13).fill = YELLOW; ws.cell(r, 13).font = BLUE
            ws.cell(r, 14, f"=IF(N(M{r})>0,M{r},(G{r}+H{r})/2)")
            for j in (2, 3, 7, 8, 11, 12, 14, 15):
                ws.cell(r, j).font = BLACK
            for j in (5, 6, 7, 8, 11, 12, 13, 14):
                ws.cell(r, j).number_format = EUR
            ws.cell(r, 10).number_format = PCT
            dv.add(ws.cell(r, 9))
            for j in range(1, 16):
                ws.cell(r, j).border = BOX
            r += 1
    last = r - 1
    r += 1

    def tot(label, formulas, bold=True, fill=None, font=None):
        nonlocal r
        ws.cell(r, 2, label).font = BOLD if bold else BLACK
        for col, f in formulas.items():
            c = ws.cell(r, col, f); c.number_format = EUR
            c.font = font or (BOLD if bold else BLACK)
        if fill:
            for j in range(1, 16):
                ws.cell(r, j).fill = fill
        r += 1
        return r - 1

    st = tot("Sous-total travaux", {c: f"=SUM({L}{first}:{L}{last})" for c, L in COLS.items()})
    imp = tot("Imprévus", {c: f"={L}{st}*Paramètres!$B$4" for c, L in COLS.items()}, bold=False, font=GREEN)
    moe = tot("Maîtrise d'œuvre", {c: f"={L}{st}*Paramètres!$B$5" for c, L in COLS.items()}, bold=False, font=GREEN)
    tt = tot(libelle_total, {c: f"={L}{st}+{L}{imp}+{L}{moe}" for c, L in COLS.items()}, fill=TOT_FILL)
    tot(f"Soit par m² ({surface} m²)", {c: f"={L}{tt}/{surface}" for c, L in COLS.items()}, bold=False)
    r += 1
    for n in [
        "Lecture : « Total min / max » = fourchette entreprise. « Auto min / max » = coût si vous réalisez vous-même les postes marqués « Oui »",
        "(vous ne payez alors que la part matériaux). « Montant retenu » = devis reçu s'il est saisi, sinon la moyenne min/max.",
        "Source : estimations indicatives de prix moyens du marché (ordre de grandeur), à remplacer par les devis d'artisans.",
    ]:
        ws.cell(r, 2, n).font = Font(name=F, italic=True, size=9); r += 1
    widths = {"A": 24, "B": 62, "C": 8, "D": 7, "E": 11, "F": 11, "G": 13, "H": 13, "I": 11, "J": 10,
              "K": 13, "L": 13, "M": 13, "N": 15, "O": 44}
    for k, v in widths.items():
        ws.column_dimensions[k].width = v
    ws.freeze_panes = "C5"
    ws["M4"].comment = Comment("Saisissez ici le montant TTC du devis : il remplace la moyenne dans « Montant retenu ».", "Claude")
    ws.sheet_view.zoomScale = 90
    return tt


tt_etage = feuille_budget(bs, "La Marinka — Budget estimatif aménagement de l'étage (77 m²)",
                          LIGNES_ETAGE, 77, "TOTAL ÉTAGE TTC")
rs = wb.create_sheet("Budget RDC", 1)
tt_rdc = feuille_budget(rs, "La Marinka — Budget estimatif travaux du rez-de-chaussée (77 m²)",
                        LIGNES_RDC, 77, "TOTAL RDC TTC")

# ------------------------------------------------------------ Synthèse
sy = wb.create_sheet("Synthèse", 0)
sy["A1"] = "La Marinka — Synthèse du budget travaux (hors ameublement)"; sy["A1"].font = TITLE
hd = ["Niveau", "Total min €", "Total max €", "Auto min €", "Auto max €", "Montant retenu €"]
for j, h in enumerate(hd, start=1):
    c = sy.cell(3, j, h); c.font = HEAD; c.fill = HEAD_FILL; c.border = BOX
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
src = [("Étage (4 chambres + 4 SdE + WC)", "'Budget étage'", tt_etage),
       ("Rez-de-chaussée (séjour, baie galandage)", "'Budget RDC'", tt_rdc)]
for i, (lab, sh, row) in enumerate(src, start=4):
    sy.cell(i, 1, lab).font = BLACK
    for j, L in enumerate(("G", "H", "K", "L", "N"), start=2):
        c = sy.cell(i, j, f"={sh}!{L}{row}"); c.font = GREEN; c.number_format = EUR; c.border = BOX
    sy.cell(i, 1).border = BOX
sy.cell(6, 1, "TOTAL TRAVAUX TTC").font = BOLD
for j in range(2, 7):
    L = "ABCDEF"[j - 1]
    c = sy.cell(6, j, f"=SUM({L}4:{L}5)"); c.font = BOLD; c.number_format = EUR
for j in range(1, 7):
    sy.cell(6, j).fill = TOT_FILL; sy.cell(6, j).border = BOX
sy.cell(8, 1, "Postes hors budget (Paramètres)").font = BOLD
sy.cell(8, 2, f"=Paramètres!B{HORS_TOT}").font = GREEN; sy.cell(8, 2).number_format = EUR
sy.cell(8, 3, f"=Paramètres!C{HORS_TOT}").font = GREEN; sy.cell(8, 3).number_format = EUR
sy.cell(9, 1, "Enveloppe globale (travaux + hors budget)").font = BOLD
sy.cell(9, 2, "=B6+B8").font = BOLD; sy.cell(9, 2).number_format = EUR
sy.cell(9, 3, "=C6+C8").font = BOLD; sy.cell(9, 3).number_format = EUR
sy.cell(11, 1, "Ameublement non compris. Escalier compté une seule fois (onglet étage).").font = Font(name=F, italic=True, size=9)
sy.column_dimensions["A"].width = 46
for L in "BCDEF":
    sy.column_dimensions[L].width = 16

wb.calculation.fullCalcOnLoad = True
wb.save("/home/user/djgedeon/la-marinka/La Marinka.xlsx")
print("ok")
