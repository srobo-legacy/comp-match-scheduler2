#!/usr/bin/env python

# Caution: matchno is one based.

import sys, datetime

if len(sys.argv) != 2:
    print >>sys.stderr, "Usage: match2time.py matchno"
    sys.exit(1)

match_length = datetime.timedelta(0, 300)
match_time = None
matchno = int(sys.argv[1])
if matchno <= 50:
    # On the first day
    start = datetime.datetime(2013, 4, 13, 13, 20)
    match_time = start + (match_length * (matchno - 1))
elif matchno <= 76:
    # On second day, first half,
    start = datetime.datetime(2013, 4, 14, 9, 35)
    match_time = start + (match_length * (matchno - 51))
else:
    start = datetime.datetime(2013, 4, 14, 13, 15)
    match_time = start + (match_length * (matchno - 77))

print match_time.isoformat()
