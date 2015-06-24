# View README.txt
workers="gangliacluster-node001"

# Restart all services on master
sudo service ganglia-monitor restart && sudo service gmetad restart && sudo service apache2 

# Restart on workers
RESTART_CMD="sudo service ganglia-monitor restart"
parallel -k --jobs +28 "/bin/echo -n '{} -- ' && ssh {} '$RESTART_CMD'" ::: $workers