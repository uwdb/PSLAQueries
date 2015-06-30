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

hostname = 'localhost'
port = 8753

connection = myria.MyriaConnection(hostname=hostname, port=port)

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

		"tpch/multi-tenant/2_tenants-2_shared/",
		#"tpch/multi-tenant/2_tenants-4_shared/",
		#"tpch/multi-tenant/2_tenants-6_shared/",
		#"tpch/multi-tenant/2_tenants-8_shared/",

		#"tpch/multi-tenant/3_tenants-2_shared/",
		#"tpch/multi-tenant/3_tenants-4_shared/",
		#"tpch/multi-tenant/3_tenants-6_shared/",
		#"tpch/multi-tenant/3_tenants-8_shared/",

		#"tpch/multi-tenant/4_tenants-2_shared/",
		#"tpch/multi-tenant/4_tenants-4_shared/",
		#"tpch/multi-tenant/4_tenants-6_shared/",
		#"tpch/multi-tenant/4_tenants-8_shared/"
		]


for p in qPath:
	counter = 0;
	print "FOR PATH " + p

	#get all queries in current path
	
	qList = os.listdir("/root/PSLAQueries/queries/"+ p)

	#call bash scripts
	subprocess.call(['/bin/bash',"clear-tpch.sh"]);
	print("postgres and os cleared")

	#for each query in the path
	for q in qList:
		try:
			q = q.strip()
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