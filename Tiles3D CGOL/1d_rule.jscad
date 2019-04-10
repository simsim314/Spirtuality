R = 10;
L = 5; 
H = 1; 

ep = 0.2; 
R1 = R/3 + ep; 
R2 = R/3 - ep; 
Rh = 1.5; 
ep = 0.01;

function place1()
{
    return linear_extrude({ height: H },polygon({ points: [[0,0],[R,0],[R,L],
	[R - R1, L], [R - R2, L+Rh],[R2, L+Rh], [R1, L], [0, L]]}));
}

function place0()
{
    return linear_extrude({ height: H },polygon({ points: [[0,0],[R,0],[R,L],
	[R - R1 + ep, L], [R - R2 + ep, L-Rh - ep],[R2-ep, L-Rh-ep], [R1 - ep, L], [0, L]]}));
}

function sq(i)
{
    if(i === 0)
        return place0();
    else 
        return place1();
}

function create_sq(i1, i2, i3)
{
    return union(
        cube([R, L, H]).rotateY(180).translate([0,0,H]),
        sq(i1),
        sq(i2).rotateX(180).translate([0,0,H]),
        sq(i3).rotateX(180).rotateY(180)
        );    
}

function create_tile(x1,x2,x3,y1)
{
    i1 = x2; 
    i2 = x3; 
    i3 = x2; 
    j1 = x1;
    j2 = y1; 
    j3 = y1; 
    
     return union(create_sq(i1, i2, i3),
            create_sq(j1, j2, j3).rotateZ(180).translate([-R, 2*L, 0]));
}

function main () {
 //return cube([R, R, H]);
 M = 4 * R; 
 return union(
     create_tile(1, 1, 1, 0).translate([0,M,0]),
     create_tile(1, 1, 0, 1).translate([0,2*M,0]),
     create_tile(1, 0, 1, 1).translate([0,3*M,0]),
     create_tile(1, 0, 0, 0).translate([M,M,0]),
     create_tile(0, 1, 1, 1).translate([M,2*M,0]),
     create_tile(0, 1, 0, 1).translate([M,3*M,0]),
     create_tile(0, 0, 1, 1).translate([2*M,M,0]),
     create_tile(0, 0, 0, 0).translate([2*M,2*M,0])
     
     );
}
