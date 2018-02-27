from fabric.api import env

#Management ip addresses of hosts in the cluster
# ctrl cfg node
host1 = 'root@172.16.70.20'
host2 = 'root@172.16.70.23'
host3 = 'root@172.16.70.26'

#analytics
host4 = 'root@172.16.70.21'
host5 = 'root@172.16.70.24'
host6 = 'root@172.16.70.27'

#openstack
host7 = 'root@172.16.70.22'
host8 = 'root@172.16.70.25'
host9 = 'root@172.16.70.28'

#compute
#host10 = 'root@172.16.70.5'
#host11 = 'root@172.16.70.6'
host12 = 'root@172.16.70.7'
host13 = 'root@172.16.70.8'


#External routers if any
#for eg.
#ext_routers = [('mx1', '10.204.216.253')]
ext_routers = []

#Autonomous system number
router_asn = 64512

#Host from which the fab commands are triggered to install and provision
host_build = 'root@172.16.70.20'


#Role definition of the hosts.
env.roledefs = {
    #'all': [host1, host2, host3, host4, host5, host6, host7, host8, host9, host10, host11],
    'all': [host1, host2, host3, host7, host8, host9, host12, host13],
    'cfgm': [host1, host2, host3],
    'openstack': [host7, host8, host9],
    'control': [host1, host2, host3],
    #'compute': [host10, host11],
    'compute': [host12, host13],
    'collector': [host1, host2, host3],
    'webui': [host1, host2, host3],
    'database': [host1, host2, host3],
    'build': [host_build],
     #storage-master should be openstack
    'storage-master': [host7, host8, host9],
    'storage-compute': [host12, host13],
    # 'vgw': [host4, host5], # Optional, Only to enable VGW. Only compute can support vgw
    # 'tsn': [host1], # Optional, Only to enable TSN. Only compute can support TSN
    # 'toragent': [host1], Optional, Only to enable Tor Agent. Only compute can
    # support Tor Agent
    #   'backup':[backup_node],  # only if the backup_node is defined
}

env.hostnames = {
    'all': [
            'ctrlcfg-node0',
            'ctrlcfg-node1',
            'ctrlcfg-node2',
#            'analytics-node0',
#            'analytics-node1',
#            'analytics-node2',
            'openstack-node0',
            'openstack-node1',
            'openstack-node2',
            #'oblocknode05',
            #'oblocknode06',
            'oblocknode07',
            'oblocknode08',
           ]
}

#Openstack admin password
env.openstack_admin_password = 'contrail123'

# Passwords of each host
# for passwordless login's no need to set env.passwords,
# instead populate env.key_filename in testbed.py with public key.
env.passwords = {
    host1: 'contrail123',
    host2: 'contrail123',
    host3: 'contrail123',
#    host4: 'contrail123',
#   host5: 'contrail123',
#   host6: 'contrail123',
    host7: 'contrail123',
    host8: 'contrail123',
    host9: 'contrail123',
    #host10: 'contrail123',
    #host11: 'contrail123',
    host12: 'contrail123',
    host13: 'contrail123',
    #  backup_node: 'secret',
    host_build: 'contrail123',
}

# SSH Public key file path for passwordless logins
# if env.passwords is not specified.
#env.key_filename = '/root/.ssh/id_rsa.pub'

#For reimage purpose
env.ostypes = {
    host1: 'ubuntu',
    host2: 'ubuntu',
    host3: 'ubuntu',
#   host4: 'ubuntu',
#   host5: 'ubuntu',
#   host6: 'ubuntu',
    host7: 'ubuntu',
    host8: 'ubuntu',
    host9: 'ubuntu',
    #host10: 'ubuntu',
    #host11: 'ubuntu',
    host12: 'ubuntu',
    host13: 'ubuntu',
}
env.orchestrator = 'openstack' #other values are 'vcenter', 'none' default:openstack

#ntp server the servers should point to
#env.ntp_server = 'ntp.juniper.net'

# OPTIONAL COMPUTE HYPERVISOR CHOICE:
#======================================
# Compute Hypervisor
#env.hypervisor = {
#    host5: 'docker',
#    host6: 'libvirt',
#    host10: 'docker',
#}
#  Specify the hypervisor to be provisioned in the compute node.(Default=libvirt)


# INFORMATION FOR DB BACKUP/RESTORE ..
#=======================================================
#Optional,Backup Host configuration if it is not available then it will put in localhost
#backup_node = 'root@2.2.2.2'

