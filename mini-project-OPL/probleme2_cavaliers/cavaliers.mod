/*********************************************
 * OPL 12.10.0.0 Model
 * Creation Date: 13 déc. 2021 at 14:59:29
 *********************************************/

using CP;

// Definition des données du problèmes
int n = 7;
//int M = (n + 4) * (n + 4);

range extended_grid = 0..n+3;
range inner_grid = 2..n+1;
{int} edges = {0, 1, n+2, n+3};



tuple motions {
  int x;
  int y;
}

{motions} motions_x_y = ...;


dvar boolean positions[extended_grid][extended_grid];
//dvar int grid[length_extended][length_extended] in 0..M;

// Objectif
minimize sum(x in inner_grid, y in inner_grid) positions[x][y];
// sum(x in length, y in length) 0.00001*grid[x + 2][y + 2];

// Contraintes
constraints {
 	// Contraintes de 
 	forall (x in inner_grid, y in inner_grid){
 	  sum(k in motions_x_y) positions[x + k.x][y + k.y] >= 1;
 	  //forall (k in motions_x_y){
 	  	//grid[x + 2 + k.x][y + 2 + k.y] >= positions[x + 2][y + 2];
 	  //}
 	  //grid[x + 2][y + 2] <= M * sum(k in motions_x_y) positions[x + 2 + k.x][y + 2 + k.y];
 	  //grid[x + 2][y + 2] >= 1;
 	}
 	forall(x in edges){
 	  forall(y in extended_grid){
 	  	positions[x][y] == 0;
 	  	positions[y][x] == 0;
 	  }
	} 
}