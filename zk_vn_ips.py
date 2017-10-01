#IP address allocated in ZK DB for a specific VN
import sys
from pprint import pprint
import json
import kazoo.client
#hostname = 'node-292'
import netaddr

db_contents = {'cassandra': {},
               'zookeeper': {}}

def get_nodes(zk, path):
    #print zk, path
    return zk.get_children(path)

def main(argv):
    if len(sys.argv) < 5:
        print "Usage: script.py <zk_hostname> <project_name> <vn_name> <cidr_value>"
        print "Insufficient number of arguments, exiting!!!"
        sys.exit(1)

    zk_hostname = argv[0]
    project = argv[1]
    vn_name = argv[2]
    subnet = argv[3]
    vn_cmd = 'default-domain:'+project+':'+str(vn_name)+':'+subnet

    #collect the info
    zk = kazoo.client.KazooClient(zk_hostname)
    zk.start()
    vn_ip_list = get_nodes(zk, '/api-server/subnets/%s'%(vn_cmd))
    zk.stop()

    #print vn_ip_list
    for ip in vn_ip_list:
        print '{0} : {1}'.format(ip.encode("utf-8"), netaddr.IPAddress(ip.encode("utf-8")[1:]))


if __name__ == "__main__":
    main(sys.argv[1:])
