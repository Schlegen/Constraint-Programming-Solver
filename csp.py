from utils.csp_errors import DomainError, UnknownVariable
from copy import copy


class CSP:
    def __init__(self, variables, domains, constraints):
        """
        Args:
            variables (list[Variable])
            domains (Domain)
        """
        self.final_solution = None
        self.variables = variables
        self.constraints = {}
        self.constraints_list = constraints
        self.domains = domains.dict  # domain of each variable : dict[Variable, Domain]
        for variable in self.variables:
            self.constraints[variable.name] = []
            if variable.name not in self.domains.keys():
                raise DomainError(variable)

        for constraint in constraints:
            for variable in constraint.variables:
                if variable not in self.variables:  # changer pour des var.name ?
                    raise UnknownVariable(variable)
                else:
                    self.constraints[variable.name].append(constraint)

    def is_consistent(self, variable_name, instantiation):
        """
            For a given variable and instantiation, tell if the variable is consistent
        """
        for constraint in self.constraints[variable_name]:
            if not constraint.is_satisfied(instantiation):
                return False
        return True

    def backtracking(self, instantiation):
        """
        Backtracking algorithm

        Args:
            instantiation (dict[Variable, int]): partial instantiation of the CSP
        """

        # If the instantiation does not fit a constraint
        for variable_name in instantiation:
            if not self.is_consistent(variable_name, instantiation):
                return False

        # If the instantiation is full
        if len(instantiation) == len(self.variables):
            self.final_solution = instantiation
            return True

        # We pick a non-instantiated variable
        var_name = self.heuristic_variable_choice_1(instantiation)
        # We extract its possible values
        values = self.heuristic_values_choice_1(var_name)

        # print(f"variable {var_name} with instantiation {instantiation}")

        for v in values:  # for all values in the domain of var
            local_instantiation = instantiation.copy()
            local_instantiation[var_name] = v
            if self.backtracking(local_instantiation):
                return True
        return False

    # Heuristic for variable choice
    def heuristic_variable_choice_1(self, instantiation):
        """ Naive approach : take the first possible variable in the list"""
        for i in range(len(self.variables)):
            if self.variables[i].name not in instantiation:
                return self.variables[i].name

    # Heuristic for values choice
    def heuristic_values_choice_1(self, variable_name):
        """ Naive approach : take the domain in its defaults order"""
        return self.domains[variable_name]

    # consistence algorithm
    def ac3(self):
        print("\nAC results :")
        to_test = list()
        for constraint in self.constraints_list:
            var = constraint.variables
            to_test += [var]
            var.reverse()  # Tres important !! cf remarque : contrainte directionnelle dans slides cours 2
            to_test += [var]
        while len(to_test) > 0:
            (x, y) = to_test.pop()
            instantiation = {x.name: 0,
                             y.name: 0}
            for x_value in self.domains[x.name]:
                # until line 100 : check if x_value has a support
                instantiation[x.name] = x_value
                is_supported = False
                for y_value in self.domains[y.name]:
                    # print(f"{x.name} : {x_value} ; {y.name} : {y_value}")
                    instantiation[y.name] = y_value
                    # if x_value is supported by at least 1 value of y, then it's ok
                    if self.is_consistent(y.name, instantiation):
                        is_supported = True
                if not is_supported:
                    print("- value " + str(x_value) + " not supported for var " + str(x.name))
                    self.domains[x.name].remove(x_value)
                    for constraint in self.constraints[x.name]:
                        for z in constraint.variables:
                            if z.name != x.name:
                                to_test += [(z, x)]

    def forward_checking(self, instantiation, x, a):  # change with .name
        for constraint in self.constraints[x]:
            y = None
            for variable in constraint.variables:
                if variable != x:
                    y = variable
            if y not in instantiation:
                for b in self.domains[y]:
                    instantiation = {x: a, y: b}
                    if not constraint.is_satisfied(self, instantiation):
                        self.domains[y].remove(b)

    def main(self, instantiation, with_arc_consistency=True, with_forward_checking=False):
        if with_arc_consistency:
            self.ac3()
        # a ce stade, si un des domaines est vide, alors il n'y a pas de solution (logique)
        # idee : on peut dailleurs modif ac3 pour qu'il sarrete des qu'un domaine est vide
        return self.backtracking(instantiation)



# IDEES :

# Comment choisir les heuristiques de selection en fonction du pb ??
# ==> en faire plusieurs, meme si elles sont simples.
# Idee d'aprofondissement : faire un truc intelligent qui choisit une en fonction du pb ou qqch comme ca


# AC3 en init (à la racine)
# puis a chaque noeud de l'arbre de recherche on fait quoi ? --> faire du forwardchecking (autre plan serait de faire du maintient d'AC : MAC)

#colorabilite = pb de decision : on dit le nbre de couleurs et ça repond oui ou non
