
## Import image using ctr command
```
 ctr -n=k8s.io image import ric-rappn-rsslaa.tar
 ctr -n=k8s.io image import ric-xapp-kpm-collector.tar
 ctr -n=k8s.io image import ric-xapp-rsslaa-ccc.tar
 ctr -n=k8s.io image import ricapiserver.tar
 ctr -n=k8s.io image import sdl-redis.tar
```

## Check max pods can be deployed in a k8s cluster
```
kubectl describe node <node_name> | grep -i capacity -A 13
```

## Tag a container image using `ctr` command
```
ctr --namespace=k8s.io image tag fiveg.azurecr.io/fiveg/ric-xapp-rsslaa-ccc:bell-canada-0a1c22fc7a1 \
        svl-artifactory.juniper.net/fiveg/ric-xapp-rsslaa-ccc:bell-canada-0a1c22fc7a1
```

## Tag a container image using `podman` command
```
podman image tag enterprise-hub.juniper.net/ric-container-prod/hostpath-provisioner svl-artifactory.juniper.net/atom-docker/fiveg/hostpath-provisioner:latest
```

## `crictl` commands
```
crictl image ls | grep ccc
crictl ps | grep xappmgr
crictl exec -it 215df184d6908 bash
```
