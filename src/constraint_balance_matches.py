from collections import defaultdict
import constraint
import utils


class BalanceMatchCountConstraint(constraint.Constraint):
    def __init__(self):
        self._team_match_counts = defaultdict(lambda: 0)
        self._id = 0

    def update(self, match):
        for team in match:
            if utils.is_actual_entrant(team):
                self._team_match_counts[team] += 1
        self._id += 1

    def evaluate(self, match):
        return 10.0 * sum(self._team_match_counts[team] for team in match) / float(self._id + 1)

    def reset(self):
        self._id = 0
        self._team_match_counts.clear()
