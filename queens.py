from objects.variable import Variable
from objects.domain import Domain
from objects.wrapper import alldiff_constraint, queens_columns_constraint
from csp import CSP


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


nb_queens = 8
queens = Queens(nb_columns=nb_queens)
print(f"Solving n Queens with n = {nb_queens} ...")
# print(f"\nDomains {queens.domains}")

solution = queens.main(instantiation=dict())
print(f"\nThere is a solution : {solution}")
