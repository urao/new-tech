## Steps to generate self-signed certificate

1. Generate a Private Key and a CSRs, these CSRs can be used to request 
   SSL certificate from CA.
```
openssl req -nodes -newkey rsa:2048 -keyout private.key -out domain.csr
```
2. Below command to view the contents of a CSR
```
openssl req -text -noout -verify -in domain.csr
```

- Below steps to generate self-signed certificate

1. Generate private key and certificate pair using below command
```
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout private.key -out keypair.crt
```
2. Above command will prompt for DN(Distinguished Name) details, please enter and complete it
3. Generate self_signed cert using private key and certificate pair using below command
```
openssl x509 -signkey private.key -in keypair.crt -req -days 265 keypair.crt
```
4. If you want to create strong Diffie-Hellman group, which is used in negotiating PFS with clients
```
openssl dhparam -out dhparam.pem 4096
```
5. Below command to view the contents of a certificate (.crt)
```
openssl x509 -text -noout -in keypair.crt
```
6. Below command to verify that a certificate(.crt) was signed by CA cert (ca.crt)
```
openssl verify -verbose -CAfile ca.crt keypair.crt
```
7. Below command to verify a private key
```
openssl rsa -check -in private.key
```
8. Below command to verify if a private key matches a .crt and .csr
```
openssl rsa -noout -modulus -in private.key | openssl md5
openssl x509 -noout -modulus -in keypair.crt | openssl md5
openssl req -noout -modulus -in domain.csr | openssl md5
```

- Convert certificate formats
1. X509 certificates are ASCII PEM encoded. There are different certificate format which some applications
   prefer.
2. Convert PEM to DER
```
openssl x509 -in keypair.crt -outform der -out keypair.der
```
3. Convert DER to PEM
```
openssl x509 -inform der -in keypair.der -out keypair.der
```
