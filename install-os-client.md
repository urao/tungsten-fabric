## Install openstack client on Linux OS

### Steps to install on Centos

```
yum install -y gcc python-devel wget
pip install virtualenv
virtualenv .op
source .op/bin/activate
pip install python-openstackclient
pip install python-ironicclient
pip install python-neutronclient
pip install python-heatclient
```

### Steps to install on Ubuntu

```
apt-get install -y gcc  python-dev wget
pip install virtualenv
virtualenv .op
source .op/bin/activate
pip install python-openstackclient
pip install python-ironicclient
pip install python-neutronclient
pip install python-heatclient
```

```
source <location_of_openstackrc.sh>
```
```
openstack hypervisor list
```
