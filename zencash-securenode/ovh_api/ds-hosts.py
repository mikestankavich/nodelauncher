#!/usr/bin/env python3

import ovh
import json
from netaddr import *
import time
import string
# from string import lowercase
# from string import digits
import sys
import re
import yaml

if len(sys.argv) > 1:
    server_name_filter = sys.argv[1]
else:
    server_name_filter = '.*'


host_suffixes = string.digits + string.ascii_lowercase
# print(json.dumps(host_names, indent=4))
host_map = {
    'sg01.4nl.co': 'zen-a10',
    'sb07.4nl.co': 'zen-b00',
    'sb08.4nl.co': 'zen-b0c',
    'sb09.4nl.co': 'zen-b0o',
    'sb10.4nl.co': 'zen-b10',
    'sr11.4nl.co': 'zen-b1c',
    'sr12.4nl.co': 'zen-b1o'
}

# Instantiate. Visit https://api.ovh.com/createToken/?GET=/me
# to get your credentials
client = ovh.Client(
    endpoint='soyoustart-ca',
    application_key='REDACTED',
    application_secret='REDACTED',
    consumer_key='REDACTED',
)

services = client.get('/dedicated/server')
# print(json.dumps(result, indent=4))

hosts = {}
for service in services:
    server_info = client.get('/dedicated/server/{}'.format(service))
    # print(json.dumps(server_info, indent=2))
    server_name = server_info.get('reverse', service)[:-1]
    # print(server_name)
    if re.search(server_name_filter, server_name) and server_name in host_map.keys():
        # servers[server_name] = {'id': service, 'ip_address': server_info['ip'], 'name': server_name}
        # print(service, server_info['reverse'])
        host_base = host_map.get(server_name)
        base_idx = host_suffixes.find(host_base[-1])
        host_names = ['{}{}.nodelauncher.com'.format(host_base[0:-1], letter) for letter in host_suffixes[base_idx:]]

        primary_ip = server_info['ip']

        failover_ip_blocks = [ipn for ipn in client.get('/dedicated/server/{}/ips'.format(service))
                          if IPNetwork(ipn).prefixlen <= 32 and IPAddress(primary_ip) not in IPNetwork(ipn)]
        failover_ips = [str(ipa) for ipn in failover_ip_blocks for ipa in IPNetwork(ipn)]

        container_hosts = dict(zip(host_names, failover_ips))
        # print(json.dumps(container_hosts, indent=2))
        hosts = {**hosts, **container_hosts}

print(json.dumps(hosts, indent=2))
