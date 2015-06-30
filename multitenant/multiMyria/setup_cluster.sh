TENANT_A=/root/multiMyria/configs/T1_2.ec2.cfg
TENANT_B=/root/multiMyria/configs/T2_2.ec2.cfg
OLD_A=
OLD_B=

cd /root/myria/myriadeploy
./stop_all_by_force.py $OLD_A
./kill_all_java_processes.py $OLD_A
./stop_all_by_force.py $OLD_B
./kill_all_java_processes.py $OLD_B

python setup_cluster.py $TENANT_A
python setup_cluster.py $TENANT_B
./launch_cluster.sh $TENANT_A
./launch_cluster.sh $TENANT_B

/root/multiMyria/ingest/ingest_2.sh
