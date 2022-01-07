from objects.constraint import Constraint
from objects.variable import Variable
from objects.domain import Domain
from objects.wrapper import alldiff_constraint, cartography_constraints
from csp import CSP
from utils.parser import parse_carto


class Cartography(CSP):
    def __init__(self, nb_colors, file_name):
        # Variables
        variables = list()
        for i in range(1, nb_colors + 1):
            variables.append(Variable("x" + str(i)))

        # Domains
        domains = Domain(variables)
        domains.fill_all_domains_by_range(lb=1, ub=nb_colors)

        # Constraints
        cartography_graph = parse_carto(file_name)
        constraints = list()
        constraints += cartography_constraints(cartography_graph)

        super().__init__(variables=variables, domains=domains, constraints=constraints)


colors = 3
file = "instances/carto_myciel4_opti5.txt"
cartography = Cartography(nb_colors=colors, file_name=file)
print(f"Solving Cartography Problem with n = {colors} colors and instance {file.split('/')[1]}...")
# print(f"\nDomains {cartography.domains}")
var = list(cartography.constraints.keys())[1]

verbose = False
if verbose:
    for constraint in cartography.constraints[var]:
        print("variables " + str(constraint.variables[0].name) + " ; " + str(constraint.variables[1].name))
        print(constraint.tuples)

instantiation = dict()
solution = cartography.main(instantiation)
print(f"\nThere is a solution : {solution}")
