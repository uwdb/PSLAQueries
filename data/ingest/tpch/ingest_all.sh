MASTER=ec2-54-158-151-56.compute-1.amazonaws.com
PORT=8753

#ingesting all lineitems
python ingest_parallel_lineitem.py $MASTER

curl -i -XPOST $MASTER:$PORT/dataset -H "Content-type: application/json"  -d @./ingest_customer.json

curl -i -XPOST $MASTER:$PORT/dataset -H "Content-type: application/json"  -d @./ingest_date.json

curl -i -XPOST $MASTER:$PORT/dataset -H "Content-type: application/json"  -d @./ingest_part.json

curl -i -XPOST $MASTER:$PORT/dataset -H "Content-type: application/json"  -d @./ingest_supplier.json

python replicate_all.py $MASTER
