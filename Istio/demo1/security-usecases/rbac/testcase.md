```
Istio Authorization builds on Kubernetes Role-based Access Control (RBAC), which maps "subjects" (such as service accounts) to Roles.
```

1. Run below commands to add RBAC to productpage and other pages
```
kubectl apply -f rbac-on.yaml
Try to open the productpage on browser and see error page
```

2. Run below commands to add RBAC to other pages expect productpage 
```
kubectl apply -f rbac-productpage.yaml
Try to open the productpage on browser and see productpage
```

3. Run below commands to add RBAC to reviews pages expect productpage/details
```
kubectl apply -f rbac-details.yaml
Try to open the productpage on browser and see productpage and details page
```
