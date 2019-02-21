## Steps to bringup vSRX [15.1X49-D130.6] on Contrail 5.0.2 with cloud-init

1) Set up OS and HEAT client environment
```
sudo apt-get install python-pip python-virtualenv
virtualenv .venv
source .venv/bin/activate
sudo pip install python-openstackclient
sudo pip install python-heatclient
```

2) Source admin-openrc.sh file
```
source /etc/kolla/kolla-toolbox/admin-openrc.sh
```

3) Download vSRX image from [Juniper Support page](https://support.juniper.net/support/downloads/)
4) Create flavor and upload vsrx image onto glance
```
openstack flavor create --ram 4096 --disk 20 --vcpus 2 --public --ephemeral 0 --swap 0 vsrx1.medium
openstack image create vsrx1-image --public --container-format bare --disk-format qcow2 --file <qcow2_file_location>
```
5) Clone this repo
```
git clone https://github.com/urao/tungsten-fabric.git
cd HEAT-templates
```
6) Modify heat template file, with location of the junos configuration file
7) Run the stack create command
```
openstack stack create -e vsrx.env -t vsrx1.yaml vsrx001
```
8) Check status using **openstack stack list **.
