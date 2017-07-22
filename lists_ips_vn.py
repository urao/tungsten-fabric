# Provide admin user and password in the file or as an argument
# Usage 
# python vn_ips.py <vn_uuid>
# python vn_ips.py 8133c4f5-6291-42ec-8813-e0b071befa39

#!/usr/bin/env python

import sys
import argparse
import ConfigParser

from vnc_api.vnc_api import *
from cfgm_common.exceptions import *

class Get_IPs_Assigned_VN(object):
    def __init__(self, args_str=None):
        self._args = None
        if not args_str:
            args_str = ' '.join(sys.argv[1:])
        self._parse_args(args_str)

        #print self._args

        connected = False
        while not connected:
            try:
                self._vnc_lib = VncApi(
                    self._args.admin_user, self._args.admin_password,
                    self._args.admin_tenant_name,
                    self._args.api_server_ip,
                    self._args.api_server_port, '/')
                connected = True
            except ResourceExhaustionError: 
                time.sleep(3)

        vn_obj = self._vnc_lib.virtual_network_read(id=self._args.vn_uuid)
        print 'Lookup IPs for virtual-network %s(%s)' % (vn_obj.display_name, vn_obj.uuid)
        for iip_ref in vn_obj.get_instance_ip_back_refs() or []:
            try:
                iip_obj = self._vnc_lib.instance_ip_read(id=iip_ref['uuid'])
            except NoIdError:
                print '\tCannot fetch IIP %s' % iip_ref['uuid']
            print '\tInstanceUUID %s have IP %s' % (iip_obj.uuid, iip_obj.instance_ip_address)


    def _parse_args(self, args_str):

        # Source any specified config/ini file
        # Turn off help, so we print all options in response to -h
        conf_parser = argparse.ArgumentParser(add_help=False)

        conf_parser.add_argument("-c", "--conf_file",
                                 help="Specify config file", metavar="FILE")
        args, remaining_argv = conf_parser.parse_known_args(args_str.split())

        defaults = {
            'api_server_ip': '127.0.0.1',
            'api_server_port': '8082',
        }
        ksopts = {
            'admin_user': 'admin',
            'admin_password': 'contrail',
            'admin_tenant_name': 'admin',
        }

        if args.conf_file:
            config = ConfigParser.SafeConfigParser()
            config.read([args.conf_file])
            defaults.update(dict(config.items("DEFAULTS")))
            if 'KEYSTONE' in config.sections():
                ksopts.update(dict(config.items("KEYSTONE")))

        # Override with CLI options
        # Don't surpress add_help here so it will handle -h
        parser = argparse.ArgumentParser(
            # Inherit options from config_parser
            parents=[conf_parser],
            # print script description with -h/--help
            description=__doc__,
            # Don't mess with format of description
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )
        defaults.update(ksopts)
        parser.set_defaults(**defaults)

        parser.add_argument(
            "--api_server_ip", help="IP address of api server")
        parser.add_argument(
            "--api_server_port", help="Port of api server")
        parser.add_argument(
            "--admin_user", help="Name of keystone admin user")
        parser.add_argument(
            "--admin_password", help="Password of keystone admin user")
        parser.add_argument(
            "--admin_tenant_name", help="Tenant name for keystone admin user")
        parser.add_argument(
            "--openstack_ip", help="IP address of openstack auth node")
        parser.add_argument(
            "vn_uuid", help="UUID of the virtual network")
        self._args = parser.parse_args(remaining_argv)


def main(args_str=None):
    Get_IPs_Assigned_VN(args_str)

if __name__ == "__main__":
    main()
