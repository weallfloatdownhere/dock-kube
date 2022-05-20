## *If a namespace is stuck at `Terminating`, you can force the removing of such namespace with the commands below.*

```bash
$ kubectl patch namespace <target-namespace> -p '{"metadata":{"finalizers":[]}}' --type='merge' -n <target-namespace>
$ kubectl delete namespace <target-namespace> --grace-period=0 --force
# eg: $ kubectl patch namespace cattle-system -p '{"metadata":{"finalizers":[]}}' --type='merge' -n cattle-system
#     $ kubectl delete namespace cattle-system --grace-period=0 --force
```

## *If the problem persist, (Which is particularly common with the namespace `cattle-monitoring-system` for instance), you will have to use a script called `k8sdel.sh`. [The script can be found here]().*

```bash
mkdir -p $HOME/.local/bin && curl -L --silent https://raw.githubusercontent.com/weallfloatdownhere/k8sdelns/master/k8sdelns -o $HOME/.local/bin/k8sdel && chmod +x $HOME/.local/bin/k8sdel
```

## *<ins>You can now use `k8sdel.sh` to force the removing of a namespace with the command below.</ins>*

```bash
./k8sdel.sh <namespace-to-remove>
# eg: k8sdel cattle-monitoring-system
```