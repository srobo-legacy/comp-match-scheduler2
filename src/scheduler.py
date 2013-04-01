from collections import namedtuple, defaultdict, deque
from random import Random
import constraint_maxteams
import constraint_distribute
import constraint_balance_zones
import constraint_balance_matches
import constraint_once_only
import constraint_roundwise
import constraint_compound
import sched

ScheduleConfiguration = namedtuple('ScheduleConfiguration',
                                   ['zones', 'teams', 'weight_zones',
                                    'round_length', 'imbalance_action',
                                    'match_count'])

def full_schedule(configuration):
    scheduler = sched.Scheduler(configuration)
    scheduler.compute_full_schedule()
    return scheduler.matches

def partial_schedule(configuration, past_matches):
    scheduler = sched.Scheduler(configuration)
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

