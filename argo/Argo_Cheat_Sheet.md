
#### Useful Argo commands
```
argo list -n argo
argo get @latest -n argo
argo delete my-wf
argo delete @latest
argo delete --all

kubectl get deployment -n argo-events --no-headers=true | awk '/group-1-/{print $1}' | xargs \
          kubectl delete -n argo-events deployment
kubectl get pods -n argo-events --no-headers=true | awk '/group-1-/{print $1}' | xargs \
          kubectl delete -n argo-events pod



```





## References
[Argo CLI](https://argoproj.github.io/argo-workflows/cli/argo/)
