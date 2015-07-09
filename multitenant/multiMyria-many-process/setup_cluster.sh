FILES=/configs/$1

cd /root/myria/myriadeploy
for f in $FILES
do 
	python setup_cluster.py $f
	./launch_cluster.sh $f
done