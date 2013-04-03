import constraint

class RoundwiseConstraint(constraint.Constraint):
    def __init__(self, sub, length):
        self._length = length
        self._id = 0
        self._sub = sub

    def update(self, match):
        self._id += 1
        if self._id % self._length == 0:
            self._sub.reset()
        else:
            self._sub.update(match)

    def evaluate(self, match):
        return self._sub.evaluate(match)

    def reset(self):
        self._id = 0
        self._sub.reset()

    def suggest_matches(self, teams):
        return self._sub.suggest_matches(teams)
