#!/usr/bin/env python3

import sys
import json
import yaml


def main():
    with open("zen-inv.yml", 'r') as stream:
        try:
            ansible_inventory = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(1)

    zen_servers = ansible_inventory['zen']['children'].keys()
    zen_nodes = {host: host_values['ip_address']
                 for server, server_items in ansible_inventory.items()
                 for hosts in server_items.values()
                 for host, host_values in hosts.items()
                 if server in zen_servers}
    # print(zen_servers)
    # print(json.dumps(zen_nodes, indent=2))
    node_names = sorted([k.split('.')[0] for k in zen_nodes.keys()])
    print(json.dumps(node_names, indent=2))
    for node in node_names:
        print(node)
    sys.exit()

if __name__ == '__main__':
    main()
