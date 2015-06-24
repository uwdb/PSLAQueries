MASTER=ec2-54-197-147-1.compute-1.amazonaws.com
PORT=8753

#ingesting all lineitems
python ingest-single-process-lineitem.py $MASTER

curl -i -XPOST $MASTER:$PORT/dataset -H "Content-type: application/json"  -d @./ingest_customer.json

curl -i -XPOST $MASTER:$PORT/dataset -H "Content-type: application/json"  -d @./ingest_date.json

curl -i -XPOST $MASTER:$PORT/dataset -H "Content-type: application/json"  -d @./ingest_part.json

curl -i -XPOST $MASTER:$PORT/dataset -H "Content-type: application/json"  -d @./ingest_supplier.json

python ingest-single-process-replicate-all.py $MASTER