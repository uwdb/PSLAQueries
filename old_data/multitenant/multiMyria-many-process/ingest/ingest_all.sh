MASTER=$1
PORT=$2
TENANT=$3

#ingesting all lineitems
python ingest_parallel_lineitem.py $MASTER $PORT $TENANT

curl -i -XPOST $MASTER:$PORT/dataset -H "Content-type: application/json"  -d @./ingest_customer.json

curl -i -XPOST $MASTER:$PORT/dataset -H "Content-type: application/json"  -d @./ingest_date.json

curl -i -XPOST $MASTER:$PORT/dataset -H "Content-type: application/json"  -d @./ingest_part.json

curl -i -XPOST $MASTER:$PORT/dataset -H "Content-type: application/json"  -d @./ingest_supplier.json

python replicate_all.py $MASTER $PORT $TENANT
