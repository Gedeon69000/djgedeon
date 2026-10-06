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
    ("Raccordements eau / électricité / assainissement individuel", 8000, 15000, "Selon raccordement existant de la grange."),
    ("Renfort du plancher / chape", 5000, 12000, "Si le plancher de l'étage est insuffisant."),
    ("Taxe d'aménagement + dossier changement de destination", 2000, 5000, "Selon taux communal et départemental."),
    ("Mise à niveau de l'assainissement (microstation 5 EH → 7 EH mini)", 10000, 15000, "Promesse : OXYFIX C-90 5 EH pour 3 pièces principales ; 6 chambres = 7 EH. Étude + accord SPANC."),
    ("Électricité de la maison existante (anomalies au diagnostic)", 6000, 10000, "Diagnostic 09/2025 : différentiel, terre, SdB, matériel vétuste."),
    ("Désamiantage conduit en cave (si touché)", 1000, 3000, "Repérage amiante 09/2025 : conduit de fluides, évaluation périodique."),
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

LIGNES_TOITURE = [
    ("Couverture (260 m²)", [
        ("Dépose de la couverture existante + évacuation", "m²", 260, 15, 30, "Non", 0.3, ""),
        ("Écran sous-toiture HPV + contre-liteaux + liteaux neufs", "m²", 260, 25, 45, "Non", 0.5, ""),
        ("Tuiles neuves terre cuite, fourniture + pose", "m²", 260, 50, 90, "Non", 0.6, "Tuiles canal / anciennes : prendre le haut de fourchette ou plus."),
        ("Faîtage, rives, arêtiers (scellés ou à sec)", "ml", 60, 35, 70, "Non", 0.5, "Linéaire à métrer."),
        ("Zinguerie : gouttières, descentes, noues", "ml", 40, 40, 80, "Non", 0.5, "Zinc ou alu."),
    ]),
    ("Façades (maison + grange)", [
        ("Ravalement sur pisé : piquage, réparations, enduit chaux 3 couches", "m²", 400, 60, 120, "Non", 0.35, "Surface de façades à métrer (≈ 250 m² grange + 150 à 250 m² maison). Jamais d'enduit ciment sur le pisé."),
        ("Encadrements, appuis, soubassement drainant (anti-remontées)", "forfait", 1, 2000, 6000, "Non", 0.4, ""),
    ]),
    ("Charpente / sécurité", [
        ("Reprise ponctuelle de charpente + traitement insectes / champignons", "forfait", 1, 2000, 10000, "Non", 0.4, "Selon diagnostic ; reprise lourde non comprise."),
        ("Échafaudage, protections, sécurité (toiture + façades)", "forfait", 1, 4000, 10000, "Non", 0.3, "À mutualiser entre couvreur et façadier."),
    ]),
]

