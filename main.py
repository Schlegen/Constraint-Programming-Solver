from csp import CSP
from objects.variable import Variable
from objects.constraint import Constraint
from objects.domain import Domain

# Init variables
variables = [Variable("x1"), Variable("x2")]

# Init domains
domains = Domain(variables)
for variable in variables:
    domains.fill_domain_with_values(variable, [1, 2, 3])

# Init constraints
tuples = [(1, 2), (2, 3), (1, 3)]
constraints = [Constraint(variables[0], variables[1], tuples)]

# Init CSP
csp = CSP(variables, domains, constraints)

# Give an instantiation
# instantiation = {variables[0]: 1, variables[1]: 3}

instantiation = {variables[0]: 1}
instantiation_str = [var.name + " : " + str(instantiation[var]) for var in instantiation]
print(f"Instantiation : {instantiation_str}")

# Check the instantiation
# print(csp.is_consistent(variables[1], instantiation))

instantiation_is_ok = csp.backtracking(instantiation)
print(f"The given partial instantiation fits the constraints : {instantiation_is_ok}")
