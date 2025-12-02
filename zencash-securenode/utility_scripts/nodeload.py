#!/usr/bin/env python3

import json
# import sys
import os
# import fnmatch
# import re
import yaml
from netaddr import *

# from collections import OrderedDict
from jinja2 import Environment, FileSystemLoader


def main():
    inventory_file = os.path.dirname(os.path.abspath(__file__)) + '/../zen-inv.yml'

    with open(inventory_file) as yml_file:
        yml_string = yml_file.read()

    ansible_inventory = yaml.load(yml_string)

    lxd_hosts = { k:[n for n,v in ansible_inventory['zen']['hosts'].items()
                     if v['lxd_host'] == k.split('.')[0]]
                  for k in ansible_inventory['lxd']['hosts'] }

    host_count = {k:len(v) for k,v in lxd_hosts.items()}
    # boxes = {k:v for k,v in ansible_inventory['zen']['hosts'].items() if v['lxd_host'] in lxd_hosts}

    print(json.dumps(lxd_hosts, indent=2))
    print(json.dumps(host_count, indent=2))
    # sys.exit()



if __name__ == "__main__":
    main()