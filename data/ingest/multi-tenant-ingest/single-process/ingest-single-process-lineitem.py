
from myria import MyriaConnection, MyriaRelation, MyriaQuery, MyriaSchema
import sys
import time

connection = MyriaConnection(hostname = sys.argv[1], port=8753)

schema = MyriaSchema({"columnNames": ["l_orderkey", "l_linenumber", "l_custkey", "l_partkey", "l_suppkey", "l_orderdate", "l_orderpriority", "l_shippriority", "l_quantity", "l_extendedprice", "l_ordtotalprice", "l_discount", "l_revenue", "l_supplycost", "l_tax", "l_commitdate", "l_shipmode"], "columnTypes": ["LONG_TYPE", "LONG_TYPE", "LONG_TYPE", "LONG_TYPE", "LONG_TYPE", "STRING_TYPE", "STRING_TYPE", "LONG_TYPE", "DOUBLE_TYPE", "DOUBLE_TYPE", "DOUBLE_TYPE", "DOUBLE_TYPE", "LONG_TYPE", "LONG_TYPE", "DOUBLE_TYPE", "LONG_TYPE", "STRING_TYPE"]})



#12 - tenant #1
relation = MyriaRelation('public:adhoc10GB_tenant1_TEMP:lineitem', connection=connection, schema=schema)

work = [(5, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part1'), 
        (6, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part2'),
        (7, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part3'),
        (8, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part4'),
        (9, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part5'),
        (10, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part6'), 
        (11, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part7'),
        (12, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part8'),
        (13, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part9'),
        (13, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part10'), 
        (15, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part11'),
        (16, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part12')]

queryImport = MyriaQuery.parallel_import(relation=relation, work=work, scan_parameters={'delimiter':'|'}, insert_parameters={'argOverwriteTable':True})

status = queryImport.status

while status!='SUCCESS':
        status = queryImport.status
        time.sleep(2);
        if status=='ERROR':
                break;

#12 - tenant #1
relation = MyriaRelation('public:adhoc10GB_tenant2_TEMP:lineitem', connection=connection, schema=schema)

work = [(5, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part1'), 
        (6, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part2'),
        (7, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part3'),
        (8, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part4'),
        (9, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part5'),
        (10, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part6'), 
        (11, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part7'),
        (12, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part8'),
        (13, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part9'),
        (13, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part10'), 
        (15, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part11'),
        (16, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part12')]

queryImport = MyriaQuery.parallel_import(relation=relation, work=work, scan_parameters={'delimiter':'|'}, insert_parameters={'argOverwriteTable':True})

status = queryImport.status

while status!='SUCCESS':
        status = queryImport.status
        time.sleep(2);
        if status=='ERROR':
                break;



# #12 - tenant #1
# relation = MyriaRelation('public:adhoc10GB_tenant1_12W:lineitem', connection=connection, schema=schema)

# work = [(1, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part1'), 
#         (2, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part2'),
#         (3, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part3'),
#         (4, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part4'),
#         (5, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part5'),
#         (6, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part6'), 
#         (7, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part7'),
#         (8, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part8'),
#         (9, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part9'),
#         (10, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part10'), 
#         (11, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part11'),
#         (12, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part12')]

# queryImport = MyriaQuery.parallel_import(relation=relation, work=work, scan_parameters={'delimiter':'|'}, insert_parameters={'argOverwriteTable':True})

# status = queryImport.status

# while status!='SUCCESS':
# 	status = queryImport.status
# 	time.sleep(2);
# 	if status=='ERROR':
# 		break;


# # tenant #2 shifting versions
# relation = MyriaRelation('public:adhoc10GB_tenant2-2shared_12W:lineitem', connection=connection, schema=schema)

# work = [(11, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part1'), 
#         (12, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part2'),
#         (13, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part3'),
#         (14, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part4'),
#         (15, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part5'),
#         (16, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part6'), 
#         (17, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part7'),
#         (18, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part8'),
#         (19, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part9'),
#         (20, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part10'), 
#         (21, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part11'),
#         (22, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part12')]

# queryImport = MyriaQuery.parallel_import(relation=relation, work=work, scan_parameters={'delimiter':'|'}, insert_parameters={'argOverwriteTable':True})


# status = queryImport.status

# while status!='SUCCESS':
# 	status = queryImport.status
# 	time.sleep(2);
# 	if status=='ERROR':
# 		break;


# #4 shared
# relation = MyriaRelation('public:adhoc10GB_tenant2-4shared_12W:lineitem', connection=connection, schema=schema)

# work = [(9, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part1'), 
#         (10, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part2'),
#         (11, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part3'),
#         (12, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part4'),
#         (13, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part5'),
#         (14, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part6'), 
#         (15, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part7'),
#         (16, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part8'),
#         (17, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part9'),
#         (18, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part10'), 
#         (19, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part11'),
#         (20, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part12')]

# queryImport = MyriaQuery.parallel_import(relation=relation, work=work, scan_parameters={'delimiter':'|'}, insert_parameters={'argOverwriteTable':True})


# status = queryImport.status

# while status!='SUCCESS':
# 	status = queryImport.status
# 	time.sleep(2);
# 	if status=='ERROR':
# 		break;


# #6 shared
# relation = MyriaRelation('public:adhoc10GB_tenant2-6shared_12W:lineitem', connection=connection, schema=schema)

# work = [(7, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part1'), 
#         (8, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part2'),
#         (9, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part3'),
#         (10, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part4'),
#         (11, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part5'),
#         (12, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part6'), 
#         (13, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part7'),
#         (14, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part8'),
#         (15, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part9'),
#         (16, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part10'), 
#         (17, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part11'),
#         (18, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part12')]

# queryImport = MyriaQuery.parallel_import(relation=relation, work=work, scan_parameters={'delimiter':'|'}, insert_parameters={'argOverwriteTable':True})


# status = queryImport.status

# while status!='SUCCESS':
# 	status = queryImport.status
# 	time.sleep(2);
# 	if status=='ERROR':
# 		break;


# #8 shared
# relation = MyriaRelation('public:adhoc10GB_tenant2-8shared_12W:lineitem', connection=connection, schema=schema)

# work = [(5, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part1'), 
#         (6, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part2'),
#         (7, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part3'),
#         (8, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part4'),
#         (9, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part5'),
#         (10, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part6'), 
#         (11, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part7'),
#         (12, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part8'),
#         (13, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part9'),
#         (14, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part10'), 
#         (15, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part11'),
#         (16, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/lineitem-part12')]

# queryImport = MyriaQuery.parallel_import(relation=relation, work=work, scan_parameters={'delimiter':'|'}, insert_parameters={'argOverwriteTable':True})

# status = queryImport.status

# while status!='SUCCESS':
# 	status = queryImport.status
# 	time.sleep(2);
# 	if status=='ERROR':
# 		break;