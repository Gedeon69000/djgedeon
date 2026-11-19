// Concepts d'objets avec 2 écrans ronds 1,85" (zone visible Ø45,7 mm) — à l'échelle
concept = 1;
$fn = 72;
noir = [0.13,0.13,0.14]; gris = [0.32,0.32,0.34]; orange = [0.98,0.45,0.08];

// Un œil (écran) dans le plan XZ, face vers -y
module oeil(regard=[3,0]){
  rotate([90,0,0]) {
    color([0.02,0.02,0.03]) cylinder(d=49, h=1);                    // bord de l'écran
    color([0.96,0.96,0.98]) translate([0,0,1]) cylinder(d=45.7, h=0.4); // blanc
    color([0.05,0.75,0.95]) translate([regard[0],regard[1],1.4]) cylinder(d=25, h=0.3); // iris
    color([0.0,0.35,0.55]) translate([regard[0],regard[1],1.5]) difference(){ cylinder(d=25,h=0.25); cylinder(d=21,h=1,center=true);} // contour iris
    color([0.02,0.02,0.02]) translate([regard[0],regard[1],1.7]) cylinder(d=11, h=0.3); // pupille
    color("white") translate([regard[0]+4,regard[1]+4,2]) cylinder(d=4, h=0.3);       // reflet
  }
}
module arceau(r, ep=10, larg=26, angle=200){
  rotate([90,0,0]) rotate([0,0,-10]) rotate_extrude(angle=angle) translate([r,-larg/2]) square([ep,larg]);
}
module ecouteur(d=70, ep=30){ rotate([0,90,0]) { color(noir) cylinder(d=d, h=ep, center=true); color(gris) translate([0,0,-ep/2-6]) cylinder(d=d-6, h=7); } }

if (concept==1){ // Mascotte avec casque DJ
  color(noir) hull(){ for(x=[-55,55],z=[25,135]) translate([x,0,z]) sphere(r=35); }   // tête
  for(x=[-28,28]) translate([x,-35.5,95]) oeil();
  color(orange) translate([-22,-36,52]) cube([44,2,5]);                                // bouche
  color(gris) translate([0,0,80]) arceau(r=104, ep=9, larg=30, angle=200);             // arceau du casque
  for(s=[-1,1]) translate([s*98,0,80]) { color(orange) ecouteur(d=80, ep=26); }
  color(noir) translate([0,0,-12]) cylinder(d1=150, d2=120, h=22);                     // socle
  color(orange) translate([0,0,-12]) cylinder(d=152, h=4);
}
if (concept==2){ // Casque DJ géant, posé de face sur un pied
  color(noir) translate([0,0,150]) rotate([90,0,0]) rotate_extrude(angle=180) translate([120,-20]) square([14,40]);   // arceau
  for(s=[-1,1]) translate([s*127,0,120]) {
    color(noir) rotate([90,0,0]) cylinder(d=110, h=44, center=true);                     // coque
    color(orange) translate([0,-22,0]) rotate([90,0,0]) cylinder(d=114, h=6);            // anneau
    color(noir) translate([0,0,15]) cube([16,20,40],center=true);                        // fourche
    translate([0,-28.5,0]) oeil([-s*4,0]);                                               // écran au centre
  }
  color(noir) translate([0,0,-10]) cylinder(d=130, h=12);                               // socle
  color(gris) cylinder(d=16, h=272);                                                     // tige
  color(orange) translate([0,0,-10]) cylinder(d=134, h=3);
}
if (concept==3){ // Support de casque avec visage
  color(noir) cylinder(d=150, h=14);
  color(orange) translate([0,0,13]) cylinder(d=140, h=2);
  color(noir) translate([0,0,14]) cylinder(d=36, h=200);
  color(noir) translate([0,0,170]) hull(){ for(x=[-50,50]) translate([x,0,0]) rotate([90,0,0]) cylinder(r=30,h=34,center=true); }
  for(x=[-28,28]) translate([x,-17.5,170]) oeil();
  color(gris) translate([0,0,214]) rotate([0,90,0]) cylinder(r=12, h=170, center=true);    // barre d'accroche
  // votre casque audio posé dessus (gris clair)
  color([0.62,0.62,0.65]) translate([0,0,226]) rotate([90,0,0]) rotate([0,0,0]) rotate_extrude(angle=180) translate([88,-14]) square([7,28]);
  for(s=[-1,1]) color([0.55,0.55,0.58]) translate([s*95,0,170]) rotate([0,90,0]) cylinder(d=78, h=32, center=true);
}
if (concept==4){ // Masque / casque à porter
  color([0.85,0.72,0.6]) translate([0,15,-20]) scale([0.78,0.92,1]) sphere(r=88);       // tête (repère d'échelle)
  color(noir) difference(){ sphere(r=118); sphere(r=110); translate([0,0,-150]) cube(300,center=true); translate([0,-60,-35]) cube([140,120,120],center=true); }
  color([0.05,0.05,0.06]) intersection(){ sphere(r=123); translate([0,-100,48]) cube([190,80,62],center=true); }   // visière
  color(orange) intersection(){ difference(){ sphere(r=124); sphere(r=117);} translate([0,-100,48]) difference(){ cube([194,80,66],center=true); cube([186,90,58],center=true);} }
  for(x=[-38,38]) translate([x,-sqrt(123*123-x*x-48*48)-6,48]) rotate([0,0,-x/2.2]) scale(0.85) oeil();
  for(s=[-1,1]) color(orange) translate([s*118,0,30]) rotate([0,90,0]) cylinder(d=64,h=12,center=true);
}
