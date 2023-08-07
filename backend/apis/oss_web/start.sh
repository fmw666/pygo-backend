srv_name="oss_web_main"
chmod +x ./$srv_name
# if srv_name is running, restart it
if pgrep -x "$srv_name" > /dev/null
then
    echo "${srv_name} is running, restart it"
    if ps -a | grep $srv_name | awk '{print $1}' | xargs kill $1
    then
        echo "starting ${srv_name}"
        ./$srv_name > /dev/null 2>&1 &
        echo "start ${srv_name} success"
    fi
else
    echo "starting ${srv_name}"
    ./$srv_name > /dev/null 2>&1 &
    echo "start ${srv_name} success"
fi
