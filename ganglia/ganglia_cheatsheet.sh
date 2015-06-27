sed -i 's/{REPLACE ME}/10.164.168.237/g' workerGangliaFiles/gmond.conf
sed -i 's/workers="gangliacluster-node001"/workers="mycluster-node001 mycluster-node002 mycluster-node003 mycluster-node004 mycluster-node005 mycluster-node006 mycluster-node007 mycluster-node008 mycluster-node009 mycluster-node010 mycluster-node011 mycluster-node012"/g' restart-ganglia.sh
sed -i 's/workers="gangliacluster-node001"/workers="mycluster-node001 mycluster-node002 mycluster-node003 mycluster-node004 mycluster-node005 mycluster-node006 mycluster-node007 mycluster-node008 mycluster-node009 mycluster-node010 mycluster-node011 mycluster-node012"/g' stop-ganglia.sh
sed -i 's/workers="gangliacluster-node001"/workers="mycluster-node001 mycluster-node002 mycluster-node003 mycluster-node004 mycluster-node005 mycluster-node006 mycluster-node007 mycluster-node008 mycluster-node009 mycluster-node010 mycluster-node011 mycluster-node012"/g' setup_ganglia_workers.sh

./setup_ganglia_workers.sh
./setup_ganglia_master.sh