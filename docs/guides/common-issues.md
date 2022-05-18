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