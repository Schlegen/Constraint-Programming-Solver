/*********************************************
 * OPL 12.10.0.0 Model
 * Creation Date: 13 déc. 2021 at 14:59:29
 *********************************************/

using CP;

// Definition des données du problèmes
int n = 8;
int M = (n + 4) * (n + 4);

range length = 0..n-1;
range length_extended = 0..n+3;



tuple motions {
  int x;
  int y;
}

{motions} motions_x_y = ...;


dvar boolean positions[length_extended][length_extended];
dvar int grid[length_extended][length_extended];

// Objectif
minimize sum(x in length, y in length) positions[x + 2][y + 2] + sum(x in length, y in length) 0.00001*grid[x + 2][y + 2];

// Contraintes
constraints {
 	// Contraintes de 
 	forall (x in length, y in length){
 	  forall (k in motions_x_y){
 	  	grid[x + 2 + k.x][y + 2 + k.y] >= positions[x + 2][y + 2];
 	  }
 	  grid[x + 2][y + 2] <= M * sum(k in motions_x_y) positions[x + 2 + k.x][y + 2 + k.y];
 	  grid[x + 2][y + 2] >= 1;
 	}
 	forall(x in 1..2, y in length){
 	  positions[x][y] == 0;
 	}
 	forall(x in n-1..n, y in length){
 	  positions[x][y] == 0;
 	}
 	forall(y in 1..2, x in length){
 	  positions[x][y] == 0;
 	}
 	forall(y in n-1..n, x in length){
 	  positions[x][y] == 0;
 	}
}