from myria import MyriaConnection, MyriaRelation, MyriaQuery, MyriaSchema
import sys

connection = MyriaConnection(hostname = sys.argv[1], port = sys.argv[2])

schema = MyriaSchema({"columnTypes" : ["LONG_TYPE", "LONG_TYPE","LONG_TYPE","LONG_TYPE","LONG_TYPE","LONG_TYPE","LONG_TYPE","LONG_TYPE","LONG_TYPE","LONG_TYPE","LONG_TYPE","LONG_TYPE","LONG_TYPE","LONG_TYPE","LONG_TYPE","LONG_TYPE","LONG_TYPE","LONG_TYPE","LONG_TYPE","LONG_TYPE","LONG_TYPE"], "columnNames" : ["fact_fk1", "fact_fk2", "fact_fk3", "fact_fk4", "fact_fk5", "fact_att6", "fact_att7","fact_att8","fact_att9","fact_att10","fact_att11","fact_att12","fact_att13","fact_att14","fact_att15","fact_att16","fact_att17","fact_att18","fact_att19","fact_att20", "fact_pk"]})

#10
relation = MyriaRelation('public:syntheticBenchmark10W:fact', connection=connection, schema=schema)

work = [(3, 'https://s3-us-west-2.amazonaws.com/custombenchmarkv2/12Workers/fact-part1'),
        (4, 'https://s3-us-west-2.amazonaws.com/custombenchmarkv2/12Workers/fact-part2'),
        (5, 'https://s3-us-west-2.amazonaws.com/custombenchmarkv2/12Workers/fact-part3'),
        (6, 'https://s3-us-west-2.amazonaws.com/custombenchmarkv2/12Workers/fact-part4'),
        (7, 'https://s3-us-west-2.amazonaws.com/custombenchmarkv2/12Workers/fact-part5'),
        (8, 'https://s3-us-west-2.amazonaws.com/custombenchmarkv2/12Workers/fact-part6'),
        (9, 'https://s3-us-west-2.amazonaws.com/custombenchmarkv2/12Workers/fact-part7'),
        (10, 'https://s3-us-west-2.amazonaws.com/custombenchmarkv2/12Workers/fact-part8'),
        (11, 'https://s3-us-west-2.amazonaws.com/custombenchmarkv2/12Workers/fact-part9'),
        (12, 'https://s3-us-west-2.amazonaws.com/custombenchmarkv2/12Workers/fact-part10'),
        (13, 'https://s3-us-west-2.amazonaws.com/custombenchmarkv2/12Workers/fact-part11'),
        (14, 'https://s3-us-west-2.amazonaws.com/custombenchmarkv2/12Workers/fact-part12')]

queryImport = MyriaQuery.parallel_import(relation=relation, work=work, scan_parameters={'delimiter':'|'}, insert_parameters={'argOverwriteTable':True})
