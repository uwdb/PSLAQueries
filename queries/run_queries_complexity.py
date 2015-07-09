import copy
import json
import os
import requests
from threading import Lock
import urllib
import subprocess
import time
import myria
import random
from os import listdir
from os.path import isfile, join

hostname = 'localhost'
port = 8753

connection = myria.MyriaConnection(hostname=hostname, port=port)

#params
cluster_name = "mycluster-ganglia"
output_shortname = "complexity_test"

first_worker_obs = "node001"
second_worker_obs = "node012"

qPath = [ 
		#"tpch/tpch-type2/4/",
		#"tpch/tpch-type2/6/",
		#"tpch/tpch-type2/8/",
		#"tpch/tpch-type2/10/",
		#"tpch/tpch-type2/12/",

		#"tpch/tpch-type3/tpch-type3a/4_datanodes/6_computenodes/",
		#"tpch/tpch-type3/tpch-type3a/4_datanodes/8_computenodes/",
		#"tpch/tpch-type3/tpch-type3a/4_datanodes/10_computenodes/",
		#"tpch/tpch-type3/tpch-type3a/4_datanodes/12_computenodes/",
		#"tpch/tpch-type3/tpch-type3a/6_datanodes/8_computenodes/",
		#"tpch/tpch-type3/tpch-type3a/6_datanodes/10_computenodes/",
		#"tpch/tpch-type3/tpch-type3a/6_datanodes/12_computenodes/",
		#"tpch/tpch-type3/tpch-type3a/8_datanodes/10_computenodes/",
		#"tpch/tpch-type3/tpch-type3a/8_datanodes/12_computenodes/",
		#"tpch/tpch-type3/tpch-type3a/10_datanodes/12_computenodes/",

		#"tpch/tpch-type3/tpch-type3b/6_datanodes/4_computenodes/",
		#"tpch/tpch-type3/tpch-type3b/8_datanodes/4_computenodes/",
		#"tpch/tpch-type3/tpch-type3b/8_datanodes/6_computenodes/",
		#"tpch/tpch-type3/tpch-type3b/10_datanodes/4_computenodes/",
		#"tpch/tpch-type3/tpch-type3b/10_datanodes/6_computenodes/",
		#"tpch/tpch-type3/tpch-type3b/10_datanodes/8_computenodes/",
		#"tpch/tpch-type3/tpch-type3b/12_datanodes/4_computenodes/",
		#"tpch/tpch-type3/tpch-type3b/12_datanodes/6_computenodes/",
		#"tpch/tpch-type3/tpch-type3b/12_datanodes/8_computenodes/",
		#"tpch/tpch-type3/tpch-type3b/12_datanodes/10_computenodes/"

		#"tpch/multi-tenant/2_tenants-2_shared/",
		#"tpch/multi-tenant/2_tenants-4_shared/",
		#"tpch/multi-tenant/2_tenants-6_shared/",
		#"tpch/multi-tenant/2_tenants-8_shared/",

		#"tpch/multi-tenant/3_tenants-2_shared/",
		#"tpch/multi-tenant/3_tenants-4_shared/",
		#"tpch/multi-tenant/3_tenants-6_shared/",
		#"tpch/multi-tenant/3_tenants-8_shared/",

		#"tpch/multi-tenant/4_tenants-2_shared/",
		#"tpch/multi-tenant/4_tenants-4_shared/",
		#"tpch/multi-tenant/4_tenants-6_shared/",
		#"tpch/multi-tenant/4_tenants-8_shared/"

		"complexity_test/"
		]


for p in qPath:
	counter = 0;
	print "FOR PATH " + p
	
	#open the file to log the runtimes
	f = open(os.path.expanduser(p + "runtimes.txt"), 'w');

	#get all queries in current path
	qList = os.listdir("/root/PSLAQueries/queries/"+ p)

	#for each query in the path
	for q in qList:
		averageTime = 0.0
		try:
			q = q.strip()
			print "Q", q
			print 'Query Path: ', p  + str(q)

			#call bash scripts
			subprocess.call(['/bin/bash',"clear-tpch.sh"]);
			print("postgres and os cleared")
			time.sleep(10)

			json_data=open(os.path.expanduser(p + str(q)))
			data = json.load(json_data)
			json_data.close()

			#try running the query
			try:
				query_start_time = time.time()
				query_status = connection.submit_query(data)
				query_id = query_status['queryId']
			except myria.MyriaError as e:
				print("MyriaError")
				print('Query #' + str(counter));


			status = (connection.get_query_status(query_id))['status']

			#keep checking, sleep a little
			while status!='SUCCESS':
				status = (connection.get_query_status(query_id))['status']
				print(status);
				if status=='SUCCESS':
					break;
				elif status=='ERROR':
					f.write('ERROR: ')
					break;
				elif status=='KILLED':
					break;
				time.sleep(2);

			if status!='KILLED':
				#collect time elapsed
				print('Query #' + str(counter) + ' Finished with ' + status);
				totalElapsedTime = int((connection.get_query_status(query_id))['elapsedNanos'])
				averageTime = averageTime + totalElapsedTime

				#mark as done and write to file
				done = True
				f.write(str(counter) + ',' + str(q) + ',' +  str(query_start_time));
				f.write(',' +  str(time.time()) + "\n");
				counter = counter + 1

				print averageTime
			else: #something went wrong, try again
				print("Trying again");
				print('Query #' + str(counter));

		except:
			print "Query does not exist"
			break

time.sleep(100)
#ganglia metics

xml_file = "cpu_user-" + output_shortname + "-" + second_worker_obs + ".xml"

bashCommand = "rrdtool dump /var/lib/ganglia/rrds/myCluster/" + cluster_name + "-" + second_worker_obs + "/cpu_user.rrd >> " + xml_file
print bashCommand
os.system(bashCommand)
bashCommand = "aws s3 cp " + xml_file + " s3://ganglia-runtimes/"
print bashCommand
os.system(bashCommand)