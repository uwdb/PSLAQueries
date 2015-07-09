from myria import MyriaConnection, MyriaRelation, MyriaQuery, MyriaSchema
import sys

connection = MyriaConnection(hostname = sys.argv[1], port=sys.argv[2])
tenant = sys.argv[3]

schema = MyriaSchema({"columnNames": ["l_orderkey", "l_linenumber", "l_custkey", "l_partkey", "l_suppkey", "l_orderdate", "l_orderpriority", "l_shippriority", "l_quantity", "l_extendedprice", "l_ordtotalprice", "l_discount", "l_revenue", "l_supplycost", "l_tax", "l_commitdate", "l_shipmode"], "columnTypes": ["LONG_TYPE", "LONG_TYPE", "LONG_TYPE", "LONG_TYPE", "LONG_TYPE", "STRING_TYPE", "STRING_TYPE", "LONG_TYPE", "DOUBLE_TYPE", "DOUBLE_TYPE", "DOUBLE_TYPE", "DOUBLE_TYPE", "LONG_TYPE", "LONG_TYPE", "DOUBLE_TYPE", "LONG_TYPE", "STRING_TYPE"]})

#12
relation = MyriaRelation('public:adhoc10GB12W_tenant'+ str(tenant) + ':lineitem', connection=connection, schema=schema)

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