# Optional, Local/Remote location of backup_data path
# if it is not passed then it will use default path
#backup_db_path= ['/home/','/root/']
#cassandra backup can be defined either "full" or "custom"
#full -> take complete snapshot of cassandra DB
#custom -> take snapshot except defined in skip_keyspace
#cassandra_backup='custom'  [ MUST OPTION]
#skip_keyspace=["ContrailAnalytics"]  IF cassandra_backup is selected as custom
#service token need to define to do  restore of backup data
#service_token = '53468cf7552bbdc3b94f'


#OPTIONAL ANALYTICS CONFIGURATION
#================================
# database_dir is the directory where cassandra data is stored
#
# If it is not passed, we will use cassandra's default
# /var/lib/cassandra/data
#
#database_dir = '<separate-partition>/cassandra'
#
# analytics_data_dir is the directory where cassandra data for analytics
# is stored. This is used to seperate cassandra's main data storage [internal
# use and config data] with analytics data. That way critical cassandra's
# system data and config data are not overrun by analytis data
#
# If it is not passed, we will use cassandra's default
# /var/lib/cassandra/data
#
#analytics_data_dir = '<separate-partition>/analytics_data'
#
# ssd_data_dir is the directory where cassandra can store fast retrievable
# temporary files (commit_logs). Giving cassandra an ssd disk for this
# purpose improves cassandra performance
#
# If it is not passed, we will use cassandra's default
# /var/lib/cassandra/commit_logs
#
#ssd_data_dir = '<seperate-partition>/commit_logs_data'

#following variables allow analytics data to have different TTL in cassandra database
#analytics_config_audit_ttl controls TTL for config audit logs
#analytics_statistics_ttl controls TTL for stats
#analytics_flow_ttl controls TTL for flow data
#database_ttl controls TTL for rest of the data
#
database_ttl = 24
analytics_config_audit_ttl = 24
analytics_statistics_ttl = 24
analytics_flow_ttl = 2

#following parameter allows to specify minimum amount of disk space in the analytics
#database partition, if configured amount of space is not present, it will fail provisioning
minimum_diskGB = 50

#OPTIONAL BONDING CONFIGURATION
#==============================
#Inferface Bonding
#bond= {
#    host2 : { 'name': 'bond0', 'member': ['p2p0p0','p2p0p1','p2p0p2','p2p0p3'], 'mode': '802.3ad', 'xmit_hash_policy': 'layer3+4' },
#    host5 : { 'name': 'bond0', 'member': ['p4p0p0','p4p0p1','p4p0p2','p4p0p3'], 'mode': '802.3ad', 'xmit_hash_policy': 'layer3+4' },
#}

#OPTIONAL SEPARATION OF MANAGEMENT AND CONTROL + DATA and OPTIONAL VLAN INFORMATION
#==================================================================================
control_data = {
    host1 : { 'ip': '172.16.80.20/24', 'gw' : '172.16.80.254', 'device':'eth1' },
    host2 : { 'ip': '172.16.80.23/24', 'gw' : '172.16.80.254', 'device':'eth1' },
    host3 : { 'ip': '172.16.80.26/24', 'gw' : '172.16.80.254', 'device':'eth1' },
    #host4 : { 'ip': '172.16.80.21/24', 'gw' : '172.16.80.254', 'device':'eth1' },
    #host5 : { 'ip': '172.16.80.24/24', 'gw' : '172.16.80.254', 'device':'eth1' },
    #host6 : { 'ip': '172.16.80.27/24', 'gw' : '172.16.80.254', 'device':'eth1' },
    host7 : { 'ip': '172.16.80.22/24', 'gw' : '172.16.80.254', 'device':'eth1' },
    host8 : { 'ip': '172.16.80.25/24', 'gw' : '172.16.80.254', 'device':'eth1' },
    host9 : { 'ip': '172.16.80.28/24', 'gw' : '172.16.80.254', 'device':'eth1' },
    #host10 : { 'ip': '172.16.80.5/24', 'gw' : '172.16.80.254', 'device':'bond0' },
    #host11 : { 'ip': '172.16.80.6/24', 'gw' : '172.16.80.254', 'device':'bond0' },
    host12 : { 'ip': '172.16.80.7/24', 'gw' : '172.16.80.254', 'device':'bond0' },
    host13 : { 'ip': '172.16.80.8/24', 'gw' : '172.16.80.254', 'device':'bond0' },
}

