## Steps to restore Config DB 
#### Tested on Contrail All-in-one R3.2.9 version

1. Backup the config db, using the below command [Could have got config_db from customer's cluster]
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
    -   Backup the existing cassandra database
        ```
        mkdir -p /var/lib/cassandra/data-orig
        mkdir -p /var/lib/cassandra/commitlog-orig
        mkdir -p /var/lib/cassandra/saved_caches-orig
        cp -R /var/lib/cassandra/data/* /var/lib/cassandra/data-orig
        cp -R /var/lib/cassandra/commitlog/* /var/lib/cassandra/commitlog-orig
        cp -R /var/lib/cassandra/saved_caches/* /var/lib/cassandra/saved_caches-orig
        rm -rf /var/lib/cassandra/data/*
        rm -rf /var/lib/cassandra/commitlog/*
        rm -rf /var/lib/cassandra/save_caches/*        
        ```
    -   Backup the existing zookeeper database
        ```
        mkdir -p /var/lib/cassandra/data-orig
        mkdir -p /var/lib/cassandra/commitlog-orig
        mkdir -p /var/lib/cassandra/saved_caches-orig
        cp -R /var/lib/cassandra/data/* /var/lib/cassandra/data-orig
        cp -R /var/lib/cassandra/commitlog/* /var/lib/cassandra/commitlog-orig
        cp -R /var/lib/cassandra/saved_caches/* /var/lib/cassandra/saved_caches-orig
        rm -rf /var/lib/cassandra/data/*
        rm -rf /var/lib/cassandra/commitlog/*
        rm -rf /var/lib/cassandra/save_caches/*        
        ```
    
