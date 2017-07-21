#!/bin/sh
# chkconfig: 123456 90 10
# PLACE TO /etc/rc.d/init.d/comments_delete

workdir=/var/www/python-lab/vkontakte_tools/comments_delete
 
start() {
    cd $workdir
    /usr/local/bin/python3 /var/www/python-lab/vkontakte_tools/comments_delete/worker_comments_delete.py &
    echo "Server started."
}
 
stop() {
    pid=`ps -ef | grep '[p]ython3 /var/www/python-lab/vkontakte_tools/comments_delete/worker_comments_delete.py' | awk '{ print $2 }'`
    echo $pid
    kill $pid
    sleep 2
    echo "Server killed."
}
 
case "$1" in
  start)
    start
    ;;
  stop)
    stop   
    ;;
  restart)
    stop
    start
    ;;
  *)
    echo "Usage: /etc/init.d/tornado-tts {start|stop|restart}"
    exit 1
esac
exit 0