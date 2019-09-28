SHELL := /bin/bash

# **** INPUT VARIABLES ***** #
CLUSTER_NAME ?= $(shell cat /etc/hostname 2>/dev/null || echo $$(hostname)) 
API_SERVER_IP ?= $(shell ip -4 route get 8.8.8.8 | awk {'print $7'} | tr -d '\n')
K8S_VERSION ?= 1.16
ISTIO_VERSION ?= 1.2.6

OS_TYPE_CENTOS := $(shell command -v yum;)
OS_TYPE_UBUNTU := $(shell command -v apt-get;)

# Setup the node with pre-sets to install required packages
.PHONY: bootstrap
bootstrap:
	@# Setup the node with pre-sets to install required packages
	@echo ""
	@echo "BOOTSTRAPPING THE NODE:"
	@echo ""

ifdef OS_TYPE_CENTOS
	sudo systemctl stop firewalld
	sudo systemctl disable firewalld
	sudo systemctl mask --now firewalld
	swapoff -a
	sed -i.bak -r 's/(.+ swap .+)/#\1/' /etc/fstab
	setenforce 0
	sed -i 's/^SELINUX=enforcing$/SELINUX=permissive/' /etc/selinux/config
endif

ifdef OS_TYPE_UBUNTU
endif

# Install minikube 
.PHONY: minikube
minikube: bootstrap
	@# Create kubernetes cluster with minikube
	@echo ""
	@echo "CREATING KUBERNETES CLUSTER WITH MINIKUBE:"
	@echo ""
ifdef OS_TYPE_CENTOS
	echo "[kubernetes]" > /etc/yum.repos.d/kubernetes.repo
	echo "name=Kubernetes" >> /etc/yum.repos.d/kubernetes.repo
	echo "baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64" >> /etc/yum.repos.d/kubernetes.repo
	echo "enabled=1" >> /etc/yum.repos.d/kubernetes.repo
	echo "gpgcheck=1" >> /etc/yum.repos.d/kubernetes.repo
	echo "repo_gpgcheck=1" >> /etc/yum.repos.d/kubernetes.repo
	echo "gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg" >> /etc/yum.repos.d/kubernetes.repo

	sudo yum install -y kubectl
	sudo yum install -y yum-utils device-mapper-persistent-data lvm2
	sudo yum-config-manager     --add-repo     https://download.docker.com/linux/centos/docker-ce.repo
	sudo yum install -y docker-ce-18.03.0.ce-1.el7.centos containerd.io
	sudo systemctl enable docker && sudo systemctl start docker
	sudo docker version

	curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 && chmod +x minikube
	mv minikube /usr/local/bin/
	minikube start --vm-driver=none --apiserver-ips $(API_SERVER_IP) apiserver-name $(CLUSTER_NAME) --extra-config=kubelet.resolv-conf=/etc/resolv.conf
	sudo mv /root/.kube /root/.minikube $HOME
	sudo chown -R $USER $HOME/.kube $HOME/.minikube
endif

# Install calico 
.PHONY: calico
calico: bootstrap minikube
	@# Deploy calico as cni
	@echo ""
	@echo "DEPLOY CALICO AS CNI:"
	@echo ""
	kubectl apply -f https://docs.projectcalico.org/v3.9/manifests/calico.yaml

# Install weave scope 
.PHONY: weave
weave: bootstrap minikube
	@# Deploy weave scope
	@echo ""
	@echo "DEPLOY WEAVE SCOPE:"
	@echo ""
	kubectl apply -f "https://cloud.weave.works/k8s/scope.yaml?k8s-version=$(kubectl version | base64 | tr -d '\n')"

# Default Target
.PHONY: usage
usage:
	@ printf "Usage: make [target]\n\nAvailable Targets:\n\n`cat Makefile | grep "^[A-z\%\-]*:" | awk '{print $$1}' | sed "s/\(.*-test\)-%:/\1[3306,4306]/g" | sed "s/://g" | sed "s/%/[1-3]/g"`\n\n"

.DEFAULT_GOAL := usage
