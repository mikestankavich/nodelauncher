#!/usr/bin/env python3

import json
import sys
import os
# import fnmatch
# import re
import yaml
from netaddr import *

# from collections import OrderedDict
from jinja2 import Environment, FileSystemLoader


def main():
    inventory_file = os.path.dirname(os.path.abspath(__file__)) + '/../ansible/zen-inv.yml'

    if len(sys.argv) < 2:
        print("Server name is required")
        sys.exit(1)

    server_name = sys.argv[1]
    server_fqdn = '{}.4nl.co'.format(server_name)

    with open(inventory_file) as yml_file:
        yml_string = yml_file.read()

    ansible_inventory = yaml.load(yml_string)
    lxd_host = ansible_inventory['lxd']['hosts'].get(server_fqdn)
    if not lxd_host:
        print('Server name not found')
        sys.exit(1)

    # container_group = ansible_inventory.get(server_name, {})
    # container_hosts = container_group.get('hosts', [])
    # if not container_hosts:
    #     print('No container inventory defined for {}'.format(server_name))
    #     sys.exit(1)

    ip_address6 = lxd_host.get('ip_address6')
    # if ip_address6:
    #     containers = [{**{'name': nme.split('.')[0], 'fqdn': nme,
    #                       'ip_address6': '{}1:{:x}'.format(ip_address6, idx)},
    #                    **container_hosts[nme]}
    #                   for idx, nme in enumerate(container_hosts, 0)]
    # else:
    #     containers = [{**{'name': nme.split('.')[0], 'fqdn': nme},
    #                    **container_hosts[nme]}
    #                   for nme in container_hosts]



    lxd_host['name'] = server_name
    lxd_host['fqdn'] = server_fqdn
    lxd_host['containers'] = [] #containers
    # lxd_host['gateway'] = lxd_host.get('gateway', lxd_host['ip_address'])
    # lxd_host['ip_address6'] = lxd_host.get('ip_address6')
    # lxd_host['gateway6'] = lxd_host.get('gateway6', lxd_host['ip_address6'])

    # print(json.dumps(lxd_host, indent=2))
    # sys.exit()

    jinja_environment = Environment(
        autoescape=False,
        loader=FileSystemLoader(os.path.dirname(os.path.abspath(__file__))),
        trim_blocks=False)
    tf = jinja_environment.get_template('lxd-tf6.j2').render({'lxd_host': lxd_host})

    print(tf)


if __name__ == "__main__":
    main()