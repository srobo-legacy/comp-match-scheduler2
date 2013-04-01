import constraint
class WeightedConstraint(constraint.Constraint):
    def __init__(self, sub, weight):
        self._sub = sub
        self._weight = weight

    def update(self, match):
        self._sub.update(match)

    def evaluate(self, match):
        return self.weight * self._sub.evaluate(match)

    def reset(self):
        self._sub.reset()
