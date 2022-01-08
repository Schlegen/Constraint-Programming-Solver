from objects.variable import Variable
from objects.domain import Domain
from objects.wrapper import alldiff_constraint
from csp import CSP
import numpy as np
import matplotlib.pyplot as plt


class SendMoreMoney(CSP):
    def __init__(self, avec_retenues=False):
        # Variables
        letters = ["S", "E", "N", "D", "M", "O", "R", "Y"]
        variables = [Variable(letter) for letter in letters]

        # Domains
        domains = Domain(variables)
        domains.fill_all_domains_by_range(lb=1, ub=9)

        # Constraints
        constraints = list()
        constraints += alldiff_constraint(variables, domains.dict)

        super().__init__(variables=variables, domains=domains, constraints=constraints)


csp = SendMoreMoney()
print(f"Solving << SEND + MORE + MONEY >> problem ...")
# print(f"\nDomains {queens.domains}")

solution = csp.main(instantiation=dict())
print(f"\nThere is a solution : {solution}")
print(f"Solution : {csp.final_solution}")
