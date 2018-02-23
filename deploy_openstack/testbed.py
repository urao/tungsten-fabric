from fabric.api import env

#Management ip addresses of hosts in the cluster
host1 = 'root@192.168.122.169'

#Host from which the fab commands are triggered to install and provision
host_build = 'root@192.168.122.169'

#Role definition of the hosts.
env.roledefs = {
    'all': [host1],
    'openstack': [host1],
    'cfgm': [host1],
    'compute': [],
    'build': [host1],
}

env.hostnames = {
    host1: 'ostest',
}

env.passwords = {
    host1: 'c0ntrail123',
    host_build: 'c0ntrail123',
}
