from objects.variable import Variable
from objects.domain import Domain
from objects.wrapper import sudoku_constraints
from utils.parser import parse_sudoku
from csp import CSP
import numpy as np
import matplotlib.pyplot as plt


class VariableSudoku(Variable):
    def __init__(self, name, i, j):
        super().__init__(name)
        self.index = (i, j)


class Sudoku(CSP):
    def __init__(self, file_name):

        self.pre_assigned = parse_sudoku(file_name)
        print(self.pre_assigned)

        # Variables
        variables = [VariableSudoku("x" + str(i) + "," + str(j), i, j)
                     for i in range(1, 10)
                     for j in range(1, 10)]

        # Domains
        domains = Domain(variables)
        domains.fill_all_domains_by_range(lb=1, ub=9)

        for cell in self.pre_assigned:
            i, j = cell  # coordinates of the pre_assigned cell
            value = self.pre_assigned[cell]
            domains.dict["x" + str(i) + "," + str(j)] = [value]

        # Constraints
        constraints = sudoku_constraints(variables, domains.dict)

        super().__init__(variables=variables, domains=domains, constraints=constraints)

    def show_solution(self):
        if solution is None:
            return 0
        n = 9
        grid = np.zeros((n, n))
        for var in self.final_solution.keys():
            coordo = var.split("x")[1].split(",")
            i, j = int(coordo[0]) - 1, int(coordo[1]) - 1
            grid[i][j] = self.final_solution[var]

        plt.figure(f"Sudoku solution :")
        plt.imshow(grid, cmap='Pastel1')
        # fig.axes.get_xaxis().set_visible(False)
        # fig.axes.get_yaxis().set_visible(False)

        ax = plt.gca()

        # Major ticks
        ax.set_xticks(np.arange(0, n, 3))
        ax.set_yticks(np.arange(0, n, 3))

        # Minor ticks
        ax.set_xticks(np.arange(-.5, n, 3), minor=True)
        ax.set_yticks(np.arange(-.5, n, 3), minor=True)

        # Gridlines based on minor ticks
        ax.grid(which='minor', color='black', linestyle='-', linewidth=2)

        plt.colorbar()
        plt.show()

    def show_pre_assigned(self):
        n = 9
        grid = np.zeros((n, n))
        for var in self.pre_assigned.keys():
            i, j = var
            grid[i - 1][j - 1] = self.pre_assigned[var]

        plt.figure(f"Sudoku solution :")
        plt.imshow(grid, cmap='Pastel1')
        # fig.axes.get_xaxis().set_visible(False)
        # fig.axes.get_yaxis().set_visible(False)

        ax = plt.gca()

        # Major ticks
        ax.set_xticks(np.arange(0, n, 3))
        ax.set_yticks(np.arange(0, n, 3))

        # Minor ticks
        ax.set_xticks(np.arange(-.5, n, 3), minor=True)
        ax.set_yticks(np.arange(-.5, n, 3), minor=True)

        # Gridlines based on minor ticks
        ax.grid(which='minor', color='black', linestyle='-', linewidth=2)

        plt.colorbar()
        plt.show()


if __name__ == "__main__":
    file = "instances/sudoku_2.txt"
    sudoku = Sudoku(file_name=file)
    var = list(sudoku.constraints.keys())[13]

    print(var)
    cons = sudoku.constraints[var]
    # print([([var.name for var in c.variables], c.tuples) for c in cons])
    print([([var.name for var in c.variables]) for c in cons])

    sudoku.show_pre_assigned()

    print(f"\nSolving Sudoku with instance = {file} ...")
    print(f"\nDomains {sudoku.domains['x1,1']}")

    solution = sudoku.main(instantiation=dict())
    print(f"\nThere is a solution : {solution}")
    if solution:
        print(f"Solution : {sudoku.final_solution}")
        sudoku.show_solution()


  	# // Toutes les variables d'un sous-tableau sont differentes
    # forall (i in sousTableaux) {
    # 	forall (j in sousTableaux) {
    # 	  // (i-1)*taille -> i*taille
	#        allDifferent(all (i1 in ((i-1)*dimension+1)..(i*dimension),
	#                          j1 in ((j-1)*dimension+1)..(j*dimension))
	#                          tableau[i1][j1]);
	#   	}