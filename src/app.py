from flask import Flask, abort, jsonify, request
from services.nodes import get_nodes
from services.tokens import build_token, check_transaction

import json
import base64

app = Flask(__name__)

def init_app(app):
   with open('public.pem','r') as f_pub:
    with open('private.pem', 'r') as f_priv:
        app.config.update(dict(
                PUBLIC_KEY=f_priv.read(),
                PRIVATE_KEY=f_pub.read(),
                PRICE=1000,
            ))


init_app(app)

# Returns the list of nodes on the network
@app.route("/nodes", methods=['GET'])
def get_nodes():
    nodes = get_nodes()
    return jsonify(nodes)

# Returns the key the nodes will use to validate access tokens
@app.route("/token_validation_key", methods=['GET'])
def get_token_validation_key():
    return app.config['PUBLIC_KEY']

# Endpoint for buying new access tokens
@app.route("/token", methods=['POST'])
def post_token():
    return "New token"

# Returns access token for a given transaction (if this transaction has been validated)
@app.route("/token", methods=['GET'])
def get_token():
    tx_id = None
    if 'TX_ID' in request.headers:
        tx_id = request.headers.get('TX_ID')
        if tx_id:
            is_transaction_valid, tx_amount = check_transaction(tx_id)
            if is_transaction_valid:
                token = build_token(tx_amount)
                return jsonify({'token': token})
            else:
                abort(401)
        else:
            abort(400)
    else:
        abort(401)
