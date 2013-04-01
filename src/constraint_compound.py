import constraint
class CompoundConstraint(constraint.Constraint):
    def __init__(self, sub_constraints):
        self._sub_constraints = sub_constraints

    def update(self, match):
        for constraint in self._sub_constraints:
            constraint.update(match)

    def evaluate(self, match):
        return sum(constraint.evaluate(match) for constraint
                                             in self._sub_constraints)

    def reset(self):
        for constraint in self._sub_constraints:
            constraint.reset()
