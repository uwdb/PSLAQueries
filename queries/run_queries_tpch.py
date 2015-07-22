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

#qList = [2,3,38,39,66,67,278,279,342,343,382,383,482,483,522,523,654,655,694,695,894]

newList = False

if newList:
	qList = random.sample(range(240, 896), 100)
	qList.sort()
	r = open(os.path.expanduser("tpch-random.txt"), 'w')
	r.write(', '.join(map(str, qList)))
	r.close()
else:
	qList = open(os.path.expanduser("tpch-random.txt"), 'r')
	qList = qList.read().split(',')


qPath = [
		#"tpch/tpch-type2/4/",
		#"tpch/tpch-type2/6/",
		#"tpch/tpch-type2/8/",
		#"tpch/tpch-type2/10/",
		#"tpch/tpch-type2/12/",

		#"tpch/tpch-type3/tpch-type3a/4_datanodes/6_computenodes/",
		#"tpch/tpch-type3/tpch-type3a/4_datanodes/8_computenodes/",
		#"tpch/tpch-type3/tpch-type3a/4_datanodes/10_computenodes/",
		#"tpch/tpch-type3/tpch-type3a/4_datanodes/12_computenodes/",
		#"tpch/tpch-type3/tpch-type3a/6_datanodes/8_computenodes/",
		#"tpch/tpch-type3/tpch-type3a/6_datanodes/10_computenodes/",
		#"tpch/tpch-type3/tpch-type3a/6_datanodes/12_computenodes/",
		#"tpch/tpch-type3/tpch-type3a/8_datanodes/10_computenodes/",
		#"tpch/tpch-type3/tpch-type3a/8_datanodes/12_computenodes/",
		#"tpch/tpch-type3/tpch-type3a/10_datanodes/12_computenodes/",

		#"tpch/tpch-type3/tpch-type3b/6_datanodes/4_computenodes/",
		#"tpch/tpch-type3/tpch-type3b/8_datanodes/4_computenodes/",
		#"tpch/tpch-type3/tpch-type3b/8_datanodes/6_computenodes/",
		#"tpch/tpch-type3/tpch-type3b/10_datanodes/4_computenodes/",
		#"tpch/tpch-type3/tpch-type3b/10_datanodes/6_computenodes/",
		#"tpch/tpch-type3/tpch-type3b/10_datanodes/8_computenodes/",
		#"tpch/tpch-type3/tpch-type3b/12_datanodes/4_computenodes/",
		#"tpch/tpch-type3/tpch-type3b/12_datanodes/6_computenodes/",
		#"tpch/tpch-type3/tpch-type3b/12_datanodes/8_computenodes/",
		#"tpch/tpch-type3/tpch-type3b/12_datanodes/10_computenodes/"

		#sm to large for baseline comparison
		"tpch/tpch-type3/tpch-type3b/4_datanodes/10_computenodes/",
		"tpch/tpch-type3/tpch-type3b/4_datanodes/11_computenodes/",
		"tpch/tpch-type3/tpch-type3b/4_datanodes/12_computenodes/",
		"tpch/tpch-type3/tpch-type3b/4_datanodes/13_computenodes/",
		"tpch/tpch-type3/tpch-type3b/4_datanodes/14_computenodes/",
		"tpch/tpch-type3/tpch-type3b/4_datanodes/15_computenodes/",
		"tpch/tpch-type3/tpch-type3b/4_datanodes/16_computenodes/",

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
		while i < 1:
			try:
				q = q.strip()
				print "Q", q
				print 'Query Path: ', p + "query" + str(q) + ".json"
				json_data=open(os.path.expanduser(p + "query" + str(q) + ".json"))
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

		timeSeconds = (averageTime / 1.0) /1000000000.0;
		print('Logging average runtime ' + str(timeSeconds));
		f.write(str(counter) + ',' + str(q) + ',' +  str(timeSeconds) + "\n");
		f.flush()
		pathSplit = p.split('/')
		bashCommand = "aws s3 cp " +  str(p) + "runtimes.txt"+ " s3://baselinecomparison/runtimesTPCH" + str(pathSplit[4]) + ".txt"
		print bashCommand
		os.system(bashCommand)
		counter = counter + 1;
	f.close();
