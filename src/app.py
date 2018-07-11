from flask import Flask, jsonify
from services.nodes import get_nodes
from services.tokens import build_token

import json
import base64

app = Flask(__name__)

@app.route("/get_token", methods=['GET'])
def get_token():
    token = build_token()
    return token.get('token')

@app.route("/get_nodes", methods={'GET'})
def get_nodes_list():
    nodes = get_nodes()
    return jsonify(nodes)