#OPTIONAL STATIC ROUTE CONFIGURATION
#===================================
#static_route  = {
#    host2 : [{ 'ip': '10.1.1.0', 'netmask' : '255.255.255.0', 'gw':'192.168.10.254', 'intf': 'bond0' },
#             { 'ip': '10.1.2.0', 'netmask' : '255.255.255.0', 'gw':'192.168.10.254', 'intf': 'bond0' }],
#    host5 : [{ 'ip': '10.1.1.0', 'netmask' : '255.255.255.0', 'gw':'192.168.10.254', 'intf': 'bond0' }],
#}

#storage compute disk config
storage_node_config = {
    host12 : { 'disks' : ['/dev/sdc:/dev/sdf', '/dev/sdd:/dev/sdf', '/dev/sde:/dev/sdf'] },
    host13 : { 'disks' : ['/dev/sdc:/dev/sdf', '/dev/sdd:/dev/sdf', '/dev/sde:/dev/sdf'] },
}

#storage_node_config = {
#    host10 : { 'disks' : ['/dev/sdc', '/dev/sdd'], 'journal' : ['/dev/sde', '/dev/sdf'] },
#    host11 : { 'disks' : ['/dev/sdc:/dev/sde', '/dev/sdd:/dev/sde'], 'ssd-disks' : ['/dev/sdf', '/dev/sdg'] },
#}
#
#Set Storage replica
#storage_replica_size = 2

#Base Openstack live migration configuration.
#live_migration = True
#Fix uid/gid for nova/libvirt-qemu so the ids are same across all nodes.
#nova_uid_fix = True

#Following are NFS based live migration configuration
#Enable this for External NFS server based live migration
#ext_nfs_livem = True
#ext_nfs_livem_mount = '11.1.0.1:/nfsvol'

#Enable this for Ceph based NFS VM server based live migration
#ceph_nfs_livem = True
#ceph_nfs_livem_subnet = '192.168.10.253/24'
#ceph_nfs_livem_image = '/ubuntu/livemnfs.qcow2'
#ceph_nfs_livem_host = host4

#To disable installing contrail interface rename package
env.interface_rename = False


#Path where the CA certificate file is stored on the node where fab is run.
#Fab copies the file to node where TOR agent is run.
#This is optional and is required only when tor_ovs_protocol is pssl.
#The certificates on the TOR are based on this CA cert.
#env.ca_cert_file = '/root/file.pem'

#In environments where keystone is deployed outside of Contrail provisioning
#scripts , you can use the below options
#
# Note :
# "insecure" is applicable only when protocol is https
# The entries in env.keystone overrides the below options which used
# to be supported earlier :
#  service_token
#  keystone_ip
#  keystone_admin_user
#  keystone_admin_password
#  region_name
#
#env.keystone = {
#    'keystone_ip'     : 'x.y.z.a',
#    'auth_protocol'   : 'http',                  #Default is http
#    'auth_port'       : '35357',                 #Default is 35357
#    'admin_token'     : '33c57636fbc2c5552fd2',  #admin_token in keystone.conf
#    'admin_user'      : 'admin',                 #Default is admin
#    'admin_password'  : 'contrail123',           #Default is contrail123
#    'nova_password'   : 'contrail123',           #Default is the password set in admin_password
#    'neutron_password': 'contrail123',           #Default is the password set in admin_password
#    'service_tenant'  : 'service',               #Default is service
#    'admin_tenant'    : 'admin',                 #Default is admin
#    'region_name'     : 'RegionOne',             #Default is RegionOne
#    'insecure'        : 'True',                  #Default = False
#    'manage_neutron'  : 'no',                    #Default = 'yes' , Does configure neutron user/role in keystone required.
#}
#

#env.nova = {
#    'cpu_mode': 'host-passthrough', # Possible options: none, host-passthrough, host-model, and custom
#                                    # if cpu_mode is 'custom' specify cpu_model option too
#    'cpu_model': 'Nehalem',         # relevant only if cpu_mode is 'custom'
#}

