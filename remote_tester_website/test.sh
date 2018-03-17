unset http_proxy

host='http://10.30.99.1:8000'

#uuid='d096dc34-93c3-400f-affb-ea806eb7eaa4'
uuid=`python -c 'from uuid import uuid4;print(uuid4())'`

payload='{"ip":"1.2.3.4","suts":[{"uuid":"'$uuid'","type":"","credential":"","reserved_by":"ailin@hpe.com","maintained_by":"apuaj@hpe.com"}]}'

curl -v -X POST -d $payload -H "Content-Type: application/json" $host/execlayer/

id=13

#curl -v -X DELETE $host/execlayer/$id
