## Steps to restore Config DB 
#### Tested on Contrail All-in-one R3.2.9 version

1. Backup the config db, using the below command [Could be on customer's cluster]
```
 python db_json_exim.py --export-to config-db-dump.json
```
2. Below steps to restore the backed up DB, performed in step 1.
    -   Stop all the contrail services including zookeeper
        ```
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
        mkdir -p /var/lib/zookeeper/data/version-2-orig
        cp -R /var/lib/zookeeper/data/version-2/* /var/lib/zookeeper/data/version-2-orig
        rm -rf /var/lib/zookeeper/data/version-2/*
        ```
    -   Start cassandra and zookeeper services
        ```
        service contrail-database start
        service zookeeper start
        ```
    -   Import DB
        ```
        python db_json_exim.py --import-to config-db-dump.json
        ```
    -   Start all the contrail services
        ```
        service supervisor-control start
        service supervisor-analytics start
        service supervisor-config start
        service supervisor-database start
        service supervisor-vrouter start
        ```
    -   Verify all the contrail services
        ```
        contrail-status
        ```
    
### Reference 
[Contrail Wiki](https://github.com/Juniper/contrail-controller/wiki/Backing-up-contrail-configuration-in-json-format)
