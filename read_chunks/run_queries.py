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

qList = ['500MB', '1GB', '2GB', '3GB', '4GB', '5GB']
p = '/root/PSLAQueries/read_chunks/'
q_type = 'ioquery_'

for q in qList:
	q = q.strip()
	print "Q", q
	print 'Query Path: ', p + q_type + str(q) + ".json"
	json_data=open(os.path.expanduser(p + q_type + str(q) + ".json"))
	data = json.load(json_data)
	json_data.close()

	#try running the query
	for j in range(3):
		#call bash scripts
		command = "ssh mycluster-node001 'sudo service postgresql restart && free && sync && echo \"echo 1 > /proc/sys/vm/drop_caches\" | sudo sh'"
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
