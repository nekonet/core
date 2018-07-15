from flask import json, jsonify
from services.wallet import create_wallet
import uuid

nodes_fpath = './data/nodes.json'

def get_network_nodes():
    data = json.load(open(nodes_fpath))
    return data


def add_network_node(ip):
    data = json.load(open(nodes_fpath))
    identifier = str(uuid.uuid4())
    wallet_address = create_wallet()
    new_node_entry = {"id": identifier, "wallet_address": wallet_address, "ip": ip}
    data["nodes"][identifier] = new_node_entry
    new_data = json.dumps(data)
    with open(nodes_fpath, 'w') as outfile:
        outfile.write(new_data)
    
    return new_node_entry



