import os
import sys
import psutil
from oslo_config import cfg
from utils import helpers
from utils.configsk import configSetup
import re
from netaddr import IPNetwork
from utils.helpers import execute, from_project_root, get_project_root
from utils.remoteoperations import RemoteConnection
from time import sleep, strftime
from run_sanity_tcs import runSanityTestCases

CONF = cfg.CONF
SK_ENV_FILE = 'starterkit_env.conf'

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

class postSanity(object):

    def __init__(self):
        install_dir = helpers.from_project_root('conf/')
        cfg_file = os.path.join(install_dir, SK_ENV_FILE)
        if not os.path.exists(os.path.join(install_dir, SK_ENV_FILE)):
            print "Missing required configuration file {}".format(cfg_file)
            sys.exit(1)
        print "Configuration file {} exists".format(cfg_file)

    def check_contrail_status(self):
        print "Checking contrail-status on the contrail controller node"
        cc_name = CONF['DEFAULTS']['reimagevms'][0]
        os_name = CONF['DEFAULTS']['reimagevms'][1]
        cc_ip = get_ip(CONF[cc_name]['management_address'])
        cc_ctrld_ip = get_ip(CONF[cc_name]['ctrldata_address'])
        os_ctrld_ip = get_ip(CONF[os_name]['ctrldata_address'])
        user = CONF['DEFAULTS']['root_username']
        passwd = CONF['DEFAULTS']['root_password']
        reconnect = RemoteConnection()
        reconnect.connect(cc_ip, username=user, password=passwd)
        cmd = 'contrail-status'
        res = reconnect.execute_cmd(cmd, timeout=20)
        if re.search(r'NTP state|inactive', res, re.M|re.I):
            print "\n"
            print "Command: %s"%(cmd)
            print "Response: %s"%(res)
            print "========================================================================================="
            print "contrail services on controller show in NTP state unsynchronized/inactive. please check."
            print "========================================================================================="
            sys.exit(1)
        else:
            print "All the services on contrail controller shows active. Installation successfully done."

if __name__ == '__main__':

    pSanity = postSanity()

    #read conf file
    config = configSetup()
    config.set_base_config_options()

    try:
        config.load_configs(['conf/{}'.format(SK_ENV_FILE)])
        print "Loaded configuration file successfully"
    except cfg.RequiredOptError as e:
        print "Missing required input in starterkit_env.conf file, {0}: {1}".format(SK_ENV_FILE, e)
        sys.exit(1)

    config.set_deploy_virtual_server_config_options()
    config.set_deploy_physical_server_config_options()

    #check contrail-status before running the test cases
    pSanity.check_contrail_status()

    #run sanity testcases
    rSanity = runSanityTestCases()
    rSanity.upload_image_os()
    sys.exit(0)
