#attempt at automating scaling via s3/raco 

from myria import MyriaConnection, MyriaRelation, MyriaQuery, MyriaSchema
import sys
import os
import time
from raco.catalog import FromFileCatalog
import raco.myrial.parser as parser
import raco.myrial.interpreter as interpreter
import raco.algebra as alg
from raco.expression.expression import UnnamedAttributeRef
from myria import MyriaConnection
from myria import MyriaSchema
from myria import MyriaRelation
from raco.language.myrialang import compile_to_json
from raco.scheme import Scheme
from raco.language.myrialang import MyriaQueryScan

connection = MyriaConnection(hostname = "localhost", port=8753)

schema = {"columnNames": ["l_orderkey", "l_linenumber", "l_custkey", "l_partkey", "l_suppkey", "l_orderdate", "l_orderpriority", "l_shippriority", "l_quantity", "l_extendedprice", "l_ordtotalprice", "l_discount", "l_revenue", "l_supplycost", "l_tax", "l_commitdate", "l_shipmode"], "columnTypes": ["LONG_TYPE", "LONG_TYPE", "LONG_TYPE", "LONG_TYPE", "LONG_TYPE", "STRING_TYPE", "STRING_TYPE", "LONG_TYPE", "DOUBLE_TYPE", "DOUBLE_TYPE", "DOUBLE_TYPE", "DOUBLE_TYPE", "LONG_TYPE", "LONG_TYPE", "DOUBLE_TYPE", "LONG_TYPE", "STRING_TYPE"]}

zippedSchema = zip(schema['columnNames'], schema['columnTypes'])

f = open(os.path.expanduser("runtimes.txt"), 'w');

startWorkers = 4
receiveWorkers = [6]#[6,8,10,12]
correspondingChunks = [3]#[3,2,5,3]

s3Read = False

positionCount = 0
for r in receiveWorkers: #first case is 6

	finishWorkers = list(set(range(1,r+1))- set(range(1,startWorkers+1)))

	collectRuntimesFromOneWorker = []
	runtime = 0

	print 'r',r 
	for d in range(1, startWorkers+1): #for each data node
		#basically how many chunks should it provide from d worker? assume '1' for now
		#build query

		if s3Read:
			chunkRead = 'https://s3-us-west-2.amazonaws.com/read-lineitem-chunks/' + str(startWorkers) + 'Workers/'+ 'Worker' + str(d) +  '/Chunks-' + str(correspondingChunks[positionCount]) +'/lineitem-part' + str('1')
			pretty_list = '(' + ','.join(map(lambda x :  x[0].lower() + ':'  + x[1].lower(), zippedSchema)) + ')'
			pretty_list = pretty_list.replace('long_type', 'float').replace('double_type', 'float').replace('string_type', 'string')
			load = 'load(\"' + str(chunkRead) + '\", csv(schema' + str(pretty_list) + ',delimiter = \'|\'))'
			store = 'public:adhoc10GBFromS3'+ str(startWorkers) + 'to' + str(r) + 'FromWorker' + str(d) + 'part' + str('1') + ':lineitem'
		else:
			chunkRead = 'public:adhoc10GB' + str(startWorkers) + 'WorkersChunks' + str(correspondingChunks[positionCount]) + ':lineitemPart1'
			load = 'scan('+ str(chunkRead) + ')'
			store = 'public:adhoc10GBFromDisk'+ str(startWorkers) + 'to' + str(r) + 'FromWorker' + str(d) + 'part' + str('1') + ':lineitem'

		current_query = 'T1 = ' + load + '; Store(T1,' + store + ');';
		
		#schema
		FromFileCatalog.scheme_write_to_file(path='schema.py',new_rel_key=chunkRead, new_rel_schema=str(schema))
		catalog = FromFileCatalog.load_from_file('schema.py')

		_parser = parser.Parser()
		statement_list = _parser.parse(current_query);
		processor = interpreter.StatementProcessor(catalog, True)
		processor.evaluate(statement_list)
		p = processor.get_logical_plan()
		#modify p
		tail = p.args[0].input
		p.args[0].input = alg.Shuffle(tail, [UnnamedAttributeRef(0), UnnamedAttributeRef(1)])
		p = processor.get_physical_plan()
		finalplan = processor.get_json()
		#modify json
		finalplan['plan']['fragments'][0]['overrideWorkers'] = finishWorkers


		print 'd',d
		query_status= connection.submit_query(finalplan)
		query_id = query_status['queryId']
		status = (connection.get_query_status(query_id))['status']

		while status!='SUCCESS':
			status = (connection.get_query_status(query_id))['status']
			time.sleep(2);
			if status=='ERROR':
				break;

		totalElapsedTime = int((connection.get_query_status(query_id))['elapsedNanos'])
		runtime += totalElapsedTime
		collectRuntimesFromOneWorker.append(runtime)

	print "Round finished " + str(startWorkers) + " to " +  str(receiveWorkers[positionCount])
	f.write("Round finished " + str(startWorkers) + " to " +  str(receiveWorkers[positionCount]))
	f.write(str(sum(collectRuntimesFromOneWorker)))
	positionCount = positionCount + 1
f.close()