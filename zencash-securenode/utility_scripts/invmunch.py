#!/usr/bin/env python3

import json
# import sys
import os
# import fnmatch
# import re
import yaml
from netaddr import *
import csv

# from collections import OrderedDict
from jinja2 import Environment, FileSystemLoader


def main():
    inventory_file = os.path.dirname(os.path.abspath(__file__)) + '/../ansible/zen-inv.yml'

    with open(inventory_file) as yml_file:
        yml_string = yml_file.read()

    ansible_inventory = yaml.load(yml_string)

    # print(json.dumps(ansible_inventory['zen'], indent=2))

    # host_keys = []
    # for zhost_key, zhost_values in ansible_inventory['zen']['hosts'].items():
        # print(zhost_values.get('lxd_host'), zhost_key)
        # host_keys += zhost[1].keys()
        # print(zhost[1].keys())


    zhosts = [{'lxd_host':zhost_values.get('lxd_host'),
               'node_fqdn':zhost_key,
               'node_name':zhost_key.split('.')[0],
               'owner_email': zhost_values.get('owner_email', ''),
               'tracker_region': zhost_values.get('tracker_region', ''),
               'ip_address': zhost_values.get('ip_address', ''),
               'mac_address': zhost_values.get('mac_address', ''),
               'challenge_address': zhost_values.get('challenge_address', ''),
               'staking_address': zhost_values.get('staking_address', ''),
               'node_id': zhost_values.get('node_id', ''),
               'notify_email': zhost_values.get('notify_email', ''),
               'lxd_image': zhost_values.get('lxd_image', 'zen-base')  }
              for zhost_key, zhost_values in ansible_inventory['zen']['hosts'].items()]
    # print(set(host_keys))
    print(json.dumps(zhosts,indent=2))

    with open('invmunch.csv', 'w') as f:
        writer = csv.writer(f)
        for zhost in zhosts:
            writer.writerow([zhost.get('lxd_host'),
                             zhost.get('node_fqdn'),
                             zhost.get('node_name'),
                             zhost.get('owner_email', ''),
                             zhost.get('tracker_region', ''),
                             zhost.get('ip_address', ''),
                             zhost.get('mac_address', ''),
                             zhost.get('challenge_address', ''),
                             zhost.get('staking_address', ''),
                             zhost.get('node_id', ''),
                             zhost.get('notify_email', ''),
                             zhost.get('lxd_image', '')])

# 'lxd_host', 'owner_email', 'tracker_region', 'ip_address', 'mac_address', 'challenge_address', 'staking_address', 'node_id', 'notify_email', 'lxd_image'

if __name__ == "__main__":
    main()

