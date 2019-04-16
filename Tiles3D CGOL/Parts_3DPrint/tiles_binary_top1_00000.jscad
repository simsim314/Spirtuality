epsilon_material = 0.01;
depth_factor = 0.6;
symbolR_factor = 0.5; 
sumbolH_factor = 0.12;
symbolW_factor = 0.3;
r_factor = 0.1; 
 circle_fn = 100; 

    
R = 10; //The length of cube
v = 0;
d1 = 2.75;
d2 = 3;

h_extrusion = v * depth_factor;
sH = R * sumbolH_factor;
sR = R * symbolR_factor * 0.5;
sW = (1 - symbolW_factor) * sR; 
sWcube = symbolW_factor * sR; 
TileH = R * 0.35;

function Draw0(ep)
{
   l = (sR - sW)/2 + ep; 
   u = (sR + sW)/2; 
   
   return union(rotate_extrude({fn:circle_fn},  polygon({points:[ [u-l,0],[u+l,0],[u,l]]}) ).translate([0,0,sH+ep]),
    difference(cylinder({r:(sR + ep), h:(sH + ep), fn: circle_fn}), cylinder({r:(sW - ep), h:(sH + ep), fn: circle_fn})));
    
}

function DrawLine(ep)
{
   sWc = sWcube * 2;
   sw2 = sWc / 2;
   s1R = sR;
   s1H = sH / 2; 
   
   var p = polygon({points:[ [-sw2-ep,0],[sw2+ep,0],[0,sw2+ep]]});
   var exp = linear_extrude({ height: 2*s1R + 2 * ep }, p).translate([0,s1H+ep,-s1R-ep]);
   
   return union(cube([2*s1R+2*ep, sWc + 2 * ep, s1H+ep]).translate([-s1R-ep, -(sWc)/2-ep, 0]),
                 exp.rotateX(90).rotateZ(90));
}

function draw0_cube()
{
  return difference(union(Draw0(0).translate([R/2,R/2,R]), cube(R), cylinder({r: R * r_factor, h:(R), fn: circle_fn}).translate([0, R/2, 0])), union(Draw0(epsilon_material).translate([R/2,R/2,0]), cylinder({r: R * r_factor + epsilon_material, h:(R), fn: circle_fn}).translate([R, R/2, 0])));
}

function draw1_cube()
{
    return difference(union(DrawLine(0).translate([R/2,R/2,R]), cube(R), cylinder({r: R * r_factor, h:(R), fn: circle_fn}).translate([0, R/2, 0])), union(Draw0(epsilon_material).translate([R/2,R/2,0]), cylinder({r: R * r_factor + epsilon_material, h:(R), fn: circle_fn}).translate([R, R/2, 0])));
}

function draw_platform()
{
    ep = epsilon_material;
    realR = R + 2 * ep; 
    N = 8;
    PlatH = R * 0.2; 
    H = PlatH + realR + TileH + ep;
    PlatW = R / 3;
    
    v =  cube([2 * realR - 2 * ep, N * realR, PlatH ]);
    
    for(var i=0; i<N; i+=1) {
            v = union(v, Draw0(0).translate([R/2 ,R/2 + i * realR, PlatH]));
            v = union(v, Draw0(0).translate([R/2 + realR, R/2 + i * realR, PlatH]));
        }
        
    return union(v.translate([0,PlatW,0]), cube([2 * realR - 2 * ep, PlatW,H]), cylinder({r: R * r_factor, h:(H), fn: circle_fn}).translate([R/2, PlatW, 0]),  cylinder({r: R * r_factor, h:(H), fn: circle_fn}).translate([R/2 + realR, PlatW, 0]));
}

function add_inputs(v, i1, i2)
{
    ep = epsilon_material;
    realR = R + 2 * ep; 
     
    if(i1 == 0)
        v = difference(v, Draw0(ep).translate([R/2 ,R/2, 0]));
    else 
        v = difference(v, DrawLine(ep).translate([R/2 ,R/2, 0]));
        
    if(i2 == 0)
        v = difference(v, Draw0(ep).translate([R/2 ,R/2+realR, 0]));
    else
        v = difference(v, DrawLine(ep).translate([R/2 ,R/2+realR, 0]));
        
    return v; 
}

function add_output(v, o)
{
	ep = epsilon_material;
    
    if(o == 0)
        return union(v, Draw0(0).translate([R/2 ,R + ep, TileH]))    
    else
        return union(v, DrawLine(0).translate([R/2 ,R + ep, TileH]))    
}

function add_input_c(v, c)
{
   ep = epsilon_material;
    realR = R + 2 * ep; 
    
   if(c == 0)
      return difference(v, union(cylinder({r: R * r_factor + ep, h:(R), fn: circle_fn}).translate([0, R/2, 0]), cylinder({r: R * r_factor + ep, h:(R), fn: circle_fn}).translate([0, R/2 + realR, 0])));
   else 
      return difference(v, cylinder({r: R * r_factor * 1.5 + ep, h:(R), fn: circle_fn}).translate([0, R + ep, 0]));
   
}

function add_output_c(v, c)
{
   ep = epsilon_material;
   realR = R + 2 * ep; 
    
   if(c === 0)
      return union(v, union(cylinder({r: R * r_factor, h:(TileH), fn: circle_fn}).translate([R, R/2, 0]), cylinder({r: R * r_factor, h:(TileH), fn: circle_fn}).translate([R, R/2 + realR, 0])));
   else 
      return union(v, cylinder({r: R * r_factor * 1.5, h:(TileH), fn: circle_fn}).translate([R, R + ep, 0]));
   
}

function add_tile(i1, i2, ci, co, o)
{
    ep = epsilon_material;
    realR = R + ep; 
    v = cube([R, 2 * realR, TileH]);
    v = add_inputs(v, i1, i2);
    v = add_output(v, o);
    v = add_input_c(v, ci)
    return add_output_c(v, co);
}

//Platform - 1 √
//0-1 blocks - 2 √
//8 tiles to add - 8 

function main () {
//return union(draw1_cube(), draw0_cube().translate([2*R, 0,0]));
//platform 
R3 = R * 3; 
R6 = R * 6; 
//return ;
return union(
    add_tile(0,0,0,0,0)
    //add_tile(1,0,0,0,1)//.translate([R3, 0, 0]),
    //add_tile(0,1,0,0,1)//.translate([R6, 0, 0]),
    //add_tile(0,0,1,0,1)//.translate([0, R3, 0]),
    //add_tile(1,1,0,1,0)//.translate([R3, R3, 0]),
    //add_tile(1,0,1,1,0)//.translate([R6, R3, 0]),
    //add_tile(0,1,1,1,0)//.translate([R3, R6, 0]),
    //add_tile(1,1,1,1,1)//.translate([R6, R6, 0]),
    //draw_platform()//.translate([R*8, 0, 0]),
    //draw1_cube()//.translate([-R3, 0, 0]), draw0_cube().translate([-R3, R3, 0])
    );
}