#!/usr/bin/env python3

import CloudFlare
import os
import sys
import json
import yaml


def main():
    cf = CloudFlare.CloudFlare()

    with open("../ansible/zen-inv.yml", 'r') as stream:
        try:
            ansible_inventory = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(1)

    zen_servers = ansible_inventory['zen']['children'].keys()
    zen_nodes = {hk:hv['ip_address'] for ik, iv in ansible_inventory.items()
                 for sk, sv in iv.items()
                 for hk, hv in sv.items()
                 if ik in zen_servers and sk == 'hosts' and 'ip_address' in hv.keys()}
    # print(zen_nodes)
    # zen_nodes = {host: host_values['ip_address'] for server, server_items in ansible_inventory.items()
    #              for hosts in server_items.values() for host, host_values in hosts.items()
    #              if server in zen_servers}
    # print(zen_servers)
    # print(json.dumps(zen_nodes, indent=2))
    # sys.exit()

    zones = [zone for zone in cf.zones.get() if zone['name'] == 'nodelauncher.com']
    if zones:
        zone_id = zones[0]['id']
    else:
        print('nodelauncher zone not found')
        sys.exit(1)

    # print(json.dumps(zone, indent=2))

    rec_page = 0
    # recs = cf.zones.dns_records.get(zone_id, params = {'page':rec_page, 'per_page':5})

    rec_len = -1
    recs = []

    # for recs in iter(cf.zones.dns_records.get(zone_id, params = {'page':rec_page, 'per_page':5}), []):
    while rec_len < len(recs):
        rec_len = len(recs)
        recs += cf.zones.dns_records.get(zone_id, params={'type:': 'A', 'page': rec_page, 'per_page': 100})
        rec_page += 1
        # print(len(recs))

    a_recs = {rec['name']: {'id': rec['id'], 'content': rec['content'], 'proxied': rec['proxied']}
              for rec in recs if rec['type'] == 'A'}
    for ar in a_recs:
        if 'zen-b1' in ar or 'zen-m1' in ar:
            print('{}: {}'.format(ar,a_recs[ar]['content']))
    # print(json.dumps(a_recs, indent=2))

    # r = cf.zones.dns_records.post(zone_id, data=dns_record)
    # print(json.dumps(r, indent=2))
    # sys.exit()
    for name, ip in zen_nodes.items():
        a_rec = a_recs.get(name)
        # print(name,ip)
        # print(json.dumps(a_rec, indent=2))
        dns_record = {'name':name.split('.')[0], 'type':'A', 'content':ip, 'proxied':False}
        if not a_rec:
            print('Create A record for {}: {}'.format(name, ip))
            # print(json.dumps(dns_record, indent=2))
            result = cf.zones.dns_records.post(zone_id, data=dns_record)
            print(json.dumps(result, indent=2))
        if a_rec and (a_rec['content'] != ip or a_rec['proxied']):
            print('Update A record for {}: {}'.format(name, ip))
            # print(json.dumps(dns_record, indent=2))
            result = cf.zones.dns_records.put(zone_id, a_rec['id'], data=dns_record)
            print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
