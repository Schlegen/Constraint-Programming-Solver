from objects.variable import Variable
from objects.domain import Domain
from objects.wrapper import cartography_constraints
from csp import CSP
from utils.parser import parse_carto


class Cartography(CSP):
    def __init__(self, nb_colors, file_name):

        nb_nodes, edges = parse_carto(file_name)

        # Variables
        variables = [Variable("x" + str(i)) for i in range(1, nb_nodes + 1)]

        # Domains
        domains = Domain(variables)
        domains.fill_all_domains_by_range(lb=1, ub=nb_colors)

        # Constraints
        constraints = cartography_constraints(variables, domains.dict, edges)
        # print([[v.name for v in c.variables] for c in constraints])

        super().__init__(variables=variables, domains=domains, constraints=constraints)


colors = 5
file = "instances/carto_queen5_5_opti5.txt"
cartography = Cartography(nb_colors=colors, file_name=file)
print(f"Solving Cartography Problem with n = {colors} colors and instance {file.split('/')[1]}...")
# print(f"\nDomains {cartography.domains}")

solution = cartography.main(instantiation=dict())
print(f"\nThere is a solution : {solution}")
print(cartography.final_solution)
