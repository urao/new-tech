```
Enforce end-user ("origin") authentication for the productpage service, using JSON Web Tokens (JWT)
Using JWT authentication alongside mTLS (and not JWT by itself), because plaintext JWTs are not 
themselves encrypted, only signed. Forged or intercepted JWTs could compromise your service mesh. 
We're building on the mutual TLS authentication already configured for the default namespace
```
1. Run the below commands to enforce End-User JWT authentication
```
curl <IP_ADDRESS>:31380/productpage -s -o /dev/null -w "%{http_code}\n"   <=== 200 OK
kubectl apply -f jwt-auth-policy.yaml
curl <IP_ADDRESS>:31380/productpage -s -o /dev/null -w "%{http_code}\n"   <=== 401 OK
TOKEN=$(curl https://raw.githubusercontent.com/istio/istio/release-1.3/security/tools/jwt/samples/demo.jwt -s )
TOKEN=$(curl https://raw.githubusercontent.com/istio/istio/release-1.3/security/tools/jwt/samples/demo.jwt -s --expire 5)
curl --header "Authorization: Bearer $TOKEN" <IP_ADDRESS>:31380/productpage -s -o /dev/null -w "%{http_code}\n"  <=== 200OK
for i in `seq 1 10`; do curl --header "Authorization: Bearer $TOKEN" <IP_ADDRESS>:31380/productpage -s -o /dev/null -w "%{http_code}\n"; sleep 1; done
```
