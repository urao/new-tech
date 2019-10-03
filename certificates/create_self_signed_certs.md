## Steps to generate self-signed certificate

1. Generate private key and certificate pair
`openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout private.key -out keypair.crt
`
