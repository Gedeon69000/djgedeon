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

# ------------------------------------------------------------ Budget étage
bs["A1"] = "La Marinka — Budget estimatif aménagement de l'étage (77 m²)"; bs["A1"].font = TITLE
bs["A2"] = ("Prix TTC indicatifs (marché France 2025-2026, entreprise). Cellules en BLEU = à ajuster ; "
            "colonne JAUNE « Devis reçu » = à remplir au fil des devis (remplace alors la moyenne).")
bs["A2"].font = Font(name=F, italic=True, size=9)
heads = ["Lot", "Poste", "Unité", "Qté", "PU min €", "PU max €", "Total min €", "Total max €",
         "Faisable soi-même", "Part matériaux", "Auto min €", "Auto max €", "Devis reçu €", "Montant retenu €", "Commentaire"]
HR = 4
for j, h in enumerate(heads, start=1):
    c = bs.cell(HR, j, h); c.font = HEAD; c.fill = HEAD_FILL
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True); c.border = BOX
bs.row_dimensions[HR].height = 32

lignes = [
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

dv = DataValidation(type="list", formula1='"Oui,Non"', allow_blank=False)
bs.add_data_validation(dv)
r = HR + 1
first = r
for lot, items in lignes:
    bs.cell(r, 1, lot).font = BOLD
    for j in range(1, 16):
        bs.cell(r, j).fill = LOT_FILL; bs.cell(r, j).border = BOX
    r += 1
    for poste, unite, q, pmin, pmax, auto, mat, com in items:
        vals = {2: poste, 3: unite, 4: q, 5: pmin, 6: pmax, 9: auto, 10: mat, 15: com}
        for j, v in vals.items():
            bs.cell(r, j, v)
        for j in (4, 5, 6, 9, 10):
            bs.cell(r, j).font = BLUE
        bs.cell(r, 7, f"=D{r}*E{r}"); bs.cell(r, 8, f"=D{r}*F{r}")
        bs.cell(r, 11, f'=IF(I{r}="Oui",G{r}*J{r},G{r})'); bs.cell(r, 12, f'=IF(I{r}="Oui",H{r}*J{r},H{r})')
        bs.cell(r, 13).fill = YELLOW; bs.cell(r, 13).font = BLUE
        bs.cell(r, 14, f"=IF(N(M{r})>0,M{r},(G{r}+H{r})/2)")
        for j in (2, 3, 7, 8, 11, 12, 14, 15):
            bs.cell(r, j).font = BLACK
        for j in (5, 6, 7, 8, 11, 12, 13, 14):
            bs.cell(r, j).number_format = EUR
        bs.cell(r, 10).number_format = PCT
        dv.add(bs.cell(r, 9))
        for j in range(1, 16):
            bs.cell(r, j).border = BOX
        r += 1
last = r - 1

r += 1
def tot(label, formulas, bold=True, fill=None, font=None):
    global r
    bs.cell(r, 2, label).font = BOLD if bold else BLACK
    for col, f in formulas.items():
        c = bs.cell(r, col, f); c.number_format = EUR
        c.font = font or (BOLD if bold else BLACK)
    if fill:
        for j in range(1, 16):
            bs.cell(r, j).fill = fill
    r += 1
    return r - 1

cols = {7: "G", 8: "H", 11: "K", 12: "L", 14: "N"}
st = tot("Sous-total travaux", {c: f"=SUM({L}{first}:{L}{last})" for c, L in cols.items()})
imp = tot("Imprévus", {c: f"={L}{st}*Paramètres!$B$4" for c, L in cols.items()}, bold=False, font=GREEN)
moe = tot("Maîtrise d'œuvre", {c: f"={L}{st}*Paramètres!$B$5" for c, L in cols.items()}, bold=False, font=GREEN)
tt = tot("TOTAL ÉTAGE TTC", {c: f"={L}{st}+{L}{imp}+{L}{moe}" for c, L in cols.items()}, fill=TOT_FILL)
tot("Soit par m² (77 m²)", {c: f"={L}{tt}/77" for c, L in cols.items()}, bold=False)
r += 1
bs.cell(r, 2, "Postes hors budget (voir onglet Paramètres)").font = BOLD
bs.cell(r, 7, f"=Paramètres!B{HORS_TOT}").font = GREEN; bs.cell(r, 7).number_format = EUR
bs.cell(r, 8, f"=Paramètres!C{HORS_TOT}").font = GREEN; bs.cell(r, 8).number_format = EUR
r += 2
notes = [
    "Lecture : « Total min / max » = fourchette entreprise. « Auto min / max » = coût si vous réalisez vous-même les postes marqués « Oui »",
    "(vous ne payez alors que la part matériaux). « Montant retenu » = devis reçu s'il est saisi, sinon la moyenne min/max.",
    "Source : estimations indicatives de prix moyens du marché (ordre de grandeur), à remplacer par les devis d'artisans.",
]
for n in notes:
    bs.cell(r, 2, n).font = Font(name=F, italic=True, size=9); r += 1

widths = {"A": 22, "B": 58, "C": 8, "D": 7, "E": 11, "F": 11, "G": 13, "H": 13, "I": 11, "J": 10,
          "K": 13, "L": 13, "M": 13, "N": 15, "O": 40}
for k, v in widths.items():
    bs.column_dimensions[k].width = v
bs.freeze_panes = "C5"
bs["M4"].comment = Comment("Saisissez ici le montant TTC du devis : il remplace la moyenne dans « Montant retenu ».", "Claude")
bs.sheet_view.zoomScale = 90

wb.calculation.fullCalcOnLoad = True
wb.save("/home/user/djgedeon/la-marinka/La Marinka.xlsx")
print("ok")
