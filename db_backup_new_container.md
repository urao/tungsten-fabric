#### Steps to backup config database without stopping containers
##### Tested with 1909.30 version

1. Create temp directory
```
mkdir /temp
mkdir /temp/tmp-config-dir
```
2. Copy `contrail-api.conf` file to the above temp directory
```
docker cp config_api_1:/etc/contrail/contrail-api.conf /temp/tmp-config-dir
```
3. Run config-api container
```
docker image ls | grep config-api
docker run --rm -it -v /temp/tmp-config-dir/:/tmp/ -v /etc/contrail/ssl/controller/:/etc/contrail/ssl/:ro \
   --network host --entrypoint=/bin/bash hub.juniper.net/contrail/contrail-controller-config-api:<version>
```
4. Run the command
```
cd /usr/lib/python2.7/site-packages/cfgm_common
python db_json_exim.py --export-to /tmp/db-dump.json --api-conf /temp/tmp-config-dir/contrail-api.conf
```
```
python db_manage.py --api-conf /etc/contrail/contrail-api.conf --verbose check_virtual_networks_id
python db_manage.py --api-conf /etc/contrail/contrail-api.conf \
            check --log_file /root/db_manage_check_op_cluster
```
