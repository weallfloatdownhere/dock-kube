# ***<ins>Getting started.</ins>***

***This tutorial is going to go through the whole process from having a standard 6x Vanilla Ubuntu nodes to a working RKE & ArgoCD powered on-premise Kubernetes cluster.***

## ***<ins>Dependencies.</ins>***

***Minimum requirements***

![Capture](https://user-images.githubusercontent.com/102635491/164043817-7143bfae-a8a8-47ed-9ac5-23f74c86c82d.PNG)

***1. Install curl, git and make***

```bash
# Ubuntu >= 18.04
$ sudo apt -y install curl git make
# Archlinux
$ sudo pacman -S curl git make --needed --no-confirm
```

[***2. Install Docker***](https://docs.docker.com/engine/install/)

```bash
# Ubuntu >= 18.04
$ sudo apt -y install docker.io
# Archlinux
$ sudo pacman -S docker --needed --no-confirm
```

***3. Enable docker and containerd services***

```bash
# Enabled the docker service.
$ sudo systemctl enable docker --now
# Enabled the containerd service.
$ sudo systemctl enable containerd --now
# Ensure docker group exists.
$ sudo groupadd docker
# Add sudo user to the docker group.
$ sudo usermod -aG docker $USER
# Reboot your system.
$ sudo reboot
```
  
*`Optional: pre-pulling the images.`*
  
```bash
# Kubernetes installer image.
$ docker pull silentreatmen7/rgm-rke:latest
# ArgoCD installer image.
$ docker pull silentreatmen7/rgm-argocd:latest
# Devops toolkit installer image.
$ docker pull silentreatmen7/rgm-dtoolkit:latest
```

---

# ***<ins>Configuration</ins>***

***Minimum required configuration. <ins>**Please note that all the subsequents settings (nuget, npm feeds, argocd etc..) must be added to the `config.yml` file.**</ins>***

```yaml
# config.yml

cluster:
  domain: example.com
  environment: dev
  user: 'admin'
  password: 'admin'
  ingress_controller: 'nginx'
  etcd_snapshots: True

  nodes:
    - address: 13.14.33.44
      hostname: rkeqa-master-0

    - address: 13.14.34.45
      hostname: rkeqa-master-1

    - address: 13.14.35.46
      hostname: rkeqa-master-2

    - address: 13.14.36.47
      hostname: rkeqa-worker-0

    - address: 13.14.37.48
      hostname: rkeqa-worker-1

    - address: 13.14.38.49
      hostname: rkeqa-worker-2

networking:
  default_network_cni_enabled: True
  default_ingress_ctrl_enabled: True
```

***<ins>Nuget feeds configuration.</ins>***

```yaml
nuget:
  feed_username: 0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a
  feed_token: 0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a
  feed_url: https://pkgs.dev.azure.com/[ORGANIZATION]/Repository/_packaging/[NUGETFEED]/nuget/v3/index.json
  # eg: https://pkgs.dev.azure.com/groupexamle/Repository/_packaging/NugetExample/nuget/v3/index.json
```

***<ins>Npm feeds configuration.</ins>***

```yaml
npm:
  feed_username: 0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a
  feed_token: 0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a
```

***<ins>Repositories credentials.</ins>***

```yaml
credentials:
  git_repositories: []
  container_registries:
    - secret_name: acr-secret-name
      url: azureacr.azurecr.io
      username: username
      password: 0a0a0a0a0a0a0a0a0a0a0a+B1b1b1b1=
```

---

# ***<ins>Kubernetes installation.</ins>***

*This step is assuming that the current directory is containing a valid `config.yml` file like the examples above.*

```bash
# Install Kubernetes.
docker run -it --rm --mount type=bind,source=$(pwd),target=/data silentreatmen7/rgm-rke install
# Uninstall Kubernetes.
docker run -it --rm --mount type=bind,source=$(pwd),target=/data silentreatmen7/rgm-rke remove
```

*If the installation is successful, the current directory should now contains additionals files.*

```text
$ ls -al
drwxrwxrw- 2 user user   4096 May  8 14:03 .
drwxrwxr-x 4 user user   4096 May  7 08:23 ..
-rw------- 1 root root 123195 May  8 14:04 cluster.rkestate
-rw-rw-rw- 1 root root    639 May  7 10:45 cluster.yml
-rw-rw-r-- 1 user user   1032 May  7 23:04 config.yml
-rw------- 1 root root   3357 May  7 10:45 id_rsa
-rw-r--r-- 1 root root    726 May  7 10:45 id_rsa.pub
-rw-rw-rw- 1 root root   5533 May  8 14:03 kube_config_cluster.yml
```

# ***<ins>ArgoCD Installation.</ins>***

***Deploy ArgoCD to the cluster.***

```bash
# eg: export TARGETENV=dev
export TARGETENV=<environment>
# Install ArgoCD into the Kubernetes cluster.
make install
# Remove ArgoCD from the Kubernetes cluster.
make remove
```

***Creating a new ArgoCD cluster secret.***

*https://github.com/argoproj/argo-cd/issues/8107*

*https://argo-cd.readthedocs.io/en/stable/operator-manual/declarative-setup/#clusters*

![Capture](https://user-images.githubusercontent.com/102635491/167630255-f1d1bbb9-b6ab-4e80-a27f-f8d29f8aa2f1.PNG)

---

# ***<ins>Common issues.</ins>***

## ***Rancher.***

*If a rancher namespace is stuck at `Terminating`, you can force the removing of such namespace with the commands below.*

```bash
$ kubectl patch namespace <target-namespace> -p '{"metadata":{"finalizers":[]}}' --type='merge' -n <target-namespace>
$ kubectl delete namespace <target-namespace> --grace-period=0 --force
# eg: $ kubectl patch namespace cattle-system -p '{"metadata":{"finalizers":[]}}' --type='merge' -n cattle-system
#     $ kubectl delete namespace cattle-system --grace-period=0 --force
```

*If the problem persist, (Which is particularly common with the namespace `cattle-monitoring-system` for example), you will have to install a tool called `k8sdel`. Execute the command below to install `k8sdel`.*

```bash
mkdir -p $HOME/.local/bin && curl -L --silent https://raw.githubusercontent.com/weallfloatdownhere/k8sdelns/master/k8sdelns -o $HOME/.local/bin/k8sdel && chmod +x $HOME/.local/bin/k8sdel
```

*<ins>You can now use `k8sdel` to force the removing of target namespace.</ins>*

```bash
k8sdel <namespace-to-remove>
# eg: k8sdel cattle-monitoring-system
```

---

# ***<ins>Additionals guide and tutorials.</ins>***

## ***<ins>ArgoCD</ins>***

[***Great basic ArgoCD repository example from Github.***](https://github.com/argoproj/argoproj-deployments/tree/master/argocd)

[***All ArgoCD manifests for Kustomize patch references.***](https://github.com/argoproj/argo-cd/tree/master/manifests)

---

## ***<ins>Manifests guidelines examples.</ins>***

<details>

***<summary>Helm umbrella example.</summary>***

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

</details>

<details>

***<summary>Applicationset Helm.</summary>***

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

</details>

<details>

***<summary>Applicationset Kustomize.</summary>***

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
              repoURL: https://github.com/weallfloatdownhere/argocd.git
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

</details>

---

</br>