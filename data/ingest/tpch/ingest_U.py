from myria import MyriaConnection, MyriaRelation, MyriaQuery, MyriaSchema
import sys

connection = MyriaConnection(hostname = sys.argv[1], port=8753)

schema = MyriaSchema({"columnNames": ["l_orderkey", "l_linenumber", "l_custkey", "l_partkey", "l_suppkey", "l_orderdate", "l_orderpriority", "l_shippriority", "l_quantity", "l_extendedprice", "l_ordtotalprice", "l_discount", "l_revenue", "l_supplycost", "l_tax", "l_commitdate", "l_shipmode"], "columnTypes": ["LONG_TYPE", "LONG_TYPE", "LONG_TYPE", "LONG_TYPE", "LONG_TYPE", "STRING_TYPE", "STRING_TYPE", "LONG_TYPE", "DOUBLE_TYPE", "DOUBLE_TYPE", "DOUBLE_TYPE", "DOUBLE_TYPE", "LONG_TYPE", "LONG_TYPE", "DOUBLE_TYPE", "LONG_TYPE", "STRING_TYPE"]})

#4
relation = MyriaRelation('public:adhoc10GB4_U:lineorder', connection=connection, schema=schema)

work = [(1, 'https://s3-us-west-2.amazonaws.com/tpchssb/chunks-quickStatic-ingest/4-chunks/lineorder-part1'), 
        (2, 'https://s3-us-west-2.amazonaws.com/tpchssb/chunks-quickStatic-ingest/4-chunks/lineorder-part2'),
        (3, 'https://s3-us-west-2.amazonaws.com/tpchssb/chunks-quickStatic-ingest/4-chunks/lineorder-part3'),
        (4, 'https://s3-us-west-2.amazonaws.com/tpchssb/chunks-quickStatic-ingest/4-chunks/lineorder-part4')]

queryImport = MyriaQuery.parallel_import(relation=relation, work=work, scan_parameters={'delimiter':'|'}, insert_parameters={'argOverwriteTable':True})

#6
relation = MyriaRelation('public:adhoc10GB6W_U:lineorder', connection=connection, schema=schema)

work = [(1, 'https://s3-us-west-2.amazonaws.com/tpchssb/chunks-quickStatic-ingest/6-chunks/lineorder-part1'), 
        (2, 'https://s3-us-west-2.amazonaws.com/tpchssb/chunks-quickStatic-ingest/6-chunks/lineorder-part2'),
        (3, 'https://s3-us-west-2.amazonaws.com/tpchssb/chunks-quickStatic-ingest/6-chunks/lineorder-part3'),
        (4, 'https://s3-us-west-2.amazonaws.com/tpchssb/chunks-quickStatic-ingest/6-chunks/lineorder-part4'),
        (5, 'https://s3-us-west-2.amazonaws.com/tpchssb/chunks-quickStatic-ingest/6-chunks/lineorder-part5'),
        (6, 'https://s3-us-west-2.amazonaws.com/tpchssb/chunks-quickStatic-ingest/6-chunks/lineorder-part6')]

queryImport = MyriaQuery.parallel_import(relation=relation, work=work, scan_parameters={'delimiter':'|'}, insert_parameters={'argOverwriteTable':True})

#8
relation = MyriaRelation('public:adhoc10GB8W_U:lineorder', connection=connection, schema=schema)

work = [(1, 'https://s3-us-west-2.amazonaws.com/tpchssb/chunks-quickStatic-ingest/8-chunks/lineorder-part1'), 
        (2, 'https://s3-us-west-2.amazonaws.com/tpchssb/chunks-quickStatic-ingest/8-chunks/lineorder-part2'),
        (3, 'https://s3-us-west-2.amazonaws.com/tpchssb/chunks-quickStatic-ingest/8-chunks/lineorder-part3'),
        (4, 'https://s3-us-west-2.amazonaws.com/tpchssb/chunks-quickStatic-ingest/8-chunks/lineorder-part4'),
        (5, 'https://s3-us-west-2.amazonaws.com/tpchssb/chunks-quickStatic-ingest/8-chunks/lineorder-part5'),
        (6, 'https://s3-us-west-2.amazonaws.com/tpchssb/chunks-quickStatic-ingest/8-chunks/lineorder-part6'), 
        (7, 'https://s3-us-west-2.amazonaws.com/tpchssb/chunks-quickStatic-ingest/8-chunks/lineorder-part7'),
        (8, 'https://s3-us-west-2.amazonaws.com/tpchssb/chunks-quickStatic-ingest/8-chunks/lineorder-part8')]

