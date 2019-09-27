## Steps to deploy istio 

1. Run below steps to download istio package
```
curl -L https://git.io/getLatestIstio | ISTIO_VERSION=1.2.6 sh -
export PATH="$PATH:/root/istio-1.2.6/bin"
cp istio-1.2.6/bin/istioctl /usr/local/bin
```
2. Run below steps to install istio with auth enabled
```
cd istio-1.2.6/
for i in install/kubernetes/helm/istio-init/files/crd*yaml; do kubectl apply -f $i; done
kubectl apply -f install/kubernetes/istio-demo-auth.yaml
kubectl get pods,svc -n istio-system -o wide
```
3. Verify that the Grafana, Prometheus, Kiali and Jaeger add-ons were installed successfully. 
All add-ons are installed into the istio-system namespace
```
kubectl get pods -n istio-system
kubectl get services -n istio-system
```
4. Run below steps to install bookinfo app in default namespace and gateway as BMS IP
```
A Gateway allows Istio features such as monitoring and route rules to be applied to traffic entering the cluster.
```
```
kubectl label namespace default istio-injection=enabled
kubectl apply -f samples/bookinfo/platform/kube/bookinfo.yaml
kubectl get pods
export INGRESS_PORT=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="http2")].nodePort}')
export SECURE_INGRESS_PORT=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="https")].nodePort}')
export INGRESS_HOST=$(minikube ip)
kubectl apply -f samples/bookinfo/networking/bookinfo-gateway.yaml
kubectl get gateway
```
5. Verify bookinfo productpage is accessible
```
export GATEWAY_URL=$INGRESS_HOST:$INGRESS_PORT
curl -s http://${GATEWAY_URL}/productpage | grep -o "<title>.*</title>"
curl -v ${GATEWAY_URL}/productpage -s -o /dev/null -w "%{http_code}\n" return 200 OK
kubectl exec -it $(kubectl get pod -l app=ratings -o jsonpath='{.items[0].metadata.name}') -c ratings -- curl productpage:9080/productpage | grep -o "<title>.*</title>"
```
6. Generate traffic
```
for i in {1..100}; do sleep 0.2; curl http://<IP_ADDRESS>:<PORT>/productpage; done
```

## References
[Install](https://istio.io/)
