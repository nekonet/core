import requests
def wallet_request(method, params):
    headers = {
        'Accept': 'application/json'
    }

    url = 'http://localhost:9090/json_rpc'

    data = {
        "params": params,
        "jsonrpc": "2.0",
        "id": "test",
        "method": method,
    }

    r = requests.post(url, json=data)

    return r.json()

def network_status():
    response = wallet_request("getStatus", {})
    return {
        'blockCount': response['result']['blockCount'],
        'lastBlockHash': response['result']['lastBlockHash'],
        'peerCount': response['result']['peerCount']
    }

