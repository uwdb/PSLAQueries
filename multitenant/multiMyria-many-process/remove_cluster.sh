FILES=/configs/$1

cd /root/myria/myriadeploy
for f in $FILES
do
	./stop_all_by_force.py $f
	./kill_all_java_processes.py $f
done