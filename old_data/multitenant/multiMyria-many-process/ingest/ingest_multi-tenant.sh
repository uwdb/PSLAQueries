master_name="mycluster-large-master"
master_port_list="9001 9002 9003 9004 9005 9006 9007 9008 9009 9010"

for i in {1..10};
do
	arr_list=($master_port_list)
	./ingest_all.sh $master_name ${arr_list[$(($i-1))]} $i
done