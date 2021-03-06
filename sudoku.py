from objects.variable import Variable
from objects.domain import Domain
from objects.wrapper import sudoku_constraints
from utils.parser import parse_sudoku
from csp import CSP
import numpy as np
import matplotlib.pyplot as plt


class Sudoku(CSP):
    def __init__(self, file_name):

        self.pre_assigned = parse_sudoku(file_name)

        # Variables
        variables = [Variable("x" + str(i) + "," + str(j))
                     for i in range(1, 10)
                     for j in range(1, 10)]

        # Domains
        domains = Domain(variables)
        domains.fill_all_domains_by_range(lb=1, ub=9)

        # Constraints
        constraints = sudoku_constraints(variables, domains.dict)

        for cell in self.pre_assigned:
            i, j = cell  # coordinates of the pre_assigned cell
            value = self.pre_assigned[cell]
            domains.dict["x" + str(i) + "," + str(j)] = [value]

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
        ax.set_xticks([])
        ax.set_yticks([])

        # Minor ticks
        ax.set_xticks(np.arange(-.5, n, 3), minor=True)
        ax.set_yticks(np.arange(-.5, n, 3), minor=True)

        # Gridlines based on minor ticks
        ax.grid(which='minor', color='black', linestyle='-', linewidth=2)

        plt.colorbar()
        plt.show()

    def show_pre_assigned(self):
        n = 9
        grid = np.empty((n, n))
        grid[:] = np.NaN
        for var in self.pre_assigned.keys():
            i, j = var
            grid[i - 1][j - 1] = self.pre_assigned[var]

        plt.figure(f"Sudoku pre assigned values")
        plt.imshow(grid, cmap='Pastel1')
        # fig.axes.get_xaxis().set_visible(False)
        # fig.axes.get_yaxis().set_visible(False)

        ax = plt.gca()

        # Major ticks
        ax.set_xticks([])
        ax.set_yticks([])

        # Minor ticks
        ax.set_xticks(np.arange(-.5, n, 3), minor=True)
        ax.set_yticks(np.arange(-.5, n, 3), minor=True)

        # Gridlines based on minor ticks
        ax.grid(which='minor', color='black', linestyle='-', linewidth=2)

        plt.colorbar()
        plt.show()


if __name__ == "__main__":
    file = "instances/sudoku_1.txt"
    sudoku = Sudoku(file_name=file)
    sudoku.show_pre_assigned()
    print(len(sudoku.pre_assigned))

    print(f"\nSolving Sudoku with instance = {file} ...")
    # print(f"\nDomains {sudoku.domains}")

    solution, termination_status, execution_time, n_branching = sudoku.main(instantiation=dict(),
                                                                            mode_var_heuristic=1,
                                                                            mode_val_heuristic=1,
                                                                            arc_consistence=False,
                                                                            forward_check=True,
                                                                            time_limit=180)
    if not termination_status:
        print(f"\nInterruption : time limit has been attained")
    print(f"\nThere is a solution : {solution}")
    print(f"\nExecution time : {execution_time}")
    print(f"\nNumber of branchings : {n_branching}")
    if solution:
        print(f"\nSolution : {sudoku.final_solution}")
        sudoku.show_solution()

