#!/usr/bin/env bash
# Generate Keystone Token and set an ENV variable
# Change username and password, admin/contrail123 as per your settings and run

TOKEN=$(curl http://10.87.28.249:5000/v2/auth/tokens -s -i -H "Content-Type: application/json" -d '{ "auth": {"identity": {"methods": ["password"],"password": {"user": {"domain": { "id": "default" }, "name": "admin", "password": "contrail123"} } },"scope": {"project": { "domain": { "id": "default" }, "name": "admin" } } } }'  | grep ^X-Subject-Token: | awk '{print $2}')
echo $TOKEN
echo "exporting token"
export OS_TOKEN=$TOKEN
