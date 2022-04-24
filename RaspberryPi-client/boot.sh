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
fi

if [ $i -gt 0 ]; then
    i+=1
    echo "$i"
    sed -i "1c ${i}" logs/start.log

    rm /tmp/appLog.out > /dev/null 2>&1
    touch /tmp/appLog.out
    chmod 777 /tmp/appLog.out
    echo "hello pi~" >> /tmp/appLog.out

    python3 /home/pi/remoteControlApp/app.py > /tmp/appLog.out 2>&1
    python3 ./app.py > /tmp/appLog.out 2>&1
fi