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
