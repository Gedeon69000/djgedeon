// Cadre mural fin pour iPad 9,7" (iPad 5e génération, A1822/A1823 — ex. MP2F2NF/A)
// Portrait, vissé au mur. L'iPad se glisse par le haut (ouvert) et repose en bas.
// Câble : une goulotte cachée dans le "menton" du cadre, sortie à gauche ou à droite
// (prévoir un câble Lightning coudé à 90° vers le côté).
// Impression : dos sur le plateau, sans supports. PLA blanc.
vue = "piece";   // "piece" | "mur" (visuel avec iPad)

/* ---- iPad (fiche Apple) ---- */
W = 169.5; H = 240; T = 7.5; Ripad = 10;
home_z = 10.5; home_d = 11;          // centre du bouton Home depuis le bas
/* ---- Réglages ---- */
c     = 0.6;   // jeu autour de l'iPad
dos   = 3.0;   // épaisseur du dos
paroi = 3.0;   // parois latérales
levre = 2.2;   // épaisseur de la lèvre avant
recouv = 3.5;  // la lèvre recouvre le bord de l'iPad (bord noir/blanc, pas l'écran)
menton = 14;   // hauteur de la goulotte sous l'iPad
vis_d = 4.2; vis_tete = 8.5;   // vis à tête fraisée Ø4
$fn = 48;

Wi = W + 2*c;  Wo = Wi + 2*paroi;
Hb = paroi + menton;            // bas de l'iPad au-dessus du bas du cadre
Ho = Hb + H + c;                // hauteur totale (le haut est ouvert)
Do = dos + T + c + levre;       // épaisseur totale
Ro = Ripad + paroi;

module rr2(w,h,r){ hull() for(x=[r,w-r],y=[r,h-r]) translate([x,y]) circle(r); }
// coordonnées pièce : x = largeur, y = hauteur (bas = 0), z = épaisseur (dos = 0)
module cadre(){
  difference(){
    // volume plein : bas arrondi, haut droit
    linear_extrude(Do) union(){ rr2(Wo, Ho*0.5, Ro); translate([0,Ho*0.25]) square([Wo, Ho*0.75]); }
    // logement iPad (ouvert vers le haut)
    translate([paroi, Hb, dos]) linear_extrude(T + c) union(){ rr2(Wi, H, Ripad+c); translate([0,H/2]) square([Wi, H]); }
    // goulotte sous l'iPad (toute la largeur)
    translate([paroi, paroi, dos]) cube([Wi, menton + 1, T + c]);
    // fenêtre avant : on voit l'écran, la lèvre recouvre le bord
    translate([paroi+recouv, Hb+recouv, dos]) linear_extrude(Do) union(){ rr2(Wi-2*recouv, H, Ripad); translate([0,H/2]) square([Wi-2*recouv, H]); }
    // dégagement du bouton Home
    translate([Wo/2, Hb + home_z, dos]) cylinder(d=home_d + 4, h=Do);
    // fenêtre boutons de volume (côté droit vu de face), 20 à 80 mm sous le haut
    translate([Wo - paroi - 1, Hb + H - 80, dos]) cube([paroi + 2, 60, T + c]);
    // sorties de câble gauche et droite, au niveau de la goulotte
    for (x=[-1, Wo - paroi - 1]) translate([x, paroi + 2, dos + 1]) cube([paroi + 2, 8, 6]);
    // grilles pour les haut-parleurs (dessous du cadre)
    for (s=[-1,1], i=[0:4]) translate([Wo/2 + s*(30 + i*7) - 1.5, -1, dos + 2]) cube([3, paroi + 2, T - 2]);
    // allègement du dos (laisse un cadre de 18 mm + une barre haute pour les vis)
    translate([paroi + 18, Hb + 30, -1]) cube([Wi - 36, H - 110, dos + 2]);
    translate([paroi + 18, Hb + H - 55, -1]) cube([Wi - 36, 40, dos + 2]);
    // 4 trous de vis fraisés (2 en haut sur la barre, 2 en bas dans le menton)
    for (p=[[Wo/2-55, Hb+H-70], [Wo/2+55, Hb+H-70], [paroi+14, paroi+menton/2+3], [Wo-paroi-14, paroi+menton/2+3]])
      translate([p[0], p[1], -1]) { cylinder(d=vis_d, h=dos+2); translate([0,0,dos+1-(vis_tete-vis_d)/2]) cylinder(d1=vis_d, d2=vis_tete, h=(vis_tete-vis_d)/2+0.01); }
  }
}

module ipad(){ // pour le visuel
  translate([paroi+c, Hb, dos+c/2]) {
    color([0.92,0.92,0.93]) linear_extrude(T) rr2(W,H,Ripad);
    color([0.05,0.07,0.12]) translate([(W-148)/2,(H-197)/2,T]) cube([148,197,0.3]);
    color([0.3,0.55,0.9])  translate([(W-148)/2,(H-197)/2+120,T+0.05]) cube([148,40,0.3]);
    color([0.82,0.82,0.84]) translate([W/2,home_z,T]) cylinder(d=home_d,h=0.3);
  }
}

if (vue == "piece") cadre();
else {
  color([0.96,0.96,0.95]) translate([-150,-120,-8]) cube([Wo+300, Ho+240, 8]);  // mur blanc
  color([1,1,1]) cadre(); ipad();
}
