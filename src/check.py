import match_stats


def schedule_check(matches):
    print '{0} matches total'.format(len(matches))
    match_counter, opponents, collisions = match_stats.match_statistics(matches)
    all_teams = set(match_counter.iterkeys())
    for team, matches in match_counter.iteritems():
        print '{0}: {1} matches, missed opponents: {2}'.format(team, matches, ', '.join(all_teams - opponents[team] - {team}))
        if team in collisions:
            print '\t{0} DO have a match collision'.format(team)
