#!/usr/bin/env python3

# requires pip install pylxd

# should parameterize
src = 'sr08:zen-a4t'
dest_server = 'sg01'
dest_region = 'eu'

from pylxd import Client
import yaml
import json
import urllib3
# import os


src_server = src.split(':')[0]
src_host = src.split(':')[1]
dest_host = 'zen-base'

# todo: figure out the cert mess
# https://serverfault.com/questions/882880/authenticate-to-lxd-rest-api-over-network-certificate-auth-keeps-failing
# cert_ref =(os.path.expanduser("~/.config/lxc/client.crt"), os.path.expanduser("~/.config/lxc/client.key"))
# tell urllib to shut up about self signed certificates
urllib3.disable_warnings()

try:
    src_container = src_client.containers.get(src_host)
except:
    print('Cannot connect to source server')
    sys.exit(1)

try:
    src_client = Client(endpoint='https://{}.4nl.co:8443'.format(src_server),verify=False)
except:
    print('Cannot connect to source container')
    sys.exit(1)

try:
    dest_client = Client(endpoint='https://{}.4nl.co:8443'.format(dest_server),verify=False)
except:
    print('Cannot connect to destination server')
    sys.exit(1)

if dest_client.containers.exists(dest_host):
    # delete destination container so we can "overwrite"
    dest_container = dest_client.containers.get(dest_host)
    dest_container.delete()

print('copy to zen-base container')

# if dest_container:
#     print('yes dest')
# else:
#     print('no dest')


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