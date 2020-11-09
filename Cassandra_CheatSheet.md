## Debug Cassandra 
### Execute below commands on config_DB node

```
netstat -tpunl | grep 9160
docker exec -it config_database_1 bash
pycassaShell -k config_db_uuid -H <IP_ADDRESS>:9160
OBJ_UUID_TABLE.get('uuid')
dict(OBJ_UUID_TABLE.get('uuid'))
OBJ_FQNAME_TABLE.get('route_targets')
```

```
nodetool status
nodetool tpstats
nodetool cfstats
```
