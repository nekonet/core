from datetime import datetime
from datetime import timedelta
from Crypto.PublicKey import RSA

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



