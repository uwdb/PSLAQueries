import sys, os, json
import time
from raco.catalog import FromFileCatalog
import raco.myrial.parser as parser
import raco.myrial.interpreter as interpreter
import raco.algebra as alg
import raco.language.myrialang
from raco.language.logical import OptLogicalAlgebra
from raco.expression.expression import UnnamedAttributeRef
import schemaDetector

catalog = FromFileCatalog.load_from_file("schema.py")
_parser = parser.Parser()

use_cases = ['tpch/tpch-myrial.txt'] #, 'synth/synth-myrial.txt']
plan_workers = [4,6,8]

type_2 = False
type_3 = True

#Queries Transformation:
for current_use_case in use_cases: 
	current_file = open(current_use_case, 'r')
	counter = 0
	print '*****Queries for ' + current_use_case + '*****'
	for line in current_file:
		current_query = line.strip()

		#create type-2
		if(type_2):
			statement_list = _parser.parse(current_query);
			processor = interpreter.StatementProcessor(catalog, True)
			processor.evaluate(statement_list)
			p = processor.get_logical_plan()
			p = processor.get_physical_plan(push_sql=True, type2=True, type3=False)
			json_data = processor.get_json(push_sql=True, type2=True, type3=False)

			for w in plan_workers:
				json_data['plan']['fragments'][0]['overrideWorkers'] = range(1,w +1)
				with open('tpch/tpch-type2/' + str(w) + '/query' + str(counter) + '.json', 'w') as f:
					json.dump(json_data, f)
				f.close()	

		#create type-3
		if(type_3):
			statement_list = _parser.parse(current_query);
			processor = interpreter.StatementProcessor(catalog, True)
			processor.evaluate(statement_list)
			p = processor.get_logical_plan()
			p = processor.get_physical_plan(push_sql=True, type2=False, type3=True)
			json_data = processor.get_json(push_sql=True, type2=False, type3=True)

			#Manipulate Workers
			#Type-3a & Type3b - Growth Compute Nodes and Shrink Compute Nodes
			for i in plan_workers:
				for j in plan_workers:
					if (i != j) and (len(json_data['plan']['fragments']) > 1): #join queries should only scale
						if (len(json_data['plan']['fragments']) > 2):
							print "ERROR: more than two fragments"
							sys.exit(0)
						from_fragment = None
						to_fragment = None
						for frag in json_data['plan']['fragments']: #find to/from fragment
							for op in frag['operators']:
								if 'DbQueryScan' in op['opType'] and ('lineitem' in op['sql'] or 'fact' in op['sql']):
									from_fragment = frag
								elif 'TableScan' in op['opType'] and ('lineitem' in op['relationKey']['relationName'] or 'fact' in op['relationKey']['relationName']):
									from_fragment = frag
								else:
									if(frag != from_fragment): #this is hacky, but given there are two fragments at most, this works for now
										to_fragment = frag
						from_fragment['overrideWorkers'] = range(1,i+1)
						to_fragment['overrideWorkers'] = range(1,j+1)

						#write the json
						directory = 'tpch/tpch-type3/tpch-type3a/' if (i < j) else 'tpch/tpch-type3/tpch-type3b/'
						f = open(directory+ str(i) + '_datanodes/' + str(j) + '_computenodes/query' + str(counter) + '.json', 'w')
						json.dump(json_data, f)
						f.close()
		print "Done with Query "  + str(counter)
		counter = counter + 1
