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

hostname = 'mycluster-large-master'
port_list = ["9001","9002","9003","9004","9005","9006","9007","9008","9009","9010"]

qPath = [ 
		"queries/case_663/"
		]


for p in qPath:
	counter = 0;
	print "FOR PATH " + p

	#call bash scripts
	subprocess.call(['/bin/bash',"clear-mt-many.sh"]);
	print("postgres and os cleared")

	#for each tenant...run the query on that port
	for c in range(1,10+1):
		q = "query_to_run_tenant" + c +  ".json"
		connection = myria.MyriaConnection(hostname=hostname, port=port_list[c-1])
		try:
			print "Q", q
			print 'Query Path: ', p  + str(q)
			json_data=open(os.path.expanduser(p + str(q)))
			data = json.load(json_data)
			json_data.close()

			#try running the query
			try:
				query_status = connection.submit_query(data)
				query_id = query_status['queryId']
			except myria.MyriaError as e:
				print("MyriaError")
				print('Query #' + str(counter));

		except:
			print "Query does not exist"
			break