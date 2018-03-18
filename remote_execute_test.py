import requests

#te_id=1
#payload={"test_execution_id":te_id,"console":"...","report":"...","log":"...","output":"..."}
#r = requests.post('http://127.0.0.1:8888/testresult/', json=payload)

local_site = 'http://127.0.0.1:8000'
payload = {
        "test_data": {"filename": "basic.robot", "content": "*** test cases ***\nTC\n  log  message  console=yes\n"},
        "remote_id": 2
        }
r = requests.post(f'{local_site}/execute_test/', json=payload)
