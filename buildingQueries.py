import sys, os, json
import time
from raco.catalog import FromFileCatalog
import raco.myrial.parser as parser
import raco.myrial.interpreter as interpreter
import raco.algebra as alg
import raco.language.myrialang
from raco.language.logical import OptLogicalAlgebra
from raco.expression.expression import UnnamedAttributeRef
from myria import MyriaConnection
from myria import MyriaSchema
from myria import MyriaRelation

# building type 3 queries (can also build type 2)

connection = MyriaConnection(hostname = "rest.myria.cs.washington.edu", port=1776, ssl=True, execution_url="https://myria-web.appspot.com")

lineitemRelation = 'public:adhoc10GB:lineitemHash'
supplierRelation = 'public:adhoc10GB:supplier'
customerRelation = 'public:adhoc10GB:customer'

f = open('schema.py', 'w')
f.write("{" + '\n');
#--1
current_schema = (MyriaRelation(relation= lineitemRelation, connection=connection).schema.to_dict())
columnNames = [x.encode('utf-8') for x in current_schema['columnNames']]
columnTypes = [x.encode('utf-8') for x in current_schema['columnTypes']]
columns = zip(columnNames, columnTypes)
f.write("'" + lineitemRelation + "' : " +  str(columns) + ',\n');
#--2
current_schema = (MyriaRelation(relation= supplierRelation, connection=connection).schema.to_dict())
columnNames = [x.encode('utf-8') for x in current_schema['columnNames']]
columnTypes = [x.encode('utf-8') for x in current_schema['columnTypes']]
columns = zip(columnNames, columnTypes)
f.write("'" + supplierRelation + "' : " +  str(columns) + ',\n');
#--3
current_schema = (MyriaRelation(relation= customerRelation, connection=connection).schema.to_dict())
columnNames = [x.encode('utf-8') for x in current_schema['columnNames']]
columnTypes = [x.encode('utf-8') for x in current_schema['columnTypes']]
columns = zip(columnNames, columnTypes)
f.write("'" + customerRelation + "' : " +  str(columns) + ',\n');
f.write("}" + '\n');
f.close()

test_query_2join = "T1 = [from scan(public:adhoc10GB:lineitemHash) as l, scan(public:adhoc10GB:supplier) as s, scan(public:adhoc10GB:customer) as c where l.l_suppkey = s.s_suppkey and c.c_custkey = l.l_custkey and l.l_linenumber = 3 emit s.*, c.*]; store(T1, test);"
catalog = FromFileCatalog.load_from_file("schema.py")
_parser = parser.Parser()

statement_list = _parser.parse(test_query_2join);
processor = interpreter.StatementProcessor(catalog, True)
processor.evaluate(statement_list)

p = processor.get_logical_plan()

p = processor.get_physical_plan(push_sql=True)

json_data = processor.get_json()

#there will always be two fragments, so add overrideworkers
#perhaps check which is the fragment with the shuffle and know that is where the scan  is......
first_fragment = json_data['plan']['fragments'][0]
first_fragment['overrideWorkers'] = [1,2,3,4]


second_fragment = json_data['plan']['fragments'][1]
second_fragment['overrideWorkers'] = [1,2,3,4,5,6,7,8]


with open('output.json', 'w') as f:
	json.dump(json_data, f)	

