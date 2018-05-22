## Steps to restore Config DB 
#### Tested on Contrail All-in-one R3.2.9 version

1. Backup the config db, using the below command [Got config_db from customer's cluster]
```
 python db_json_exim.py --export-to config-db-dump.json
```
2. Below steps to restore the backed up DB, performed in step 1.
    -   Stop all the contrail services including zookeeper
        ```
        service supervisor-config restart
        service supervisor-vrouter stop
        service supervisor-control stop
        service supervisor-analytics stop
        service supervisor-config stop
        service supervisor-database stop
        service contrail-database stop
        service zookeeper stop
        ```
    -   Backup the existing cassandra and zookeeper database
    
