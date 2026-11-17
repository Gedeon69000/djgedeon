// Boîtier pour Waveshare ESP32-S3-LCD-1.85 (écran rond)
// Cotes reprises du plan constructeur (mm). Vue de face : écran vers soi.
// Pièce = "face" (coque avant) ou "dos" (couvercle arrière) ou "les_deux" (aperçu)
piece = "les_deux";

/* ---- Module (plan Waveshare) ---- */
lcd_d        = 48.08;  // diamètre hors tout de l'écran
actif_d      = 45.68;  // zone visible
pcb_d        = 47.86;  // diamètre du PCB
// !!! À MESURER : épaisseur totale verre -> dos des composants
module_ep    = 12.0;

/* ---- Réglages boîtier ---- */
jeu     = 0.3;    // jeu autour du module
paroi   = 2.0;
levre   = 1.2;    // épaisseur de la lèvre avant
recouv  = 1.0;    // la lèvre recouvre le bord noir de l'écran
fond    = 2.0;    // épaisseur du couvercle arrière
emboit  = 3.0;    // profondeur d'emboîtement du couvercle
$fn = 128;

int_d   = max(lcd_d, pcb_d) + 2*jeu;
ext_d   = int_d + 2*paroi;
hauteur = levre + module_ep;   // hauteur de la coque avant

/* ---- Découpes (ouvertes vers l'arrière, tolèrent l'épaisseur) ---- */
// angle 0 = droite (vue de face), 90 = haut, -90 = bas
module encoche(angle, largeur, z_debut) {
    rotate([0,0,angle])
        translate([int_d/2 - 1, -largeur/2, z_debut])
            cube([paroi + 3, largeur, 100]);
}
module decoupes() {
    // USB-C en bas, centré (place pour la fiche)
    encoche(-90, 12.5, levre + module_ep - 7);
    // Boutons PWR / BOOT / RST : côté droit vu de face
    rotate([0,0,-3]) for (a=[-30:3:28]) encoche(a, 3, levre + module_ep - 6);
    // Lecteur microSD : côté gauche vu de face
    encoche(180, 14, levre + module_ep - 5);
}

/* ---- Coque avant ---- */
module face() {
    difference() {
        cylinder(d=ext_d, h=hauteur);
        // logement du module
        translate([0,0,levre]) cylinder(d=int_d, h=hauteur);
        // fenêtre écran avec chanfrein
        translate([0,0,-0.01]) cylinder(d1=actif_d - 2*recouv + 2*levre + 1.2,
                                         d2=lcd_d - 2*recouv, h=levre + 0.02);
        // poche pour la nappe (FPC) en bas de l'écran
        translate([-8, -int_d/2 - 2.2, levre]) cube([16, 4, hauteur]);
        decoupes();
    }
}

/* ---- Couvercle arrière (emboîtement à friction) ---- */
module dos() {
    difference() {
        union() {
            cylinder(d=ext_d, h=fond);
            // anneau d'emboîtement
            translate([0,0,fond]) difference() {
                cylinder(d=int_d - 0.25, h=emboit);
                cylinder(d=int_d - 0.25 - 3.2, h=emboit + 1);
            }
            // 3 picots qui plaquent le PCB contre la lèvre
            for (a=[30,150,270]) rotate([0,0,a]) translate([int_d/2 - 5,0,fond])
                cylinder(d=3, h=emboit + 1);
        }
        // mêmes encoches que la coque (vu de dos, donc miroir en X)
        translate([0,0,fond]) mirror([1,0,0])
            translate([0,0,-(levre + module_ep - 7)]) decoupes();
        // aération (fentes)
        for (y=[-12:6:12]) translate([-14, y - 1, -1]) cube([28, 2, fond + 2]);
        // passage de câble (batterie / haut-parleur)
        translate([0, int_d/2 - 6, -1]) cylinder(d=5, h=fond + 2);
    }
}

if (piece == "face") face();
else if (piece == "dos") dos();
else {
    face();
    translate([ext_d + 8, 0, 0]) dos();
}
