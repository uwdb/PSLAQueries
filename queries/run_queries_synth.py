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
from urllib2 import Request, urlopen

hostname = 'ec2-174-129-111-140.compute-1.amazonaws.com'
port = 8753

connection = myria.MyriaConnection(hostname=hostname, port=port)

newList = False

if newList:
	qList = random.sample(range(1, 1223), 200)
	qList.sort()
	r = open(os.path.expanduser("synth-random.txt"), 'w')
	r.write(', '.join(map(str, qList)))
	r.close()
else:
	qList = open(os.path.expanduser("synth-random.txt"), 'r')
	qList = qList.read().split(',')

#all possible paths

qPath = [
		#"synth/synth-type2/4/", 
		# "synth/synth-type2/6/", 
		 "synth/synth-type2/8/", 

		 "synth/synth-type3/synth-type3a/4_datanodes/6_computenodes/", 
		 "synth/synth-type3/synth-type3a/4_datanodes/8_computenodes/",
		 "synth/synth-type3/synth-type3a/6_datanodes/8_computenodes/",

		 "synth/synth-type3/synth-type3b/6_datanodes/4_computenodes/",
		 "synth/synth-type3/synth-type3b/8_datanodes/6_computenodes/",
		 "synth/synth-type3/synth-type3b/8_datanodes/4_computenodes/"]



for p in qPath:
	counter = 0;
	#open the file to log the runtimes
	f = open(os.path.expanduser(p + "runtimes.txt"), 'w');
	print "FOR PATH " + p
	#for each query
	for q in qList:
		averageTime = 0.0
		i = 0
		while i < 1:
			try:
				q = q.strip()
				print 'Query Path: ', p + "query" + str(q) + ".json"
				json_data=open(os.path.expanduser(p + "query" + str(q) + ".json"))
				data = json.load(json_data)
				json_data.close()

				#call bash scripts
				subprocess.call(['/bin/bash',"clear-synth.sh"]);
				print("postgres and os cleared")

				#try running the query
				try:
					query_status = connection.submit_query(data)
					query_id = query_status['queryId']
				except myria.MyriaError as e:
					print("MyriaError")
					print('Query #' + str(counter));

				status = (connection.get_query_status(query_id))['status']

				#for timeouts -- no more than 10 min
				now_time = time.time()
				future_time = now_time + 600

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
						f.write('KILLED TIMEOUT: ')
						break;
					time.sleep(2)
					if time.time() > future_time:
						print "Query Stopped"
						connection.kill_query(query_id)
						#status should now be KILLING
				#Regardless if the query was killed or not, keep going
				print('Query #' + str(counter) + status);
				totalElapsedTime = int((connection.get_query_status(query_id))['elapsedNanos'])
				averageTime = averageTime + totalElapsedTime
				i = i + 1
				print averageTime

			except:
				print "Query Error"
				f.write('N/A: ')
				break
		timeSeconds = (averageTime / 1.0) /1000000000.0;
		print('Logging average runtime ' + str(timeSeconds));
		f.write(str(counter) + ',' + str(timeSeconds) + "\n");
		f.flush()
		counter = counter + 1;
	f.close();
