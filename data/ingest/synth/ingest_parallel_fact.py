from myria import MyriaConnection, MyriaRelation, MyriaQuery, MyriaSchema

connection = MyriaConnection(hostname = sys.argv[0], port=8753)

schema = MyriaSchema({"columnTypes" : ["LONG_TYPE", "LONG_TYPE","LONG_TYPE","LONG_TYPE","LONG_TYPE","LONG_TYPE","LONG_TYPE","LONG_TYPE","LONG_TYPE","LONG_TYPE","LONG_TYPE","LONG_TYPE","LONG_TYPE","LONG_TYPE","LONG_TYPE","LONG_TYPE","LONG_TYPE","LONG_TYPE","LONG_TYPE","LONG_TYPE","LONG_TYPE"], "columnNames" : ["fact_fk1", "fact_fk2", "fact_fk3", "fact_fk4", "fact_fk5", "fact_att6", "fact_att7","fact_att8","fact_att9","fact_att10","fact_att11","fact_att12","fact_att13","fact_att14","fact_att15","fact_att16","fact_att17","fact_att18","fact_att19","fact_att20", "fact_pk"]})

#4
relation = MyriaRelation('public:adhoc10GB4W:fact', connection=connection, schema=schema)

work = [(1, 'https://s3-us-west-2.amazonaws.com/tpchssb/4Workers/fact-part1'), 
        (2, 'https://s3-us-west-2.amazonaws.com/tpchssb/4Workers/fact-part2'),
        (3, 'https://s3-us-west-2.amazonaws.com/tpchssb/4Workers/fact-part3'),
        (4, 'https://s3-us-west-2.amazonaws.com/tpchssb/4Workers/fact-part4')]

queryImport = MyriaQuery.parallel_import(relation=relation, work=work, scan_parameters={'delimiter':'|'}, insert_parameters={'argOverwriteTable':True})

#6
relation = MyriaRelation('public:adhoc10GB6W:fact', connection=connection, schema=schema)

work = [(1, 'https://s3-us-west-2.amazonaws.com/tpchssb/6Workers/fact-part1'), 
        (2, 'https://s3-us-west-2.amazonaws.com/tpchssb/6Workers/fact-part2'),
        (3, 'https://s3-us-west-2.amazonaws.com/tpchssb/6Workers/fact-part3'),
        (4, 'https://s3-us-west-2.amazonaws.com/tpchssb/6Workers/fact-part4'),
        (5, 'https://s3-us-west-2.amazonaws.com/tpchssb/6Workers/fact-part5'),
        (6, 'https://s3-us-west-2.amazonaws.com/tpchssb/6Workers/fact-part6')]

queryImport = MyriaQuery.parallel_import(relation=relation, work=work, scan_parameters={'delimiter':'|'}, insert_parameters={'argOverwriteTable':True})

#8
relation = MyriaRelation('public:adhoc10GB8W:fact', connection=connection, schema=schema)

work = [(1, 'https://s3-us-west-2.amazonaws.com/tpchssb/8Workers/fact-part1'), 
        (2, 'https://s3-us-west-2.amazonaws.com/tpchssb/8Workers/fact-part2'),
        (3, 'https://s3-us-west-2.amazonaws.com/tpchssb/8Workers/fact-part3'),
        (4, 'https://s3-us-west-2.amazonaws.com/tpchssb/8Workers/fact-part4'),
        (5, 'https://s3-us-west-2.amazonaws.com/tpchssb/8Workers/fact-part5'),
        (6, 'https://s3-us-west-2.amazonaws.com/tpchssb/8Workers/fact-part6'), 
        (7, 'https://s3-us-west-2.amazonaws.com/tpchssb/8Workers/fact-part7'),
        (8, 'https://s3-us-west-2.amazonaws.com/tpchssb/8Workers/fact-part8')]

queryImport = MyriaQuery.parallel_import(relation=relation, work=work, scan_parameters={'delimiter':'|'}, insert_parameters={'argOverwriteTable':True})

#10
relation = MyriaRelation('public:adhoc10GB10W:fact', connection=connection, schema=schema)

work = [(1, 'https://s3-us-west-2.amazonaws.com/tpchssb/10Workers/fact-part1'), 
        (2, 'https://s3-us-west-2.amazonaws.com/tpchssb/10Workers/fact-part2'),
        (3, 'https://s3-us-west-2.amazonaws.com/tpchssb/10Workers/fact-part3'),
        (4, 'https://s3-us-west-2.amazonaws.com/tpchssb/10Workers/fact-part4'),
        (5, 'https://s3-us-west-2.amazonaws.com/tpchssb/10Workers/fact-part5'),
        (6, 'https://s3-us-west-2.amazonaws.com/tpchssb/10Workers/fact-part6'), 
        (7, 'https://s3-us-west-2.amazonaws.com/tpchssb/10Workers/fact-part7'),
        (8, 'https://s3-us-west-2.amazonaws.com/tpchssb/10Workers/fact-part8'),
        (9, 'https://s3-us-west-2.amazonaws.com/tpchssb/10Workers/fact-part9'),
        (10, 'https://s3-us-west-2.amazonaws.com/tpchssb/10Workers/fact-part10')]

queryImport = MyriaQuery.parallel_import(relation=relation, work=work, scan_parameters={'delimiter':'|'}, insert_parameters={'argOverwriteTable':True})

#12
relation = MyriaRelation('public:adhoc10GB12W:fact', connection=connection, schema=schema)

work = [(1, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/fact-part1'), 
        (2, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/fact-part2'),
        (3, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/fact-part3'),
        (4, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/fact-part4'),
        (5, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/fact-part5'),
        (6, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/fact-part6'), 
        (7, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/fact-part7'),
        (8, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/fact-part8'),
        (9, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/fact-part9'),
        (10, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/fact-part10'), 
        (11, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/fact-part11'),
        (12, 'https://s3-us-west-2.amazonaws.com/tpchssb/12Workers/fact-part12')]

queryImport = MyriaQuery.parallel_import(relation=relation, work=work, scan_parameters={'delimiter':'|'}, insert_parameters={'argOverwriteTable':True})

