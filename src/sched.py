from collections import deque
from random import Random
import constraint_balance_matches
import constraint_balance_zones
import constraint_compound
import constraint_distribute
import constraint_maxteams
import constraint_once_only
import constraint_roundwise


class Scheduler(object):
    def __init__(self, configuration):
        self.configuration = configuration
        self.matches = []
        self._constraint = None
        self._rng = Random(3)
        self._init_constraint()
        self._fill_order = deque(self.configuration.teams)
        self._rng.shuffle(self._fill_order)

    def _init_constraint(self):
        subconstraints = []
        if self.configuration.round_length is not None:
            subconstraints.append(constraint_roundwise.RoundwiseConstraint(sub = constraint_once_only.OnceOnlyConstraint(),
                                                      length = self.configuration.round_length))
        subconstraints.append(constraint_balance_matches.BalanceMatchCountConstraint())
        subconstraints.append(constraint_maxteams.MaximiseTeamsConstraint(2))
        subconstraints.append(constraint_distribute.DistributeMatchesConstraint(1, 2))
        if self.configuration.weight_zones:
            subconstraints.append(constraint_balance_zones.BalanceZoneCountConstraint())
        self._constraint = constraint_compound.CompoundConstraint(subconstraints)

    def add_match(self, match):
        self.matches.append(match)
        self._constraint.update(match)

    def _random_match(self):
        return self._rng.sample(self.configuration.teams +
                               ['-']*self.configuration.zones,
                               self.configuration.zones)

    def _random_match_pool(self, pool_size = 1400):
        return [self._random_match() for i in xrange(pool_size)]

    def _best_match_from_pool(self, pool):
        return min(pool, key = self._constraint.evaluate)

    def _is_viable(self, match):
        return self._constraint.evaluate(match) < float('inf')

    def _imbalance_surrogate(self, match):
        assert self.configuration.imbalance_action != 'empty'
        for i, team in enumerate(match):
            if team == '-':
                while True:
                    team = self._fill_order.popleft()
                    self._fill_order.append(team)
                    if team in match:
                        continue
                    match[i] = '-{0}'.format(team)
                    break

    def pick_match(self):
        pool = self._random_match_pool()
        next_match = self._best_match_from_pool(pool)
        if not self._is_viable(next_match):
            raise ValueError("no viable matches")
        if self.configuration.imbalance_action == 'surrogate':
            self._imbalance_surrogate(next_match)
        self.add_match(next_match)

    def pick_all_matches(self):
        while len(self.matches) < self.configuration.match_count:
            self.pick_match()

    def reset(self):
        if self.matches:
            self._constraint.reset()
            self.matches = []

    def compute_full_schedule(self):
        self.reset()
        self.pick_all_matches()

    def compute_partial_schedule(self, past_matches):
        self.reset()
        for match in past_matches:
            self.add_match(match)
        self.pick_all_matches()
