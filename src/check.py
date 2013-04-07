import match_stats
import sys
import utils


def schedule_check(matches):
    print >>sys.stderr, '{0} matches total'.format(len(matches))
    match_counter, opponents, collisions = match_stats.match_statistics(matches)
    all_teams = set(x for x in match_counter.iterkeys() if utils.is_actual_entrant(x))
    for team, matches in match_counter.iteritems():
        if not utils.is_actual_entrant(team):
            continue
        print >>sys.stderr, '{0}: {1} matches, missed opponents: {2}'.format(team, matches, ', '.join(all_teams - opponents[team] - {team}))
        if team in collisions:
            print >>sys.stderr, '\t{0} DO have a match collision'.format(team)
