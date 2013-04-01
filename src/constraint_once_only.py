import constraint
import utils


class OnceOnlyConstraint(constraint.Constraint):
    def __init__(self, punishment = float('inf')):
        self._teams = set()
        self._punishment = punishment

    def update(self, match):
        for team in match:
            if utils.is_actual_entrant(team):
                self._teams.add(team)

    def _team_evaluate(self, team):
        return self._punishment if team in self._teams else 0.0

    def evaluate(self, match):
        return sum(self._team_evaluate(team) for team in match)

    def reset(self):
        self._teams.clear()