# In Openstack or Contrail High Availability setups.
# internal_vip          : Virtual IP of the openstack HA Nodes in the data/control(internal) nerwork,
#                         all the Openstack services behind this VIP are accessed using this VIP.
# external_vip          : Virtual IP of the Openstack HA Nodes in the management(external) nerwork,
#                         Openstack dashboard and novncproxy  services behind this VIP are accessed using this VIP.
# contrail_internal_vip : Virtual IP of the Contrail HA Nodes in the data/control(internal) nerwork,
#                         all the Contrail services behind this VIP is accessed using this VIP.
# contrail_external_vip : Virtual IP of the Contrail HA Nodes in the management(external) nerwork,
#                         Contrail introspects are are accessed using this VIP.
# nfs_server            : NFS server to be used to store the glance images.
# nfs_glance_path       : NFS server image path, which will be mounted on the Openstack Nodes and
#                         the glance images will be placed/accesed in/from this location.
# internal_virtual_router_id : Virtual router ID for the Openstack HA nodes in control/data(internal) network.
# external_virtual_router_id : Virtual router ID for the Openstack HA nodes in management(external) network.
# contrail_internal_virtual_router_id : Virtual router ID for the Contrail HA nodes in control/data(internal) network.
# contrail_external_virtual_router_id : Virtual router ID for the Contrail HA nodes in  management(external) network.
env.ha = {
    'internal_vip'   : '172.16.80.222',               #Internal Virtual IP of the openstack HA Nodes.
    'external_vip'   : '172.16.70.222',               #External Virtual IP of the openstack HA Nodes.
    'contrail_internal_vip'   : '172.16.80.220',       #Internal Virtual IP of the contrail HA Nodes.
    'contrail_external_vip'   : '172.16.70.220',       #External Virtual IP of the contrail HA Nodes.
#    'nfs_server'      : '3.3.3.3',                #IP address of the NFS Server which will be mounted to /var/lib/glance/images of openstack Node, Defaults to env.roledefs['compute'][0]
#    'nfs_glance_path' : '/var/tmp/images/',       #NFS Server path to save images, Defaults to /var/tmp/glance-images/
    'internal_virtual_router_id' :  180,                   #Default = 100
    'external_virtual_router_id' :  190,          #Default = 100
    'contrail_internal_virtual_router_id' :  200, #Default = 100
    'contrail_external_virtual_router_id' :  210, #Default = 100
}

# In environments where openstack services are deployed independently
# from contrail, you can use the below options
# service_token : Common service token for for all services like nova,
#                 neutron, glance, cinder etc
# amqp_host     : IP of AMQP Server to be used in openstack
# manage_amqp   : Default = 'no', if set to 'yes' provision's amqp in openstack nodes and
#                 openstack services uses the amqp in openstack nodes instead of config nodes.
#                 amqp_host is neglected if manage_amqp is set
#
#env.openstack = {
#    'service_token' : '33c57636fbc2c5552fd2', #Common service token for for all openstack services
#    'amqp_host' : '10.204.217.19',            #IP of AMQP Server to be used in openstack
#    'manage_amqp' : 'yes',                    #Default no, Manage seperate AMQP for openstack services in openstack nodes.
#    'osapi_compute_workers' : 40,             #Default 40, For low memory system reduce the osapi compute workers thread.
#    'conductor_workers' : 40,                 #Default 40, For low memory system reduce the conductor workers thread.
#}

# Link-Local Metadata Service
# By default fab scripts will retrieve metadata secret from openstack node.
# To override, Specify Metadata proxy secret from Openstack node
#neutron_metadata_proxy_shared_secret = <secret>

#To enable multi-tenancy feature
multi_tenancy = True

#To enable haproxy feature
#haproxy = True

#To Enable prallel execution of task in multiple nodes
#do_parallel = True

# To configure the encapsulation priority. Default: MPLSoGRE
#env.encap_priority =  "'MPLSoUDP','MPLSoGRE','VXLAN'"

# Optional proxy settings.
# env.http_proxy = os.environ.get('http_proxy')

#To enable LBaaS feature
# Default Value: False
env.enable_lbaas = True

# Ceilometer enable/disable installation and provisioning
# Default Value: False
#enable_ceilometer = True

# Ceilometer polling interval for meters in seconds
# Default Value: 600
#ceilometer_polling_interval = 600

# Ceilometer data TTL in seconds
# Default Value: 7200
#ceilometer_ttl = 7200

