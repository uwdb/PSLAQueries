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

qList = [4,6,8,10]

qPath = [
		"folder/"
		]

for p in qPath:
	counter = 0;
	#open the file to log the runtimes
	f = open(os.path.expanduser(p + "runtimes.txt"), 'w');
	print "FOR PATH " + p
	#for each query
	for q in qList:
		averageTime = 0.0
		i = 0
		while i < 3:
			try:
				print "Q", q
				print 'Query Path: ', p + "move_12_" + str(q) + ".json"
				json_data=open(os.path.expanduser(p + "move_12_" + str(q) + ".json"))
				data = json.load(json_data)
				json_data.close()

				#call bash scripts
				subprocess.call(['/bin/bash',"clear-tpch.sh"]);
				print("postgres and os cleared")

				#try running the query
				try:
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
					print('Query #' + str(counter) + ' Finished with ' + status);
					totalElapsedTime = int((connection.get_query_status(query_id))['elapsedNanos'])
					averageTime = averageTime + totalElapsedTime
					i = i + 1
					print averageTime
				else:
					print("Do over");
					print('Query #' + str(counter));
			except:
				print "Query does not exist"
				f.write('N/A ')
				break

		timeSeconds = (averageTime / 3.0) /1000000000.0;
		print('Logging average runtime ' + str(timeSeconds));
		f.write(str(counter) + ',' + str(q) + ',' +  str(timeSeconds) + "\n");
		f.flush()
		
		counter = counter + 1;
	f.close();
