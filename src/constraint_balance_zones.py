from collections import defaultdict
import constraint
import utils


class BalanceZoneCountConstraint(constraint.Constraint):
    def __init__(self):
        self._team_zone_counts = defaultdict(lambda: 0)
        self._id = 0

    def update(self, match):
        for zone, team in enumerate(match):
            if utils.is_actual_entrant(team):
                self._team_zone_counts[team, zone] += 1
        self._id += 1

    def evaluate(self, match):
        return (sum(self._team_zone_counts[team, zone] for zone, team in enumerate(match))
                / float(self._id + 1))

    def reset(self):
        self._id = 0
        self._team_zone_counts.clear()
