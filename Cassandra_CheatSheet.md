## Debug Cassandra 
### Execute below commands on config_DB node

```
netstat -tpunl | grep 9161
docker exec -it config_database_1 bash
pycassaShell -k config_db_uuid -H <IP_ADDRESS>:9161
OBJ_UUID_TABLE.get('uuid')
dict(OBJ_UUID_TABLE.get('uuid'))
OBJ_FQNAME_TABLE.get('route_targets')
OBJ_FQNAME_TABLE.get('project', column_count=10000)
OBJ_UUID_TABLE.remove('f6d9a1a5-1bd5-48be-89f5-2b4689e001e7',\
               columns=['parent:virtual_network:1424f5b2-0750-4958-b759-f16678aa3b 6']) 
OBJ_UUID_TABLE.insert('f6d9a1a5-1bd5-48be-89f5-2b4689e001e7',\
               {'parent:virtual_network:71ac7795-6f1e-4a98-ad84-d87e91af0edb':'nul '}) 
OBJ_UUID_TABLE.get('f6d9a1a5-1bd5-48be-89f5-2b4689e001e7') 
docker restart config_api_1 > All on 3 controllers
```

```
nodetool status
nodetool tpstats
nodetool cfstats -H > cass_size.txt;cat cass_size.txt | egrep "Keyspace|Table:|GB"
nodetool -p 7201 info
docker exec -it config_database_cassandra_1 nodetool repair -p 7201 -pr
docker exec -it config_database_cassandra_1 nodetool repair -p 7201 -pr --full
```
