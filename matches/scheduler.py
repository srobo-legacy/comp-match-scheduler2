from collections import namedtuple, defaultdict, deque
from random import Random

ScheduleConfiguration = namedtuple('ScheduleConfiguration',
                                   ['zones', 'teams', 'weight_zones',
                                    'round_length', 'imbalance_action',
                                    'match_count'])

INFINITY = float('inf')

def is_actual_entrant(team):
    return team[0] != '-'

class Constraint(object):
    def __init__(self):
        pass

    def update(self, match):
        pass

    def evaluate(self, match):
        return 0.0

    def reset(self):
        pass

class CompoundConstraint(Constraint):
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

class WeightedConstraint(Constraint):
    def __init__(self, sub, weight):
        self._sub = sub
        self._weight = weight

    def update(self, match):
        self._sub.update(match)

    def evaluate(self, match):
        return self.weight * self._sub.evaluate(match)

    def reset(self):
        self._sub.reset()

class RoundwiseConstraint(Constraint):
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

class OnceOnlyConstraint(Constraint):
    def __init__(self, punishment = INFINITY):
        self._teams = set()
        self._punishment = punishment

    def update(self, match):
        for team in match:
            if is_actual_entrant(team):
                self._teams.add(team)

    def _team_evaluate(self, team):
        return self._punishment if team in self._teams else 0.0

    def evaluate(self, match):
        return sum(self._team_evaluate(team) for team in match)

    def reset(self):
        self._teams.clear()

class BalanceMatchCountConstraint(Constraint):
    def __init__(self):
        self._team_match_counts = defaultdict(lambda: 0)
        self._id = 0

    def update(self, match):
        for team in match:
            if is_actual_entrant(team):
                self._team_match_counts[team] += 1
        self._id += 1

    def evaluate(self, match):
        return 10.0 * sum(self._team_match_counts[team] for team in match) / float(self._id + 1)

    def reset(self):
        self._id = 0
        self._team_match_counts.clear()

class BalanceZoneCountConstraint(Constraint):
    def __init__(self):
        self._team_zone_counts = defaultdict(lambda: 0)
        self._id = 0

    def update(self, match):
        for zone, team in enumerate(match):
            if is_actual_entrant(team):
                self._team_zone_counts[team, zone] += 1
        self._id += 1

    def evaluate(self, match):
        return (sum(self._team_zone_counts[team, zone] for zone, team in enumerate(match))
                / float(self._id + 1))

    def reset(self):
        self._id = 0
        self._team_zone_counts.clear()

class DistributeMatchesConstraint(Constraint):
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
            return INFINITY
        return 7.0 * (self._target_separation - distance_from_last)

    def evaluate(self, match):
        return sum(self._evaluate_team(team) for team in match)

    def reset(self):
        self._id = 0
        self._last_matches.clear()

class MaximiseTeamsConstraint(Constraint):
    def __init__(self, max_blanks, punishment = 12.0):
        self._punishment = punishment
        self._max_blanks = max_blanks

    def evaluate(self, match):
        number_blank = len([x for x in match if not is_actual_entrant(x)])
        if number_blank > self._max_blanks:
            # this is not a viable match at all
            return INFINITY
        return (self._punishment * 2**number_blank) - self._punishment

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
            subconstraints.append(RoundwiseConstraint(sub = OnceOnlyConstraint(),
                                                      length = self.configuration.round_length))
        subconstraints.append(BalanceMatchCountConstraint())
        subconstraints.append(MaximiseTeamsConstraint(2))
        subconstraints.append(DistributeMatchesConstraint(1, 2))
        if self.configuration.weight_zones:
            subconstraints.append(BalanceZoneCountConstraint())
        self._constraint = CompoundConstraint(subconstraints)

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
        return self._constraint.evaluate(match) < INFINITY

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

def full_schedule(configuration):
    scheduler = Scheduler(configuration)
    scheduler.compute_full_schedule()
    return scheduler.matches

def partial_schedule(configuration, past_matches):
    scheduler = Scheduler(configuration)
    scheduler.compute_partial_schedule(past_matches)
    return scheduler.matches

def match_statistics(matches):
    from collections import Counter, defaultdict
    match_counter = Counter()
    opponents = defaultdict(set)
    prev_match = []
    collisions = set()
    for match in matches:
        for team in match:
            if team in prev_match:
                collisions.add(team)
            match_counter[team] += 1
            for other_team in match:
                if team != other_team:
                    opponents[team].add(other_team)
    return match_counter, opponents, collisions

def schedule_check(matches):
    print '{0} matches total'.format(len(matches))
    match_counter, opponents, collisions = match_statistics(matches)
    all_teams = set(match_counter.iterkeys())
    for team, matches in match_counter.iteritems():
        print '{0}: {1} matches, missed opponents: {2}'.format(team, matches, ', '.join(all_teams - opponents[team] - {team}))
        if team in collisions:
            print '\t{0} DO have a match collision'.format(team)

if __name__ == '__main__':
    config = ScheduleConfiguration(zones = 4,
                                   teams = ['Team {0}'.format(x) for x in xrange(1, 11)],
                                   weight_zones = True,
                                   round_length = None,
                                   imbalance_action = 'empty',
                                   match_count = 25)
    schedule = full_schedule(config)
    schedule_check(schedule)
    import json
    print json.dumps(schedule)

