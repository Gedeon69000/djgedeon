// Housse anti-poussière pour Pioneer DJM-V10 / DJM-V10-LF
// 100 % imprimable : 4 quarts (chacun ~224 x 238 mm) vissés entre eux
// par des ailettes internes (vis M3 x 12 + écrous). Rien ne dépasse à l'extérieur.
//
// piece = "avant_gauche" | "avant_droite" | "arriere_gauche" | "arriere_droite" | "assemblage"
// Impression : tel que généré (dessus de la housse posé sur le plateau), sans supports.
piece = "assemblage";

/* ---- Table de mixage (fiche Pioneer) ---- */
mix_l = 437.6;   // largeur
mix_p = 467.0;   // profondeur
mix_h = 107.9;   // hauteur hors tout (boutons compris)

/* ---- Réglages ---- */
jeu      = 2.0;   // jeu tout autour
marge_h  = 4.0;   // espace au-dessus des boutons
t        = 2.0;   // épaisseur dessus et parois
levre_ar = 25;    // hauteur de la paroi arrière (le reste est ouvert pour les câbles)
fe       = 3.0;   // épaisseur des ailettes d'assemblage
fh       = 10.0;  // saillie des ailettes vers l'intérieur
trou     = 3.4;   // perçage M3
$fn = 32;

Wi = mix_l + 2*jeu;  Di = mix_p + 2*jeu;  Hi = mix_h + marge_h;
Wo = Wi + 2*t;       Do = Di + 2*t;
hx = Wo/2;           hy = Do/2;   // dimensions d'un quart

function pas(a, b, n) = [for (i=[0:n-1]) a + (b-a)*i/(n-1)];

// Un quart, en coordonnées locales : coutures sur x=0 et y=0,
// paroi latérale en x=hx, paroi avant/arrière en y=hy. z=0 = face visible du dessus.
module quart(arriere) {
    hw = arriere ? levre_ar : Hi;
    difference() {
        union() {
            cube([hx, hy, t]);                                   // dessus
            translate([hx - t, 0, 0]) cube([t, hy, t + Hi]);     // paroi latérale
            translate([0, hy - t, 0]) cube([hx, t, t + hw]);     // paroi avant / lèvre arrière
            // ailettes couture x=0
            cube([fe, hy - t, t + fh]);
            translate([0, hy - t - fh, 0]) cube([fe, fh, t + hw]);
            // ailettes couture y=0
            cube([hx - t, fe, t + fh]);
            translate([hx - t - fh, 0, 0]) cube([fh, fe, t + Hi]);
        }
        // perçages couture x=0 (axe X)
        for (y = pas(25, hy - t - fh - 15, 4))
            translate([-1, y, t + fh/2]) rotate([0,90,0]) cylinder(d=trou, h=fe + 2);
        for (z = (hw > 40 ? pas(t + 15, t + hw - 12, 3) : [t + hw/2 + 3]))
            translate([-1, hy - t - fh/2, z]) rotate([0,90,0]) cylinder(d=trou, h=fe + 2);
        // perçages couture y=0 (axe Y)
        for (x = pas(25, hx - t - fh - 15, 4))
            translate([x, -1, t + fh/2]) rotate([-90,0,0]) cylinder(d=trou, h=fe + 2);
        for (z = pas(t + 15, t + Hi - 12, 3))
            translate([hx - t - fh/2, -1, z]) rotate([-90,0,0]) cylinder(d=trou, h=fe + 2);
    }
}

// Placement final (vue de dessus, avant de la table = y négatif)
module place(gauche, arriere) {
    mirror([gauche ? 1 : 0, 0, 0]) mirror([0, arriere ? 0 : 1, 0]) quart(arriere);
}

if (piece == "avant_gauche")        place(true,  false);
else if (piece == "avant_droite")   place(false, false);
else if (piece == "arriere_gauche") place(true,  true);
else if (piece == "arriere_droite") place(false, true);
else {
    // housse assemblée, posée à l'endroit, éclatée de 6 mm pour voir les coutures
    rotate([180,0,0]) for (g=[true,false], a=[true,false])
        translate([g ? -3 : 3, a ? 3 : -3, 0]) place(g, a);
}
