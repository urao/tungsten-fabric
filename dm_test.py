#!/usr/bin/env python

# Script helps to do a quick sanity check whether DM is working correctly or not
# Provide Junos Device IP address, username and password

from ncclient import manager
from ncclient.xml_ import new_ele
from lxml import etree

device_ip = "10.8.8.1"
username = "root"
password = "test123"

try:
    with manager.connect(host=device_ip, port=22, username=username,
         password=password, timeout=10, device_params = {'name':'junos'},
         unknown_host_cb=lambda x, y: True) as m:
        rpc = new_ele('get-software-information')
        result = m.rpc(rpc)
        print 'Product Model:', result.xpath('//software-information/product-model')[0].text
        print 'Product Name:', result.xpath('//software-information/product-name')[0].text

        e = result.xpath("//software-information/package-information[name='junos-version']")[0]
        version = e.find('comment').text
        print 'Version:' + version

        xml = m.get()
        print xml.xpath("//configuration/version")[0].text
        print xml.xpath("//interfaces")
        for e in xml.xpath("//interfaces/interface[name='lo0']"):
            #if e.find('name').text == 'lo0':
            print etree.tostring(e, pretty_print=True)
except:
    raise
