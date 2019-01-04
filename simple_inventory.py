#!/usr/bin/python
####################################################################################
# Simple example of inventory script for ansible. It generates required            #
# JSON from ordinary text inventory for ansible. Do not use grouping by            #
# bracket lines, such as "[group1]", Grouping is done by filling JSON              #
# formatted list variable "inv_groupnames", see hosts_example                      #
#                                                                                  #
# Usage:                                                                           #
#  simple_inventory.py [--file /some/file] <--list|<--host hostname > [--pretty]   #
#    --list          List all hosts in inventory                                   #
#    --host <host>   Print a single host                                           #
#    --file          ansible inventory file (defaults to ./hosts_example)          #
#    --pretty        Pretty formatting for puny 'umies                             #
#                                                                                  #
# Script contains check if it runs under Ansible Tower (assuming that Tower runs   #
# under user "awx" and scripts are run in directory /tmp/ansible_tower_launch ).   #
# If that is true, then it filters out all nodes in group with name "NO_TOWER"     #
# Useful when for any reason (licensing or user convenience reason, for example)   #
# you do not wish some server present in Tower inventory, but still be available   #
# to admin from CLI.                                                               #
####################################################################################

import os
import sys
import re
import argparse
try:
    import json
except ImportError:
    import simplejson as json

inv_file_name = './hosts_example'
run_from_tower = 0

def grouplist():
    inventory = {}
    inventory['all'] = {}
    inventory['all']['hosts'] = []
    inventory['_meta'] = {}
    inventory['_meta']['hostvars'] = {}

    for line in inventory_list:
        if not (run_from_tower == 1 and re.search('"NO_TOWER"',line)):
            fields = line.split()
            host = fields[0]
            inventory['all']['hosts'].append(host)
            del fields[0]
            inv_groupname_index = [i for i,x in enumerate(fields) if re.search('^inv_groupnames=',x)]
            for igroup in json.loads(re.sub('^inv_groupnames=[\']?|\'$','',fields[inv_groupname_index[0]])):
                if not inventory.has_key(igroup):
                    inventory[igroup] = {}
                    inventory[igroup]['hosts'] = []
                inventory[igroup]['hosts'].append(host)
            if len(fields) > 0:
                for inv_var in fields:
                    if not inventory['_meta']['hostvars'].has_key(host):
                        inventory['_meta']['hostvars'][host] = {}
                    inv_var_name = inv_var.split('=')[0]
                    inv_var_value = re.sub('^'+inv_var_name+'=[\']?|\'$','',inv_var)
                    if not re.search('^\[|\"|\'|\{',inv_var_value):
                        inv_var_value = '\"'+inv_var_value+'\"'
                    inventory['_meta']['hostvars'][host][inv_var_name] = json.loads(inv_var_value)

    if args.pretty:
        print json.dumps(inventory,sort_keys=True,indent=4)
    else:
        print json.dumps(inventory)

def hostinfo(name):
    inventory = {}
    for line in inventory_list:
        if not (run_from_tower == 1 and re.search('"NO_TOWER"',line)):
            fields = line.split()
            host = fields[0]
            if host == name:
                del fields[0]
                if len(fields) > 0:
                    for inv_var in fields:
                        inv_var_name = inv_var.split('=')[0]
                        inv_var_value = re.sub('^'+inv_var_name+'=[\']?|\'$','',inv_var)
                        if not re.search('^\[|\"|\'|\{',inv_var_value):
                            inv_var_value = '\"'+inv_var_value+'\"'
                        inventory[inv_var_name] = json.loads(inv_var_value)
            

    if args.pretty:
        print json.dumps(inventory,sort_keys=True,indent=4)
    else:
        print json.dumps(inventory)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='hosts file (defaults to ./hosts_example)', action='store')
    parser.add_argument('--list', help='List all hosts in inventory', action='store_true')
    parser.add_argument('--pretty', help='Pretty formatting for puny humies', action='store_true')
    parser.add_argument('--host', help='Print a single host', action='store')
    args = parser.parse_args()

    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)

    if args.file:
        inv_file_name = args.file

    log = open('/tmp/simple_inventory.log','w')
    for param in os.environ.keys():
        log.write(param+"="+os.environ[param]+"\n")
    log.close()
    if ( os.environ['USER'] == 'awx' ) and re.search('^/tmp/ansible_tower_launch',os.environ['PWD']):
        run_from_tower = 1

    with open(inv_file_name, "r") as f:
        inventory_list = f.read().splitlines()

    if args.list:
        grouplist()

    if args.host:
        hostinfo(args.host)

