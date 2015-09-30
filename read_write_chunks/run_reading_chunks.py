#attempt at automating scaling 

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
import subprocess
import json

connection = MyriaConnection(hostname = "localhost", port=8753)

schema = {"columnNames": ["l_orderkey", "l_linenumber", "l_custkey", "l_partkey", "l_suppkey", "l_orderdate", "l_orderpriority", "l_shippriority", "l_quantity", "l_extendedprice", "l_ordtotalprice", "l_discount", "l_revenue", "l_supplycost", "l_tax", "l_commitdate", "l_shipmode"], "columnTypes": ["LONG_TYPE", "LONG_TYPE", "LONG_TYPE", "LONG_TYPE", "LONG_TYPE", "STRING_TYPE", "STRING_TYPE", "LONG_TYPE", "DOUBLE_TYPE", "DOUBLE_TYPE", "DOUBLE_TYPE", "DOUBLE_TYPE", "LONG_TYPE", "LONG_TYPE", "DOUBLE_TYPE", "LONG_TYPE", "STRING_TYPE"]}

zippedSchema = zip(schema['columnNames'], schema['columnTypes'])

f = open(os.path.expanduser("runtimes.txt"), 'w');

startWorkers = 4
receiveWorkers = [6]#[6,8,10,12]
correspondingChunks = [3]#[3,2,5,3]
numberChunksToMove = [1,1,3,2]

positionCount = 0
for r in receiveWorkers: #first case is 6

	finishWorkers = list(set(range(1,r+1))- set(range(1,startWorkers+1)))
	collectRuntimes_perLoop = []
	print 'r',r 

	for loop in range(1): #for each loop, we read from n data nodes and move a chunk via RR on destination
		#build query
		currentChunksToMove = numberChunksToMove[positionCount]
		chunkTimes = []
		runtime = 0
		for c in range(1,currentChunksToMove+1):
			#clear cache
			subprocess.call(['/bin/bash',"../queries/clear-tpch.sh"])
			print("postgres and os cleared")

			chunkRead = 'public:adhoc10GB' + str(startWorkers) + 'WorkersChunks' + str(correspondingChunks[positionCount]) + ':lineitemPart1'
			load = 'scan('+ str(chunkRead) + ')'
			store = 'public:adhoc10GBFromDisk'+ str(startWorkers) + 'to' + str(r) + 'part' + str(c) + ':lineitem'

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
			p.input.input.input = MyriaQueryScan(sql="select * from \"" + chunkRead + "\"", scheme=Scheme(zippedSchema))
			finalplan = compile_to_json('chunkQuery',p,p)

			#modify json
			finalplan['plan']['fragments'][0]['overrideWorkers'] = finishWorkers
			finalplan['plan']['fragments'][1]['overrideWorkers'] = range(1,startWorkers+1)

			print 'chunk',c
			query_status= connection.submit_query(finalplan)
			query_id = query_status['queryId']
			status = (connection.get_query_status(query_id))['status']

			while status!='SUCCESS':
				status = (connection.get_query_status(query_id))['status']
				time.sleep(1);
				if status=='ERROR':
					break;

			totalElapsedTime = int((connection.get_query_status(query_id))['elapsedNanos'])
			chunkTimes.append(totalElapsedTime)
			print chunkTimes
		runtime += sum(chunkTimes) #adding runtime from all chunks
		print "sum chunk times", runtime
	collectRuntimes_perLoop.append(runtime)
	print collectRuntimes_perLoop
	print "Round finished " + str(startWorkers) + " to " +  str(receiveWorkers[positionCount]) + " " 
	f.write("Round finished " + str(startWorkers) + " to " +  str(receiveWorkers[positionCount]) + " ")
	f.write('average: ' + str(sum(collectRuntimes_perLoop)/float(len(collectRuntimes_perLoop)))+ '\n')
	f.write('min :' + str(min(collectRuntimes_perLoop))+ '\n')
	f.write('max : ' + str(max(collectRuntimes_perLoop))+ '\n')
	f.write('\n')
	positionCount = positionCount + 1
f.close()