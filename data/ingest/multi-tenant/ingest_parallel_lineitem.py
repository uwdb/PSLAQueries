from myria import MyriaConnection, MyriaRelation, MyriaQuery, MyriaSchema
import sys

connection = MyriaConnection(hostname = sys.argv[1], port=8753)

schema = MyriaSchema({"columnNames": ["l_orderkey", "l_linenumber", "l_custkey", "l_partkey", "l_suppkey", "l_orderdate", "l_orderpriority", "l_shippriority", "l_quantity", "l_extendedprice", "l_ordtotalprice", "l_discount", "l_revenue", "l_supplycost", "l_tax", "l_commitdate", "l_shipmode"], "columnTypes": ["LONG_TYPE", "LONG_TYPE", "LONG_TYPE", "LONG_TYPE", "LONG_TYPE", "STRING_TYPE", "STRING_TYPE", "LONG_TYPE", "DOUBLE_TYPE", "DOUBLE_TYPE", "DOUBLE_TYPE", "DOUBLE_TYPE", "LONG_TYPE", "LONG_TYPE", "DOUBLE_TYPE", "LONG_TYPE", "STRING_TYPE"]})

#2 shared
relation = MyriaRelation('public:adhoc10GB12W_tenant1_2shared:lineitem', connection=connection, schema=schema)

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

status = queryImport.status

while status!='SUCCESS':
        status = queryImport.status
        time.sleep(2);
        if status=='ERROR':
                break;


relation = MyriaRelation('public:adhoc10GB12W_tenant2_2shared:lineitem', connection=connection, schema=schema)

