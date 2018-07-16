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

def blockchain_status():
    response = wallet_request("getStatus", {})
    return {
        'blockCount': response['result']['blockCount'],
        'lastBlockHash': response['result']['lastBlockHash'],
        'peerCount': response['result']['peerCount']
    }

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
                        return 'CONFIRMED', transfer['amount'] / 1.0e10, transaction['timestamp']

    unconfirmed_tx_response = wallet_request("getUnconfirmedTransactionHashes", {})
    unconfirmed_tx = unconfirmed_tx_response['result']['transactionHashes']

    for transaction in unconfirmed_tx:
        if transaction == tx_id:
            return 'UNCONFIRMED', None, None

    return 'NOT_FOUND', None, None

def create_wallet():
    create_address_response = wallet_request("createAddress", {})
    new_address = create_address_response['result']['address']
    return new_address
