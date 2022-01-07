from csp import CSP
from objects.variable import Variable
from objects.constraint import Constraint
from objects.domain import Domain

# Init variables
variables = [Variable("x1"), Variable("x2"), Variable("x3")]

# Init domains
domains = Domain(variables)
for variable in variables:
    domains.fill_domain_with_values(variable, [1, 2, 3])

# Init constraints
tuples = [(1, 2), (2, 3), (1, 3)]  # x1 < x2
tuples_2 = [(1, 1), (2, 2), (3, 3)]  # x2 = x3
tuples_3 = [(2, 1), (3, 2), (3, 1)]  # x1 > x3

constraints = [Constraint(variables[0], variables[1], tuples),
               Constraint(variables[1], variables[2], tuples_2),
               Constraint(variables[0], variables[2], tuples_3)]

# Init CSP
csp = CSP(variables, domains, constraints)
print(f"Domains : {csp.domains}")
# Give an instantiation
# instantiation = {variables[0]: 1, variables[1]: 3}

instantiation = {variables[0]: 1}
instantiation = dict()
instantiation_str = [var.name + " : " + str(instantiation[var]) for var in instantiation]
print(f"\nInstantiation : {instantiation_str}")

# Check the instantiation
# print(csp.is_consistent(variables[1], instantiation))

instantiation_is_ok = csp.main(instantiation)
print(f"\nThere is a solution : {instantiation_is_ok}")
