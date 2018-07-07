from flask import Flask, jsonify

from datetime import datetime 
from datetime import timedelta

from Crypto.PublicKey import RSA
import pandas as pd
import json
import base64


app = Flask(__name__)

def get_nodes():
    '''Used to retreive the node list stored in a .csv file.
        
        Returns: nodes (a list of nodes, each one contains a dict with
        info about the node).
    '''

    df=pd.read_csv('./nodes/nodelist.csv')
    nodes = []
    for row in range(0,df.shape[0]): # get number of rows
        nodes.append(dict(ip=df.at[row,'ip'],
            wallet=df.at[row,'wallet']))
    return nodes

def get_expire_date(days):
    expire_date = datetime.now() + timedelta(days=days)
    return expire_date.strftime('%m/%d/%Y')

def _encrypt():
    with open('public.pem','r') as f_pub:
        with open('private.pem', 'r') as f_priv:
            pub_key = RSA.importKey(f_pub.read())
            priv_key = RSA.importKey(f_priv.read())
            token = get_expire_date(1)
            encrypted_token = pub_key.encrypt(token.encode('utf-8'), 32)
            return encrypted_token

def build_token():
    encrypted_token = _encrypt()[0]
    return dict(token=encrypted_token)


@app.route("/get_token", methods=['GET'])
def get_token():
    token = build_token()
    return token.get('token')
