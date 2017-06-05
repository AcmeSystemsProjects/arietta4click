#!/bin/sh 

#trap 'echo "argh"' KILL INT TERM EXIT

/bin/echo "GNSS3 `/bin/date`"

while [ "1" ] ; do
	sleep 1
	/bin/stty  -F /dev/ttyS2 ispeed 115200 ospeed 115200 -crtscts cs8 min 0 time 100
	/bin/cat < /dev/ttyS2 > gps_gnss3.txt
done




