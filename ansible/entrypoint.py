#!/usr/bin/python3

from ast import arg
from logging import raiseExceptions
import os, subprocess, argparse
from argparse import RawTextHelpFormatter

USAGE="""
USAGE
---------------------------------
entrypoint.py [task] [components]
---------------------------------
task: install | remove
components: rke | argocd
---------------------------------
EXAMPLES
* entrypoint.py install rke
* entrypoint.py install argocd
"""

def start_playbook(cmd="ls"):
    try:
        return subprocess.run(cmd, shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')
    except Exception as err:
        print(err)

def generate_command(args=[]):
    command = ['ansible-playbook', '-i', 'localhost', '--tags']
    tags = args.task + ',' + ','.join(args.components)
    command.append(tags)
    command.append('/usr/share/bin/ansible/playbook.yml')
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

    #command = generate_command()
    #start_playbook(command)

if __name__ == '__main__':
    main()

