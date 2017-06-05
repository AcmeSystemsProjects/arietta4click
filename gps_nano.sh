#!/bin/sh

#trap 'echo "argh"' KILL INT TERM EXIT
 
/bin/echo "Nano GPS `/bin/date`"


while [ "1" ] ; do
        sleep 1
        /bin/stty  -F /dev/ttyS1 ispeed 4800 -crtscts cs8 min 0 time 10
        /bin/cat < /dev/ttyS1 > gps_nano.txt
done




