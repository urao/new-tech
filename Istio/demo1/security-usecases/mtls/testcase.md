```
TLS (Transport Layer Security) offers encryption for applications when communicating over a network.
TLS requires a CA (Certificate Authority) to issue a digital certificate to a service. 
The certificate is handed over the consumer of the service to validate with the CA. 
mTLS is an extension of this concept where both provider and consumer of a service must produce 
their own certs, which are mutually validated. This is considered to be the most secure way to
deploy microservices today. 
```
1. Create a pod, called sleep in default namespace and check the connectivity to backend, reviews page
```
kubectl apply -f $HOME/istio-1.2.6/samples/sleep/sleep.yaml
kubectl exec $(kubectl get pod -l app=sleep -n default -o jsonpath={.items..metadata.name}) \
                -n default -- curl http://reviews.default:9080/reviews/1
kubectl exec $(kubectl get pod -l app=sleep -n default -o jsonpath={.items..metadata.name}) \
                -n default -- curl http://reviews.default:9080/reviews/2
```
2. Create a pod, called sleep in non-default namespace and check the connectivity to backend, reviews page
```
kubectl create ns securitydemo
kubectl apply -f sleep-securitydemo.yaml
kubectl exec $(kubectl get pod -l app=sleep -n default -o jsonpath={.items..metadata.name}) \
                -n default -- curl http://reviews.default:9080/reviews/1
```

Note. Check Kiali UI -> Istio Config section and see if there are any warnings coming from validation system.

PS: If you are running kubernetes v1.16, sleep.yaml will not work, run the below command and re-run
```
kubectl convert -f ./sleep.yaml --output-version apps/v1 > <file_name>.yaml
```
