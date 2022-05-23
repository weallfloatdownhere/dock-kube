#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['stable'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: argocd_user
short_description: ArgoCD password setting.
version_added: "1.0"
description:
    - "Update target user password."
dependencies:
    - htpasswd: https://httpd.apache.org/docs/2.4/programs/htpasswd.html
    - kubectl: https://github.com/kubernetes/kubectl
options:
    username:
        description:
            - Target user to apply the configuration to.
        required: true
        type: str
    namespace:
        description:
            - Namespace containing target user to update.
        required: false
        type: str
        default: argocd
    kubeconfig:
        description:
            - Path to the kubeconfig file to use for CLI requests.
        required: false
        type: str
        default: /root/.kube/config
    password:
        description:
            - Password of the specified user.
        required: true
        type: str
author:
    - Anonymous
'''

EXAMPLES = '''
- name: "[ARGOCD] - Setup admin user password."
  argocd_user:
    username: admin
    password: password
'''

RETURN = '''
changed:
    description: Whether the module performed a change.
    type: bool
stdout:
    description: The output message that the sample module generates.
    type: str
'''

import sys, os, subprocess, json
from ansible.module_utils.basic import AnsibleModule
from pathlib import Path

def executeProcess(cmd="", result=None, module=None):
    try:
        my_env = os.environ.copy()
        my_env['KUBECONFIG'] = os.path.realpath(module.params["kubeconfig"])
        return subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, env=my_env).stdout.decode('utf-8').rstrip()
    except Exception as err:
        result['stdout'] = err
        module.fail_json(msg=err, **result)
        module.exit_json(**result)

class argocd_chpasswd:
    def encrypt_password(self, result=None, module=None):
        command = f"htpasswd -bnBC 10 \"\" {module.params['password']} | tr -d ':\n'"
        return executeProcess(command, result, module)

    def set_password(self, result=None, module=None):
        # https://argo-cd.readthedocs.io/en/stable/operator-manual/user-management/#create-new-user
        # https://argo-cd.readthedocs.io/en/stable/operator-manual/rbac/
        data = {}
        encrypted_password=self.encrypt_password(result, module)
        json_data = json.dumps({module.params['username'].strip() + '.password': encrypted_password.strip()})
        command = f"kubectl patch secret -n {module.params['namespace']} argocd-secret -p '{json_data}'"
        return executeProcess(command, result, module)

    def __init__(self):
        module_args = dict(
            username=dict(type='str', required=True),
            namespace=dict(type='str', required=False, default='argocd'),
            kubeconfig=dict(type='str', required=False, default='/root/.kube/config'),
            password=dict(type='str', required=False, default=None, no_log=True)
        )

        result = dict(
            changed=False,
            stdout='Default message.'
        )

        module = AnsibleModule(
            argument_spec=module_args,
            supports_check_mode=True
        )

        try:
            result['stdout'] = self.set_password(result, module)
            result['changed'] = True
            module.exit_json(**result)
        except Exception as err:
            result['stdout'] = err
            module.fail_json(msg=result['stdout'])
            module.exit_json(**result)

def main():
    argo = argocd_chpasswd()

if __name__ == '__main__':
    main()