from objects.variable import Variable
from objects.domain import Domain
from objects.wrapper import alldiff_constraint, queens_binary_var_constraints
from csp import CSP
import numpy as np
import matplotlib.pyplot as plt


# MARCHE PAS


class VariableQueensBinary(Variable):
    def __init__(self, name, i, j):
        super().__init__(name)
        self.index = (i, j)


class QueensModel2(CSP):
    def __init__(self, nb_columns):
        # Variables
        variables = [VariableQueensBinary("x" + str(i) + "," + str(j), i, j)
                     for i in range(0, nb_columns)
                     for j in range(0, nb_columns)]

        # Domains
        domains = Domain(variables)
        domains.fill_all_domains_by_range(lb=0, ub=1)

        # Constraints
        constraints = list()
        constraints += queens_binary_var_constraints(variables, nb_columns)

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
    nb_queens = 5
    queens = QueensModel2(nb_columns=nb_queens)
    var = list(queens.constraints.keys())[0]
    print(var)
    print(queens.constraints)
    cons = queens.constraints[var]
    print([[var.name for var in c.variables] for c in cons])

    print(f"Solving n Queens with n = {nb_queens} ...")
    # print(f"\nDomains {queens.domains}")

    solution = queens.main(instantiation=dict())
    print(f"\nThere is a solution : {solution}")
    if solution:
        print(f"Solution : {queens.final_solution}")
        queens.show_solution()
