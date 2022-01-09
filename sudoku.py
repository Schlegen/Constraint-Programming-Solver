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
        constraints = list()
        constraints += sudoku_constraints(variables, domains.dict)

        super().__init__(variables=variables, domains=domains, constraints=constraints)

    def show_solution(self):
        if solution is None:
            return 0
        n = len(self.variables)
        grid = np.zeros((n, n))
        for var in self.final_solution.keys():
            column = int(var.split("x")[1]) - 1
            row = self.final_solution[var] - 1
            grid[row][column] = 1

        plt.figure(f"n Queens solution with n = {n}")
        plt.imshow(grid, cmap='Greys')
        # fig.axes.get_xaxis().set_visible(False)
        # fig.axes.get_yaxis().set_visible(False)

        ax = plt.gca()

        # Major ticks
        ax.set_xticks(np.arange(0, n, 1))
        ax.set_yticks(np.arange(0, n, 1))

        # Minor ticks
        ax.set_xticks(np.arange(-.5, n, 1), minor=True)
        ax.set_yticks(np.arange(-.5, n, 1), minor=True)

        # Gridlines based on minor ticks
        ax.grid(which='minor', color='black', linestyle='-', linewidth=2)

        plt.show()


if __name__ == "__main__":
    file = "instances/sudoku_1.txt"
    sudoku = Sudoku(file_name=file)
    var = list(sudoku.constraints.keys())[0]
    print(var)
    print(sudoku.constraints)
    cons = sudoku.constraints[var]

    print([[var.name for var in c.variables] for c in cons])

    print(f"Solving Sudoku with instance = {file} ...")
    # print(f"\nDomains {sudoku.domains}")

    solution = sudoku.main(instantiation=dict())
    print(f"\nThere is a solution : {solution}")
    if solution:
        print(f"Solution : {sudoku.final_solution}")
        # sudoku.show_solution()


  	# // Toutes les variables d'un sous-tableau sont differentes
    # forall (i in sousTableaux) {
    # 	forall (j in sousTableaux) {
    # 	  // (i-1)*taille -> i*taille
	#        allDifferent(all (i1 in ((i-1)*dimension+1)..(i*dimension),
	#                          j1 in ((j-1)*dimension+1)..(j*dimension))
	#                          tableau[i1][j1]);
	#   	}