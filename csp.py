from collections import defaultdict
from networkx.algorithms.assortativity.correlation import numeric_assortativity_coefficient
from networkx.algorithms.structuralholes import constraint
from utils.csp_errors import DomainError, UnknownVariable
from copy import copy, deepcopy


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

    def backtracking(self, instantiation, domains, mode_var_heuristic=1, args_var_selection=()):
        """
        Backtracking algorithm

        Args:
            instantiation (dict[Variable, int]): partial instantiation of the CSP
        """
        for variable_name in instantiation:
            if not self.is_consistent(variable_name, instantiation):
                #print("instanciation")
                return False

        # If the instantiation is full
        if len(instantiation) == len(self.variables):
            self.final_solution = instantiation
            return True

        # We pick a non-instantiated variable
        # var_name = self.heuristic_variable_choice_1(instantiation, domains)
        var_name = self.heuristic_variable_selector(mode_var_heuristic, instantiation, domains, args=args_var_selection)
 
        # We extract its possible values
        if not domains[var_name]: # liste vide
            return False


        values = self.heuristic_values_choice_1(var_name, domains)

        # print(f"variable {var_name} with instantiation {instantiation}")

        for v in values:  # for all values in the domain of var
            local_instantiation = instantiation.copy()
            local_instantiation[var_name] = v
            #Forward checking
            local_domains = self.forward_checking(instantiation, domains, var_name, v)
            print("A", var_name, local_domains)

            if self.backtracking(local_instantiation, local_domains, mode_var_heuristic, args_var_selection):
                return True
        return False

    # Heuristic for variable choice (first variable allowed)
    def heuristic_variable_choice_1(self, instantiation, domains):
        """ Naive approach : take the first possible variable in the list"""
        for i in range(len(self.variables)):
            if self.variables[i].name not in instantiation:
                return self.variables[i].name

    # Heuristic for variable choice (smaller domain)
    def heuristic_variable_choice_2(self, instantiation, domains):
        """ Second approach : take the variable with the smaller remaining domain"""
        return min([k for k in domains.keys() if k not in instantiation], key=lambda x : len(domains[x]))

    # Heuristic for variable choice (most constrainted)
    def heuristic_variable_choice_3(self, instantiation, domains, list_var_sorted_by_nconstraints):
        """ Third approach : take the variable involved in the highest number of constraints"""
        #TODO: coder tri en amont 
        for i in range(len(self.variables)):
            #print("A", list_var_sorted_by_nconstraints[i], instantiation)
            if list_var_sorted_by_nconstraints[i] not in instantiation:
                return list_var_sorted_by_nconstraints[i]
    
    def compute_list_heuristic_var_3(self):
        dict_var_nconstr = {}
        for var in self.variables:
            dict_var_nconstr[var.name] = len(self.constraints[var.name])
        return sorted(dict_var_nconstr.keys(), key=lambda x : dict_var_nconstr[x], reverse=True)

    # Heuristic for variable choice (most linked to instance)
    def heuristic_variable_choice_4(self, instantiation, domains):
        """ Fourth approach : take the variable involved in the highest number of constraints"""
        dict_var_n_linked_constraints = {}
        for var in self.variables:
            if var.name not in instantiation:
                dict_var_n_linked_constraints[var.name] = 0
                for constraint in self.constraints[var.name]:
                    y = None
                    for u in constraint.variables:
                        if u.name != var.name:
                            y = u.name
                    if y in instantiation:
                        dict_var_n_linked_constraints[var.name] += 1
        return max(dict_var_n_linked_constraints.items(), key=lambda a: a[1])[0]

    def heuristic_variable_selector(self, i, instantiation, domains, args=()):
        if i == 1:
            return self.heuristic_variable_choice_1(instantiation, domains)
        elif i == 2:
            return self.heuristic_variable_choice_2(instantiation, domains)
        elif i == 3:
            return self.heuristic_variable_choice_3(instantiation, domains, *args)
        else:
            return self.heuristic_variable_choice_4(instantiation, domains)

    # Heuristic for values choice (first variable allowed)
    def heuristic_values_choice_1(self, variable_name, domains):
        """ Naive approach : take the domain in its defaults order"""
        return domains[variable_name]

    def heuristic_values_choice_2(self):
        """most suppported value"""

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

    def forward_checking(self, instantiation, domains, x, a):  # change with .name
        new_domains = deepcopy(domains)
        new_domains[x] = [a]
        for constraint in self.constraints[x]:
            y = None
            for variable in constraint.variables:
                if variable.name != x:
                    y = variable.name
            # print("C", instantiation, y)
            if y not in instantiation:
                # print("A", new_domains)
                # print("B", y.name)
                for b in new_domains[y]:
                    instantiation = {x: a, y: b}
                    if not constraint.is_satisfied(instantiation):
                        #print("value removed", y , b)
                        new_domains[y].remove(b)
        return new_domains
                

    def main(self, instantiation, mode_var_heuristic=3):
        self.ac3()

        args_var_selection = ()
        if mode_var_heuristic == 3:
            list_var_sorted_by_nconstraints = self.compute_list_heuristic_var_3()
            print("A", list_var_sorted_by_nconstraints)
            args_var_selection = (list_var_sorted_by_nconstraints,)


        # a ce stade, si un des domaines est vide, alors il n'y a pas de solution (logique)
        # idee : on peut dailleurs modif ac3 pour qu'il sarrete des qu'un domaine est vide
        return self.backtracking(instantiation, self.domains, mode_var_heuristic=mode_var_heuristic, args_var_selection=args_var_selection)



# IDEES :

# Comment choisir les heuristiques de selection en fonction du pb ??
# ==> en faire plusieurs, meme si elles sont simples.
# Idee d'aprofondissement : faire un truc intelligent qui choisit une en fonction du pb ou qqch comme ca


# AC3 en init (à la racine)
# puis a chaque noeud de l'arbre de recherche on fait quoi ? --> faire du forwardchecking (autre plan serait de faire du maintient d'AC : MAC)

#colorabilite = pb de decision : on dit le nbre de couleurs et ça repond oui ou non
