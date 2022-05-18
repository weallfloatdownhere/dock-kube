# ***<ins>Dock-kube.</ins>***

## *Containers Orchestration + Gitops opinionated installer.*

---

# *<ins>Usage.</ins>*

## Configuration

| value                                 |            description             |              default |   type | required |
| ------------------------------------- | :--------------------------------: | -------------------: | -----: | -------: |
| cluster.domain                        |        organization domain         |          local.local | string |      yes |
| cluster.environment                   |     target cluster environment     |                  dev | string |      yes |
| cluster.user                          |          nodes sudo user           |                admin | string |      yes |
| cluster.password                      |     nodes user's sudo password     |                admin | string |      yes |
| cluster.nodes                         |    list of nodes in the cluster    |                   [] |   list |      yes |
| cluster.nodes.address                 |          node ip address           |                 None | string |      yes |
| cluster.nodes.hostname                |           node hostname            |              cluster | string |      yes |
| cluster.addons                        |        dictionary of addons        |                   {} |   dict |       no |
| cluster.addons.etcd_snapshots.enabled |      enabling etcd snapshots       |                False |   bool |       no |
| cluster.addons.argocd.enabled         |    enabling ArgoCD installation    |                False |   bool |       no |
| cluster.addons.argocd.flavor          | specify ArgoCD installation flavor |              vanilla | string |       no |
| networking.enable_default             |      use default network cni       |                False |   bool |       no |
| networking.custom_network_cni         |      custom network cni name       |                 None | string |       no |
| ingress.enable_default                |   use default ingress controller   |                False |   bool |       no |
| ingress.custom_ingress_controller     |   custom ingress controller name   |                nginx | string |       no |
| docker_socket_path                    |         docker daemon path         | /var/run/docker.sock | string |       no |
| workspace_directory                   | output files destination directory |            $HOME/rke | string |       no |
