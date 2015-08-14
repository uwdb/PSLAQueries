#import replication tables and lineitem
FOLDERLIST=("4W" "6W" "8W" "10W" "12W")

for currentFolder in "${FOLDERLIST[@]}"
do
curl -i -XPOST $MASTER:$PORT/dataset/importDataset -H "Content-type: application/json"  -d @."$currentFolder"/import_customer.json

curl -i -XPOST $MASTER:$PORT/dataset/importDataset -H "Content-type: application/json"  -d @."$currentFolder"/import_date.json

curl -i -XPOST $MASTER:$PORT/dataset/importDataset -H "Content-type: application/json"  -d @."$currentFolder"/import_part.json

curl -i -XPOST $MASTER:$PORT/dataset/importDataset -H "Content-type: application/json"  -d @."$currentFolder"/import_supplier.json

curl -i -XPOST $MASTER:$PORT/dataset/importDataset -H "Content-type: application/json"  -d @."$currentFolder"/import_lineitem.json
done