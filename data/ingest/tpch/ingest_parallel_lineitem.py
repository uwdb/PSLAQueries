from myria import MyriaConnection, MyriaRelation, MyriaQuery, MyriaSchema

connection = MyriaConnection(hostname = sys.argv[1], port=8753)

schema = MyriaSchema({"columnNames": ["l_orderkey", "l_linenumber", "l_custkey", "l_partkey", "l_suppkey", "l_orderdate", "l_orderpriority", "l_shippriority", "l_quantity", "l_extendedprice", "l_ordtotalprice", "l_discount", "l_revenue", "l_supplycost", "l_tax", "l_commitdate", "l_shipmode"], "columnTypes": ["LONG_TYPE", "LONG_TYPE", "LONG_TYPE", "LONG_TYPE", "LONG_TYPE", "STRING_TYPE", "STRING_TYPE", "LONG_TYPE", "DOUBLE_TYPE", "DOUBLE_TYPE", "DOUBLE_TYPE", "DOUBLE_TYPE", "LONG_TYPE", "LONG_TYPE", "DOUBLE_TYPE", "LONG_TYPE", "STRING_TYPE"]})

#4
relation = MyriaRelation('public:adhoc10GB4W:lineitem', connection=connection, schema=schema)

work = [(1, 'https://s3-us-west-2.amazonaws.com/tpchssb/4Workers/lineitem-part1'), 
        (2, 'https://s3-us-west-2.amazonaws.com/tpchssb/4Workers/lineitem-part2'),
        (3, 'https://s3-us-west-2.amazonaws.com/tpchssb/4Workers/lineitem-part3'),
        (4, 'https://s3-us-west-2.amazonaws.com/tpchssb/4Workers/lineitem-part4')]

queryImport = MyriaQuery.parallel_import(relation=relation, work=work, scan_parameters={'delimiter':'|'}, insert_parameters={'argOverwriteTable':True})

#6
relation = MyriaRelation('public:adhoc10GB6W:lineitem', connection=connection, schema=schema)

work = [(1, 'https://s3-us-west-2.amazonaws.com/tpchssb/6Workers/lineitem-part1'), 
        (2, 'https://s3-us-west-2.amazonaws.com/tpchssb/6Workers/lineitem-part2'),
        (3, 'https://s3-us-west-2.amazonaws.com/tpchssb/6Workers/lineitem-part3'),
        (4, 'https://s3-us-west-2.amazonaws.com/tpchssb/6Workers/lineitem-part4'),
        (5, 'https://s3-us-west-2.amazonaws.com/tpchssb/6Workers/lineitem-part5'),
        (6, 'https://s3-us-west-2.amazonaws.com/tpchssb/6Workers/lineitem-part6')]

queryImport = MyriaQuery.parallel_import(relation=relation, work=work, scan_parameters={'delimiter':'|'}, insert_parameters={'argOverwriteTable':True})

#8
relation = MyriaRelation('public:adhoc10GB8W:lineitem', connection=connection, schema=schema)

work = [(1, 'https://s3-us-west-2.amazonaws.com/tpchssb/8Workers/lineitem-part1'), 
        (2, 'https://s3-us-west-2.amazonaws.com/tpchssb/8Workers/lineitem-part2'),
        (3, 'https://s3-us-west-2.amazonaws.com/tpchssb/8Workers/lineitem-part3'),
        (4, 'https://s3-us-west-2.amazonaws.com/tpchssb/8Workers/lineitem-part4'),
        (5, 'https://s3-us-west-2.amazonaws.com/tpchssb/8Workers/lineitem-part5'),
        (6, 'https://s3-us-west-2.amazonaws.com/tpchssb/8Workers/lineitem-part6'), 
        (7, 'https://s3-us-west-2.amazonaws.com/tpchssb/8Workers/lineitem-part7'),
        (8, 'https://s3-us-west-2.amazonaws.com/tpchssb/8Workers/lineitem-part8')]

queryImport = MyriaQuery.parallel_import(relation=relation, work=work, scan_parameters={'delimiter':'|'}, insert_parameters={'argOverwriteTable':True})

#10
relation = MyriaRelation('public:adhoc10GB10W:lineitem', connection=connection, schema=schema)

work = [(1, 'https://s3-us-west-2.amazonaws.com/tpchssb/10Workers/lineitem-part1'), 
        (2, 'https://s3-us-west-2.amazonaws.com/tpchssb/10Workers/lineitem-part2'),
        (3, 'https://s3-us-west-2.amazonaws.com/tpchssb/10Workers/lineitem-part3'),
        (4, 'https://s3-us-west-2.amazonaws.com/tpchssb/10Workers/lineitem-part4'),
        (5, 'https://s3-us-west-2.amazonaws.com/tpchssb/10Workers/lineitem-part5'),
        (6, 'https://s3-us-west-2.amazonaws.com/tpchssb/10Workers/lineitem-part6'), 
        (7, 'https://s3-us-west-2.amazonaws.com/tpchssb/10Workers/lineitem-part7'),
        (8, 'https://s3-us-west-2.amazonaws.com/tpchssb/10Workers/lineitem-part8'),
        (9, 'https://s3-us-west-2.amazonaws.com/tpchssb/10Workers/lineitem-part9'),
        (10, 'https://s3-us-west-2.amazonaws.com/tpchssb/10Workers/lineitem-part10')]

queryImport = MyriaQuery.parallel_import(relation=relation, work=work, scan_parameters={'delimiter':'|'}, insert_parameters={'argOverwriteTable':True})

#12
relation = MyriaRelation('public:adhoc10GB12W:lineitem', connection=connection, schema=schema)

work = [(1, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part1'), 
        (2, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part2'),
        (3, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part3'),
        (4, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part4'),
        (5, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part5'),
        (6, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part6'), 
        (7, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part7'),
        (8, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part8'),
        (9, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part9'),
        (10, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part10'), 
        (11, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part11'),
        (12, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part12')]

queryImport = MyriaQuery.parallel_import(relation=relation, work=work, scan_parameters={'delimiter':'|'}, insert_parameters={'argOverwriteTable':True})

