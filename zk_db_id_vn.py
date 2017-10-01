#Prints VN/Id mapping to which VN name
#Ex: id : /id/virtual-networks/0000000362/  ===> virtual_network : default-domain:sample-project:sample-vn

# Change hostname in the below script and run it

import sys
from pprint import pprint
import json
import kazoo.client
hostname = 'cc-01'

db_contents = {'cassandra': {},
               'zookeeper': {}}

def get_nodes(zk, path):
    if not zk.get_children(path)
         return [(path, zk.get(path))]
    nodes = []
    for child in zk.get_children(path):
        nodes.extend(get_nodes('%s%s/' %(path, child)))
    return nodes
    
zk = kazoo.client.KazooClient(hostname)
zk.start()
nodes = get_nodes('/id/virtual-networks/')
zk.stop()

#print node
for id, details in nodes:
    print 'id : %s  ===> virtual_network : %s' %(id, details[0])
exit()
