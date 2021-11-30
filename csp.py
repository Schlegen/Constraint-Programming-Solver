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

    # Heuristics for variable and values choices
    def heuristic_variable_choice_1(self, instantiation):
        """ Naive approach : take the first possible variable in the list"""
        index_var = 0
        for i in range(len(self.variables)):
            if self.variables[i] not in instantiation:
                index_var = i
                break

        return self.variables[index_var]

    def heuristic_values_choice_1(self, variable):
        """ Naive approach : take the domain in its defaults order"""
        return self.domains[variable]

