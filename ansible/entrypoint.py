#!/usr/bin/python3

from ast import arg
from logging import raiseExceptions
import subprocess, argparse
from argparse import RawTextHelpFormatter

from os import path

USAGE="""
USAGE
---------------------------------
entrypoint.py [components] [task]
---------------------------------
task:       {install, remove}
components: {rke, argocd, sealed-secrets}
verbose:    true / false
---------------------------------
EXAMPLES
* entrypoint.py install
* entrypoint.py -c argocd remove
* entrypoint.py install -c argocd --verbose
"""

CONST_SHARED_DIR_PATH='/root/rke'
CONST_CONFIG_PATH=f'{CONST_SHARED_DIR_PATH}/config.yml'
CONST_PLAYBOOK_PATH='/usr/share/bin/ansible/playbook.yml'

def start_playbook(cmd=None):
    try:
        return subprocess.run(cmd, shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')
    except Exception as err:
        print(err)

def generate_command(args=[]):
    command = ['ansible-playbook', '-i', 'localhost', '--extra-vars']

    triggers = [args.task]
    if args.components != None: triggers.extend(args.components)
    if args.verbose: triggers.append('verbose')
    
    command.append("'" + '{"triggers": [%s]}' % ','.join(triggers) + "'")
    if [path.exists(CONST_CONFIG_PATH)]: command.append(f'--extra-vars @{CONST_CONFIG_PATH}')
    command.append(CONST_PLAYBOOK_PATH)
    return ' '.join(command)

def get_arguments():
    parser = argparse.ArgumentParser(description=USAGE, formatter_class=RawTextHelpFormatter)
    parser.add_argument('task', type=str, help='Task to execute', nargs='?', default='install', choices=['install', 'remove'])
    parser.add_argument('-c', '--component', type=str, dest='components', action='append', choices=['argocd', 'sealed-secrets'])
    parser.add_argument('--verbose', '-v', action='store_true', default=False)
    args = parser.parse_args()
    return args

def main():
    args = get_arguments()
    command = generate_command(args)
    print(command)
    output = start_playbook(command)
    print(output)

if __name__ == '__main__':
    main()

