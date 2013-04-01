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
import sched_utils
import match_stats

ScheduleConfiguration = namedtuple('ScheduleConfiguration',
                                   ['zones', 'teams', 'weight_zones',
                                    'round_length', 'imbalance_action',
                                    'match_count'])

def schedule_check(matches):
    print '{0} matches total'.format(len(matches))
    match_counter, opponents, collisions = match_stats.match_statistics(matches)
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
    schedule = sched_utils.full_schedule(config)
    schedule_check(schedule)
    import json
    print json.dumps(schedule)

