#!/usr/bin/env python3

import ovh
import json
from netaddr import *
# import time
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

servers = {}
for service in services:
    server_info = client.get('/dedicated/server/{}'.format(service))
    # print(json.dumps(server_info, indent=2))
    server_name = server_info.get('reverse', service)[:-1]
    if re.match(server_name_filter, server_name) or re.match(server_name_filter, service):
        servers[server_name] = {'id': service, 'ip_address': server_info['ip'], 'name': server_name}
        # print(service, server_info['reverse'])
        servers[server_name]['ip_blocks'] = [ipn for ipn in client.get('/dedicated/server/{}/ips'.format(service))
                  if IPNetwork(ipn).prefixlen <= 32 and IPAddress(server_info['ip']) not in IPNetwork(ipn)]

print(yaml.dump(servers, default_flow_style=False))

# print(json.dumps(sorted_macs, indent=4))
