from myria import MyriaConnection
from myria import MyriaSchema
from myria import MyriaRelation
import json
import time
import sys

port = 8753

connection = MyriaConnection(hostname = sys.argv[1], port=8753)

configurations = [42]

dimensionFiles = ['replicateCustomer.json', 'replicateDate.json', 'replicatePart.json', 'replicateSupplier.json']
tenants = ['tenant_1', 'tenant_2', 'tenant_3', 'tenant_4']

for t in tenants:
	for c in configurations:
		#dimension tables
		for d in dimensionFiles:
			dim_file = open(d, 'r+')
			dim_json = json.load(dim_file)
			dim_json['rawQuery'] = "Replicate " + str(d) + " on " + str(c)
			dim_json['fragments'][1]['overrideWorkers'] = range(1,c+1)
			dim_json['fragments'][1]['operators'][1]['relationKey']['programName'] = 'adhoc10GB' + str(c) + 'W' + '_' + str(t)
			print 'Replicating ' + str(d) +  ' on ' + str(c) + ' workers'
			query_status= connection.submit_query(dim_json)
			query_id = query_status['queryId']
			status = (connection.get_query_status(query_id))['status']
			while status!='SUCCESS':
				status = (connection.get_query_status(query_id))['status']
				time.sleep(2);
			print 'done'
