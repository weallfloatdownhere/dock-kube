#!/usr/bin/python3

from ast import arg
from logging import raiseExceptions
import subprocess, argparse
from argparse import RawTextHelpFormatter
import os.path
from os import path

USAGE="""
USAGE
---------------------------------
entrypoint.py [components] [task]
---------------------------------
task:       {install, remove}
components: {rke, argocd}
---------------------------------
EXAMPLES
* entrypoint.py -c rke install
* entrypoint.py -c rke -c argocd install
* entrypoint.py -c argocd remove
"""

CONST_CONFIG_PATH='/root/rke/config.yml'
CONST_PLAYBOOK_PATH='/usr/share/bin/playbook.yml'

def start_playbook(cmd=None):
    try:
        return subprocess.run(cmd, shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')
    except Exception as err:
        print(err)

def generate_command(args=[]):
    command = ['ansible-playbook', '-i', 'localhost', '--extra-vars']
    triggers = args.task + ',' + ','.join(args.components)
    command.append("'" + '{"triggers": [%s]}' % triggers + "'")
    if [path.exists(CONST_CONFIG_PATH)]: command.append(f'--extra-vars @{CONST_CONFIG_PATH}')
    command.append(CONST_PLAYBOOK_PATH)
    return ' '.join(command)

def get_arguments():
    parser = argparse.ArgumentParser(description=USAGE, formatter_class=RawTextHelpFormatter)
    parser.add_argument('task', type=str, help='Task to execute', nargs='?', default='install', choices=['install', 'remove'])
    parser.add_argument('-c', '--component', type=str, dest='components', action='append', choices=['rke', 'argocd'])
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

