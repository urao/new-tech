```
Istio Mixer provides a generic intermediation layer between app code and infrastructure backends. 
Its design moves policy decisions out of the app layer and into configuration instead, under 
operator control. Instead of having app code integrate with specific backends, the app code 
instead does a fairly simple integration with Mixer, and Mixer takes responsibility for 
interfacing with the backend systems.
Some built-in adapters include denier, prometheus, memquota, and stackdriver.
```

1. Run below commands to deploy denier adapter 
```
kubectl apply -f enforce-denier-policy.yaml
Try to open the productpage on browser and see error page
```
