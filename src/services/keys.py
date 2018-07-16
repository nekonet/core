from Crypto.PublicKey import RSA
import os.path

def get_server_wallet():
    server_wallet_fpath = './data/server_address.dat'
    hasWallet = os.path.isfile(server_wallet_fpath)
    if hasWallet:
        f = open(server_wallet_fpath)
        return f.read().strip()
    else:
        print("Error: Server wallet not found")
        return ""
    

def get_server_keys():
    pub_fname = './data/core_public_key.pem'
    priv_fname = './data/core_private_key.pem'
    
    hasPublicKeyFile = os.path.isfile(pub_fname) 
    hasPrivateKeyFile = os.path.isfile(priv_fname) 

    if not hasPublicKeyFile or not hasPrivateKeyFile:
        pub_key, priv_key = generate_server_keys(pub_fname, priv_fname)
        return pub_key, priv_key
    else:
        with open(pub_fname,'r') as f_pub:
            with open(priv_fname, 'r') as f_priv:
                return f_pub.read(), f_priv.read()

def generate_server_keys(pub_fname, priv_fname):
    public_key = RSA.generate(1024)
    private_key = public_key.publickey()
    pub_str = public_key.exportKey(format='PEM').decode('utf-8')
    priv_str = private_key.exportKey(format='PEM').decode('utf-8')

    with open (pub_fname, "w") as pub_file:
        with open (priv_fname, "w") as priv_file:
            priv_file.write(priv_str)
            pub_file.write(pub_str)
            return pub_str, priv_str


