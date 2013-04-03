import constraint
import utils
import random


class OnceOnlyConstraint(constraint.Constraint):
    def __init__(self, punishment = float('inf')):
        self._teams = set()
        self._punishment = punishment

    def update(self, match):
        for team in match:
            if utils.is_actual_entrant(team):
                self._teams.add(team)
        print 'Contained teams: ', list(sorted(self._teams))

    def _team_evaluate(self, team):
        return self._punishment if team in self._teams else 0.0

    def evaluate(self, match):
        return sum(self._team_evaluate(team) for team in match)

    def reset(self):
        self._teams.clear()

    def suggest_teams(self, full_roster):
        viable = set(full_roster) - self._teams
        yield random.sample(list(viable), 4)

