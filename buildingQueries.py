import sys, os, json
import time
from raco.catalog import FromFileCatalog
import raco.myrial.parser as parser
import raco.myrial.interpreter as interpreter
import raco.algebra as alg
import raco.language.myrialang
from raco.language.logical import OptLogicalAlgebra
from raco.expression.expression import UnnamedAttributeRef

catalog = FromFileCatalog.load_from_file("schema.py")
_parser = parser.Parser()

use_cases = ['queries/synth/synth-myrial.txt']
plan_workers = [4,6,8]

type_2 = True
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
			json_data_clean_copy = json_data

			for w in plan_workers:
				json_data = json_data_clean_copy
				json_data['plan']['fragments'][0]['overrideWorkers'] = range(1,w +1)

				#rename tables correctly
				if(current_use_case == 'queries/tpch/tpch-myrial.txt'):
					json_string = json.dumps(json_data)
					json_string = json_string.replace('adhoc10GB', 'adhoc10GB' + str(w) + 'W')
					json_data = json.loads(json_string)
					directory = 'queries/tpch/tpch-type2/' 

				elif (current_use_case == 'queries/synth/synth-myrial.txt'):
					json_string = json.dumps(json_data)
					json_string = json_string.replace('syntheticBenchmark', 'syntheticBenchmark' + str(w) + 'W')
					json_data = json.loads(json_string)
					directory ='queries/synth/synth-type2/'  

				json_data['rawQuery'] = 'Query ' + str(counter) + ' for type-2 on ' + str(w) + ' workers'
				f = open(directory + str(w) + '/query' + str(counter) + '.json', 'w')
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
			#Type-3a & Type3b - Grow Compute Nodes and Shrink Compute Nodes
			for i in plan_workers: #data_nodes
				for j in plan_workers: #compute_nodes
					if (i != j) and (len(json_data['plan']['fragments']) > 1): #join queries should only scale
						json_data = processor.get_json(push_sql=True, type2=False, type3=True)

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

						if(current_use_case == 'queries/tpch/tpch-myrial.txt'):
							for current_operator in from_fragment['operators']:
								if current_operator['opType'] == 'DbQueryScan':
									sql_value = current_operator['sql']
									current_operator['sql'] = sql_value.replace('adhoc10GB', 'adhoc10GB' + str(i) + 'W')
								elif current_operator['opType'] == 'TableScan':
									current_operator['relationKey']['programName'] =  'adhoc10GB' + str(i) + 'W'

							for current_operator in to_fragment['operators']:
								if current_operator['opType'] == 'DbQueryScan':
									sql_value = current_operator['sql']
									current_operator['sql'] = sql_value.replace('adhoc10GB', 'adhoc10GB' + str(j) + 'W')
								elif current_operator['opType'] == 'TableScan':
									current_operator['relationKey']['programName'] =  'adhoc10GB' + str(j) + 'W'

							directory = 'queries/tpch/tpch-type3/tpch-type3a/' if (i < j) else 'queries/tpch/tpch-type3/tpch-type3b/'
							json_data['rawQuery'] = 'Query ' + str(counter) + ' for type-3 on ' + str(i) + ' starting datanodes'

						elif (current_use_case == 'queries/synth/synth-myrial.txt'):
							for current_operator in from_fragment['operators']:
								if current_operator['opType'] == 'DbQueryScan':
									sql_value = current_operator['sql']
									current_operator['sql'] = sql_value.replace('syntheticBenchmark', 'syntheticBenchmark' + str(i) + 'W')
								elif current_operator['opType'] == 'TableScan':
									current_operator['relationKey']['programName'] =  'syntheticBenchmark' + str(i) + 'W'

							for current_operator in to_fragment['operators']:
								if current_operator['opType'] == 'DbQueryScan':
									sql_value = current_operator['sql']
									current_operator['sql'] = sql_value.replace('syntheticBenchmark', 'syntheticBenchmark' + str(j) + 'W')
								elif current_operator['opType'] == 'TableScan':
									current_operator['relationKey']['programName'] =  'syntheticBenchmark' + str(j) + 'W'

							directory = 'queries/synth/synth-type3/synth-type3a/' if (i < j) else 'queries/synth/synth-type3/synth-type3b/'
							json_data['rawQuery'] = 'Query ' + str(counter) + ' for type-3 on ' + str(i) + ' starting datanodes'

						#write the json to a file
						f = open(directory+ str(i) + '_datanodes/' + str(j) + '_computenodes/query' + str(counter) + '.json', 'w')
						json.dump(json_data, f)
						f.close()
		print "Done with Query "  + str(counter)
		counter = counter + 1
