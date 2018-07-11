from flask import current_app as app
from datetime import datetime
from datetime import timedelta
import time
from Crypto.PublicKey import RSA

def get_expiration_timestamp(minutes):
    expire_date = datetime.now() + timedelta(minutes=minutes)
    return time.mktime(expire_date.timetuple())

def generate_token(minutes):
    pub_key = RSA.importKey(app.config['PRIVATE_KEY'])
    priv_key = RSA.importKey(app.config['PUBLIC_KEY']) 
    expiration_date = get_expiration_timestamp(minutes)
    encrypted_token = pub_key.encrypt(str(expiration_date).encode('utf-8'), 32)
    return encrypted_token

# Calculate time of access, build and encrypt token based on the price per unit of time
def build_token(tx_amount):
    encrypted_token = generate_token(10)[0]
    return dict(token=encrypted_token)


# TODO: Connect to the wallet daemon and check if transaction is there
def check_transaction(tx_id):
    if tx_id:
        return True, 10
    else:
        return False, None
