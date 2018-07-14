from flask import Flask, abort, jsonify, request
from services.nodes import get_network_nodes 
from services.tokens import build_token, check_transaction
from services.keys import  get_server_keys
from services.wallet import network_status, server_wallet
import json
import base64

app = Flask(__name__)

def init_app(app):
    pub_key, priv_key = get_server_keys()
    app.config.update(dict(
            PUBLIC_KEY=pub_key,
            PRIVATE_KEY=priv_key,
            PRICE=1000,
        ))


init_app(app)

# Returns the network status
@app.route("/network_status", methods=['GET'])
def get_network_status():
    status = network_status()
    return jsonify(status)

@app.route("/wallet_address", methods=['GET'])
def get_wallet_address():
    address = server_wallet()
    return jsonify(address)

# Returns the list of nodes on the network
@app.route("/nodes", methods=['GET'])
def get_nodes():
    nodes = get_network_nodes()
    return jsonify(nodes)

# Returns the key the nodes will use to validate access tokens
@app.route("/token_validation_key", methods=['GET'])
def get_token_validation_key():
    return app.config['PUBLIC_KEY']

# Returns access token for a given transaction (if this transaction has been validated)
@app.route("/token", methods=['GET'])
def get_token():
    tx_id = None
    if 'TX_ID' in request.headers:
        tx_id = request.headers.get('TX_ID')
        if tx_id:
            is_transaction_valid, tx_amount = check_transaction(tx_id)
            if is_transaction_valid:
                response = build_token(tx_amount, tx_id)
                return jsonify(response)
            else:
                abort(401)
        else:
            abort(400)
    else:
        abort(401)
