from flask import current_app as app
from datetime import datetime, timedelta
import time
import base64
from Crypto.PublicKey import RSA

def get_expiration_timestamp(minutes, tx_timestamp):
    tx_time = datetime.fromtimestamp(int(tx_timestamp))
    expire_date = tx_time + timedelta(minutes=minutes)
    return time.mktime(expire_date.timetuple())

def generate_token(minutes, tx_timestamp):
    pub_key = RSA.importKey(app.config['PRIVATE_KEY'])
    priv_key = RSA.importKey(app.config['PUBLIC_KEY']) 
    expiration_date = int(get_expiration_timestamp(minutes, tx_timestamp))
    rsa_result = pub_key.encrypt(str(expiration_date).encode('utf-8'), 32)
    encrypted_token = base64.b64encode(rsa_result[0])
    return encrypted_token.decode('utf-8'), expiration_date

# Calculate time of access, build and encrypt token based on the price per unit of time
def build_token(tx_status, tx_amount, tx_timestamp, tx_id):
    minutes_bought = float(tx_amount) / app.config['PRICE']
    token, expiration = generate_token(minutes_bought, tx_timestamp)
    data = {
        'token': token,
        'price': app.config['PRICE'],
        'expires_at': expiration,
        'tx_id': tx_id,
        'tx_status': tx_status,
        'tx_amount': tx_amount,
        'tx_timestamp': tx_timestamp
    }
    return data
