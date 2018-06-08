#
# Tested on all-in-one contrail cluster based on centos 7.4 contrail image
# Collect all the required contrail logs to sent to dev or jtac
#!/usr/bin/env bash
set -e
set -x

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi

# declare variables
declare -a logs=("/var/log/contrail" "/var/log/cassandra" "/var/log/rabbitmq" "/var/log/zookeeper" "/var/log/kafka" "/var/log/redis")
declare -a configs=("/etc/contrail" "/etc/cassandra" "/etc/rabbitmq" "/etc/zookeeper")
declare -a cmd_outputs=("/etc/redhat-release" "uname -a" "contrail-status -d" "nodetool status" "contrail-version" "df -h" "free -mh")

log_folder='/tmp/contrail_logs'
rm -rf $log_folder
mkdir -p $log_folder

# collect logs
for log in "${logs[@]}"
do
   echo "Copying logs from $log"
   specific_log=$log_folder/logs/$(echo $log | awk -F/ '{print $4}')
   echo $specific_log
   mkdir -p $specific_log
   cp --parents -r $log $specific_log
done

# collect configs
for config in "${configs[@]}"
do
   echo "Copying configs from $config"
   specific_config=$log_folder/configs/$(echo $config | awk -F/ '{print $4}')
   echo $specific_config
   mkdir -p $specific_config
   cp --parents -r $config $specific_config
done

# collect command ouputs in a file
cmd_op_file=$log_folder/cmd_outputs/cmd_output
echo $cmd_op_file
rm -rf $cmd_op_file
touch $cmd_op_file
for cmd in "${cmd_outputs[@]}"
do
   echo "Running cmd: $cmd_outputs"
   $cmd | tee -a $cmd_op_file
done

cd
hostname=$(hostname | cut -d . -f 1)
time=$(date "+%Y-%m-%d")
TAR_FILE=contrail_logs_cfg_cmdoutputs.$hostname.$time.tar.gz
tar zcf $TAR_FILE $log_folder --remove-files
echo "Contrail RSI tar file $TAR_FILE is created !!!!!"
