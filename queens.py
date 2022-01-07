from objects.constraint import Constraint
from objects.variable import Variable
from objects.domain import Domain
from objects.wrapper import alldiff_constraint, queens_columns_constraint
from csp import CSP


class Queens(CSP):
    def __init__(self, nb_columns):
        # Variables
        variables = list()
        for i in range(1, nb_columns + 1):
            variables.append(Variable("x" + str(i)))

        # Domains
        domains = Domain(variables)
        domains.fill_all_domains_by_range(lb=1, ub=nb_columns)

        # Constraints
        constraints = list()
        constraints += alldiff_constraint(variables, domains.dict)
        constraints += queens_columns_constraint(variables, domains.dict)

        super().__init__(variables=variables, domains=domains, constraints=constraints)


instantiation = dict()
instantiation_str = [var.name + " : " + str(instantiation[var]) for var in instantiation]
print(f"\nInstantiation : {instantiation_str}")

queens = Queens(nb_columns=8)
var = list(queens.constraints.keys())[1]

verbose = False
if verbose:
    for constraint in queens.constraints[var]:
        print("variables " + str(constraint.variables[0].name) + " ; " + str(constraint.variables[1].name))
        print(constraint.tuples)

solution = queens.main(instantiation)
print(f"\nThere is a solution : {solution}")
