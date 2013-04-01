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
import check

ScheduleConfiguration = namedtuple('ScheduleConfiguration',
                                   ['zones', 'teams', 'weight_zones',
                                    'round_length', 'imbalance_action',
                                    'match_count'])

if __name__ == '__main__':
    config = ScheduleConfiguration(zones = 4,
                                   teams = ['Team {0}'.format(x) for x in xrange(1, 11)],
                                   weight_zones = True,
                                   round_length = None,
                                   imbalance_action = 'empty',
                                   match_count = 25)
    schedule = sched_utils.full_schedule(config)
    check.schedule_check(schedule)
    import json
    print json.dumps(schedule)

