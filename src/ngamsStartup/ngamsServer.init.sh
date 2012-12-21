#!/bin/sh
#
#
# chkconfig: 2345 99 70
# description: Starts and stops the ngamsServer
# processname: ngamsServer
# config: /etc/ngamsServer.conf

# Source function library.
. /etc/rc.d/init.d/functions

RETVAL=0
NGAMS_PID_FILE="/NGAS/.NGAS-"${HOSTNAME}"-7777"

# See how we were called.
case "$1" in
  start)
#	echo -n "Starting ngamsServer: "

#	daemon --user ngas "/opsw/packages/bin/ngamsServer -cfg /etc/ngamsServer.conf -autoOnline -force"
   	su - ngas -c "ngamsServer -cfg ngamsServer.conf -autoOnline -force -multiplesrvs&"

	echo "NG/AMS startup"
	[ $RETVAL -eq 0 ] && touch /var/lock/subsys/ngamsServer
#	RETVAL=$?
	;;
  stop)
#	echo -n "Stopping ngamsServer: "
	su - ngas -c "/opsw/packages/bin/ngamsPClient -port 7777 -host $HOSTNAME -status -cmd OFFLINE -force" 1>/dev/null 2>&1
	su - ngas -c "/opsw/packages/bin/ngamsPClient -port 7777 -host $HOSTNAME -status -cmd EXIT" 1>/dev/null 2>&1
        if [[ -e ${NGAMS_PID_FILE} ]]
	then
	  NGAMS_PID=$(cat ${NGAMS_PID_FILE})
	  /bin/kill -9 ${NGAMS_PID}
	  echo "NG/AMS PID "${NGAMS_PID}" killed."
	  rm -f ${NGAMS_PID_FILE}
	  echo "NG/AMS PID FILE "${NGAMS_PID_FILE}" removed."
	fi
	RETVAL=$?
	echo "NG/AMS shutdown"
	;;
  status)
	echo "Status ngamsServer: "
	su - ngas -c "/opsw/packages/bin/ngamsPClient -port 7777 -host $HOSTNAME -status -cmd STATUS"
	RETVAL=$?
	;;
  restart)
	echo -n "Restarting ngamsServer: "
	$0 stop
	$0 start
	RETVAL=$?
	;;
  *)
	echo "Usage: $0 {start|stop|status|restart}"
	exit 1
esac

#exit $RETVAL