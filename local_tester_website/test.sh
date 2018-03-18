unset http_proxy

host='http://127.0.0.1:8000'

test_data='{"filename": "basic.robot", "content": "*** test cases ***\nTC\n  log  message  console=yes\n"}'
payload='{"test_data":'$test_data',"remote_id": 1}'

curl -v -X POST -d "$payload" -H "Content-Type: application/json" $host/execute_test/