OPTION_SARKING = [
    ("Isolation sarking fibre de bois 160-200 mm + pare-pluie (sur chevrons)", "m²", 260, 80, 150, "Non", 0.55, "Charpente apparente à l'étage, R ≈ 4 à 5."),
    ("Rehausse des rives et adaptation zinguerie à l'épaisseur d'isolant", "forfait", 1, 1500, 4000, "Non", 0.5, ""),
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

# ------------------------------------------------------------ Toiture + option sarking
ts = wb.create_sheet("Budget Toiture", 2)
tt_toit = feuille_budget(ts, "La Marinka — Budget estimatif toiture (260 m²) et ravalement des façades",
                         LIGNES_TOITURE, 260, "TOTAL TOITURE + FAÇADES TTC (sans sarking)")
r = ts.max_row + 2
ts.cell(r, 1, "OPTION SARKING").font = HEAD
for j in range(1, 16):
    ts.cell(r, j).fill = HEAD_FILL
ts.cell(r, 2, "Isolation posée par l'extérieur pendant la réfection (remplace l'isolation intérieure des rampants de l'étage)").font = HEAD
r += 1
o_first = r
for poste, unite, q, pmin, pmax, auto, mat, com in OPTION_SARKING:
    for jj, v in {2: poste, 3: unite, 4: q, 5: pmin, 6: pmax, 9: auto, 10: mat, 15: com}.items():
        ts.cell(r, jj, v)
    for jj in (4, 5, 6, 9, 10):
        ts.cell(r, jj).font = BLUE
    ts.cell(r, 7, f"=D{r}*E{r}"); ts.cell(r, 8, f"=D{r}*F{r}")
    ts.cell(r, 11, f'=IF(I{r}="Oui",G{r}*J{r},G{r})'); ts.cell(r, 12, f'=IF(I{r}="Oui",H{r}*J{r},H{r})')
    ts.cell(r, 13).fill = YELLOW; ts.cell(r, 13).font = BLUE
    ts.cell(r, 14, f"=IF(N(M{r})>0,M{r},(G{r}+H{r})/2)")
    for jj in (5, 6, 7, 8, 11, 12, 13, 14):
        ts.cell(r, jj).number_format = EUR
    ts.cell(r, 10).number_format = PCT
    for jj in range(1, 16):
        ts.cell(r, jj).border = BOX
        if ts.cell(r, jj).font != BLUE:
            ts.cell(r, jj).font = BLACK if jj not in (4, 5, 6, 9, 10) else BLUE
    r += 1
o_last = r - 1
# ligne d'isolation des rampants dans l'onglet étage (économisée si sarking)
ramp = next(rr for rr in range(5, bs.max_row + 1) if str(bs.cell(rr, 2).value).startswith("Isolation rampants"))
def ligne(label, formulas, bold=False, fill=None, font=None):
    global r
    ts.cell(r, 2, label).font = BOLD if bold else BLACK
    for col, f in formulas.items():
        c = ts.cell(r, col, f); c.number_format = EUR; c.font = font or (BOLD if bold else BLACK)
    if fill:
        for jj in range(1, 16):
            ts.cell(r, jj).fill = fill
    r += 1
    return r - 1
o_st = ligne("Sous-total option sarking", {c: f"=SUM({L}{o_first}:{L}{o_last})" for c, L in COLS.items()}, bold=True)
o_eco = ligne("Économie : isolation intérieure des rampants supprimée (onglet étage)",
              {c: f"=-'Budget étage'!{L}{ramp}" for c, L in COLS.items()}, font=GREEN)
o_net = ligne("SURCOÛT NET OPTION SARKING TTC (imprévus + MOE inclus)",
              {c: f"=({L}{o_st}+{L}{o_eco})*(1+Paramètres!$B$4+Paramètres!$B$5)" for c, L in COLS.items()},
              bold=True, fill=TOT_FILL)
ts.cell(r + 1, 2, "Le sarking garde la charpente apparente, libère quelques cm de hauteur sous rampant et facilite la pose étanche des Velux.").font = Font(name=F, italic=True, size=9)

# ------------------------------------------------------------ Synthèse
sy = wb.create_sheet("Synthèse", 0)
sy["A1"] = "La Marinka — Synthèse du budget travaux (hors ameublement)"; sy["A1"].font = TITLE
hd = ["Poste", "Total min €", "Total max €", "Auto min €", "Auto max €", "Montant retenu €"]
for j, h in enumerate(hd, start=1):
    c = sy.cell(3, j, h); c.font = HEAD; c.fill = HEAD_FILL; c.border = BOX
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
src = [("Étage (4 chambres + 4 SdE + WC)", "'Budget étage'", tt_etage),
       ("Rez-de-chaussée (séjour, baie galandage)", "'Budget RDC'", tt_rdc),
       ("Toiture 260 m² + ravalement des façades", "'Budget Toiture'", tt_toit)]
for i, (lab, sh, row) in enumerate(src, start=4):
    sy.cell(i, 1, lab).font = BLACK; sy.cell(i, 1).border = BOX
    for j, L in enumerate(("G", "H", "K", "L", "N"), start=2):
        c = sy.cell(i, j, f"={sh}!{L}{row}"); c.font = GREEN; c.number_format = EUR; c.border = BOX

def ligne_sy(rr, label, formulas, bold=True, fill=None, font=None):
    sy.cell(rr, 1, label).font = BOLD if bold else BLACK
    for j, f in formulas.items():
        c = sy.cell(rr, j, f); c.number_format = EUR; c.font = font or (BOLD if bold else BLACK)
    for j in range(1, 7):
        sy.cell(rr, j).border = BOX
        if fill:
            sy.cell(rr, j).fill = fill

LET = "ABCDEF"
ligne_sy(7, "TOTAL TRAVAUX TTC — sans sarking", {j: f"=SUM({LET[j-1]}4:{LET[j-1]}6)" for j in range(2, 7)}, fill=TOT_FILL)
ligne_sy(8, "Option sarking : surcoût net (onglet Toiture)",
         {j: f"='Budget Toiture'!{L}{o_net}" for j, L in zip(range(2, 7), ("G", "H", "K", "L", "N"))}, bold=False, font=GREEN)
ligne_sy(9, "TOTAL TRAVAUX TTC — avec sarking", {j: f"={LET[j-1]}7+{LET[j-1]}8" for j in range(2, 7)}, fill=TOT_FILL)
ligne_sy(11, "Postes hors budget (Paramètres)", {2: f"=Paramètres!B{HORS_TOT}", 3: f"=Paramètres!C{HORS_TOT}"}, font=GREEN)
ligne_sy(12, "Enveloppe globale sans sarking", {2: "=B7+B11", 3: "=C7+C11"})
ligne_sy(13, "Enveloppe globale avec sarking", {2: "=B9+B11", 3: "=C9+C11"})
sy.cell(15, 1, "Ameublement non compris. Escalier compté une seule fois (onglet étage). Prix TTC indicatifs, à remplacer par les devis.").font = Font(name=F, italic=True, size=9)
sy.column_dimensions["A"].width = 50
for L in "BCDEF":
    sy.column_dimensions[L].width = 16

# ------------------------------------------------------------ Estimation de revente
ev = wb.create_sheet("Estimation revente", 1)
ev.sheet_view.zoomScale = 90
WRAP = Alignment(wrap_text=True, vertical="top")
ITAL = Font(name=F, italic=True, size=9)
H2 = Font(name=F, bold=True, size=12, color="5B4636")


def entete(row, titres):
    for j, h in enumerate(titres, start=1):
        c = ev.cell(row, j, h); c.font = HEAD; c.fill = HEAD_FILL; c.border = BOX
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ev.row_dimensions[row].height = 30


def ecrire(row, vals, fonts=None, fmts=None):
    for j, v in enumerate(vals, start=1):
        c = ev.cell(row, j, v); c.border = BOX; c.alignment = WRAP
        c.font = (fonts or {}).get(j, BLACK)
        if fmts and j in fmts:
            c.number_format = fmts[j]


ev["A1"] = "La Marinka — Estimation de la valeur de revente après travaux"; ev["A1"].font = TITLE
ev["A2"] = ("139 impasse du Brézet, 38440 Sainte-Anne-sur-Gervonde. Estimation indicative (octobre 2026), établie à partir des "
            "prix publiés et d'annonces ; à confirmer par des ventes réelles (DVF) et des avis de valeur d'agences locales.")
ev["A2"].font = ITAL

# --- 1. Hypothèses
r = 4
ev.cell(r, 1, "1. Hypothèses du bien").font = H2; r += 1
entete(r, ["Paramètre", "Valeur", "Commentaire"]); r += 1
HYP = {}
for lab, val, fmt, com in [
    ("Surface habitable finale (m²)", 232, "0", "90 m² maison + 72 m² RDC grange + 69 m² étage ; l'étage sous rampant peut descendre à 55-62 m² légaux."),
    ("Terrain (m²)", 1987, "0", "Cadastre B1861+1860 = 1 487 m² d'un seul tenant autour de la maison ; B1160+1163 = 500 m² détachés de l'autre côté de l'impasse (servitude d'écoulement)."),
    ("Prix d'achat frais de notaire compris (€)", 200000, EUR, "Donnée fournie."),
    ("Extérieurs hors budget travaux (€) : piscine, jacuzzi, pergola, paysager, irrigation", 85000, EUR, "Hypothèse centrale (60 à 110 k€) : non chiffrés dans les onglets travaux."),
    ("Grange attenante, partie non aménagée : surface utile (m²)", 500, "0", "≈ 300 m² au sol + 200 m² à l'étage (écuries, granges, combles). Sol terre battue, plafonds paille ; 70 m² de toiture refaits en 2024 seulement. Non habitable."),
    ("DPE maison existante", "E (258 kWh/m².an) — GES B", "@", "Diagnostic 09/2025 ; audit 2023 : G avant isolation des combles et poêle."),
]:
    ecrire(r, [lab, val, com], fonts={2: BLUE}, fmts={2: fmt}); HYP[lab.split(" (")[0]] = r; r += 1
R_SURF, R_ACHAT, R_EXT = HYP["Surface habitable finale"], HYP["Prix d'achat frais de notaire compris"], HYP["Extérieurs hors budget travaux"]

# --- 2. Marché local
r += 1
ev.cell(r, 1, "2. Prix du marché local (maisons)").font = H2; r += 1
entete(r, ["Commune", "€/m² maison", "Nature de la donnée"]); r += 1
for com, prix, nat in [
    ("Sainte-Anne-sur-Gervonde", "1 983 (DVF 2025, 6 ventes) à 2 286-2 458", "Ventes réelles / estimations agrégateurs ; tendance 12 mois en baisse"),
    ("Châtonnay", "2 301-2 362", "Estimation"),
    ("Saint-Jean-de-Bournay", "2 223-2 458", "Estimation ; pic 2 589 en 2022 puis repli"),
    ("Meyrieu-les-Étangs", "2 321", "Estimation ; -12,6 % sur un an"),
    ("Villeneuve-de-Marc", "2 333", "Estimation"),
    ("Savas-Mépin", "2 504", "Estimation"),
    ("Artas", "2 742", "Estimation"),
    ("Beauvoir-de-Marc", "2 952", "Estimation ; commune plus proche de Lyon"),
    ("Grandes maisons vendues à Saint-Jean-de-Bournay (202-235 m²)", "1 213-1 906", "Ventes réelles : forte décote au m² des grandes surfaces"),
]:
    ecrire(r, [com, prix, nat]); r += 1

# --- 3. Comparables
r += 1
ev.cell(r, 1, "3. Biens comparables").font = H2; r += 1
entete(r, ["Commune", "Habitable", "Terrain", "Dépendances", "Piscine", "État", "Statut", "Prix €", "€/m²", "Comparabilité"]); r += 1
for row in [
    ("Saint-Jean-de-Bournay", "293 m², 6 ch.", "4 800 m²", "n.c.", "Oui", "Bon (présumé)", "Affiché", 580000, 1980, "Élevée : plafond affiché du secteur"),
    ("Saint-Jean-de-Bournay", "169 m², 6 ch.", "2 513 m²", "n.c.", "Oui", "Standard", "Affiché", 383000, 2266, "Moyenne (plus petit)"),
    ("Beauvoir-de-Marc", "n.c.", "1 514 m²", "n.c.", "Oui (creusée)", "n.c.", "Affiché", 502000, None, "Moyenne (commune plus chère)"),
    ("Collines dauphinoises (Safer)", "≈ 250 m², pisé", "1,9 ha", "Bâtiment agricole pisé aménagé", "n.c.", "Rénové", "Affiché HFS", 570000, 2280, "Moyenne à élevée (pisé + grande dépendance)"),
    ("Secteur Vienne (3 min A7)", "220 m², 6 ch.", "1 125 m²", "n.c.", "Oui", "Pierre, rénové", "Affiché", 630000, 2864, "Faible à moyenne (emplacement supérieur)"),
    ("Châtonnay", "≈ 300 m²", "1 000 m²", "n.c.", "Oui", "Tout à rénover", "Affiché", 275000, 917, "Faible (illustre la décote travaux)"),
    ("Saint-Jean-de-Bournay", "202 m²", "n.c.", "n.c.", "n.c.", "n.c.", "Vendu", 385000, 1906, "Moyenne (vente réelle)"),
    ("Lieudieu", "300 m², 6 ch.", "9 702 m²", "Domaine", "n.c.", "Exception", "Affiché", 1290000, 4300, "Très faible (hors norme)"),
    ("Satolas (Nord-Isère) — dépendance seule", "—", "—", "Hangars 2 680 m²", "—", "—", "Affiché", 230000, 86, "Référence grange"),
    ("Isère — dépendance seule", "—", "—", "Grange 727 m²", "—", "—", "Affiché", 120000, 165, "Référence grange"),
]:
    ecrire(r, list(row), fmts={8: EUR, 9: '#,##0 "€/m²";;"n.c."'}); r += 1
ev.cell(r, 1, "Aucune vente réelle documentée > 500 000 € dans la commune ni dans les communes limitrophes.").font = ITAL; r += 1
ev.cell(r, 1, "Points relevés dans la promesse de vente (10/2025) : mitoyenneté avec la parcelle voisine dont le propriétaire envisage une démolition ; servitude d'eau (bélier hydraulique) ; "
              "absence de puits déclaré ; sismicité 3/5 ; commune en zone inondation (CatNat 1982-1993).").font = ITAL; r += 1

# --- 4. Construction de la valeur
r += 1
ev.cell(r, 1, "4. Construction de la valeur (approche par composantes)").font = H2; r += 1
entete(r, ["Composante", "Bas €", "Central €", "Haut €", "Justification"]); r += 1
c0 = r
for lab, lo, mid, hi, why in [
    ("Maison rénovée ≈ 230 m² (hors extérieurs)", 450000, 485000, 530000, "2 050-2 350 €/m² : grande maison de caractère rénovée, décote des grandes surfaces."),
    ("Piscine enterrée 3 × 5 m", 15000, 20000, 25000, "Atout réel mais perçu aussi comme une charge d'entretien."),
    ("Pergola bioclimatique + espace repas", 5000, 7500, 10000, ""),
    ("Jacuzzi, pétanque, brasero, barbecue", 0, 2500, 5000, "Équipements, pas de valeur foncière."),
    ("Calme absolu (impasse de 3 maisons)", 10000, 15000, 20000, "Prime réelle mais fréquente en secteur rural."),
    ("Puits fonctionnel + irrigation du jardin", 5000, 7500, 10000, "Utile sur 1 700 m² ; usage limitable par arrêtés sécheresse."),
    ("Façades neuves (enduit chaux)", 10000, 12500, 15000, "Évite la décote « ravalement à prévoir »."),
    ("Partie non aménagée de la grange ≈ 500 m² utiles (sol terre, pas de dalle)", 25000, 45000, 70000, "50-140 €/m² utile en l'état ; +20 à +30 k€ si dalle béton et toiture complète. Acheteurs ciblés."),
    ("Ajustement plafond de marché local / délai", -25000, -30000, -66000, "Bien au sommet du marché local : peu d'acheteurs, négociation 5-10 %."),
]:
    ecrire(r, [lab, lo, mid, hi, why], fonts={2: BLUE, 3: BLUE, 4: BLUE}, fmts={2: EUR, 3: EUR, 4: EUR}); r += 1
c1 = r - 1
ecrire(r, ["VALEUR ESTIMÉE", f"=SUM(B{c0}:B{c1})", f"=SUM(C{c0}:C{c1})", f"=SUM(D{c0}:D{c1})", "Bas ≈ vente rapide ; central = valeur retenue ; haut = annonce ambitieuse."],
       fonts={1: BOLD, 2: BOLD, 3: BOLD, 4: BOLD}, fmts={2: EUR, 3: EUR, 4: EUR})
for j in range(1, 6):
    ev.cell(r, j).fill = TOT_FILL
R_VAL = r; r += 1
ecrire(r, ["Option non comprise : grange identifiée « changement de destination » au PLUi", 0, 0, 50000,
           "À ne compter que si confirmé en mairie (PLUi Région Saint-Jeannaise + avis CDPENAF en zone A)."],
       fonts={2: BLUE, 3: BLUE, 4: BLUE}, fmts={2: EUR, 3: EUR, 4: EUR}); r += 1

# --- 5. Scénarios
r += 1
ev.cell(r, 1, "5. Scénarios de vente").font = H2; r += 1
entete(r, ["Scénario", "Prix €", "€/m² habitable", "€/m² hors grange", "Délai probable", "Commentaire"]); r += 1
s0 = r
for lab, prix, delai, com in [
    ("Vente rapide", f"=B{R_VAL}", "< 3 mois", ""),
    ("Valeur de marché réaliste", f"=C{R_VAL}", "6 à 9 mois", "= valeur centrale ; fourchette ± 15 k€."),
    ("Annonce ambitieuse mais défendable", f"=D{R_VAL}", "9 à 18 mois", "Négociation probable vers 590-600 k€."),
    ("VALEUR CENTRALE RETENUE", f"=C{R_VAL}", "", "Maison ≈ 515 k€ + calme / puits / façades + grange ≈ 65 k€, après plafond de marché."),
]:
    bold = lab.startswith("VALEUR")
    ecrire(r, [lab, prix, f"=B{r}/$B${R_SURF}", f"=(B{r}-$C${c0 + 7})/$B${R_SURF}", delai, com],
           fonts={1: BOLD if bold else BLACK, 2: BOLD if bold else (BLUE if isinstance(prix, int) else BLACK)},
           fmts={2: EUR, 3: '#,##0 "€/m²"', 4: '#,##0 "€/m²"'})
    if bold:
        for j in range(1, 7):
            ev.cell(r, j).fill = TOT_FILL
    r += 1
R_CENTRALE = r - 1

# --- 6. Seuils
r += 1
ev.cell(r, 1, "6. Ces prix sont-ils réalistes ?").font = H2; r += 1
entete(r, ["Prix", "€/m² habitable", "Verdict", "Pourquoi"]); r += 1
for prix, verdict, why in [
    (600000, "Objectif haut atteignable", "Exécution parfaite + acheteur qui valorise la grange ; haut de la fourchette, pas le cas de base."),
    (650000, "Prix d'annonce, pas de vente", "Au-dessus de tout ce qui s'affiche localement hors cas d'exception."),
    (700000, "Irréaliste aujourd'hui", "≈ 3 000 €/m², > 50 % au-dessus des ventes réelles de la commune ; aucun comparable."),
]:
    ecrire(r, [prix, f"=A{r}/$B${R_SURF}", verdict, why], fonts={1: BLUE, 3: BOLD}, fmts={1: EUR, 2: '#,##0 "€/m²"'}); r += 1

# --- 7. Coût vs valeur
r += 1
ev.cell(r, 1, "7. Coût total du projet face à la valeur").font = H2; r += 1
entete(r, ["Élément", "Montant €", "Source"]); r += 1
k0 = r
ecrire(r, ["Prix d'achat", f"=B{R_ACHAT}", "Hypothèses"], fonts={2: GREEN}, fmts={2: EUR}); r += 1
ecrire(r, ["Travaux (étage + RDC + toiture + façades), montant retenu sans sarking", "=Synthèse!F7", "Onglet Synthèse"], fonts={2: GREEN}, fmts={2: EUR}); r += 1
ecrire(r, ["Postes hors budget (moyenne)", f"=(Paramètres!B{HORS_TOT}+Paramètres!C{HORS_TOT})/2", "Onglet Paramètres"], fonts={2: GREEN}, fmts={2: EUR}); r += 1
ecrire(r, ["Extérieurs (piscine, jacuzzi, pergola, paysager…)", f"=B{R_EXT}", "Hypothèses"], fonts={2: GREEN}, fmts={2: EUR}); r += 1
ecrire(r, ["COÛT TOTAL DU PROJET", f"=SUM(B{k0}:B{r - 1})", ""], fonts={1: BOLD, 2: BOLD}, fmts={2: EUR})
R_COUT = r; r += 1
ecrire(r, ["Valeur centrale retenue", f"=B{R_CENTRALE}", "Section 5"], fonts={2: GREEN}, fmts={2: EUR}); r += 1
ecrire(r, ["PLUS / MOINS-VALUE LATENTE", f"=B{r - 1}-B{R_COUT}", "Négatif = le marché ne rembourse pas tout l'investissement"],
       fonts={1: BOLD, 2: BOLD}, fmts={2: '#,##0 €;[Red]-#,##0 €'})
for j in range(1, 4):
    ev.cell(r, j).fill = TOT_FILL
r += 2

# --- 8. Facteurs de variation
ev.cell(r, 1, "8. Ce qui peut faire varier la valeur de ± 50 k€ ou plus").font = H2; r += 1
entete(r, ["Facteur", "Sens", "Impact estimé"]); r += 1
for fac, sens, imp in [
    ("Grange identifiée « changement de destination » au PLUi", "+", "+20 à +50 k€"),
    ("DPE A/B (sarking, PAC, pisé sain)", "+", "+10 à +30 k€"),
    ("Maison existante rénovée au même niveau, cuisine ouverte vers le séjour", "+", "+15 à +40 k€"),
    ("Historique Airbnb 12-24 mois avec comptes certifiés", "+", "+10 à +40 k€ (acheteur investisseur)"),
    ("Acheteur collectionneur / artisan valorisant la grange", "+", "+20 à +50 k€"),
    ("Maison existante pas au niveau de la grange (effet « deux bâtiments »)", "−", "−30 à −60 k€"),
    ("Surface habitable légale réduite par les rampants", "−", "−10 à −30 k€ (lecture de l'annonce)"),
    ("DPE D ou pire, humidité dans le pisé", "−", "−20 à −50 k€"),
    ("Assainissement non conforme (SPANC)", "−", "−10 à −25 k€"),
    ("Dossiers incomplets : changement de destination, DAACT, amiante grange", "−", "Blocage ou −20 à −50 k€"),
    ("Hausse des taux de crédit", "−", "−5 à −10 % de la valeur"),
    ("Bien perçu comme « gîte » plutôt que maison familiale", "−", "−10 à −30 k€"),
]:
    ecrire(r, [fac, sens, imp], fonts={2: BOLD}); r += 1

# --- 9. Sources
r += 1
ev.cell(r, 1, "9. Sources").font = H2; r += 1
for lab, url in [
    ("Square Habitat – Sainte-Anne-sur-Gervonde", "https://www.squarehabitat.fr/prix-immobilier/auvergne-rhone-alpes/isere/sainte-anne-sur-gervonde-38440"),
    ("PAP – Sainte-Anne-sur-Gervonde", "https://www.pap.fr/vendeur/prix-m2/sainte-anne-sur-gervonde-38440-g21905"),
    ("Immovrai – Sainte-Anne-sur-Gervonde (DVF)", "https://www.immovrai.com/prix-immobilier/auvergne-rhone-alpes/isere/38440-sainte-anne-sur-gervonde"),
    ("Immovrai – Châtonnay", "https://www.immovrai.com/prix-immobilier/auvergne-rhone-alpes/isere/38440-chatonnay"),
    ("Immovrai – Meyrieu-les-Étangs", "https://www.immovrai.com/prix-immobilier/auvergne-rhone-alpes/isere/38440-meyrieu-les-etangs"),
    ("PAP – Saint-Jean-de-Bournay", "https://www.pap.fr/vendeur/prix-m2/saint-jean-de-bournay-38440-g21897"),
    ("MeilleursAgents – Saint-Jean-de-Bournay", "https://www.meilleursagents.com/prix-immobilier/saint-jean-de-bournay-38440/"),
    ("PAP – Beauvoir-de-Marc", "https://www.pap.fr/vendeur/prix-m2/beauvoir-de-marc-38440-g21845"),
    ("Logic-immo – maisons avec piscine à Saint-Jean-de-Bournay", "https://www.logic-immo.com/maison-saint-jean-de-bournay/vente-maison-saint-jean-de-bournay/maison-avec-piscine-saint-jean-de-bournay-38440-28320_2.html"),
    ("Nestenn – Beauvoir-de-Marc, maison avec piscine", "https://immobilier-heyrieux.nestenn.com/beauvoir-de-marc-maison-a-vendre-avec-piscine-au-calme-dpe-d-ref-38743724"),
    ("Propriétés Rurales – corps de ferme rénové", "https://www.proprietes-rurales.com/immobilier/vente-propriete-agricole-elevage-isere-fr_VN23101.htm"),
    ("Belles Demeures – secteur Vienne", "https://www.bellesdemeures.com/vente/france/rhone-alpes/isere/vienne/maison-luxe-option-piscine/tt-2-tb-2-opt-1-pl-16210/"),
    ("Zimo – hangars à vendre en Isère", "https://www.zimo.fr/annonces/immobilier-professionnel/vente/hangar/isere-38"),
    ("French Property – hangars Nord-Isère", "https://www.french-property.com/sale-property/3772-An88y0i9gsieel8p"),
    ("MRAe – PLUi Bièvre Isère, secteur Région Saint-Jeannaise", "https://www.mrae.developpement-durable.gouv.fr/IMG/pdf/2023acara4_mod2-plui-bievreiserecommunaute-secteurregionsaintjeannaise_ys.pdf"),
    ("DVF officiel (ventes réelles, à consulter)", "https://app.dvf.etalab.gouv.fr"),
]:
    c = ev.cell(r, 1, lab); c.font = Font(name=F, color="0563C1", underline="single"); c.hyperlink = url; r += 1

for col, w in zip("ABCDEFGHIJ", (52, 18, 18, 22, 14, 18, 12, 14, 12, 34)):
    ev.column_dimensions[col].width = w
ev.column_dimensions["E"].width = 40
ev.column_dimensions["F"].width = 34

wb.calculation.fullCalcOnLoad = True
wb.save("/home/user/djgedeon/la-marinka/La Marinka.xlsx")
print("ok")
