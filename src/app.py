from flask import Flask, jsonify
from services.nodes import get_nodes
from services.tokens import build_token

import json
import base64

app = Flask(__name__)

# Returns the list of nodes on the network
@app.route("/nodes", methods=['GET'])
def get_nodes():
    nodes = get_nodes()
    return jsonify(nodes)

# Returns the key the nodes will use to validate access tokens
@app.route("/token_validation_key", methods=['GET'])
def get_token_validation_key():
    return "Token key"

# Endpoint for buying new access tokens
@app.route("/token", methods=['POST'])
def post_token():
    return "New token"

# Returns access token for a given transaction (if this transaction has been validated)
@app.route("/token", methods=['GET'])
def get_token():
    token = build_token()
    return token.get('token')
