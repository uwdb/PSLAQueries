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

hostname = 'ec2-54-145-53-252.compute-1.amazonaws.com'
port = 8753

connection = myria.MyriaConnection(hostname=hostname, port=port)

qList = [3,4,39,40,67,279,280,343,344,383,384,483,484,523,524,655,656,695,696,895];
qPath = ["tpch/tpch-type2/6/", "tpch/tpch-type2/8/"]

for p in qPath:
	counter = 0;
	#open the file to log the runtimes
	f = open(os.path.expanduser(p + "runtimes.txt"), 'w');
	print "FOR PATH " + P
	#for each query
	for q in qList:
		averageTime = 0.0
		i = 0
		while i < 3:
			#call bash scripts
			subprocess.call(['/bin/bash',"clear.sh"]);
			print("postgres and os cleared")

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

			#keep checking, sleep a little
			while status!='SUCCESS':
				status = (connection.get_query_status(query_id))['status']
				print(status);
				if status=='SUCCESS':
					break;
				elif status=='ERROR':
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


		timeSeconds = (averageTime / 3.0) /1000000000.0;
		print('Logging average runtime ' + str(timeSeconds));
		f.write(str(counter) + ',' + str(timeSeconds) + "\n");
		counter = counter + 1;
	f.close();
