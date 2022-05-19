#!/bin/bash
kubectl apply -f namespace.yaml

# Install ArgoCD
helm repo add argo https://argoproj.github.io/argo-helm
helm install argocd argo/argo-cd --version 3.27.1 -f argocd/values.yaml -n shared-services --atomic
# Once generated apply sealed secret with the repository credentials
# kubectl apply -f chillfs-sealed-secret.yaml -n shared-services

Install Sealed-Secrets
helm repo add sealed-secrets https://bitnami-labs.github.io/sealed-secrets
helm install sealed-secrets sealed-secrets/sealed-secrets --version 1.16.1 -f kubeseal/values.yaml -n shared-services --atomic
kubectl get secret --field-selector type=kubernetes.io/tls -o=jsonpath="{.items[*].data.tls\.crt}" -n shared-services | base64 -d >> mycert.pem

Install kubeseal CLI into /usr/local/bin/
GOOS=$(go env GOOS)
GOARCH=$(go env GOARCH)

case $GOOS in 
    'linux')
    wget https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.16.0/kubeseal-$GOOS-$GOARCH
    sudo install -m 755 kubeseal-$GOOS-$GOARCH /usr/local/bin/kubeseal
      ;;
    'darwin')
      echo 'GOOS:' $GOOS
      brew install kubeseal
      ;;
esac
