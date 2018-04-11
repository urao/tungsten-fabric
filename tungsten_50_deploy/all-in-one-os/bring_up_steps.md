
## Steps to deploy all-in-one Contrail + Kolla Ocata OpenStack

Below steps are tested on a VM

1. Bring up VM with Centos 7.4 OS with 2 interfaces eth0, eth1
2. Modify ifcfg-eth0, ifcfg-eth1 under /etc/sysconfig/network-scripts similiar to below
```
TYPE=Ethernet
BOOTPROTO=static
NAME=eth0
DEVICE=eth0
ONBOOT=yes
NM_CONTROLLED=no
USERCTL=no
IPADDR=192.168.122.238
PREFIX=24
GATEWAY=192.168.122.1
```
```
TYPE=Ethernet
BOOTPROTO=static
NAME=eth1
DEVICE=eth1
ONBOOT=yes
NM_CONTROLLED=no
USERCTL=no
IPADDR=192.0.2.181
PREFIX=24
```
3. Remove file /etc/sysconfig/network-scripts/ifcfg-Wired_connection_1 if exists
