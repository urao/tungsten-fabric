
# Steps to deploy openstack orchestrator only
# Below steps are tested on Ubuntu 14.04.4 with mitaka version of contrail debian package

1. Bring up single server/VM with Ubuntu 14.04.4 version of OS
2. Copy contrail debian package onto the server
3. dpkg -i contrail-install-packages_x.x.x~mitaka_all.deb
4. cd /opt/contrail/contrail_packages && setup.sh
5. Copy testbed.py file into /opt/contrail/utils/fabfile/testbeds/
6. cd /opt/contrail/contrail_packages && fab install_orchestrator
7. cd /opt/contrail/contrail_packages && fab setup_orchestrator
6. source /etc/contrail/openstackrc && openstack-status
