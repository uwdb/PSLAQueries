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

hostname = 'ec2-54-204-137-94.compute-1.amazonaws.com'
port = 8753

connection = myria.MyriaConnection(hostname=hostname, port=port)

qList = random.sample(range(1, 1223), 500)
qList.sort()
r = open(os.path.expanduser("synth-random.txt"), 'w');
r.write(', '.join(map(str, qList)))
r.close()

#all possible paths

qPath = ["synth/synth-type2/4/", "synth/synth-type2/6/", "synth/synth-type2/8/", 

		 "synth/synth-type3/synth-type3a/4_datanodes/6_computenodes/", 
		 "synth/synth-type3/synth-type3a/4_datanodes/8_computenodes/",
		 "synth/synth-type3/synth-type3a/6_datanodes/8_computenodes/",

		 "synth/synth-type3/synth-type3a/6_datanodes/4_computenodes/",
		 "synth/synth-type3/synth-type3b/8_datanodes/6_computenodes/",
		 "synth/synth-type3/synth-type3a/8_datanodes/4_computenodes/"]


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
			#call bash scripts
			subprocess.call(['/bin/bash',"clear-synth.sh"]);
			print("postgres and os cleared")

			try:
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
			except:
				print "Query does not exist"
				f.write('N/A ')

		timeSeconds = (averageTime / 3.0) /1000000000.0;
		print('Logging average runtime ' + str(timeSeconds));
		f.write(str(counter) + ',' + str(timeSeconds) + "\n");
		counter = counter + 1;
	f.close();
