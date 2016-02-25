from myria import MyriaConnection, MyriaRelation, MyriaQuery, MyriaSchema
import sys

connection = MyriaConnection(hostname = sys.argv[1], port=8753)

schema = MyriaSchema({"columnNames": ["l_orderkey", "l_linenumber", "l_custkey", "l_partkey", "l_suppkey", "l_orderdate", "l_orderpriority", "l_shippriority", "l_quantity", "l_extendedprice", "l_ordtotalprice", "l_discount", "l_revenue", "l_supplycost", "l_tax", "l_commitdate", "l_shipmode"], "columnTypes": ["LONG_TYPE", "LONG_TYPE", "LONG_TYPE", "LONG_TYPE", "LONG_TYPE", "STRING_TYPE", "STRING_TYPE", "LONG_TYPE", "DOUBLE_TYPE", "DOUBLE_TYPE", "DOUBLE_TYPE", "DOUBLE_TYPE", "LONG_TYPE", "LONG_TYPE", "DOUBLE_TYPE", "LONG_TYPE", "STRING_TYPE"]})

#4
relation = MyriaRelation('public:adhoc10GB4_U_Check:lineorder', connection=connection, schema=schema)

work = [(1, 'https://s3-us-west-2.amazonaws.com/tpchssb/chunks-quickStatic-ingest/4-chunks/lineorder-part1')]

queryImport = MyriaQuery.parallel_import(relation=relation, work=work, scan_parameters={'delimiter':'|'}, insert_parameters={'argOverwriteTable':True})

#
work = [(1, 'https://s3-us-west-2.amazonaws.com/tpchssb/chunks-quickStatic-ingest/6-chunks/lineorder-part1')]

queryImport = MyriaQuery.parallel_import(relation=relation, work=work, scan_parameters={'delimiter':'|'}, insert_parameters={'argOverwriteTable':False})
#
work = [(1, 'https://s3-us-west-2.amazonaws.com/tpchssb/chunks-quickStatic-ingest/8-chunks/lineorder-part1')]

queryImport = MyriaQuery.parallel_import(relation=relation, work=work, scan_parameters={'delimiter':'|'}, insert_parameters={'argOverwriteTable':False})
#
work = [(1, 'https://s3-us-west-2.amazonaws.com/tpchssb/chunks-quickStatic-ingest/10-chunks/lineorder-part1')]

queryImport = MyriaQuery.parallel_import(relation=relation, work=work, scan_parameters={'delimiter':'|'}, insert_parameters={'argOverwriteTable':False})
#
work = [(1, 'https://s3-us-west-2.amazonaws.com/tpchssb/chunks-quickStatic-ingest/12-chunks/lineorder-part1')]

queryImport = MyriaQuery.parallel_import(relation=relation, work=work, scan_parameters={'delimiter':'|'}, insert_parameters={'argOverwriteTable':False})
