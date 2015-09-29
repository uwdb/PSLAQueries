from myria import MyriaConnection, MyriaRelation, MyriaQuery, MyriaSchema
import sys

connection = MyriaConnection(hostname = "localhost", port=8753)

schema = MyriaSchema({"columnNames": ["l_orderkey", "l_linenumber", "l_custkey", "l_partkey", "l_suppkey", "l_orderdate", "l_orderpriority", "l_shippriority", "l_quantity", "l_extendedprice", "l_ordtotalprice", "l_discount", "l_revenue", "l_supplycost", "l_tax", "l_commitdate", "l_shipmode"], "columnTypes": ["LONG_TYPE", "LONG_TYPE", "LONG_TYPE", "LONG_TYPE", "LONG_TYPE", "STRING_TYPE", "STRING_TYPE", "LONG_TYPE", "DOUBLE_TYPE", "DOUBLE_TYPE", "DOUBLE_TYPE", "DOUBLE_TYPE", "LONG_TYPE", "LONG_TYPE", "DOUBLE_TYPE", "LONG_TYPE", "STRING_TYPE"]})


numberWorkers = 4
totalChunks = [2,3,5]

#for each worker, ingest all the chunks
for nw in range(1,numberWorkers + 1):
	for tc in totalChunks:
		for currentChunk in range(1,tc+1): 
			relName = str(numberWorkers) + 'Workers'
			relation = MyriaRelation('public:adhoc10GB'+ relName + '-Chunks' + str(tc) +':lineitem-part' + str(currentChunk) , connection=connection, schema=schema)
			print relation.name
			work = [(nw, 'https://s3-us-west-2.amazonaws.com/read-lineitem-chunks/' + relName + '/'+ str(nw)+ 'Workers' +  '/lineitem-part' + str(currentChunk))]
			print 'https://s3-us-west-2.amazonaws.com/read-lineitem-chunks/' + relName + '/Worker' + str(nw)  + '/Chunks-' + str(tc) +  '/lineitem-part' + str(currentChunk)
			queryImport = MyriaQuery.parallel_import(relation=relation, work=work, scan_parameters={'delimiter':'|'}, insert_parameters={'argOverwriteTable':True})

			#loop until ready for next chunk
			status = queryImport.status

			while status!='SUCCESS':
			        status = queryImport.status
			        time.sleep(2);
			        if status=='ERROR':
			                break;