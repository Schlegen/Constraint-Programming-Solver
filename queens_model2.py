from objects.variable import Variable
from objects.domain import Domain
from objects.constraint import Constraint
from objects.wrapper import alldiff_constraint, queens_columns_constraint
from csp import CSP
import numpy as np
import matplotlib.pyplot as plt


def queens_binary_var_constraints(variables, nb_columns):
    constraints = list()
    for i1 in range(nb_columns):
        for j1 in range(nb_columns):
            for i2 in range(nb_columns):
                for j2 in range(j1, nb_columns):
                    tuples = [(1, 0), (0, 1)]
                    index_1 = i1 * nb_columns + j1
                    index_2 = i2 * nb_columns + j2

                    same_row = (i1 == i2)
                    same_column = (j1 == j2)
                    same_diag = (i1 < i2 and j2 - j1 == i2 - i1) or (i1 < i2 and j1 - j2 == i2 - i1)

                    if same_column or same_row or same_diag:
                        constraint = Constraint(variables[index_1], variables[index_2], tuples)
                        constraints.append(constraint)

    return constraints


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


nb_queens = 12
queens = Queens(nb_columns=nb_queens)
print(f"Solving n Queens with n = {nb_queens} ...")
# print(f"\nDomains {queens.domains}")

solution = queens.main(instantiation=dict())
print(f"\nThere is a solution : {solution}")
print(f"Solution : {queens.final_solution}")
queens.show_solution()
