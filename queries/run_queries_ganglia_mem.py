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

hostname = 'localhost'
port = 8753

connection = myria.MyriaConnection(hostname=hostname, port=port)

newList = False

if newList:
	qList = random.sample(range(240, 896), 100)
	qList.sort()
	r = open(os.path.expanduser("tpch-random.txt"), 'w')
	r.write(', '.join(map(str, qList)))
	r.close()
else:
	qList = open(os.path.expanduser("tpch-random.txt"), 'r')
	qList = qList.read().split(',')

#params
cluster_name = "mycluster-ganglia"
output_shortname = "DataNodes"

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

		#RUN THESE FOR GANGLIA
		"tpch/tpch-type3/tpch-type3b/12_datanodes/4_computenodes/",
		"tpch/tpch-type3/tpch-type3b/12_datanodes/6_computenodes/",
		"tpch/tpch-type3/tpch-type3b/12_datanodes/8_computenodes/",
		"tpch/tpch-type3/tpch-type3b/12_datanodes/10_computenodes/"
		]

currentPath = 0
for p in qPath:
	counter = 0
	#open the file to log the runtimes
	f = open(os.path.expanduser(p + "DATA_MEMORY_runtimes.txt"), 'w');
	print "FOR PATH " + p
	#for each query
	for q in qList:
		averageTime = 0.0
		done = False
		while not done: #keep trying until query runs sucessfully
			try:
				q = q.strip()
				print "Q", q
				print 'Query Path: ', p + "query" + str(q) + ".json"
				json_data=open(os.path.expanduser(p + "query" + str(q) + ".json"))
				data = json.load(json_data)
				json_data.close()

				#call bash scripts
				subprocess.call(['/bin/bash',"clear-tpch.sh"]);
				print("postgres and os cleared")

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

				#if the query was not killed then get the runtime and increase counter by one
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
				#f.write('N/A ')
				break

		timeSeconds = (averageTime / 1.0) /1000000000.0;
		print('Logging average runtime ' + str(timeSeconds));
		f.flush()
		#save to s3
		pathSplit = p.split('/')
		bashCommand = "aws s3 cp " +  str(p) + "DATA_MEMORY_runtimes.txt"+ " s3://ganglia-runtimes/DATA_MEMORY_timesTPCH" + str(currentPath) + ".txt"
		print bashCommand
		os.system(bashCommand)

		#kill myria/re-launch
		os.chdir("/root/myria/myriadeploy/")
		print os.getcwd()

		#kill myria/re-launch
		os.chdir("/root/myria/myriadeploy/")
		print os.getcwd()

		bashCommand = "./stop_all_by_force.py /root/deployment.cfg.ec2"
		print bashCommand
		os.system(bashCommand)

		bashCommand = "./kill_all_java_processes.py /root/deployment.cfg.ec2"
		print bashCommand
		os.system(bashCommand)

		bashCommand = "./launch_cluster.sh /root/deployment.cfg.ec2"
		print bashCommand
		os.system(bashCommand)

        	os.chdir("/root/PSLAQueries/queries/")
	        print os.getcwd()
		#time buffer for metrics
		time.sleep(30)
	
	currentPath = currentPath + 1
	f.close()

#ganglia metics
xml_file = "mem_cached-" + output_shortname + "-" + second_worker_obs + ".xml"

bashCommand = "rrdtool dump /var/lib/ganglia/rrds/myCluster/" + cluster_name + "-" + second_worker_obs + "/mem_cached.rrd >> " + xml_file
print bashCommand
os.system(bashCommand)
bashCommand = "aws s3 cp " + xml_file + " s3://ganglia-runtimes/"
print bashCommand
os.system(bashCommand)

xml_file = "mem_buffers-" + output_shortname + "-" + second_worker_obs + ".xml"

bashCommand = "rrdtool dump /var/lib/ganglia/rrds/myCluster/" + cluster_name + "-" + second_worker_obs + "/mem_buffers.rrd >> " + xml_file
print bashCommand
os.system(bashCommand)
bashCommand = "aws s3 cp " + xml_file + " s3://ganglia-runtimes/"
print bashCommand
os.system(bashCommand)

xml_file = "mem_free-" + output_shortname + "-" + second_worker_obs + ".xml"

bashCommand = "rrdtool dump /var/lib/ganglia/rrds/myCluster/" + cluster_name + "-" + second_worker_obs + "/mem_free.rrd >> " + xml_file
print bashCommand
os.system(bashCommand)
bashCommand = "aws s3 cp " + xml_file + " s3://ganglia-runtimes/"
print bashCommand
os.system(bashCommand)

xml_file = "mem_total-" + output_shortname + "-" + second_worker_obs + ".xml"

bashCommand = "rrdtool dump /var/lib/ganglia/rrds/myCluster/" + cluster_name + "-" + second_worker_obs + "/mem_total.rrd >> " + xml_file
print bashCommand
os.system(bashCommand)
bashCommand = "aws s3 cp " + xml_file + " s3://ganglia-runtimes/"
print bashCommand
os.system(bashCommand)