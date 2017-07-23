import os
import sys
import re
import ConfigParser
import subprocess
from oslo_config import cfg
from jinja2 import Environment, FileSystemLoader
from netaddr import IPNetwork
from time import sleep, strftime

from utils.helpers import execute, from_project_root, get_project_root
from utils.remoteoperations import RemoteConnection
from openstackapi import openstackApi
from contraiapi import contrailVncApi

CONF = cfg.CONF

sk_img_path = '/var/www/html/starterkit_images'

def get_ip(ip_w_pfx):
    return str(IPNetwork(ip_w_pfx).ip)

def get_netmask(ip_w_pfx):
    return str(IPNetwork(ip_w_pfx).netmask)

def waiting(count):
    for i in range(count):
        print ".",
        sys.stdout.flush()
        sleep(1)
    print "\n"


# read the config file
config = ConfigParser.RawConfigParser()
config.read('config.ini')

def get_keystone_creds():
    d = {}
    d['username'] = 'admin'
    d['password'] = CONF['DEFAULTS']['contrail_os_webui_passwd']
    d['auth_url'] = 'http://%s:5000/v2.0/'.%(get_ip(CONF['OPENSTACK']['ctrldata_address']))
    d['tenant_name'] = 'admin'
    return d

def get_nova_creds():
    d = {}
    d['username'] = 'admin'
    d['api_key'] = CONF['DEFAULTS']['contrail_os_webui_passwd']
    d['auth_url'] = 'http://%s:5000/v2.0/'.%(get_ip(CONF['OPENSTACK']['ctrldata_address']))
    d['project_id'] = 'admin'
    return d

class runSanityTestCases(object):

    def __init__(self):
        global jinja_env
        jinja_env = Environment(loader=FileSystemLoader(from_project_root('sanity')))

        #Check the reachability to api_server and auth_server
        password = CONF['DEFAULTS']['contrail_os_webui_passwd']
        api_server = CONF['CONTRAILCTRL']['ctrldata_address']
        auth_server = CONF['OPENSTACK']['ctrldata_address']
        self._imageid = None

        if self.checkPing(api_server) and self.checkPing(auth_server):
            print "Contrail API server (%s) and Keystone server (%s) is reachable"%(api_server,auth_server)
            #Get handle to OS and VNC API
            self._osapi = openstackApi(get_keystone_creds(), get_nova_creds())
            self._vncapi = contrailVncApi(username='admin', password=password, tenant_name='admin'
                        api_server_host=api_server, auth_host=auth_server)
        else:
            print "Contrail API server (%s) and Keystone server (%s) is not reachable"%(api_server,auth_server)
            sys.exit(1)

    def checkPing(self, server):
        try:
            output = subprocess.check_output("ping -c 5 "+server, shell=True)
        except Exception, e:
            return False

        return True

    def upload_image_os(self):
        cirros_image = CONF['DEFAULTS']['cirrosimage']
        image_file = sk_img_path+cirros_image
        self._imageid = self._osapi.create_image('cirros_sk', image_file, 'qcow2', 'bare')

    def testcase_1(self):

        #create vn1
        vn_name = config.get('VN1', 'name')
        vn_cidr = config.get('VN1', 'subnet')
        vn_gw = config.get('VN1', 'gateway')
        self._vncapi.create_vn(vn_name, vn_cidr, vn_gw)
        #create vm1 on server03
        computes = self._osapi.get_compute_list()
        vm1_compute = computes[0]
        vm1_id = self._osapi.create_instance('vn1-vm1', self._imageid, 'tiny', vn_name, vm1_compute)
        #create vm2 on server04
        vm2_compute = computes[1]
        vm2_id = self._osapi.create_instance('vn1-vm2', self._imageid, 'tiny', vn_name, vm2_compute)
        #ping from vm1-vm2, verify
        vm1_ip = self._osapi.get_instance_ipaddress(vm1_id)
        vm2_ip = self._osapi.get_instance_ipaddress(vm2_id)
        #delete vm1
        #delete vm2
        pass

    def testcase_2(self):
        #create vn1
        #create vn2
        #create vm1
        #create vm2
        #create policy pass
        #ping from vm1-vm2, verify
        #update policy deny
        #ping from vm1-vm2, verify
        #delete vm1
        #delete vm2
        pass

    def testcase_3(self):
        #create fip vn
        #create vn1
        #create vm1
        #attach fip to vm1
        #ping fip ip address, verify
        pass

    def testcase_4(self):
        #lbaas
        pass

    def testcase_5(self):
        #snat
        pass

    def testcase_6(self):
        #service-chain with vSRX
        pass


if __name__=='__main__':
    pprint( vn['fq_name'] )
