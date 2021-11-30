class Domain:
    def __init__(self, variables):
        self.variables = variables
        self.dict = {variable: [] for variable in variables}

    def fill_domain_with_values(self, variable, values):
        """
        Build a domain for given variable with explicit values.

        Args:
            variable (Variable)
            values (list of int) : possible values for variable
        """
        self.dict[variable] = values

    def fill_domain_by_range(self, variable, lb, ub):
        """
        Build a linear domain for given variable, from lower bound lb to upper bound ub.

        Args:
            variable (Variable)
            lb (int) : lower bound
            ub (int) : upper bound
        """
        self.dict[variable] = [x for x in range(lb, ub + 1)]
