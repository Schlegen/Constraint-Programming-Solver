from objects.variable import Variable
from objects.domain import Domain
from objects.wrapper import cartography_constraints
from csp import CSP
from utils.parser import parse_carto
import matplotlib.pyplot as plt
import networkx as nx
from random import randint
import matplotlib.pyplot as plt



class Cartography(CSP):
    def __init__(self, nb_colors, file_name):

        self.nb_colors = nb_colors

        self.nb_nodes, self.edges = parse_carto(file_name) 
        # print(self.edges)

        # Variables
        variables = [Variable("x" + str(i)) for i in range(1, self.nb_nodes + 1)]

        # Domains
        domains = Domain(variables)
        domains.fill_all_domains_by_range(lb=1, ub=nb_colors)

        # Constraints
        constraints = cartography_constraints(variables, domains.dict, self.edges)
        
        # print([[v.name for v in c.variables] for c in constraints])

        super().__init__(variables=variables, domains=domains, constraints=constraints)

    def show_solution(self):
        if solution is None:
            return 0

        G = nx.Graph()

        G.add_nodes_from(self.final_solution.keys())#nodes)
        G.add_edges_from([("x" + str(e[0]), "x" + str(e[1])) for e in self.edges])

        nx.draw(G, with_labels=True, cmap=plt.cm.tab20, node_color=list(self.final_solution.values()))
        plt.show()          
        return 0

if __name__ == "__main__":
    colors = 5
    file = "instances/carto_queen5_5_opti5.txt"
    cartography = Cartography(nb_colors=colors, file_name=file)
    print(f"Solving Cartography Problem with n = {colors} colors and instance {file.split('/')[1]}...")
    # print(f"\nDomains {cartography.domains}")

    solution = cartography.main(instantiation=dict())
    print(f"\nThere is a solution : {solution}")
    if solution:
        print(cartography.final_solution)
        cartography.show_solution()
