#!/usr/bin/env bash
# Tested on Ubuntu 18.04 and k3s in AWS env

set -exu
EXITCODE=0

# check if the script is run by root
if (( $EUID !=0 )); then
    echo "Please run as root"
    exit 1
fi

swapoff -a
sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab
systemctl disable systemd-resolved.service
systemctl stop systemd-resolved.service
rm /etc/resolv.conf
echo "nameserver 8.8.8.8" >> /etc/resolv.conf

#check
ping -c 5 www.google.com
if (( $? -eq 0 )); then
    echo "DNS works"
else
    echo "DNS fails, check, exiting for now"
    exit 1
fi

apt-get update
apt-get install -y ntp unzip net-tools curl wget
apt-get purge -y lxd lxd-client
echo "server 169.254.169.123 prefer iburst minpoll 4 maxpoll 4" | tee --append /etc/ntp.conf
echo "server 0.pool.ntp.org iburst" | tee --append /etc/ntp.conf
systemctl enable ntp
systemctl restart ntp

#stop
systemctl stop ufw
systemctl disable ufw
iptables -F

#/etc/hosts
IFNAME=$1
HOSTNAME=$2
ADDRESS="$(ip -4 addr show $IFNAME | grep "inet" | head -1 |awk '{print $2}' | cut -d/ -f1)"
sed -e "s/^.*${HOSTNAME}.*/${ADDRESS} ${HOSTNAME} ${HOSTNAME}.local/" -i /etc/hosts

# remove existing entry
sed -e '/${HOSTNAME}/d' -i /etc/hosts

# Update /etc/hosts about other hosts
cat >> /etc/hosts <<EOF
 ${ADDRESS}  ${HOSTNAME} ${HOSTNAME}
EOF

hostnamectl set-hostname "${HOSTNAME}"

#docker
curl https://releases.rancher.com/install-docker/19.03.sh | sh
usermod -aG docker root
systemctl enable docker
systemctl restart docker

#iptables
echo "net.bridge.bridge-nf-call-iptables=1" | sudo tee -a /etc/sysctl.conf
sysctl -p

#k8s
curl -sfL https://get.k3s.io | sh -s - --docker - --write-kubeconfig-mode 644
mkdir -p $HOME/.kube
sudo cp -i /etc/rancher/k3s/k3s.yaml $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

#check k8s cluster printing output
kubectl cluster-info
echo ''
kubectl get nodes
echo ''
crictl ps

#install helm
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash
helm version
if (( $? -eq 0 )); then
    echo "HELM works!!"
else
    echo "HELM FAILS, check, exiting for now"
    exit 1
fi

#install argo
kubectl create namespace argo
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update
helm repo list
helm install argo argo/argo -n argo
kubectl get all -n argo
kubectl --namespace argo get services -o wide | grep argo-server
kubectl expose service -n argo argo-server --type NodePort --name argo-server-svc

#argo-events
kubectl create namespace argo-events
kubectl apply -f https://raw.githubusercontent.com/argoproj/argo-events/stable/manifests/install.yaml -n argo-events
kubectl apply -f https://raw.githubusercontent.com/argoproj/argo-events/master/examples/eventbus/native.yaml -n argo-events
kubectl get all -n argo-events

#install argo CLI tool
curl -sLO https://github.com/argoproj/argo/releases/download/v3.0.0-rc4/argo-linux-amd64.gz
gunzip argo-linux-amd64.gz
mv argo-linux-amd64 argo
mv argo /usr/local/bin/
chmod +x /usr/local/bin/argo
rm -rf argo-linux-amd64.gz

#Argo WEB-UI
echo "Accessing Argo-WeUI"
echo "curl http://<host_ip>:<node_port>/"

#Execute examples
echo "Execute examples"
echo "https://argoproj.github.io/argo-events/tutorials/01-introduction/"

#exiting the script
exit $EXITCODE
