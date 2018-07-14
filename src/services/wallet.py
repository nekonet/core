from flask import current_app as app
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


def server_wallet():
    response = wallet_request("getAddresses", {})
    addresses = response['result']['addresses']
    address = ""

    if len(addresses) == 1:
        address = addresses[0]

    return {
        'address': address 
    }

# TODO: Connect to the wallet daemon and check if transaction is there
def check_transaction(tx_id):
    status_response = wallet_request("getStatus", {})
    last_block = status_response['result']['blockCount']

    confirmed_tx_response = wallet_request("getTransactions", {
        'firstBlockIndex': 1,
        'blockCount': last_block
    })

    confirmed_tx_blocks = confirmed_tx_response['result']['items']

    for block in confirmed_tx_blocks:
        for transaction in block['transactions']:
            if transaction['transactionHash'] == tx_id:
                for transfer in transaction['transfers']:
                    if transfer['address'] == app.config['SERVER_WALLET_ADDRESS']:
                        return 'CONFIRMED', transfer['amount']

    unconfirmed_tx_response = wallet_request("getUnconfirmedTransactionHashes", {})
    unconfirmed_tx = unconfirmed_tx_response['result']['transactionHashes']

    for transaction in unconfirmed_tx:
        if transaction == tx_id:
            return 'UNCONFIRMED', None

    return 'NOT_FOUND', None
