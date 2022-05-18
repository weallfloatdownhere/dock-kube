# *Manifests guidelines examples.*

## ***<summary>Helm umbrella example.</summary>***

```yaml
apiVersion: v2
name: sealed-secrets
description: A Helm chart for sealed-secrets
type: application
version: 0.1.0
appVersion: "1.0"
dependencies:
  - name: sealed-secrets
    version: "2.1.6"
    repository: https://bitnami-labs.github.io/sealed-secrets
```

## ***<summary>Applicationset Helm.</summary>***

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: cluster-addons-helms
spec:
  generators:
    - matrix:
        generators:
          - git:
              repoURL: https://github.com/user/argocd.git
              revision: HEAD
              directories:
                - path: charts/**/*
          - list:
              elements:
              - cluster: my-cluster
                address: https://kubernetes.default.svc
                values:
                  env: dev
  template:
    metadata:
      name: '{{path.basename}}'
    spec:
      project: default
      source:
        chart: '{{path.basename}}'
        repoURL: https://github.com/user/argocd.git
        path: '{{path}}'
        helm:
          releaseName: '{{path.basename}}'
          ignoreMissingValueFiles: true
          valueFiles:
          - '{{path}}/values-{{values.env}}.yaml'
      destination:
        server: '{{address}}'
        namespace: cluster-addons
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
        syncOptions:
        - CreateNamespace=true
```

## ***<summary>Applicationset Kustomize.</summary>***

```yaml
---
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: cluster-addons-kustomize
spec:
  generators:
    - matrix:
        generators:
          - git:
              repoURL: https://github.com/username/argocd.git
              revision: HEAD
              directories:
                - path: kustomize/*
          - list:
              elements:
              - cluster: my-cluster
                address: https://kubernetes.default.svc
                values:
                  env: dev
  template:
    metadata:
      name: '{{path.basename}}'
    spec:
      project: default
      source:
        repoURL: https://github.com/argoproj/applicationset.git
        targetRevision: HEAD
        path: '{{path}}'
      destination:
        server: '{{address}}'
        namespace: cluster-addons
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
        syncOptions:
        - CreateNamespace=true
```

## ***Creating a new ArgoCD cluster secret.***

*https://github.com/argoproj/argo-cd/issues/8107*

*https://argo-cd.readthedocs.io/en/stable/operator-manual/declarative-setup/#clusters*

![Capture](https://user-images.githubusercontent.com/102635491/167630255-f1d1bbb9-b6ab-4e80-a27f-f8d29f8aa2f1.PNG)