/*********************************************
 * OPL 12.10.0.0 Model
 * Creation Date: 13 d�c. 2021 at 14:59:29
 *********************************************/

using CP;

// Definition des donn�es du probl�mes
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
 	//
 	forall (x in inner_grid, y in inner_grid){
 	  sum(k in motions_x_y) positions[x + k.x][y + k.y] >= 1;
 	}
 	forall(x in edges){
 	  forall(y in extended_grid){
 	  	positions[x][y] == 0;
 	  	positions[y][x] == 0;
 	  }
	}
	
	// symetries
	if (n mod 2 == 1) {
	  positions[2 + (n div 2)][2 + (n div 2)] + positions[(n div 2)][1 + (n div 2)] >= 1;
	} 
	else {
	  positions[2][2] + positions[3][4] >= 1;
	}

}

main {
  thisOplModel.generate();
  cp.solve();
  for (var i in thisOplModel.inner_grid) {
    for(var j in thisOplModel.inner_grid) {
    	write(thisOplModel.positions[i][j]+" ");
    }
    write("\n");
  }
}

