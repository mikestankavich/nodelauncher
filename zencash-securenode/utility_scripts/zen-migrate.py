#!/usr/bin/env python3

# requires pip install pylxd

# should parameterize
src = 'sr08:zen-a4t'
dest = 'sg01:zen-a10'
dest_region = 'eu'
# can discover this?
dest_ip = '137.74.177.0'
dest_mac = '02:00:00:a5:2c:c3'
dest_gateway = '149.202.81.254'

from pylxd import Client
import yaml
import json
import urllib3
# import os


src_server = src.split(':')[0]
src_host = src.split(':')[1]
dest_server = dest.split(':')[0]
dest_host = dest.split(':')[1]

# todo: figure out the cert mess
# cert_ref =(os.path.expanduser("~/.config/lxc/client.crt"), os.path.expanduser("~/.config/lxc/client.key"))
# tell urllib to shut up about self signed certificates
urllib3.disable_warnings()
src_client = Client(endpoint='https://{}.4nl.co:8443'.format(src_server),verify=False)
dest_client = Client(endpoint='https://{}.4nl.co:8443'.format(dest_server),verify=False)


src_container = src_client.containers.get(src_host)
dest_container = dest_client.containers.get(dest_host)
# dest_config = dest_container.config
# dest_container.config['limits.memory.enforce'] = 'soft'
# dest_container.save()
# print(json.dumps(dest_container.config,indent=2))
# net_cfg = dest_container.files.get('/etc/netplan/50-cloud-init.yaml')
# print(net_cfg)

network_config = {
    'network': {
        'ethernets': {
            'eth0': {
                'addresses': ['{}/32'.format(dest_ip)],
                'gateway4': dest_gateway,
                'nameservers': {
                    'addresses': ['208.67.222.222', '208.67.220.22'],
                    'search': ['nodelauncher.com', '4nl.co']
                },
                'routes': {
                    'scope': 'link',
                    'to': dest_gateway,
                    'via': '0.0.0.0'
                }
            }
        },
        'version': 2
    }
}
network_config_yml = yaml.dump(network_config, default_flow_style=False)
print(network_config_yml)
dest_container.files.put('/etc/netplan/50-cloud-init.yaml', network_config_yml)
dest_container.config['user.network-config'] = network_config_yml

# dest_container.save()

# do we need to save() ?

# for container in src_client.containers.all():
#     print(container.name)
#
# for container in dest_client.containers.all():
#     print(container.name)


# # check that $1 is a running container
# if [ ! $(lxc list --format csv --columns=n $1) ]; then
#   echo Container $1 does not exist
#   exit 1
# fi
#
# # check that $2 is NOT a running container
# if [ $(lxc list --format csv --columns=n $2) ]; then
#   echo Migration stopped because container $2 already exists
#   exit 1
# fi
#
# # check that $3 is valid region ie na or eu
# if [[ ! $1 =~ ^(na|eu)$ ]]; then
#     echo "Region must be either na or eu"
#     exit 1
# fi
#
# echo migrating node $1 to node $2 in region $3
#
# if [ $(lxc info $1 | yq r - Snapshots | grep -o zen-migrate-snap) ]; then
#   echo deleting previous migration snapshot
#   lxc delete $1/zen-migrate-snap
# fi

#echo creating migration snapshot
#lxc snapshot $1 zen-migrate-snap
#
#echo copying snapshot $1/zen-migrate-snap to $2
#lxc copy $1/zen-migrate-snap $2
#
#echo deleting migration snapshot
#lxc delete $1/zen-migrate-snap

# update user.network-config in profile
# update netplan config and apply (if needed after changing profile)
# update host name in /etc/hosts and secnodetracker/config
# use sed to update region in secnodetracker/config/region and secnodetracker/config/home

#echo set home region and server
#lxc file push region.$3 $2:zen-migrate/home/zen/secnodetracker/config/region
#lxc file push home.$3 $2:zen-migrate/home/zen/secnodetracker/config/home

#echo set file ownership
#lxc start $2:zen-migrate
#lxc exec $2:zen-migrate bash -- -c "chown root:root /etc/hosts"
#lxc exec $2:zen-migrate bash -- -c "chown zen:zen /home/zen/secnodetracker/config/*"
#lxc stop $2:zen-migrate
#
#echo publish cleaned up container to image
#lxc image delete $2:zen-migrate || true
#lxc publish --verbose $2:zen-migrate $2: --alias zen-migrate

#echo delete zen-migrate container
#lxc delete $2:zen-migrate