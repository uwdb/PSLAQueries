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

hostname = 'ec2-54-197-147-1.compute-1.amazonaws.com'
port = 8753

connection = myria.MyriaConnection(hostname=hostname, port=port)

qList = ['_case399_t1','_case399_shared8_t2']


qPath = [ 
		"tpch/multi-tenant-queries/single-process/"
		]

for p in qPath:
	caseCount = 0
	counter = 0;
	#open the file to log the runtimes
	f = open(os.path.expanduser(p + "runtimes.txt"), 'w');
	print "FOR PATH " + p
	#for each query
	#call bash scripts
	subprocess.call(['/bin/bash',"clear-tpch-msp.sh"]);
	print("postgres and os cleared")
	for q in qList:
		averageTime = 0.0
		i = 0

		while i < 1:
			try:
				print "Q", q
				print 'Query Path: ', p + "query" + str(q) + ".json"
				json_data=open(os.path.expanduser(p + "query" + str(q) + ".json"))
				data = json.load(json_data)
				json_data.close()


				#try running the query
				try:
					query_status = connection.submit_query(data)
					query_id = query_status['queryId']
				except myria.MyriaError as e:
					print("MyriaError")
					print('Query #' + str(counter));

				status = (connection.get_query_status(query_id))['status']

			except:
				print "Query does not exist"
				f.write('N/A ')
				break
			i = i + 1
		timeSeconds = (averageTime / 1.0) /1000000000.0;
		print('Logging average runtime ' + str(timeSeconds));
		f.write(str(counter) + ',' + str(q) + ',' +  str(timeSeconds) + "\n");
		f.flush()
		pathSplit = p.split('/')
		counter = counter + 1;
	f.close();
