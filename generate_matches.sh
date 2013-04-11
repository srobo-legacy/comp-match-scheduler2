#!/bin/sh

# Imported data; and Alistair assures me there are 103 matches this year...
cwd=`pwd`
matchcount=1
for line in `./run full ${cwd}/teams-2013 103`; do
  # Fixme
  cd /srv/compd/command

  teamlist=`echo $line | tr '|' ' '`

  # Match name
  name="match-${matchcount}"
  echo $name

  # Starting at 13:20...
  matchsub1=`expr $matchcount - 1`
  # 5 minutes matches..
  mins=`expr $matchsub1 \* 5`
  mins=`expr $mins + 20`
  hours=`expr $mins / 60`
  mins=`expr $mins % 60`
  hours=`expr $hours + 13`

  # Hard coded because bah.
  #/srv/compd/command add-match $name $time

  matchcount=`expr $matchcount + 1`
done
