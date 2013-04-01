import constraint
from utils import is_actual_entrant


class DistributeMatchesConstraint(constraint.Constraint):
    def __init__(self, minimum_separation = 3, target_separation = 5):
        self._minimum_separation = minimum_separation
        self._target_separation = target_separation
        self._last_matches = {}
        self._id = 0

    def update(self, match):
        for team in match:
            if is_actual_entrant(team):
                self._last_matches[team] = self._id
        self._id += 1

    def _evaluate_team(self, team):
        if team not in self._last_matches:
            return 0.0
        distance_from_last = self._id - self._last_matches[team] - 1
        if distance_from_last < self._minimum_separation:
            return float('inf')
        return 7.0 * (self._target_separation - distance_from_last)

    def evaluate(self, match):
        return sum(self._evaluate_team(team) for team in match)

    def reset(self):
        self._id = 0
        self._last_matches.clear()

