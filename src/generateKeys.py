from Crypto.PublicKey import RSA

private_key = RSA.generate(1024)
public_key = private_key.publickey()
print( private_key.exportKey(format='PEM'))
print( public_key.exportKey(format='PEM'))


with open ("private.pem", "w") as prv_file:
    prv_file.write(private_key.exportKey(format='PEM'))

with open ("public.pem", "w") as pub_file:
    pub_file.write(public_key.exportKey(format='PEM'))
