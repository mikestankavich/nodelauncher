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
    # print(server_name)
    if re.search(server_name_filter, server_name) or re.search(server_name_filter, service):
        servers[server_name] = {'id': service, 'ip_address': server_info['ip'], 'name': server_name}
        # print(service, server_info['reverse'])

host_suffixes = string.digits + string.ascii_lowercase
# print(json.dumps(host_names, indent=4))
base_map = {
    'sb02.4nl.co': 'zen-a3c',
    'sb03.4nl.co': 'zen-a3k',
    'sb04.4nl.co': 'zen-a3o',
    'sb07.4nl.co': 'zen-b00',
    'sb08.4nl.co': 'zen-b0c',
    'sb09.4nl.co': 'zen-b0o',
    'sb10.4nl.co': 'zen-b10',
    'sr11.4nl.co': 'zen-b2g',
    'sr12.4nl.co': 'zen-b2k',
    'sr01.4nl.co': 'zen-b20'
}
for server in servers:
    host_base = base_map.get(server, 'a')
    base_idx = host_suffixes.find(host_base[-1])
    host_names = ['{}{}.nodelauncher.com'.format(host_base[0:-1], letter) for letter in host_suffixes[base_idx:]]

    srv_obj = servers[server]
    # print(json.dumps(srv_obj['id'], indent=2))
    primary_ip = srv_obj['ip_address']
    # server_ips = client.get('/dedicated/server/{}/ips'.format(srv_obj['id']))
    failover_ip_blocks = [ipn for ipn in client.get('/dedicated/server/{}/ips'.format(srv_obj['id']))
                      if IPNetwork(ipn).prefixlen <= 32 and IPAddress(primary_ip) not in IPNetwork(ipn)]
    failover_ips = [str(ipa) for ipn in failover_ip_blocks for ipa in IPNetwork(ipn)]
    vmacs = client.get('/dedicated/server/{}/virtualMac'.format(srv_obj['id']))
    # print(vmacs)
    ip_vmacs = {client.get('/dedicated/server/{}/virtualMac/{}/virtualAddress'.format(srv_obj['id'], vmac))[0]: vmac
                for vmac in vmacs}

    container_host_names = dict(zip(host_names, failover_ips))
    for host_name, ip in container_host_names.items():
        if ip not in ip_vmacs.keys():
            print('add mac for {}'.format(ip))
            # ip_vmacs[ip] = 'new mac'
            virtual_mac_post = client.post(
                '/dedicated/server/{}/virtualMac'.format(srv_obj['id']),
                ipAddress=ip, # Required: Ip address to link with this virtualMac (type: ipv4)
                type='ovh', # Required: vmac address type (type: dedicated.server.VmacTypeEnum)
                virtualMachineName=host_name  # Required: Friendly name of your Virtual Machine behind this IP/MAC (type: string)
            )
            while not client.get('/dedicated/server/{}/task/{}'.format(srv_obj['id'], virtual_mac_post['taskId']))['doneDate']:
                print('Waiting for mac...')
                time.sleep(3)
            print('done waiting for mac')

    if len(ip_vmacs) < len(failover_ips):
        time.sleep(3)
        ip_vmacs = {client.get('/dedicated/server/{}/virtualMac/{}/virtualAddress'.format(srv_obj['id'], vmac))[0]: vmac
                    for vmac in vmacs}

    srv_obj['failover_ip_blocks'] = failover_ip_blocks
    srv_obj['failover_ips'] = failover_ips
    srv_obj['failover_hosts'] = {server: {'hosts': {h: {} for h in container_host_names}}}

    # for name, ip in container_host_names.items():
    #
    # print(json.dumps(container_host_names, indent=2))
    # sys.exit()

    # for ip_block in server_ips:
    #     for ip in IPNetwork(ip_block):
    #         if not ip_vmacs.get(ip):
    #             print('add mac for {}'.format(ip))
    #
    #             result = client.post('/dedicated/server/{}/virtualMac'.format(server),
    #                                  ipAddress=ip, # Required: Ip address to link with this virtualMac (type: ipv4)
    #                                  type='ovh', # Required: vmac address type (type: dedicated.server.VmacTypeEnum)
    #                                  virtualMachineName=ip.replace('.','-')  # Required: Friendly name of your Virtual Machine behind this IP/MAC (type: string)
    #                                  )


    container_hosts = {host_name: {
        'lxd_host': srv_obj['name'].split('.')[0],
        'ip_address': ip,
        'mac_address': ip_vmacs.get(ip)
    } for host_name, ip in container_host_names.items()}

    srv_obj['container_hosts'] = container_hosts

    # print a recs
    print(json.dumps(container_host_names,indent=2))
    # ip_vmacs = {vmac: client.get('/dedicated/server/{}/virtualMac/{}/virtualAddress'.format(srv_obj['id'], vmac))[0]
    #             for vmac in vmacs}
    # flipped = {ip: [k for k,v in ip_vmacs.items() if ip in v] for ip in set([v for v in ip_vmacs.values()])}
    # print(json.dumps(flipped, indent=2))
    # sys.exit()
    # print(json.dumps(ip_vmacs, indent=2))

    # print(json.dumps(server_ips, indent=2))
    # for ipn in server_ips:
    #     if IPNetwork(ipn).prefixlen < 32:
    #         print(IPNetwork(ipn))

#
print(yaml.dump(servers, default_flow_style=False).replace('{}', ''))


# client = ovh.Client(
#     endpoint='ovh-ca',
#     application_key='REDACTED',
#     application_secret='REDACTED',
#     consumer_key='REDACTED',
# )
#
# # server_id = 'ns365661.ip-94-23-35.eu'
# server_id = 'ns518086.ip-192-99-15.net'
#
# result = client.get('/dedicated/server/{}/virtualMac'.format(server_id))
# #print(json.dumps(result, indent=4))
#
# lxd_host = 'sb07'
#
# host_base = 'zen-b1a'
# base_idx = ascii_lowercase.find(host_base[-1])
# hosts = ['{}{}'.format(host_base[0:-1],letter) for letter in ascii_lowercase[base_idx:base_idx+12]]
# print(json.dumps(hosts, indent=4))
#
# # ip_macs = []
# ip_macs = {}
# for mac in result:
#     ip = client.get('/dedicated/server/{}/virtualMac/{}/virtualAddress'.format(server_id, mac))
#     # ip_macs.append({ip[0]: mac})
#     ip_macs = {**ip_macs, **{ip[0]: mac}}
#     # print(mac,ip[0])
#
# sorted_macs = {hosts[idx]:{'ip_address':ip, 'lxd_host': lxd_host, 'mac_address':ip_macs[ip]} for idx, ip in enumerate(sorted(ip_macs))}
# print(json.dumps(sorted_macs, indent=4))
#
# # for ip in enumerate(sorted_macs):
#     # print(ip)
