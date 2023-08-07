srv_name="order_srv_server"
py_exec_path="/root/.virtualenvs/pygo_srv/bin/"
chmod +x ./$srv_name.py
# if srv_name is running, restart it
PIDS=`ps -ef | grep ${srv_name} | grep -v grep | awk '{print $2}'`
if [ "$PIDS" != "" ];
then
    echo "${srv_name} is running, restart it"
    if ps -ef | grep $srv_name | awk '{print $2}' | xargs kill $1
    then
        echo "starting ${srv_name}"
        $py_exec_path/pip install -r requirements.txt
        $py_exec_path/python $srv_name.py > /dev/null 2>&1 &
        echo "start ${srv_name} success"
    fi
else
    echo "starting ${srv_name}"
    $py_exec_path/pip install -r requirements.txt
    $py_exec_path/python $srv_name.py > /dev/null 2>&1 &
    echo "start ${srv_name} success"
fi
