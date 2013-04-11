#!/bin/sh

# Imported data; and Alistair assures me there are 103 matches this year...
cwd=`pwd`
compd_dir=/srv/compd
matchcount=1
# Actually say 102 matches, because this script always produces one more...
for line in `./run full ${cwd}/teams-2013 102`; do
  # Fixme
  cd $compd_dir

  teamlist=`echo $line | tr '|' ' '`

  # Match name
  name="match-${matchcount}"
  echo $name

  matchtime=`${cwd}/match2time.py ${matchcount}`
  echo $matchtime

  # Hard coded because bah.
  ./command add-match $name $matchtime
  ./command set-match-teams $name $teamlist

  matchcount=`expr $matchcount + 1`
done
