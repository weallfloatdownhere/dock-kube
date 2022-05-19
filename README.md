# ***<ins>Devops the Gitops way walkthrough.</ins>***

***Dock-kube - Containers Orchestration + Gitops opinionated installer facilitating the process of RKE & ArgoCD powered on-premise Kubernetes cluster installations.***

---

![Animation](https://user-images.githubusercontent.com/102635491/169345280-b262c112-b55b-4a07-9600-e31e0fbfa097.gif)

# *<ins>Requirements.</ins>*

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
$ docker pull silentreatmen7/dock-kube:latest
```

---

</br>

# *<ins>Usage.</ins>*

**Please note that this step is assuming that there is a valid `config.yml` file in the current directory.**

```bash
$ docker run -it -v "$(pwd)/:/root/rke/" silentreatmen7/dock-kube:latest [PARAMETERS]
```

# *<ins>Examples.</ins>*

**Install Kubernetes `ONLY` into the cluster.**

```bash
$ docker run -it -v "$(pwd)/:/root/rke/" silentreatmen7/dock-kube:latest -c rke install
```

**Install Kubernetes and ArgoCD Gitops engine.**

```bash
$ docker run -it -v "$(pwd)/:/root/rke/" silentreatmen7/dock-kube:latest -c rke -c argocd install
```

---

# *<ins>Parameters.</ins>*

| parameter | description                    | cmd                | default | type   | required | choices          | dependencies         |
| :-------- | :----------------------------- | :----------------- | :------ | :----- | :------- | :--------------- | :------------------- |
| task      | Command execution mode         |                    | install | string | yes      | {install,remove} | {install,remove}     |
| rke       | Install Kubernetes on nodes    | -c,    --component | rke     | string |          |                  |                      |
| argocd    | Deploy ArgoCD into the cluster | -c,    --component | argocd  | string |          |                  | Kubernetes installed |

---

# *<ins>Configuration file values.</ins>*

| value                                 | description                                                | default              | type   | required |
| :------------------------------------ | :--------------------------------------------------------- | :------------------- | :----- | :------- |
| cluster.domain                        | organization domain                                        | local.local          | string | yes      |
| cluster.environment                   | target cluster environment                                 | dev                  | string | yes      |
| cluster.user                          | nodes sudo user                                            | admin                | string | yes      |
| cluster.password                      | nodes user's sudo password                                 | admin                | string | yes      |
| cluster.nodes                         | list of nodes in the cluster                               | []                   | list   | yes      |
| cluster.nodes.address                 | node ip address                                            | None                 | string | yes      |
| cluster.nodes.hostname                | node hostname                                              | cluster              | string | yes      |
| cluster.addons                        | dictionary of addons                                       | {}                   | dict   | no       |
| cluster.addons.etcd_snapshots.enabled | enabling etcd snapshots                                    | False                | bool   | no       |
| cluster.addons.argocd.enabled         | enabling ArgoCD installation                               | False                | bool   | no       |
| cluster.addons.argocd.version         | ArgoCD version to deploy                                   | 4.5.12               | string | no       |
| cluster.addons.sealed_secrets.enabled | enabling Sealed secrets operator (recommended with argocd) | False                | bool   | no       |
| cluster.addons.sealed_secrets.version | Sealed secrets operator version to deploy                  | 1.16.1               | string | no       |
| networking.enable_default             | use default network cni                                    | False                | bool   | no       |
| networking.custom_network_cni         | custom network cni name                                    | None                 | string | no       |
| ingress.enable_default                | use default ingress controller                             | False                | bool   | no       |
| ingress.custom_ingress_controller     | custom ingress controller name                             | nginx                | string | no       |
| docker_socket_path                    | docker daemon path                                         | /var/run/docker.sock | string | no       |
| workspace_directory                   | output files destination directory                         | $HOME/rke            | string | no       |

</br>

# *<ins>Addons.</ins>*

- [**ArgoCD**](https://github.com/argoproj/argo-cd)

  ***Configuration***

  *In order to overwrite the default values, create a file name `argocd-values.yaml` in your workspace directory.*
  *If `argocd-values.yaml` is not present, the [default settings are applied].(ansible/roles/argocd/files/default-values.yml)*
  *You can also find a full configuration examples [HERE].(ansible/roles/argocd/files/full-sample-values.yml)*

- [**Sealed-secrets operator**](https://github.com/bitnami-labs/sealed-secrets)

</br>

# *<ins>Samples.</ins>*

- [**Full configuration file example.**](docs/samples/configurations/config_full.yml)

- [**Minimal single node configuration.**](docs/samples/configurations/config_minimal.yml)

- [**Basic multiple nodes configuration.**](docs/samples/configurations/config_multiple_nodes.yml)

- [**Basic single node configuration.**](docs/samples/configurations/config_single_node.yml)

</br>

---

</br>

# *<ins>Examples.</ins>*

## Docker version *`(Recommended)`*

**Install Kubernetes `ONLY` into the cluster.**

```bash
$ docker run -it -v "$(pwd)/:/root/rke/" silentreatmen7/dock-kube:latest -c rke install
```

**Install Kubernetes and ArgoCD Gitops engine.**

```bash
$ docker run -it -v "$(pwd)/:/root/rke/" silentreatmen7/dock-kube:latest -c rke -c argocd install
```

</br>

## Client version

<ins>*Currently in beta test.*</ins>

**Install Kubernetes `ONLY` into the cluster.**

```bash
$ python3 entrypoint.py -c rke install
```

**Install Kubernetes and ArgoCD vanilla flavored into the cluster.**

```bash
$ python3 entrypoint.py -c rke -c argocd install
```