work = [(1, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part1'), 
        (2, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part2'),
        (13, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part3'),
        (14, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part4'),
        (15, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part5'),
        (16, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part6'), 
        (17, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part7'),
        (18, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part8'),
        (19, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part9'),
        (20, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part10'), 
        (21, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part11'),
        (22, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part12')]

queryImport = MyriaQuery.parallel_import(relation=relation, work=work, scan_parameters={'delimiter':'|'}, insert_parameters={'argOverwriteTable':True})

status = queryImport.status

while status!='SUCCESS':
        status = queryImport.status
        time.sleep(2);
        if status=='ERROR':
                break;


relation = MyriaRelation('public:adhoc10GB12W_tenant3_2shared:lineitem', connection=connection, schema=schema)

work = [(1, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part1'), 
        (2, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part2'),
        (23, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part3'),
        (24, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part4'),
        (25, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part5'),
        (26, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part6'), 
        (27, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part7'),
        (28, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part8'),
        (29, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part9'),
        (30, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part10'), 
        (31, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part11'),
        (32, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part12')]

queryImport = MyriaQuery.parallel_import(relation=relation, work=work, scan_parameters={'delimiter':'|'}, insert_parameters={'argOverwriteTable':True})

status = queryImport.status

while status!='SUCCESS':
        status = queryImport.status
        time.sleep(2);
        if status=='ERROR':
                break;


relation = MyriaRelation('public:adhoc10GB12W_tenant4_2shared:lineitem', connection=connection, schema=schema)

work = [(1, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part1'), 
        (2, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part2'),
        (33, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part3'),
        (34, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part4'),
        (35, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part5'),
        (36, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part6'), 
        (37, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part7'),
        (38, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part8'),
        (39, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part9'),
        (40, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part10'), 
        (41, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part11'),
        (42, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part12')]

queryImport = MyriaQuery.parallel_import(relation=relation, work=work, scan_parameters={'delimiter':'|'}, insert_parameters={'argOverwriteTable':True})

status = queryImport.status

while status!='SUCCESS':
        status = queryImport.status
        time.sleep(2);
        if status=='ERROR':
                break;


#4 shared
relation = MyriaRelation('public:adhoc10GB12W_tenant1_4shared:lineitem', connection=connection, schema=schema)

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

status = queryImport.status

while status!='SUCCESS':
        status = queryImport.status
        time.sleep(2);
        if status=='ERROR':
                break;


relation = MyriaRelation('public:adhoc10GB12W_tenant2_4shared:lineitem', connection=connection, schema=schema)

work = [(1, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part1'), 
        (2, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part2'),
        (3, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part3'),
        (4, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part4'),
        (13, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part5'),
        (14, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part6'), 
        (15, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part7'),
        (16, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part8'),
        (17, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part9'),
        (18, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part10'), 
        (19, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part11'),
        (20, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part12')]

queryImport = MyriaQuery.parallel_import(relation=relation, work=work, scan_parameters={'delimiter':'|'}, insert_parameters={'argOverwriteTable':True})

status = queryImport.status

while status!='SUCCESS':
        status = queryImport.status
        time.sleep(2);
        if status=='ERROR':
                break;


relation = MyriaRelation('public:adhoc10GB12W_tenant3_4shared:lineitem', connection=connection, schema=schema)

work = [(1, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part1'), 
        (2, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part2'),
        (3, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part3'),
        (4, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part4'),
        (21, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part5'),
        (22, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part6'), 
        (23, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part7'),
        (24, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part8'),
        (25, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part9'),
        (26, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part10'), 
        (27, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part11'),
        (28, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part12')]

queryImport = MyriaQuery.parallel_import(relation=relation, work=work, scan_parameters={'delimiter':'|'}, insert_parameters={'argOverwriteTable':True})

status = queryImport.status

while status!='SUCCESS':
        status = queryImport.status
        time.sleep(2);
        if status=='ERROR':
                break;


relation = MyriaRelation('public:adhoc10GB12W_tenant4_4shared:lineitem', connection=connection, schema=schema)

work = [(1, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part1'), 
        (2, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part2'),
        (3, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part3'),
        (4, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part4'),
        (29, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part5'),
        (30, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part6'), 
        (31, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part7'),
        (32, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part8'),
        (33, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part9'),
        (34, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part10'), 
        (35, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part11'),
        (36, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part12')]

queryImport = MyriaQuery.parallel_import(relation=relation, work=work, scan_parameters={'delimiter':'|'}, insert_parameters={'argOverwriteTable':True})

status = queryImport.status

while status!='SUCCESS':
        status = queryImport.status
        time.sleep(2);
        if status=='ERROR':
                break;


#6 shared

relation = MyriaRelation('public:adhoc10GB12W_tenant1_6shared:lineitem', connection=connection, schema=schema)

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

status = queryImport.status

while status!='SUCCESS':
        status = queryImport.status
        time.sleep(2);
        if status=='ERROR':
                break;



relation = MyriaRelation('public:adhoc10GB12W_tenant2_6shared:lineitem', connection=connection, schema=schema)

work = [(1, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part1'), 
        (2, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part2'),
        (3, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part3'),
        (4, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part4'),
        (5, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part5'),
        (6, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part6'), 
        (13, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part7'),
        (14, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part8'),
        (15, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part9'),
        (16, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part10'), 
        (17, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part11'),
        (18, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part12')]

queryImport = MyriaQuery.parallel_import(relation=relation, work=work, scan_parameters={'delimiter':'|'}, insert_parameters={'argOverwriteTable':True})

status = queryImport.status

while status!='SUCCESS':
        status = queryImport.status
        time.sleep(2);
        if status=='ERROR':
                break;



relation = MyriaRelation('public:adhoc10GB12W_tenant3_6shared:lineitem', connection=connection, schema=schema)

work = [(1, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part1'), 
        (2, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part2'),
        (3, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part3'),
        (4, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part4'),
        (5, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part5'),
        (6, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part6'), 
        (19, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part7'),
        (20, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part8'),
        (21, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part9'),
        (22, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part10'), 
        (23, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part11'),
        (24, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part12')]

queryImport = MyriaQuery.parallel_import(relation=relation, work=work, scan_parameters={'delimiter':'|'}, insert_parameters={'argOverwriteTable':True})

status = queryImport.status

while status!='SUCCESS':
        status = queryImport.status
        time.sleep(2);
        if status=='ERROR':
                break;



relation = MyriaRelation('public:adhoc10GB12W_tenant4_6shared:lineitem', connection=connection, schema=schema)

work = [(1, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part1'), 
        (2, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part2'),
        (3, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part3'),
        (4, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part4'),
        (5, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part5'),
        (6, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part6'), 
        (25, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part7'),
        (26, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part8'),
        (27, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part9'),
        (28, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part10'), 
        (29, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part11'),
        (30, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part12')]

queryImport = MyriaQuery.parallel_import(relation=relation, work=work, scan_parameters={'delimiter':'|'}, insert_parameters={'argOverwriteTable':True})

status = queryImport.status

while status!='SUCCESS':
        status = queryImport.status
        time.sleep(2);
        if status=='ERROR':
                break;


#8 shared

relation = MyriaRelation('public:adhoc10GB12W_tenant1_8shared:lineitem', connection=connection, schema=schema)

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

status = queryImport.status

while status!='SUCCESS':
        status = queryImport.status
        time.sleep(2);
        if status=='ERROR':
                break;



relation = MyriaRelation('public:adhoc10GB12W_tenant2_8shared:lineitem', connection=connection, schema=schema)

work = [(1, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part1'), 
        (2, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part2'),
        (3, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part3'),
        (4, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part4'),
        (5, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part5'),
        (6, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part6'), 
        (7, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part7'),
        (8, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part8'),
        (13, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part9'),
        (14, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part10'), 
        (15, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part11'),
        (16, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part12')]

queryImport = MyriaQuery.parallel_import(relation=relation, work=work, scan_parameters={'delimiter':'|'}, insert_parameters={'argOverwriteTable':True})

status = queryImport.status

while status!='SUCCESS':
        status = queryImport.status
        time.sleep(2);
        if status=='ERROR':
                break;



relation = MyriaRelation('public:adhoc10GB12W_tenant3_8shared:lineitem', connection=connection, schema=schema)

work = [(1, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part1'), 
        (2, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part2'),
        (3, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part3'),
        (4, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part4'),
        (5, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part5'),
        (6, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part6'), 
        (7, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part7'),
        (8, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part8'),
        (17, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part9'),
        (18, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part10'), 
        (19, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part11'),
        (20, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part12')]

queryImport = MyriaQuery.parallel_import(relation=relation, work=work, scan_parameters={'delimiter':'|'}, insert_parameters={'argOverwriteTable':True})

status = queryImport.status

while status!='SUCCESS':
        status = queryImport.status
        time.sleep(2);
        if status=='ERROR':
                break;


relation = MyriaRelation('public:adhoc10GB12W_tenant4_8shared:lineitem', connection=connection, schema=schema)

work = [(1, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part1'), 
        (2, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part2'),
        (3, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part3'),
        (4, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part4'),
        (5, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part5'),
        (6, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part6'), 
        (7, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part7'),
        (8, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part8'),
        (21, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part9'),
        (22, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part10'), 
        (23, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part11'),
        (24, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part12')]

queryImport = MyriaQuery.parallel_import(relation=relation, work=work, scan_parameters={'delimiter':'|'}, insert_parameters={'argOverwriteTable':True})

status = queryImport.status

while status!='SUCCESS':
        status = queryImport.status
        time.sleep(2);
        if status=='ERROR':
                break;



