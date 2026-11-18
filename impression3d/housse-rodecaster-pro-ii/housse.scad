// Housse anti-poussière pour RØDECaster Pro II
// 100 % imprimable : 2 moitiés (gauche / droite, ~157 x 278 mm) vissées entre elles
// par des ailettes internes (vis M3 x 10/12 + écrous). Arrière ouvert pour les câbles.
//
// piece = "gauche" | "droite" | "assemblage"
// Impression : tel que généré (dessus posé sur le plateau), sans supports.
piece = "assemblage";

/* ---- Console (fiche RØDE) ---- */
mix_l = 305;    // largeur
mix_p = 270;    // profondeur
mix_h = 83;     // hauteur au point le plus haut — À MESURER (fiche : 60, certains revendeurs : 83)

/* ---- Réglages ---- */
jeu      = 2.0;
marge_h  = 4.0;
t        = 2.0;
levre_ar = 20;    // hauteur de la paroi arrière (le reste est ouvert pour les câbles)
fe       = 3.0;
fh       = 10.0;
trou     = 3.4;
$fn = 32;

Wi = mix_l + 2*jeu;  Di = mix_p + 2*jeu;  Hi = mix_h + marge_h;
Wo = Wi + 2*t;       Do = Di + 2*t;
hx = Wo/2;

function pas(a, b, n) = [for (i=[0:n-1]) a + (b-a)*i/(n-1)];

// Moitié droite en coordonnées locales : couture sur x=0, avant en y=0, arrière en y=Do.
// z=0 = face visible du dessus.
module moitie() {
    difference() {
        union() {
            cube([hx, Do, t]);                                        // dessus
            translate([hx - t, 0, 0]) cube([t, Do, t + Hi]);          // paroi latérale
            cube([hx, t, t + Hi]);                                    // paroi avant
            translate([0, Do - t, 0]) cube([hx, t, t + levre_ar]);    // lèvre arrière
            // ailettes de couture
            cube([fe, Do, t + fh]);
            cube([fe, t + fh, t + Hi]);
            translate([0, Do - t - fh, 0]) cube([fe, t + fh, t + levre_ar]);
        }
        for (y = pas(t + fh + 15, Do - t - fh - 15, 5))
            translate([-1, y, t + fh/2]) rotate([0,90,0]) cylinder(d=trou, h=fe + 2);
        for (z = pas(t + 15, t + Hi - 12, 3))
            translate([-1, t + fh/2, z]) rotate([0,90,0]) cylinder(d=trou, h=fe + 2);
        translate([-1, Do - t - fh/2, t + levre_ar/2 + 3]) rotate([0,90,0]) cylinder(d=trou, h=fe + 2);
    }
}

module place(gauche) { mirror([gauche ? 1 : 0, 0, 0]) moitie(); }

if (piece == "gauche")      place(true);
else if (piece == "droite") place(false);
else rotate([180,0,0]) for (g=[true,false]) translate([g ? -3 : 3, 0, 0]) place(g);
