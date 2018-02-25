#
#Works for all-in-one contrail cluster based on unbuntu 14.04 contrail image
#
#!/usr/bin/env bash
set -e
#set -x

service supervisor-config stop
service supervisor-analytics stop
service zookeeper stop

backup_folder='/root/contrail_backup'

mkdir -p $backup_folder

#copy zk
cp -r /var/lib/zookeeper $backup_folder

#snapshot db
nodetool -h localhost -p 7199 snapshot config_db_uuid
nodetool -h localhost -p 7199 snapshot to_bgp_keyspace
nodetool -h localhost -p 7199 snapshot svc_monitor_keyspace
nodetool -h localhost -p 7199 snapshot dm_keyspace
nodetool -h localhost -p 7199 snapshot useragent

declare -a arr=("config_db_uuid" "to_bgp_keyspace" "svc_monitor_keyspace" "dm_keyspace" "useragent")
for key in "${arr[@]}"
do
   echo "$key"
   cd "/var/lib/cassandra/data/$key/"
   for dir in $(ls); do
       if [ -d "$dir/snapshots/" ]; then
           echo "/var/lib/cassandra/data/$key/$dir/snapshots/$(ls -t $dir/snapshots/ | head -n1)"
       fi
   done > $backup_folder/$key.txt
done

for key in "${arr[@]}"
do
   echo "$key"
   for dir in $(<$backup_folder/$key.txt); do
       cp --parents -r $dir $backup_folder
   done
done

service zookeeper start
service supervisor-analytics start
service supervisor-config start

cd
hostname=$(hostname | cut -d . -f 1)
time=$(date "+%Y-%m-%d")
IFS='/' read -ra FOLDER <<< "$backup_folder"
TAR_FILE=contrail_backup.$hostname.$time.tar.gz
tar zcf $TAR_FILE ${FOLDER[2]} --remove-files
echo "Backup tar file $TAR_FILE is created !!!!!"
