
Enable mgmt plugin
```
rabbitmq-plugins enable rabbitmq_management
```
Download rabbitmqadmin
```
curl -O http://localhost:15672/cli/rabbitmqadmin
```
chmod u+x rabbitmqadmin
List queues
```
rabbitmqadmin -f tsv -q list queues name
```
Delete queue 
```
rabbitmqadmin -q delete queue name=<queue_name>
```
Connect to rabbitmq UI with default credentials guest/guest, to list all the queues
```
http://<VHOST_IP>:15672/#/queues/
```
