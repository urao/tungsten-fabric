Contrail Software running R3.2.9 version.

1. Perform below steps 

    -   On all 3 controllers, stop contrail services including Zookeeper

        ```
        service supervisor-control stop
        service supervisor-config stop
        service contrail-database stop
        service zookeeper stop
        ```
    -   On all 3 controllers, verify contrail services including Zookeeper are inactive
        ```
        service supervisor-control status
        service supervisor-config status
        service contrail-database status
        service zookeeper status
        ```

    -   On all 3 analytics nodes, stop kafka service, since they use Zookeeper service 
        ```
        service kafka stop
        ```
    -   On all 3 analytics nodes, verify kafka service is STOPPED 
        ```
        service kafka status
        ```

    -   On all 3 controllers, backup the existing Cassandra database
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
    -   On all 3 controllers, backup the existing Zookeeper database
        ```
        mkdir -p /var/lib/zookeeper/version-2-orig
        cp -R /var/lib/zookeeper/version-2/* /var/lib/zookeeper/version-2-orig
        rm -rf /var/lib/zookeeper/version-2/*
        ```
    -   On all 3 controllers, start Cassandra and Zookeeper services
        ```
        service contrail-database start
        service zookeeper start
        ```
    -   On all 3 controllers, verify Cassandra and Zookeeper services are running
        ```
        service contrail-database status
        service zookeeper status
        ```
2. On one of the controller, 

    -   Import DB
        ```
        cd /usr/lib/python2.7/site-packages/cfgm_common/
        python db_json_exim.py --import-to <file_name_path>.json
        ```
3. On all 3 controllers

    -   Start all the contrail services
        ```
        service supervisor-control start
        service supervisor-config start
        ```
    -   Verify all the contrail services are “active”
        ```
        contrail-status
        ```
4. On all 3 analytics nodes

    -   Start kafka service
        ```
        service kafka start
        ```
    -   Verify the kafka service is “RUNNING”
        ```
        service kafka status
        ```
