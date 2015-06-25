run ./start.sh with the first argument as your starcluster cluster name (i.e. ./start.sh mycluster). This script moves data to the master, installs raco, aws, gnu parallel, myria-python

If you need to delete generated queries, run ./queries/remove_queries.sh

Tasks handled by user on master:

*ingest data (run ingest_all.sh)
*install ganglia
*generate queries
*configure AWS