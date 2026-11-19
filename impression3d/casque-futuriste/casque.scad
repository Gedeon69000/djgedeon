// Casque futuriste original à yeux animés (2 écrans ronds 1,85")
// Maquette de style — pièces séparées pour le rendu (part = ...)
part = "coque";
$fn = 120;

module crane(){ translate([0,15,40]) scale([0.98,1.12,1.0]) sphere(r=118, $fn=18); }
module corps(){
  hull(){
    crane();
    translate([0,-90,-78]) scale([1.3,1,0.8]) sphere(r=20, $fn=8);           // menton
    for(s=[-1,1]) translate([s*64,-72,-46]) sphere(r=26, $fn=8);             // pommettes
    for(s=[-1,1]) translate([s*94,18,-60]) sphere(r=30, $fn=10);              // mâchoire arrière
    translate([0,70,-55]) sphere(r=55, $fn=12);                               // nuque
  }
}
module corps_coupe(){ difference(){ corps(); translate([0,0,-300]) cube(400,center=true); } } // bas coupé à z=-100
module couche(e){ difference(){ scale(1+e) corps_coupe(); corps_coupe(); } }  // fine peau extérieure

module visiere_poly(){ polygon([[-100,40],[-70,52],[-14,44],[0,36],[14,44],[70,52],[100,40],[96,22],[62,-6],[24,-6],[0,-26],[-24,-6],[-62,-6],[-96,22]]); }
module prisme(){ rotate([90,0,0]) linear_extrude(320) children(); }            // extrusion vers l'avant (-y)

module rainure(slab){ intersection(){ children(); difference(){ cube(800,center=true); scale(0.986) corps_coupe(); } } }

if (part=="coque") difference(){
  union(){
    corps_coupe();
    // crête centrale
    intersection(){ scale(1.025) corps_coupe(); translate([-5,-130,70]) cube([10,230,200]); }
  }
  scale(0.93) corps_coupe();                                       // creux intérieur
  translate([0,25,-180]) cylinder(r=78, h=140);                    // ouverture du cou
  rainure() translate([-400,38.8,-30]) cube([800,2.4,400]);        // rainure verticale (côtés + dessus)
  rainure() translate([-400,40,66]) cube([800,400,2.4]);           // rainure arrière horizontale
  rainure() translate([-400,-400,-62]) cube([800,330,2.4]);        // rainure basse du masque
}
if (part=="visiere") intersection(){ couche(0.013); prisme() visiere_poly(); }
if (part=="liseres") intersection(){ couche(0.016); prisme() difference(){ offset(delta=7) visiere_poly(); offset(delta=3) visiere_poly(); } }
if (part=="lumieres") intersection(){ couche(0.015); prisme() union(){
    for(s=[-1,1]) scale([s,1]) polygon([[44,-36],[82,-14],[84,-19],[46,-42]]);     // traits de joues
    for(x=[-12,0,12]) translate([x-2.2,-70]) square([4.4,26]);                     // fentes du menton
} }
if (part=="oreilles") for(s=[-1,1]) translate([s*113,22,2]) rotate([0,s*90,0]) difference(){
  cylinder(d=84, h=16); translate([0,0,10]) cylinder(d=56, h=10);
}
if (part=="anneaux") for(s=[-1,1]) translate([s*(113+10.2),22,2]) rotate([0,s*90,0]) difference(){ cylinder(d=50,h=1.5); cylinder(d=42,h=5,center=true); }
if (part=="socle") { translate([0,25,-262]) cylinder(r=46, h=175); translate([0,25,-290]) cylinder(r1=120, r2=108, h=28); }
