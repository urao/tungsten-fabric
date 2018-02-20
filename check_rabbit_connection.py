#
#Connect to remote or local rabbitmq cluster to check the connectivity
#
#!/usr/bin/env python

from cfgm_common.vnc_kombu import VncKombuClient
import time

def lognprint(x, level):
    print x

def callb(x):
    print x
    
x = VncKombuClient('10.18.12.1:5672,10.18.12.2:5672,10.18.12.4:5672', '5672', 'guest', 'guest', '', False, 'vnc-config.issu-queue', callb, lognprint)

while (1):
    time.sleep(1)
    print x
