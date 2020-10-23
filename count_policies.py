#!/usr/bin/python

# Count # of network policies in the config DB
import sys
import json
from collections import OrderedDict
import requests


def main():
    if len(sys.argv) != 2:
        print("Usage: count_policies.py <controller_ip>")
        sys.exit(1)

    ctrl_ip = sys.argv[1]
    print("Controller IP: {}".format(ctrl_ip))

    hdrs = {
            'Accept': 'application/json'
    }
    
    response = requests.get('http://{}:8082/network-policys'.format(ctrl_ip), hdrs)
    data = response.json()['network-policys']

    unsorted = {}
    for policy in data:
        try:
            name = policy['network-policy']['display_name']
            policy_entries = len(policy['network-policy']['network_policy_entries']['policy_rule'])
            unsorted[name] = policy_entries
        except Exception as e:
            pass


    sorted_data = OrderedDict(sorted(unsorted.items(), key=lambda x:x[1]))
    for k in sorted_data:
        print "{} ---- {}".format(k, sorted_data[k])

    print len(data)

if __name__ == "__main()__":
    sys.exit(0 if main() else 1)
