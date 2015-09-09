#imported some  from myria-web-py
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

tenant_limit = range(10)
qList = ['1GB']
p = '/root/PSLAQueries/read_chunks/multi-network/'
q_type = 'netquery_'

query_id_mapper = []

f = open(os.path.expanduser("/root/runtimes.txt"), 'w');

for q in qList:
	q = q.strip()
	print "Q", q
	print 'Query Path: ', p + q_type + str(q) + ".json"
	json_data=open(os.path.expanduser(p + q_type + str(q) + ".json"))
	data = json.load(json_data)
	json_data.close()

	#try running the query
	for j in tenant_limit:
		query_id_mapper = []
		command = "ssh mycluster-node001 'sudo service postgresql restart && free && sync && echo \"echo 1 > /proc/sys/vm/drop_caches\" | sudo sh'"
		os.system(command)

		#amount of times to fire query
		for k in range(j+1): 
			try:
				query_status = connection.submit_query(data)
				query_id = query_status['queryId']
				query_id_mapper.append(query_id)
			except myria.MyriaError as e:
				print("MyriaError")

		#wait for all queries to finish
		done = False
		while not done:
			done = True
			for q in query_id_mapper:
				status = (connection.get_query_status(q))['status']
				print status
				time.sleep(10)
				if status!='SUCCESS':
					done = False

		#record the runtimes
		f.write(str(j) + " batch : \n")
		for q in query_id_mapper:
			totalElapsedTime =  (connection.get_query_status(q))['elapsedNanos']
			f.write(str(totalElapsedTime)+ ",")
		f.write("\n")
		f.flush()
	f.close()
