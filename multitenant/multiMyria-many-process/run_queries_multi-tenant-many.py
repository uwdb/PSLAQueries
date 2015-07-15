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

hostname = 'mycluster-master'
port_list = ["9001","9002","9003","9004","9005","9006","9007","9008","9009","9010"]

qPath = [ 
		"queries/case_663/"
		]

f = open(os.path.expanduser("/root/runtimes-multi.txt"), 'w')

for numberTenants in range(1,11):
	for p in qPath:
		counter = 0;
		print "FOR PATH " + p

		#call bash scripts
		subprocess.call(['/bin/bash',"clear-mt-many.sh"]);
		print("postgres and os cleared")

		#each master will have an active query running
		query_id_mapper = []

		#for each tenant...run the query on that port
		for c in range(1,numberTenants+1):
			q = "query_to_run_tenant" + str(c) +  ".json"
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

				query_id_mapper.append(query_id)

			except:
				print "Query does not exist"
				break

		#wait for all tenants to finish
		print query_id_mapper
		done = False
		while not done:
			done = True
			time.sleep(5)
			for c in range(1,numberTenants+1):
				connection = myria.MyriaConnection(hostname=hostname, port=port_list[c-1])
				status = (connection.get_query_status(query_id_mapper[c-1]))['status']
				if status!='SUCCESS':
					done = False 

		#record the runtimes
		f.write(str(numberTenants) + "-" + str(p) + "\n")
		for c in range(1,numberTenants+1):
			connection = myria.MyriaConnection(hostname=hostname, port=port_list[c-1])
			totalElapsedTime =  (connection.get_query_status(query_id_mapper[c-1]))['elapsedNanos']
			f.write(str(totalElapsedTime)+ ",")
		f.write("\n")
		f.flush()
f.close()