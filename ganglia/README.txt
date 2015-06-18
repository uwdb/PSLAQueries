To install ganglia on an AWS cluster, do the following:

1.  Update list of workers in setup_ganglia_workers.sh with correct cluster name

2.  Copy ganglia folder to master node:
      starcluster put mycluster --node mycluster-master ./ganglia /root/

3.  SSH to the master node:
      starcluster sshmaster mycluster

4.  Replace {REPLACE_ME} in workerGangliaFiles/gmond.conf with IP
    address of cluster master.

5.  Install parallel with:
      (wget -O - pi.dk/3 || curl pi.dk/3/ || fetch -o - http://pi.dk/3) | bash

6.  Run setup_ganglia_workers.sh from the ganglia directory

7.  Run setup_ganglia_master.sh from the ganglia directory

8.  View metrics at http://ec2-**-**-**-**.compute-1.amazonaws.com:8080
