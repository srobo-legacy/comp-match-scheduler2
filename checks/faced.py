
import collections
import sys

VERBOSE = False

if len(sys.argv) != 2 or '--help' in sys.argv:
    print 'Usage: faced.py <schedule-file>'
    print '  Displays statistics about which others a team have faced'
    exit(1)

matches = []
lines = [x.strip() for x in open(sys.argv[1])]
for line in lines:
    players = line.split('|')
    while len(players) > 4:
        matches.append(players[0:3])
        players = players[4:]
    matches.append(players[0:3])

c = collections.defaultdict(collections.Counter)

for match in matches:
    for tla in match:
        for faces in match:
            c[tla][faces] += 1

all_teams = set(c.keys())

# total appearances / teams => max appearances per team
# 4.0 is teams-per-match
matches_per_team = int(round(len(matches) * 4.0 / len(all_teams)))

# 4.0 means this is 1/4 of a team's matches
LOTS_REPEATS_LIMIT = int(round(matches_per_team / 4.0))

for tla, opponents in c.iteritems():
    missed = all_teams - set(opponents.keys())
    del opponents[tla]
    all_repeats = {}
    lots_repeats = collections.Counter()
    faced = opponents.keys()
    for opp in faced:
        times = opponents[opp]
        if times > 1:
            all_repeats[opp] = times
        if times > LOTS_REPEATS_LIMIT:
            lots_repeats[opp] = times
    if VERBOSE:
        print '{0} faces {1} opponents: {2}'.format(tla, len(faced), faced)
        print '{0} repeats {1} opponents: {2}'.format(tla, len(all_repeats), all_repeats)
        print '{0} repeats {1} opponents lots of times: {2}'.format(tla, len(lots_repeats), lots_repeats)
        print '{0} misses {1} opponents: {2}'.format(tla, len(missed), missed)
    else:
        print '{0: <4} faces {1: >2}, misses {2: >2}, repeats {3: >2} more than {4} times' \
                .format(tla, len(faced), len(missed), len(lots_repeats), LOTS_REPEATS_LIMIT),
        if len(lots_repeats) > 1:
            worst = lots_repeats.most_common(1)[0]
            if worst[1] > 10:
                print '(including {0} {1} times)'.format(*worst),
        print
