from objects.variable import Variable
from objects.domain import Domain
from objects.wrapper import alldiff_constraint, queens_columns_constraint
from csp import CSP
import numpy as np
import matplotlib.pyplot as plt


class Queens(CSP):
    def __init__(self, nb_columns):
        # Variables
        variables = [Variable("x" + str(i)) for i in range(1, nb_columns + 1)]

        # Domains
        domains = Domain(variables)
        domains.fill_all_domains_by_range(lb=1, ub=nb_columns)

        # Constraints
        constraints = list()
        constraints += alldiff_constraint(variables, domains.dict)
        constraints += queens_columns_constraint(variables, domains.dict)

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


nb_queens = 12
queens = Queens(nb_columns=nb_queens)
print(f"Solving n Queens with n = {nb_queens} ...")
# print(f"\nDomains {queens.domains}")

solution = queens.main(instantiation=dict())
print(f"\nThere is a solution : {solution}")
print(f"Solution : {queens.final_solution}")
queens.show_solution()
