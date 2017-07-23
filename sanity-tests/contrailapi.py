import sys
from vnc_api import vnc_api 
from netaddr import IPNetwork
from pprint import pprint

def get_ip(ip_w_pfx):
    return str(IPNetwork(ip_w_pfx).ip)

def get_netmask(ip_w_pfx):
    return str(IPNetwork(ip_w_pfx).netmask)

class contrailVncApi(object):

    def __init__(self, username=None, password=None, tenant_name=None,
                api_server_host='127.0.0.1', api_server_port='8082',
                api_server_url=None, auth_host=None, domain_name='default-domain'):

        self._tenant_name = tenant_name
        self._domain = domain_name
        self._username = username
        self._password = password
        self._vnc_lib = vnc_api.VncApi(username=username, password=password, 
                tenant_name=tenant_name, api_server_host=api_server_host, auth_host=auth_host)

    def get_vn_list(self):
        print "Return list of all virtual networks"
        return self._vnc_lib.virtual_networks_list()

    def create_vn(self, vn_name, vn_subnetmask, vn_gw):
        print "Create virtual_network %s"%vn_name

        project = self._vnc_lib.project_read(fq_name=[self._domain, self._tenant_name])
        vn_obj = vnc_api.VirtualNetwork(name=vn_name, parent_obj=project)
        vn_subnet = vn_subnetmask.split('/')[0]
        vn_mask = int(vn_subnetmask.split('/')[1])

        vn_obj.add_network_ipam(vnc_api.NetworkIpam(), 
                vnc_api.VnSubnetsType([vnc_api.IpamSubnetType(subnet = vnc_api.SubnetType(vn_subnet,vn_mask), 
                    default_gateway = vn_gw)]))
        self._vnc_lib.virtual_network_create(vn_obj)

    def delete_vn(self, vn_name):
        print "Delete virtual_network %s"%vn_name
        try:
            self._vnc_lib.virtual_network_delete(fq_name=[self._domain, self._tenant_name, vn_name])
        except:
            print "Virtual network %s does not exist\n"%(vn_name)


    def create_networkpolicy(self, policy_name, vn1_name, vn2_name, action):
        print "Create network policy %s between %s <---> %s"%(policy_name, vn1_name, vn2_name)

        project = self._vnc_lib.project_read(fq_name=[self._domain, self._tenant_name])
        rule = vnc_api.PolicyRuleType(direction = '<>', protocol = 'any', 
                action_list = vnc_api.ActionListType(simple_action = action), 
                src_addresses = [vnc_api.AddressType(virtual_network = vn1_name)], 
                src_ports = [vnc_api.PortType(start_port = -1, end_port = -1)], 
                dst_addresses = [vnc_api.AddressType(virtual_network = vn2_name)], 
                dst_ports = [vnc_api.PortType(start_port = -1, end_port = -1)])

        policy = vnc_api.NetworkPolicy(name = policy_name, parent_obj = project, 
                network_policy_entries = vnc_api.PolicyEntriesType([rule]))
        self._vnc_lib.network_policy_create(policy)

    def delete_network_policy(self, policy_name):
        print "Delete network_policy %s"%policy_name

        try:
            self._vnc_lib.network_policy_delete(fq_name=[self._domain, self._tenant_name, policy_name])
        except:
            print "Network_Policy %s does not exist\n"%(policy_name)


    def attach_policy_to_vn(self, policy_name, vn_name):
        print "Attach network policy %s to virtual network %s"%(policy_name, vn_name)

        policy = self._vnc_lib.network_policy_read(fq_name=[self._domain, self._tenant_name, policy_name])

        policy_type = vnc_api.VirtualNetworkPolicyType(sequence = vnc_api.SequenceType(major = 0, minor = 0))
        vn = self._vnc_lib.virtual_network_read(fq_name = [self._domain, self._tenant_name, vn_name])
        vn.add_network_policy(ref_obj = policy, ref_data = policy_type)
        self._vnc_lib.virtual_network_update(vn)


if __name__=='__main__':
    api = contrailVncApi(username='admin', password='contrail', tenant_name='admin', api_server_host='10.87.28.249', auth_host='10.87.28.249')
    vn_list = api.get_vn_list()
    for vn in vn_list['virtual-networks']:
        pprint( vn['fq_name'] ) 
