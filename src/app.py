from flask import Flask, abort, jsonify, request
from services.nodes import get_network_nodes, add_network_node
from services.tokens import build_token
from services.keys import  get_server_keys, get_server_wallet
from services.wallet import blockchain_status, check_transaction
import json
import base64

app = Flask(__name__)

def init_app(app):
    pub_key, priv_key = get_server_keys()
    server_wallet_address = get_server_wallet()
    app.config.update(dict(
            PUBLIC_KEY=pub_key,
            PRIVATE_KEY=priv_key,
            SERVER_WALLET_ADDRESS=server_wallet_address,
            PRICE=100,
        ))


init_app(app)

# Returns the blockchain status
@app.route("/blockchain_status", methods=['GET'])
def get_blockchain_status():
    status = blockchain_status()
    return jsonify(status)

@app.route("/network_status", methods=['GET'])
def get_network_status():
    nodes = get_network_nodes()
    return jsonify({
        "server_wallet": app.config['SERVER_WALLET_ADDRESS'],
        "nodes": nodes['nodes']
    })

@app.route("/wallet_address", methods=['GET'])
def get_wallet_address():
    return jsonify({"address": app.config['SERVER_WALLET_ADDRESS'] })

# Returns the list of nodes on the network
@app.route("/nodes", methods=['GET'])
def get_nodes():
    nodes = get_network_nodes()
    return jsonify(nodes)

@app.route("/node", methods=['POST'])
def create_node():
    response = add_network_node(request.remote_addr)
    return jsonify(response)

# Returns the key the nodes will use to validate access tokens
@app.route("/token_validation_key", methods=['GET'])
def get_token_validation_key():
    return jsonify({
        'public_key': app.config['PUBLIC_KEY']
    })

@app.route("/check_transaction_status", methods=['POST'])
def check_transaction_status():
    tx_id = request.get_json().get('tx_id')
    tx_status, tx_amount = check_transaction(tx_id)
    return jsonify({'tx_status': tx_status, 'tx_amount': tx_amount})

# Returns access token for a given transaction (if this transaction has been validated)
@app.route("/token", methods=['POST'])
def get_token():
    tx_id = request.get_json().get('tx_id')
    if tx_id:
        tx_status, tx_amount, tx_timestamp = check_transaction(tx_id)
        if tx_status == 'CONFIRMED':
            response = build_token(tx_status, tx_amount, tx_timestamp, tx_id)
            return jsonify(response)
        elif tx_status == 'UNCONFIRMED':
            return jsonify({
                'tx_status': tx_status,
                'tx_amount': None,
                'tx_timestamp': None,
                'token': None,
                'price': app.config['PRICE'],
                'expires_at': None,
            })
        else:
            abort(400)
    else:
        abort(400)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
