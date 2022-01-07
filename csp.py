from utils.csp_errors import DomainError, UnknownVariable


class CSP:
    def __init__(self, variables, domains, constraints):
        """
        Args:
            variables (list[Variable])
            domains (Domain)
        """
        self.variables = variables
        self.constraints = {}
        self.constraints_list = constraints
        self.domains = domains.dict  # domain of each variable : dict[Variable, Domain]
        for variable in self.variables:
            self.constraints[variable] = []
            if variable not in self.domains.keys():
                raise DomainError(variable)

        for constraint in constraints:
            for variable in constraint.variables:
                if variable not in self.variables:
                    raise UnknownVariable(variable)
                else:
                    self.constraints[variable].append(constraint)

    def is_consistent(self, variable, instantiation):
        """
            For a given variable and instantiation, tell if the variable is consistent
        """
        for constraint in self.constraints[variable]:
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
        for variable in instantiation:
            if not self.is_consistent(variable, instantiation):
                return False

        # If the instantiation is full
        if len(instantiation) == len(self.variables):
            return True

        # We pick a non-instantiated variable
        var = self.heuristic_variable_choice_1(instantiation)
        # We extract its possible values
        values = self.heuristic_values_choice_1(var)

        for v in values:  # for all values in the domain of var
            instantiation[var] = v
            if self.backtracking(instantiation):
                return True

        return False

    # Heuristic for variable choice
    def heuristic_variable_choice_1(self, instantiation):
        """ Naive approach : take the first possible variable in the list"""
        index_var = 0
        for i in range(len(self.variables)):
            if self.variables[i] not in instantiation:
                index_var = i
                break
        return self.variables[index_var]

    # Heuristic for values choice
    def heuristic_values_choice_1(self, variable):
        """ Naive approach : take the domain in its defaults order"""
        return self.domains[variable]

    # consistence algorithm
    def ac3(self):
        print("\nAC results :")
        to_test = list()
        for constraint in self.constraints_list:
            # for constraint in self.constraints[variable]:
            var = constraint.variables
            to_test += [var]
            var.reverse()  # Tres important !! cf remarque : contrainte directionnelle dans slides cours 2 :
            to_test += [var]
        while len(to_test) > 0:
            (x, y) = to_test.pop()
            instantiation = {x: 0,
                             y: 0}
            for x_value in self.domains[x]:
                # until line 100 : check if x_value has a support
                instantiation[x] = x_value
                is_supported = False
                for y_value in self.domains[y]:
                    # print(f"{x.name} : {x_value} ; {y.name} : {y_value}")
                    instantiation[y] = y_value
                    # if x_value is supported by at least 1 value of y, then it's ok
                    if self.is_consistent(y, instantiation):
                        is_supported = True
                if not is_supported:
                    print("- value " + str(x_value) + " not supported for var " + str(x.name))
                    self.domains[x].remove(x_value)
                    for constraint in self.constraints[x]:
                        # if constraint.variables not in [[x, y], [y, x]]:
                        for z in constraint.variables:
                            if z != x:
                                to_test += [(z, x)]

    def forward_checking(self, instantiation, x, a):
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
        # a ce stade, si un domaine est vide, alors il n'y a pas de solution
        # on peut dailleurs modif ac3 pour qu'il sarrete des qu'un domaine est vide
        return self.backtracking(instantiation)


# TODO
# Comment parcourir l'arbre ? Là le backtrack c'est bien quand on a une instantiation mais comment en générer ? D'où partir ?
# partir d'instantiation partielle vide = résoudre le pb de décision ?? OUI : et ajouter à "retourner VRAI" la valeur de i pour construire une solution

# question : AC pas symetrique non ? on prend chaque x et regarde si les valeurs sont supportes mais jamais si les y le sont ?