#OPTIONAL REMOTE SYSLOG CONFIGURATION
#===================================
#For R1.10 this needs to be specified to enable rsyslog.
#For Later releases this would be enabled as part of provisioning,
#with following default values.
#
#port = 19876
#protocol = tcp
#collector = dynamic i.e. rsyslog clients will connect to servers in a round
#                         robin fasion. For static collector all clients will
#                         connect to a single collector. static - is a test
#                         only option.
#status = enable
#
#env.rsyslog_params = {'port':19876, 'proto':'tcp', 'collector':'dynamic', 'status':'enable'}

#OPTIONAL Virtual gateway CONFIGURATION
#=======================================

#Section vgw is only relevant when you want to use virtual gateway feature.
#You can use one of your compute node as  gateway .

#Definition for the Key used
#-------------------------------------
#vn: Virtual Network fully qualified name. This particular VN will be used by VGW.
#ipam-subnets: Subnets used by vn. It can be single or multiple
#gateway-routes: If any route is present then only those routes will be published
#by VGW or Default route (0.0.0.0) will be published


#env.vgw = {host4: {'vgw1':{'vn':'default-domain:admin:public:public', 'ipam-subnets': ['10.204.220.128/29', '10.204.220.136/29', 'gateway-routes': ['8.8.8.0/24', '1.1.1.0/24']}]},
#                   'vgw2':{'vn':'default-domain:admin:public1:public1', 'ipam-subnets': ['10.204.220.144/29']}},
#           host5: {'vgw2':{'vn':'default-domain:admin:public1:public1', 'ipam-subnets': ['10.204.220.144/29']}}
#          }

#OPTIONAL optional tor agent and tsn CONFIGURATION
#==================================================
#Section tor agent is only relevant when you want to use Tor Agent feature.
#You can use one of your compute node as  Tor Agent . Same or diffrent compute
#node should be enable as tsn

