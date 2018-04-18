
## Steps to deploy all-in-one Contrail + OpenStack using Helm Deployer

1. Bring up a Ubuntu 16.04.03 VM with 4 vCPU, 32 GB of RAM and 300 GB of disk
2. VM will have 2 NICs, eth0, eth1 configured with static IP.
4. Make sure internet is accessible via interface eth0
5. Interface eth1 is not been used currently, but make sure its UP and configured
6. Install required packages
```
apt-get install -y git
```
7. Clone contrail-ansible-deployer
```
mkdir -p git
cd git
git clone https://github.com/Juniper/openstack-helm.git
git clone https://github.com/Juniper/openstack-helm-infra.git
git clone https://github.com/Juniper/contrail-helm-deployer.git
```
8. Copy [instances.yaml](https://github.com/urao/tungsten-fabric/blob/master/tungsten_50_deploy/all-in-one-os/instances.yaml) into config/ folder
9. Modify ssh_pwd, ip, contrail_api_interface_address, keystone_admin_password, CONTROL_DATA_NET_LIST, CONTROLLER_NODES, VROUTER_GATEWAY in the instances.yaml file copied from the previous step
10. Install Contrail and Kolla requirements
```
cd contrail-ansible-deployer
ansible-playbook -i inventory/ playbooks/configure_instances.yml 
```
11. Verify if the requirements  was successful.
```
192.168.122.238            : ok=31   changed=22   unreachable=0    failed=0   
localhost                  : ok=10   changed=2    unreachable=0    failed=0   
```
12. Deploy Contrail and Kolla containers
```
cd contrail-ansible-deployer
ansible-playbook -i inventory/ -e orchestrator=openstack playbooks/install_contrail.yml
```
13. Verify if the deployment  was successful.
```
192.168.122.238            : ok=414  changed=200  unreachable=0    failed=0   
localhost                  : ok=7    changed=2    unreachable=0    failed=0   
```
14. Verify if 56 containers are UP and running
```
[root@contrail50 contrail-ansible-deployer]# docker ps | awk '{print $1}' | wc -l
56
```
## Access to Horizon console

1. Get the admin user password
```
sudo grep keystone_admin_password /root/contrail-kolla-ansible/etc/kolla/passwords.yml
```
2. Browse to the IP http://<VM_IP_ADDRESS> and login with the user "admin" and the password from the previous step


## Provision Weave Scope

1. Follow the below instructions to bring up Weave Scope
```
sudo curl -L git.io/scope -o /usr/local/bin/scope
sudo chmod a+x /usr/local/bin/scope
scope launch
```

2. Now you should be able to connect to the UI using http://<HOST_IP>:4040

3. The UI is totally self-explanatory. There are multiple filters that filters the components based on the scope required.

4. Containers view
<img src="./images/container_view.png" width=400>

5. Container detailed view
<img src="./images/container_detail_view.png" width=400>

6. Connecting to a container
<img src="./images/connect_to_container.png" width=400>


## Reference
[Contrail Wiki Link](https://github.com/Juniper/contrail-ansible-deployer/wiki/Contrail-with-Kolla-Ocata)
