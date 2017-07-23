import sys
import time
from netaddr import IPNetwork
from pprint import pprint
from novaclient import nclient
import keystoneclient.v2_0.client as ksclient
import glanceclient.v2.client as glclient


class openstackApi(object):

    def __init__(self, kcreds, ncreds):
        self._keystone = ksclient.Client(**kcreds)
        glance_endpoint = keystone.service_catalog.url_for(service_type='image',endpoint_type='publicURL')
        self._glance =  glclient.Client(glance_endpoint, token=self._keystone.auth_token)
        self._nova = nclient.Client('2', **ncreds)


    def create_image(self, name, filename, dformat, cformat):
        print "Create image %s onto openstack glance"%(name)

        image = self._glance.images.create(name=name, disk_format=dformat, container_format=cformat)
        self._glance.images.upload(image.id, open(filename, 'rb'))
        return image

    def get_image_list(self):
        return self._nova.images.list()

    def get_network_list(self):
        return self._nova.networks.list()

    def get_flavor(self, ftype):
        return self._nova.flavors.find(name=ftype)

    def get_compute_list(self):
        hosts = self._nova.services.list(binary='nova-compute')
        return [h.host for h in hosts if h.status=='enabled' and h.state=='up']

    def get_network_id(self, networkname):
        network = self._nova.networks.find(lable=networkname)
        return network.id

    def create_instance(self, instname, imageid, flavor, netname, azone, count=1):
        response = self._nova.servers.create(name=instname, image=imageid, 
                flavor=self.get_flavor(flavor), nics=[{'net-id': self.get_network_id(netname)}], 
                availability_zone=azone, max_count=count)
        status = response.status
        print "Current status %s"%(status)

        while status == 'BUILD':
            time.sleep(5)
            response = self._nova.servers.get(response.id)
            status = response.status
        print "Expected status %s"%(status)
        return response

    def get_instance_details(self, instid):
        server = self._nova.servers.find(id=instid)
        return server

    def get_instance_ipaddress(self, instid):
        server = self._nova.servers.find(id=instid)
        return server.addresses

    def delete_instance(self, instname):
        server = self._nova.servers.find(name=instname)
        server.delete()

    def get_floating_ip_list(self):
        return self._nova.floating_ips.list()

    def attach_floating_ip_instance(self, instname, floatingip):
        instance = self._nova.servers.find(name=instname)
        instance.add_floating_ip(floatingip)

if __name__=='__main__':
    #api = openstackApi()