#Definition for the Key used
#-------------------------------------
# tor_ip: IP of the tor switch
# tor_agent_id: Unique Id of the tor switch to identify. Typicaly a numeric value.
# tor_agent_name: Unique name for TOR Agent. This is an optional field. If this is
#                 not specified, name used will be <hostname>-<tor_agent_id>
# tor_type: Always ovs
# tor_ovs_port: Port number to be used by ovs. If any redundant TOR Agent is
#               specified for this tor-agent, it should have the same 'tor_ovs_port'
# tor_ovs_protocol: Connection protocol between TOR Agent and TOR (tcp / pssl)
# tor_tsn_ip: TSN node ip
# tor_tsn_name: Name of the TSN node
# tor_name: Name of the tor switch. If any redundant TOR Agent is specified for
#           this tor-agent, it should have the same 'tor_name'
# tor_tunnel_ip: Data plane IP for the tor switch
# tor_vendor_name: Vendor type for TOR switch
# tor_product_name: Product name of TOR switch. This is an optional field.
# tor_agent_http_server_port: HTTP server port. Same will be used by tor agent for introspect
# tor_agent_ovs_ka: Tor Agent OVSDB keepalive timer in milli seconds
#
#env.tor_agent = {host10:[{
#                    'tor_ip':'10.204.217.39',
#                    'tor_agent_id':'1',
#                    'tor_agent_name':'nodexx-1',
#                    'tor_type':'ovs',
#                    'tor_ovs_port':'9999',
#                    'tor_ovs_protocol':'tcp',
#                    'tor_tsn_ip':'10.204.221.35',
#                    'tor_tsn_name':'nodec45',
#                    'tor_name':'bng-contrail-qfx51-2',
#                    'tor_tunnel_ip':'34.34.34.34',
#                    'tor_vendor_name':'Juniper',
#                    'tor_product_name':'QFX5100',
#                    'tor_agent_http_server_port': '9010',
#                    'tor_agent_ovs_ka': '10000',
#                       }]
#                }
#######################################
#vcenter provisioning
#server is the vcenter server ip
#port is the port on which vcenter is listening for connection
#username is the vcenter username credentials
#password is the vcenter password credentials
#auth is the autentication type used to talk to vcenter, http or https
#datacenter is the datacenter name we are operating on
#cluster is the list of clusters we are operating on
#dv_switch_fab section contains distributed switch related params for fab network
#       dv_switch_name
#dv_port_group_fab section contains distributed port group params for fab network
#       dv_portgroup_name and the number of ports the group has
#dvswitch section contains distributed switch related para,s
#       dv_switch_name
#dvportgroup section contains the distributed port group info
#       dv_portgroupname and the number of ports the group has
######################################
#env.vcenter = {
#        'server':'127.0.0.1',
#        'port': '443',
#        'username': 'administrator@vsphere.local',
#        'password': 'Contrail123!',
#        'auth': 'https',
#        'datacenter': 'kd_dc',
#        'cluster': ['kd_cluster_1','kd_cluster_2'],
#        'dv_switch_fab': {'dv_switch_name': 'dvs-lag'},
#        'dv_port_group_fab': {
#                'dv_portgroup_name': 'fab-pg',
#                'number_of_ports': '3',
#         },
#        'dv_switch': { 'dv_switch_name': 'kd_dvswitch',
#                     },
#        'dv_port_group': { 'dv_portgroup_name': 'kd_dvportgroup',
#                           'number_of_ports': '3',
#                     },
#}
#
####################################################################################
# The compute vm provisioning on ESXI host
# This section is used to copy a vmdk on to the ESXI box and bring it up
# the contrailVM which comes up will be setup as a compute node with only
# vrouter running on it. Each host has an associated esxi to it.
#
# esxi_host information:
#    ip: the esxi ip on which the contrailvm(host/compute) runs
#    username: username used to login to esxi
#    password: password for esxi
#    fabric_vswitch: the name of the underlay vswitch that runs on esxi
#                    optional, defaults to 'vswitch0'
#    fabric_port_group: the name of the underlay port group for esxi
#                       optional, defaults to contrail-fab-pg'
#    uplinck_nic: the nic used for underlay
#                 optional, defaults to None
#    data_store: the datastore on esxi where the vmdk is copied to
#    cluster: name of the cluster to which this esxi is added
#    contrail_vm information:
#        uplink: The SRIOV or Passthrough PCI Id(04:10.1). If not provided
#                will default to vmxnet3 based fabric uplink
#        mac: the virtual mac address for the contrail vm
#        host: the contrail_vm ip in the form of 'user@contrailvm_ip'
#        vmdk: the absolute path of the contrail-vmdk used to spawn vm
#              optional, if vmdk_download_path is specified
#        vmdk_download_path: download path of the contrail-vmdk.vmdk used to spawn vm
#                            optional, if vmdk is specified
######################################################################################
#esxi_hosts = {
#       'esxi': {
#             'ip': '1.1.1.1',
#             'username': 'root',
#             'password': 'c0ntrail123',
#             'datastore': "/vmfs/volumes/ds1",
#             'cluster': "kd_cluster_1",
#             'contrail_vm': {
#                   'mac': "00:50:56:05:ba:ba",
#                   'host': "root@2.2.2.2",
#                   'vmdk_download_path': "http://10.84.5.100/vmware/vmdk/ContrailVM-disk1.vmdk",
#             }
#       }
# OPTIONAL DPDK CONFIGURATION
# ===========================
# If some compute nodes should use DPDK vRouter version it has to be put in
# env.dpdk dictionary. The format is:
# env.dpdk = {
#     host1: { 'huge_pages' : '50', 'coremask' : '0xf' },
#     host2: { 'huge_pages' : '50', 'coremask' : '0,3-7' },
# }
# huge_pages - Specify what percentage of host memory should be reserved
#              for access with huge pages
# coremask   - Specify CPU affinity mask to run vRouter with. Supported formats:
#              hexadecimal, comma-sepparated list of CPUs, dash-separated range
#              of CPUs.
# OPTIONAL vrouter limit parameter
# ==================================
#env.vrouter_module_params = {
#     host4:{'mpls_labels':'131072', 'nexthops':'131072', 'vrfs':'65536', 'macs':'262144'},
#     host5:{'mpls_labels':'131072', 'nexthops':'131072', 'vrfs':'65536', 'macs':'262144'}
#}
#
# OPTIONAL md5 key enabling
# There are 2 ways of enabling BGP md5 key on node apart from the webui.
# 1. Before provisioning the node, include an env dict in testbed.py as shown below specifying the desired key value #    on the node. The key should be of type "string" only.
# 2. If md5 is not included in testbed.py and the node is already provisioned, you can run the
#    contrail-controller/src/config/utils/provision_control.py script with a newly added argument for md5
# The below env dict is for first method specified, where you include a dict in testbed.py as shown below:
#  env.md5 = {
#     host1: 'juniper',
#     host2: 'juniper',
#     host3: 'juniper',
#  }
# 'juniper' is the md5 key that will be configured on the nodes.
