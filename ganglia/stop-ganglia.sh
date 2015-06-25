# View README.txt
workers="gangliacluster-node001"

# Restart all services on master
sudo service ganglia-monitor stop && sudo service gmetad stop && sudo service apache2 stop

# Restart on workers
RESTART_CMD="sudo service ganglia-monitor stop"
parallel -k --jobs +28 "/bin/echo -n '{} -- ' && ssh {} '$RESTART_CMD'" ::: $workers