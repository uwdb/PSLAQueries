sed -i 's/{REPLACE ME}/10.164.168.237/g' ganglia/workerGangliaFiles/gmond.conf
sed -i 's/workers="gangliacluster-node001"/workers="mycluster-node001 mycluster-node002 mycluster-node003 mycluster-node004 mycluster-node005 mycluster-node006 mycluster-node007 mycluster-node008"/g' ganglia/restart-ganglia.sh
sed -i 's/workers="gangliacluster-node001"/workers="mycluster-node001 mycluster-node002 mycluster-node003 mycluster-node004 mycluster-node005 mycluster-node006 mycluster-node007 mycluster-node008"/g' ganglia/stop-ganglia.sh
sed -i 's/workers="gangliacluster-node001"/workers="mycluster-node001 mycluster-node002 mycluster-node003 mycluster-node004 mycluster-node005 mycluster-node006 mycluster-node007 mycluster-node008"/g' ganglia/setup_ganglia_workers.sh

./ganglia/setup_ganglia_workers.sh
./ganglia/setup_ganglia_master.sh