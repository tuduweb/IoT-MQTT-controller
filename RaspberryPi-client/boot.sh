#!/bin/sh

declare -i i=0
i=$(cat logs/start.log)

#first boot register
if [ $i -lt 1 ]; then
    python3 ./register.py > /tmp/registerLog.out 2>&1
    cat /tmp/registerLog.out | grep "success" > /dev/null
    if [  $? == 0 ]; then
        i+=1
        sed -i "1c ${i}" logs/start.log
    fi    
else
    i+=1
    echo "$i"
    sed -i "1c ${i}" logs/start.log
    #touch /home/pi/testboot.txt
    #chmod 777 /home/pi/testboot.txt
    #echo "hello pi~" >> /home/pi/testboot.txt

    #python3 /home/pi/remoteControlApp/app.py > /tmp/appLog.out 2>&1
    python3 ./app.py > /tmp/appLog.out 2>&1
fi