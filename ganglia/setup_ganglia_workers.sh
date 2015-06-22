# View README.txt
workers="gangliacluster-node001"

# Copy ganglia files to worker
parallel -k --jobs +28 "scp ./workerGangliaFiles/gmond.conf {}:/root/" ::: $workers

# Setup all gmonds on workers
SETUP_CMD="sudo apt-get install ganglia-monitor"
CP_CMD="cp ./gmond.conf /etc/ganglia/"
START_CMD="sudo service ganglia-monitor start"
parallel -k --jobs +28 "/bin/echo -n '{} -- ' && ssh {} '$SETUP_CMD'" ::: $workers
parallel -k --jobs +28 "/bin/echo -n '{} -- ' && ssh {} '$CP_CMD'" ::: $workers
parallel -k --jobs +28 "/bin/echo -n '{} -- ' && ssh {} '$START_CMD'" ::: $workers