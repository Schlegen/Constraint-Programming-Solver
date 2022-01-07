from objects.constraint import Constraint


def alldiff_constraint(variables, domains):
    constraints = list()
    for i in range(len(variables)):
        for j in range(i + 1, len(variables)):
            tuples = list()
            for val_i in domains[variables[i].name]:
                for val_j in domains[variables[j].name]:
                    if val_i != val_j:
                        tuples.append((val_i, val_j))
            constraint = Constraint(variables[i], variables[j], tuples)
            constraints.append(constraint)
    return constraints


# acj + bci =! j - i ET bcj + aci =! j - i
def queens_columns_constraint(variables, domains, a=1, b=-1):
    constraints = list()
    for i in range(len(variables)):
        for j in range(i + 1, len(variables)):
            tuples = list()
            for val_i in domains[variables[i].name]:
                for val_j in domains[variables[j].name]:
                    if a * val_j + b * val_i != j - i and b * val_j + a * val_i != j - i:
                        tuples.append((val_i, val_j))
            constraint = Constraint(variables[i], variables[j], tuples)
            constraints.append(constraint)
    return constraints


# ax + by = c
def weighted_sum_constraint(variables, domains, a, b, c):
    constraints = None
    return constraints






