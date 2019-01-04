# ansible.simple_inventory

Simple example of inventory script for ansible. It generates required
JSON from ordinary text inventory for ansible. Do not use grouping by
bracket lines, such as "[group1]", Grouping is done by filling JSON
formatted list variable "inv_groupnames", see hosts_example

## Script usage:

'''
 ./simple_inventory.py [--file /some/file] <--list|<--host hostname > [--pretty]
   --list          List all hosts in inventory
   --host <host>   Print a single host
   --file          ansible inventory file (defaults to ./hosts_example)
   --pretty        Pretty formatting for puny 'umies
'''

Script contains check if it runs under Ansible Tower (assuming that Tower runs
under user "awx" and scripts are run in directory /tmp/ansible_tower_launch ).
If that is true, then it filters out all nodes in group with name "NO_TOWER"
Useful when for any reason (licensing or user convenience reason, for example)
you do not wish some server present in Tower inventory, but still be available
to admin from CLI.

All variables for host are always presented as host variables (including
inv_groupnames), and list contained in inv_groupnames is converted to groups containing 
given host as well.

## Example of hosts file:
'''
thanquol ansible_host=1.2.3.4 inv_groupnames='["CORPORATE","DATABASE"]'
lurk inv_groupnames='["CORPORATE","DMZ","WEBSERVER"]'
gotrek ansible_python_interpreter=/usr/bin/python26 inv_groupnames='["SECURITY","DMZ","PENTESTS","WORKER"]'
felix inv_groupnames='["SECURITY","DMZ","PENTEST","GUI"]'
teclis corp_env=devel inv_groupnames='["DEVEL","NO_TOWER"]
'''

In this case, there will be groups
'''
CORPORATE: thanquol, lurk
DATABASE: thanquol
DMZ: lurk, gotrek, felix
etc...
'''

thanquol will have defined ansible_host as host variable, for gotrek there will be
python2.6 interpreter used for ansible jobs on that node, and teclis will have
corp_env variable set to "devel" and it will not appear in Ansible Tower inventory.


