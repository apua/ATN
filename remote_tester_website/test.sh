unset http_proxy

host='http://10.30.99.1:8000'
host='http://127.0.0.1:8888'

#uuid='d096dc34-93c3-400f-affb-ea806eb7eaa4'
uuid=`python -c 'from uuid import uuid4;print(uuid4())'`
payload='{"ip":"1.2.3.4","suts":[{"uuid":"'$uuid'","type":"","credential":"","reserved_by":"ailin@hpe.com","maintained_by":"apuaj@hpe.com"}]}'
curl -v -X POST -d $payload -H "Content-Type: application/json" $host/execlayer/

id=13
curl -v -X DELETE $host/execlayer/$id

te_id=999
payload='{"test_execution_id":"'${te_id}'","console":"...","report":"...","log":"...","output":"..."}'
curl -v -X POST -d $payload -H "Content-Type: application/json" $host/testresult/
