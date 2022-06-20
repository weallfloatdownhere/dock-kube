# ***<ins>Devops the Gitops way walkthrough.</ins>***

***Dock-kube - Containers Orchestration + Gitops opinionated installer facilitating the process of RKE.***

---

![Animation](https://user-images.githubusercontent.com/102635491/169345280-b262c112-b55b-4a07-9600-e31e0fbfa097.gif)

# *<ins>Requirements.</ins>*

## ***Minimum requirements***

![Capture](https://user-images.githubusercontent.com/102635491/164043817-7143bfae-a8a8-47ed-9ac5-23f74c86c82d.PNG)

***1. Update your system.***

```bash
# Ubuntu >= 18.04
$ sudo apt -y update

# Archlinux
$ sudo pacman -Syyu

# Centos >= 7
$ sudo yum -y update
```

***2. Install curl, git and make***

```bash
# Ubuntu >= 18.04
$ sudo apt -y install curl git make

# Archlinux
$ sudo pacman -S curl git make --needed --no-confirm
```

[***3. Install Docker***](https://docs.docker.com/engine/install/)

```bash
# Ubuntu >= 18.04
$ sudo apt -y install docker.io

# Archlinux
$ sudo pacman -S docker --needed --no-confirm
```

***4. Enable docker and containerd services***

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

# *<ins>Usage.</ins>*

**Please note that this step is assuming that there is a valid [config.yml](#*minimal-configuration-file-example*) file in the current directory.**

- **How to use.**

  ```bash
  $ docker run -it -v "$(pwd)/:/root/rke/" silentreatmen7/dock-kube:latest [TASK]
  ```

- **Install Kubernetes.**
]
  ```bash
  $ docker run -it -v "$(pwd)/:/root/rke/" silentreatmen7/dock-kube:latest install
  ```

- **Uninstall everything.**

  ```bash
  $ docker run -it -v "$(pwd)/:/root/rke/" silentreatmen7/dock-kube:latest remove
  ```

---

# *<ins>Parameters.</ins>*

| parameter      | description                                     | cmd  | default | type   | required | choices          | dependencies                                                                                                 |
| :------------- | :---------------------------------------------- | :--- | :------ | :----- | :------- | :--------------- | :---------------------------------------------------------------------------------------------------------   |
| task           | Command execution mode                          |      | install | string | yes      | {install,remove} | [Minimum requirements](#minimum-requirements) and [A config.yml file](#*minimal-configuration-file-example*) |

---

# *<ins>Configuration file values.</ins>*

| value                                 | description                          | default              | type   | required                                                                                       |
| :------------------------------------ | :----------------------------------- | :------------------- | :----- | :--------------------------------------------------------------------------------------------- |
| cluster.domain                        | organization domain                  | local.local          | string | yes                                                                                            |
| cluster.environment                   | target cluster environment           | dev                  | string | yes                                                                                            |
| cluster.user                          | nodes sudo user                      | admin                | string | yes                                                                                            |
| cluster.password                      | nodes user's sudo password           | admin                | string | yes                                                                                            |
| cluster.nodes                         | list of nodes in the cluster         | []                   | list   | yes                                                                                            |
| cluster.nodes.address                 | node ip address                      | None                 | string | yes                                                                                            |
| cluster.nodes.hostname                | node hostname                        | cluster              | string | [see the nodes naming convention](#nodes-naming-convention-and-nodes-roles-detection-mechanic) |
| cluster.addons                        | dictionary of addons                 | {}                   | dict   | no                                                                                             |
| cluster.addons.etcd_snapshots.enabled | enabling Etcd snapshots              | False                | bool   | no                                                                                             |
| docker_socket_path                    | docker daemon path                   | /var/run/docker.sock | string | no                                                                                             |

---

# Nodes naming convention and nodes roles detection mechanic

***You have probably noticed that you didnt assigned any roles to the nodes. This is because there is a roles detection mechanism inside the installer.***  

***The detection routine result is based on certains patterns in found in the value `cluster.nodes.hostname` of each nodes. Below are the criterias that has to be met for a node to dynamically get roles attributed to it.*** 

***<ins>Its also important to know that, if your [config.yml](#*minimal-configuration-file-example*) file is only `containing three(3) nodes or less`, they automatically get `all possible roles attributed` to them.</ins>***


**If the `cluster.nodes.hostname` is containing either of these strings/patterns, its a `controlplane + etcd`**

```bash
master  # eg: rke-master-1
control # eg: controller1
ctrl    # eg: ctrlplane-2
manage  # eg: node-manager-1
admin   # eg: kube-admin-3
```

**If the `cluster.nodes.hostname` is containing either of these strings/patterns, its a `worker`**

```bash
work    # eg: rke-worker-2
slave   # eg: kube-slave1
runner  # eg: node-runner-1
agent   # agent3
```

---

## *Minimal configuration file example*

<details>

<summary><font size=3>config.yml</font></summary>

  ```yaml
 ---
  cluster:
    # Cluster name.
    name: 'cluster-lab'
    # Organization domain name.
    domain: local.local
    # Target environement.
    environment: dev
    # Remote nodes sudo user.
    user: admin
    # Remote nodes sudo user password.
    password: admin
    # List of nodes to include in the cluster.
    nodes:
      - address: 10.0.0.175
        hostname: node1
  ```

</details>

---

## *Full configuration file example*

<details>

<summary><font size=3>config.yml</font></summary>

  ```yaml
  cluster:
    name: 'cluster-qa'
    environment: 'qa'
    domain: organization.com
    user: 'sudo-user'
    password: 'sudo-user-password'
    nodes:
      - address: 10.10.10.11
        hostname: rkeqa-master-0
      - address: 10.10.10.12
        hostname: rkeqa-master-1
      - address: 10.10.10.13
        hostname: rkeqa-master-2
      - address: 10.10.10.14
        hostname: rkeqa-worker-0
      - address: 10.10.10.15
        hostname: rkeqa-worker-1
      - address: 10.10.10.16
        hostname: rkeqa-worker-2
    addons:
      etcd_snapshots:
        enabled: false
        creation: '12h'
        retention: '24h'
    ingress:
      enabled: false
      controller: nginx
      network_mode: hostPort

  docker_socket_path: /var/run/docker.sock
  ```

</details>

---