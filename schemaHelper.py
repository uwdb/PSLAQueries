from myria import MyriaConnection
from myria import MyriaSchema
from myria import MyriaRelation

connection = MyriaConnection(hostname = "rest.myria.cs.washington.edu", port=1776, ssl=True, execution_url="https://myria-web.appspot.com")

listRelations = ['public:adhoc10GB:lineitemHash', 'public:adhoc10GB:supplierReplicate', 'public:adhoc10GB:customerReplicate', 'public:adhoc10GB:partReplicate', 'public:adhoc10GB:dateReplicate'] #,'public:syntheticBenchmark:fact', 'public:syntheticBenchmark:dimension1Replicate', 'public:syntheticBenchmark:dimension2Replicate',  'public:syntheticBenchmark:dimension3Replicate', 'public:syntheticBenchmark:dimension4Replicate', 'public:syntheticBenchmark:dimension5Replicate']

f = open('schema.py', 'w')
f.write("{" + '\n');
for i in listRelations: 
	current_schema = (MyriaRelation(relation= i, connection=connection).schema.to_dict())
	columnNames = [x.encode('utf-8') for x in current_schema['columnNames']]
	columnTypes = [x.encode('utf-8') for x in current_schema['columnTypes']]
	columns = zip(columnNames, columnTypes)
	f.write("'" + i + "' : " +  str(columns) + ',\n');
f.write("}" + '\n');
f.close()