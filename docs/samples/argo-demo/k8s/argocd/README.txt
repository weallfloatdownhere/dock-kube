To access ArgoCD server UI run the command:
kubectl port-forward svc/argocd-server -n shared-services 8080:443

The API server can then be accessed using the localhost:8080

Credentials: admin/argo-demo

Right after the deployment the application managed by ArgoCD will have 'Out of Sync' status. ArgoCD will synchronize application automatically within 3 minutes