queryImport = MyriaQuery.parallel_import(relation=relation, work=work, scan_parameters={'delimiter':'|'}, insert_parameters={'argOverwriteTable':True})

#10
relation = MyriaRelation('public:adhoc10GB10W_U:lineorder', connection=connection, schema=schema)

work = [(1, 'https://s3-us-west-2.amazonaws.com/tpchssb/chunks-quickStatic-ingest/10-chunks/lineorder-part1'), 
        (2, 'https://s3-us-west-2.amazonaws.com/tpchssb/chunks-quickStatic-ingest/10-chunks/lineorder-part2'),
        (3, 'https://s3-us-west-2.amazonaws.com/tpchssb/chunks-quickStatic-ingest/10-chunks/lineorder-part3'),
        (4, 'https://s3-us-west-2.amazonaws.com/tpchssb/chunks-quickStatic-ingest/10-chunks/lineorder-part4'),
        (5, 'https://s3-us-west-2.amazonaws.com/tpchssb/chunks-quickStatic-ingest/10-chunks/lineorder-part5'),
        (6, 'https://s3-us-west-2.amazonaws.com/tpchssb/chunks-quickStatic-ingest/10-chunks/lineorder-part6'), 
        (7, 'https://s3-us-west-2.amazonaws.com/tpchssb/chunks-quickStatic-ingest/10-chunks/lineorder-part7'),
        (8, 'https://s3-us-west-2.amazonaws.com/tpchssb/chunks-quickStatic-ingest/10-chunks/lineorder-part8'),
        (9, 'https://s3-us-west-2.amazonaws.com/tpchssb/chunks-quickStatic-ingest/10-chunks/lineorder-part9'),
        (10, 'https://s3-us-west-2.amazonaws.com/tpchssb/chunks-quickStatic-ingest/10-chunks/lineorder-part10')]

queryImport = MyriaQuery.parallel_import(relation=relation, work=work, scan_parameters={'delimiter':'|'}, insert_parameters={'argOverwriteTable':True})

#12
relation = MyriaRelation('public:adhoc10GB12W_U:lineorder', connection=connection, schema=schema)

work = [(1, 'https://s3-us-west-2.amazonaws.com/tpchssb/chunks-quickStatic-ingest/12-chunks/lineorder-part1'), 
        (2, 'https://s3-us-west-2.amazonaws.com/tpchssb/chunks-quickStatic-ingest/12-chunks/lineorder-part2'),
        (3, 'https://s3-us-west-2.amazonaws.com/tpchssb/chunks-quickStatic-ingest/12-chunks/lineorder-part3'),
        (4, 'https://s3-us-west-2.amazonaws.com/tpchssb/chunks-quickStatic-ingest/12-chunks/lineorder-part4'),
        (5, 'https://s3-us-west-2.amazonaws.com/tpchssb/chunks-quickStatic-ingest/12-chunks/lineorder-part5'),
        (6, 'https://s3-us-west-2.amazonaws.com/tpchssb/chunks-quickStatic-ingest/12-chunks/lineorder-part6'), 
        (7, 'https://s3-us-west-2.amazonaws.com/tpchssb/chunks-quickStatic-ingest/12-chunks/lineorder-part7'),
        (8, 'https://s3-us-west-2.amazonaws.com/tpchssb/chunks-quickStatic-ingest/12-chunks/lineorder-part8'),
        (9, 'https://s3-us-west-2.amazonaws.com/tpchssb/chunks-quickStatic-ingest/12-chunks/lineorder-part9'),
        (10, 'https://s3-us-west-2.amazonaws.com/tpchssb/chunks-quickStatic-ingest/12-chunks/lineorder-part10'), 
        (11, 'https://s3-us-west-2.amazonaws.com/tpchssb/chunks-quickStatic-ingest/12-chunks/lineorder-part11'),
        (12, 'https://s3-us-west-2.amazonaws.com/tpchssb/chunks-quickStatic-ingest/12-chunks/lineorder-part12')]

queryImport = MyriaQuery.parallel_import(relation=relation, work=work, scan_parameters={'delimiter':'|'}, insert_parameters={'argOverwriteTable':True})
