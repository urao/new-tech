## Steps to deploy minikube and add-ons 

1. Bring up 1 Centos 7.6 (1810) Servers and make sure internet connectivity is available
2. Update DNS entires in `/etc/resolv.conf` file
3. Disable firewall and system settings
```
sudo systemctl stop firewalld
sudo systemctl disable firewalld
sudo systemctl mask --now firewalld
swapoff -a
sed -i.bak -r 's/(.+ swap .+)/#\1/' /etc/fstab
setenforce 0
sed -i 's/^SELINUX=enforcing$/SELINUX=permissive/' /etc/selinux/config
```
4. Run below steps to deploy kubectl and docker services
```
cat <<EOF > /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
EOF
```
```
sudo yum install -y kubectl
sudo yum install -y yum-utils device-mapper-persistent-data lvm2
sudo yum-config-manager     --add-repo     https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install -y docker-ce-18.03.0.ce-1.el7.centos containerd.io
sudo systemctl enable docker && sudo systemctl start docker
sudo docker version
```
5. Run below steps to install minikube on the baremetal server not as a virtual machine
```
curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 && chmod +x minikube
mv minikube /usr/local/bin/
minikube start --vm-driver=none --apiserver-ips <IP_ADDRESS> apiserver-name 5a1s4-node2 --extra-config=kubelet.resolv-conf=/etc/resolv.conf
sudo mv /root/.kube /root/.minikube $HOME
sudo chown -R $USER $HOME/.kube $HOME/.minikube
```
6. Check all the pods in kube-system are UP and RUNNING expect coredns(or kube-dns)
```
kubectl get pods -n kube-system -o wide
```
7. Deploy calico for the pod networking
```
kubectl apply -f https://docs.projectcalico.org/v3.9/manifests/calico.yaml
```
8. Deploy below add-ons, k8s dashboard and weave scope
```
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v1.10.1/src/deploy/recommended/kubernetes-dashboard.yaml
kubectl apply -f "https://cloud.weave.works/k8s/scope.yaml?k8s-version=$(kubectl version | base64 | tr -d '\n')"
```
7. Deploy sample ngnix app and verify its running
```
kubectl apply -f examples/pod.yaml
kubectl get pods
```

## References
[Install](https://kubernetes.io/)
