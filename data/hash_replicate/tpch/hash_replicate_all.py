from myria import MyriaConnection
from myria import MyriaSchema
from myria import MyriaRelation
import json
import time

master = "ec2-54-204-127-83.compute-1.amazonaws.com"
port = 8753

connection = MyriaConnection(hostname =master, port=port, ssl=False)

configurations = [4,6,8]

dimensionFiles = ['replicateCustomer.json', 'replicateDate.json', 'replicatePart.json', 'replicateSupplier.json']

for c in configurations:
	#hash table first
	hash_file = open('hashLineitem.json', 'r+')
	hash_json = json.load(hash_file)
	hash_json['rawQuery'] = "Hash Lineitem on " + str(c)
 	hash_json['fragments'][1]['overrideWorkers'] = range(1,c+1)
	hash_json['fragments'][1]['operators'][1]['relationKey']['programName'] = 'adhoc10GB' + str(c) + 'W'

	print 'Hashing Lineitem on ' + str(c) + ' workers'
	query_status= connection.submit_query(hash_json)
	query_id = query_status['queryId']
	status = (connection.get_query_status(query_id))['status']
	while status!='SUCCESS':
		status = (connection.get_query_status(query_id))['status']
		time.sleep(2);
	print 'done'

	#dimension tables
	for d in dimensionFiles:
		dim_file = open(d, 'r+')
		dim_json = json.load(dim_file)
		dim_json['rawQuery'] = "Replicate " + str(d) + " on " + str(c)
		dim_json['fragments'][1]['overrideWorkers'] = range(1,c+1)
		dim_json['fragments'][1]['operators'][1]['relationKey']['programName'] = 'adhoc10GB' + str(c) + 'W'
		print 'Replicating ' + str(d) +  ' on ' + str(c) + ' workers'
		query_status= connection.submit_query(dim_json)
		query_id = query_status['queryId']
		status = (connection.get_query_status(query_id))['status']
		while status!='SUCCESS':
			status = (connection.get_query_status(query_id))['status']
			time.sleep(2);
		print 'done'
