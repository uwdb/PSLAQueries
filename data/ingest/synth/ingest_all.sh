MASTER=ec2-54-204-118-137.compute-1.amazonaws.com
PORT=8753

#ingesting all
python ingest_parallel_fact.py $MASTER

curl -i -XPOST $MASTER:$PORT/dataset -H "Content-type: application/json"  -d @./ingest_dim1.json

curl -i -XPOST $MASTER:$PORT/dataset -H "Content-type: application/json"  -d @./ingest_dim2.json

curl -i -XPOST $MASTER:$PORT/dataset -H "Content-type: application/json"  -d @./ingest_dim3.json

curl -i -XPOST $MASTER:$PORT/dataset -H "Content-type: application/json"  -d @./ingest_dim4.json

curl -i -XPOST $MASTER:$PORT/dataset -H "Content-type: application/json"  -d @./ingest_dim5.json

python replicate_all.py $MASTER
