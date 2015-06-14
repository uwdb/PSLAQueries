MASTER=ec2-54-161-139-10.compute-1.amazonaws.com
PORT=8753

#ingesting all lineitems
python ingest_parallel_fact.json $MASTER

curl -i -XPOST $MASTER:$PORT/dataset -H "Content-type: application/json"  -d @./ingest_dim1.json

curl -i -XPOST $MASTER:$PORT/dataset -H "Content-type: application/json"  -d @./ingest_dim2.json

curl -i -XPOST $MASTER:$PORT/dataset -H "Content-type: application/json"  -d @./ingest_dim3.json

curl -i -XPOST $MASTER:$PORT/dataset -H "Content-type: application/json"  -d @./ingest_dim4.json

curl -i -XPOST $MASTER:$PORT/dataset -H "Content-type: application/json"  -d @./ingest_dim5.json
