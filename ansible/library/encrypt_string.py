#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['stable'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: encrypt_string
short_description: Plaintext to encrypted string.
version_added: "1.0"
description:
    - "Encrypt plaintext string with ht"
dependencies:
    - htpasswd: https://httpd.apache.org/docs/2.4/programs/htpasswd.html
    - kubectl: https://github.com/kubernetes/kubectl
options:
    clear_string:
        description:
            - Plaintext string to encrypt with htpasswd.
        required: true
        type: str
    encryption:
        description:
            - Type of encryption.
        required: false
        default: base64
        choices: ['base64', 'bcrypt']
        type: str
author:
    - Anonymous
'''

EXAMPLES = '''
- name: "Encrypt specified string."
  encrypt_string:
    clear_string: 'supersecretpassword'
    encryption: 'base64'
  register: reg_encrypted_string
'''

RETURN = '''
stdout:
    description: The output message that the sample module generates.
    type: str
'''

import subprocess
from ansible.module_utils.basic import AnsibleModule
from collections import OrderedDict

def executeProcess(cmd="", result=None, module=None):
    try:
        return subprocess.run(cmd, shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8').rstrip()
    except Exception as err:
        result['stdout'] = err
        module.fail_json(msg=err, **result)
        module.exit_json(**result)

class string_encrypter:
    def encrypt_bcrypt(self, result=None, module=None):
        command = f"htpasswd -bnBC 10 \"\" {module.params['clear_string']} | tr -d ':\n'"
        return executeProcess(command, result, module)

    def encrypt_base64(self, result=None, module=None):
        command = f"base64 -w 0 {module.params['clear_string']}"
        return executeProcess(command, result, module)

    def __init__(self):
        module_args = dict(
            clear_string=dict(type='str', required=True),
            encryption=dict(type='str', required=False, choices=['base64', 'bcrypt'])
        )

        result = dict(
            stdout='Default message.'
        )

        module = AnsibleModule(
            argument_spec=module_args,
            supports_check_mode=True
        )

        tasks = OrderedDict([
            ('bcrypt', self.encrypt_bcrypt(result, module)),
            ('base64', self.encrypt_base64(result, module))
        ])

        try:
            result['stdout'] = tasks[module.params['encryption']]
            module.exit_json(**result)
        except Exception as err:
            result['stdout'] = err
            module.fail_json(msg=result['stdout'])

def main():
    crypted = string_encrypter()

if __name__ == '__main__':
    main()