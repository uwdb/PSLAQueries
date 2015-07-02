MASTER=ec2-23-22-177-26.compute-1.amazonaws.com
PORT_A=8753
PORT_B=8754

#ingesting all
python /root/multiMyria/ingest/ingest_fact_tenantA.py $MASTER $PORT_A

curl -i -XPOST $MASTER:$PORT_A/dataset -H "Content-type: application/json"  -d @/root/multiMyria/ingest/ingest_dim1.json

curl -i -XPOST $MASTER:$PORT_A/dataset -H "Content-type: application/json"  -d @/root/multiMyria/ingest/ingest_dim2.json

curl -i -XPOST $MASTER:$PORT_A/dataset -H "Content-type: application/json"  -d @/root/multiMyria/ingest/ingest_dim3.json

curl -i -XPOST $MASTER:$PORT_A/dataset -H "Content-type: application/json"  -d @/root/multiMyria/ingest/ingest_dim4.json

curl -i -XPOST $MASTER:$PORT_A/dataset -H "Content-type: application/json"  -d @/root/multiMyria/ingest/ingest_dim5.json

python /root/multiMyria/ingest/replicate_all.py $MASTER $PORT_A


#ingesting all
python /root/multiMyria/ingest/ingest_fact_tenantB_12.py $MASTER

curl -i -XPOST $MASTER_B:$PORT_B/dataset -H "Content-type: application/json"  -d @/root/multiMyria/ingest/ingest_dim1.json

curl -i -XPOST $MASTER_B:$PORT_B/dataset -H "Content-type: application/json"  -d @/root/multiMyria/ingest/ingest_dim2.json

curl -i -XPOST $MASTER_B:$PORT_B/dataset -H "Content-type: application/json"  -d @/root/multiMyria/ingest/ingest_dim3.json

curl -i -XPOST $MASTER_B:$PORT_B/dataset -H "Content-type: application/json"  -d @/root/multiMyria/ingest/ingest_dim4.json

curl -i -XPOST $MASTER_B:$PORT_B/dataset -H "Content-type: application/json"  -d @/root/multiMyria/ingest/ingest_dim5.json

python /root/multiMyria/ingest/replicate_all.py $MASTER
