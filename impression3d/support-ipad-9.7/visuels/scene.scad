// Visuels de principe — supports muraux iPad 5e gén. (240 x 169.5 x 7.5 mm)
design = 1;
W = 169.5; H = 240; T = 7.5; R = 12;
mur = [520, 10, 420];
noir = [0.12,0.12,0.13];
$fn = 48;

module rrect(w,h,t,r){ hull() for(x=[r,w-r],z=[r,h-r]) translate([x,0,z]) rotate([-90,0,0]) cylinder(r=r,h=t); }

// iPad posé à `dy` du mur, face avant vers -y
module ipad(dy=0){
  translate([-W/2, -dy - T, 0]) {
    color([0.85,0.86,0.88]) rrect(W,H,T,R);                       // coque alu + face blanche
    color([0.93,0.93,0.94]) translate([0,-0.01,0]) rrect(W,H,0.3,R);
    color([0.05,0.07,0.12]) translate([(W-148)/2,-0.4,(H-197)/2]) cube([148,0.4,197]); // écran
    color([0.25,0.5,0.85]) translate([(W-148)/2,-0.5,(H-197)/2+120]) cube([148,0.2,40]); // fond d'écran
    color([0.8,0.8,0.82]) translate([W/2,-0.5,10.5]) rotate([-90,0,0]) cylinder(d=11,h=0.3); // bouton home
  }
}
module mur_(){ color([0.95,0.94,0.91]) translate([-mur[0]/2, 0, -110]) cube(mur); }
module cable(){ color([0.97,0.97,0.97]) translate([0,-5,-4]) { rotate([0,0,0]) cylinder(d=4,h=4); translate([0,0,-120]) cylinder(d=3.5,h=116);} }

module crochet(){ // L vu de profil : dos + semelle + lèvre avant
  color(noir) translate([-10,0,0]) { translate([0,-3,-25]) cube([20,3,30]); translate([0,-T-6.5,-3.5]) cube([20,T+6.5,3.5]); translate([0,-T-6.5,-3.5]) cube([20,2.5,8]); }
}
module clip_haut(){
  color(noir) translate([-12,0,H]) { translate([0,-3,-2]) cube([24,3,26]); translate([0,-T-6,0.5]) cube([24,T+6,3]); translate([0,-T-6,-4]) cube([24,2.5,7.5]); }
}

if (design==1){ mur_(); ipad(3); translate([-50,0,0]) crochet(); translate([50,0,0]) crochet(); clip_haut(); }
if (design==2){ mur_(); ipad(3);
  color(noir) translate([-W/2-5,-3-T-2,-5]) difference(){
    cube([W+10, T+5, H+5]);
    translate([5,-1,5]) cube([W, T+2+0.01, H+10]);   // logement (ouvert en haut)
  }
  // lèvre avant fine
  color(noir) difference(){
    translate([-W/2-5,-3-T-2,-5]) cube([W+10,2,H+5]);
    translate([-W/2+3,-3-T-3,3]) cube([W-6,4,H]);
    translate([-12,-3-T-3,-6]) cube([24,4,10]);       // passage bouton home / câble
  }
}
if (design==3){ mur_(); ipad(3);
  color(noir) translate([-W/2-25,-38,-12]) { cube([W+50,38,12]); translate([0,0,0]) cube([W+50,3,22]); }
  clip_haut();
  color([0.3,0.3,0.3]) translate([60,-25,0]) cube([30,14,6]);  // clés posées dans le vide-poche
}
if (design==4){ mur_();
  color(noir) translate([-70,-4,20]) rrect(140,200,4,10);       // plaque murale
  for(x=[-50,50],z=[50,190]) color([0.75,0.75,0.78]) translate([x,-4.2,z]) rotate([90,0,0]) cylinder(d=12,h=0.6);
  translate([0,-30,0]) { color(noir) translate([-W/2-1.5,-3,-1.5]) rrect(W+3,H+3,3,R); ipad(3); } // coque + iPad, décollés
}
