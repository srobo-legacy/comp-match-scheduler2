#!/usr/bin/env python
"""Match scheduler.

Usage:
  scheduler.py full <teams> <matches> [options]
  scheduler.py partial <teams> <previous> <matches> [options]

Options:
  -w --weight      Try to balance out between starting zones.
  --zones=<z>      Number of start zones [default: 4].
  --empty          Leave empty spaces to balance out the match distribution.
  --surrogate      Use surrogate appearances to balance out the distribution.
  --rounds=<r>     Divide the schedule into rounds of length r.
  -h --help        Show this screen.
"""

from collections import namedtuple
import sched_utils
import check
import sys
from docopt import docopt

ScheduleConfiguration = namedtuple('ScheduleConfiguration',
                                   ['zones', 'teams', 'weight_zones',
                                    'round_length', 'imbalance_action',
                                    'match_count'])

if __name__ == '__main__':
    options = docopt(__doc__)
    rl = int(options['--rounds']) if options['--rounds'] else None
    imba = 'empty'
    if options['--surrogate']:
        imba = 'surrogate'
    if options['--empty']:
        imba = 'empty'
    with open(options['<teams>'], 'r') as f:
        print >> sys.stderr, 'Using:', options["<teams>"]
        teams = [x.strip() for x in f if x.strip()]
    if options['partial']:
        with open(options['<previous>'], 'r') as f:
            partial = [x.strip().split('|') for x in f if x.strip()]
    else:
        partial = None
    config = ScheduleConfiguration(zones = int(options['--zones']),
                                   teams = teams,
                                   weight_zones = options['--weight'],
                                   round_length = rl,
                                   imbalance_action = imba,
                                   match_count = int(options['<matches>']))
    if partial is None:
        schedule = sched_utils.full_schedule(config)
    else:
        schedule = sched_utils.partial_schedule(config, partial)
    check.schedule_check(schedule)
    for item in schedule:
        print '|'.join(item)

