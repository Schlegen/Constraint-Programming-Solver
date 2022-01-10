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

    @classmethod
    def plot_time_evolution(cls, list_n_queens):
        time_ac3 = list()
        time_backtrack = list()
        time_total = list()

        for nb_queens in list_n_queens:
            queens = Queens(nb_columns=nb_queens)
            print(f"Solving n Queens with n = {nb_queens} ...")
            # print(f"\nDomains {queens.domains}")

            solution, termination_status, execution_time, n_branching = queens.main(instantiation=dict(),
                                                                                    forward_check=True,
                                                                                    arc_consistence=True,
                                                                                    mode_var_heuristic=2,
                                                                                    mode_val_heuristic=1,
                                                                                    ac3_verbose=False)
            time_ac3.append(queens.time_ac3)
            time_backtrack.append(execution_time)
            time_total.append(queens.time_ac3 + execution_time)

        print("\nTime results :")
        print(time_ac3)
        print(time_backtrack)
        print(time_total)

        # data = np.log(np.array([time_ac3, time_backtrack]))
        data = np.array([time_ac3, time_backtrack])
        columns = n_list
        rows = ['AC3', 'backtrack']

        # plt.style.use('dark_background')
        n_rows = len(data)
        bar_width = 1.2

        # Initialize the vertical-offset for the stacked bar chart.
        y_offset = np.zeros(len(columns))

        # Get some pastel shades for the colors
        colors = plt.cm.BuPu(np.linspace(0.5, 0.8, len(rows)))
        # Plot bars and create text labels for the table
        for row in range(n_rows):
            plt.bar(columns, data[row], bar_width, bottom=y_offset, color=colors[row], label=rows[row])
            y_offset = y_offset + data[row]

        # plt.grid(linestyle='-', linewidth='0.1', color='grey')
        plt.subplots_adjust(left=0.2, bottom=0.2)
        plt.xlabel("n (size of the chessboard)")
        plt.ylabel("Execution time (seconds)")
        plt.xticks(columns)
        plt.legend()
        plt.title('Execution time VS size of the chessboard')

        plt.show()


if __name__ == "__main__":

    PLOT_TIME_EVOLUTION = False

    if PLOT_TIME_EVOLUTION:
        n_list = [5, 8, 12, 16, 20, 24, 28, 30, 32]
        Queens.plot_time_evolution(n_list)

    else:
        nb_queens = 8

        queens = Queens(nb_columns=nb_queens)
        print(f"Solving n Queens with n = {nb_queens} ...")
        # print(f"\nDomains {queens.domains}")

        solution, termination_status, execution_time, n_branching = queens.main(instantiation=dict(),
                                                                                forward_check=True,
                                                                                arc_consistence=True,
                                                                                mode_var_heuristic=2,
                                                                                mode_val_heuristic=1,
                                                                                ac3_verbose=True)
        print(f"\nThere is a solution : {solution}")
        print(f"\nExecution time : {execution_time}")
        print(f"\nNumber of branchings : {n_branching}")

        if solution:
            print(f"\nSolution : {queens.final_solution}")
            queens.show_solution()

# Results
# time_ac3 = [0.006006717681884766, 0.03799247741699219, 0.46100640296936035, 2.027963399887085, 10.92726182937622, 39.65749502182007, 48.6655216217041, 59.718843936920166, 86.75914263725281]
# time_backtrack = [0.0, 0.009998798370361328, 0.08699750900268555, 0.9100401401519775, 6.869961500167847, 6.6689980030059814, 9.003243446350098, 0.5849964618682861, 195.04245924949646]
# time_total = [0.006006717681884766, 0.047991275787353516, 0.5480039119720459, 2.9380035400390625, 17.797223329544067, 46.32649302482605, 57.6687650680542, 60.30384039878845, 281.80160188674927]
