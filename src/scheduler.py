from collections import namedtuple
import sched_utils
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

