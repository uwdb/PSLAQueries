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

qList = ['500MB','1GB','2GB','3GB']
p = '/root/PSLAQueries/ioquery/'
q_type = 'ioquery_'
f = open(os.path.expanduser(p + "runtimes.txt"), 'w');
cluster_name  = 'mycluster-local'

for q in qList:
	q = q.strip()
	print "Q", q
	print 'Query Path: ', p + q_type + str(q) + ".json"
	json_data=open(os.path.expanduser(p + q_type + str(q) + ".json"))
	data = json.load(json_data)
	json_data.close()
	
	list_query_runtimes = []
	#try running the query
	for j in range(3):
		#call bash scripts
		command = "ssh " + cluster_name + "-node001 'sudo service postgresql restart && free && sync && echo \"echo 1 > /proc/sys/vm/drop_caches\" | sudo sh'"
		os.system(command)
		print("postgres and os cleared")
		try:
			query_status = connection.submit_query(data)
			query_id = query_status['queryId']
		except myria.MyriaError as e:
			print("MyriaError")

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
		#done, add the runtime
		totalElapsedTime = int((connection.get_query_status(query_id))['elapsedNanos'])
		list_query_runtimes.append(totalElapsedTime)
	#loop through times and get min, max and average
	f.write(str(q) + ': ' + '\n')
	f.write('average: ' + str(sum(list_query_runtimes)/float(len(list_query_runtimes)))+ '\n')
	f.write('min :' + str(min(list_query_runtimes))+ '\n')
	f.write('max : ' + str(max(list_query_runtimes))+ '\n')
	f.write('\n')
f.close()