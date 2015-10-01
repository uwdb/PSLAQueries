FILES=/root/PSLAQueries/multitenant/multiMyria-many-process/configs/$1/*

cd /root/myria/myriadeploy
for f in $FILES
do
	./remove_deployment.py $f
done