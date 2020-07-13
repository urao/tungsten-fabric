# Steps to add vrouter flow_aging parameters using API

1. Get UUID from the below command, say GLOBAL_UUID.
```
curl  http://<controller-ip>:8082/global-vrouter-configs | python -mjson.tool
```

2. Create the payload file(globaltemp.json), example for ICMP with timeout 180seconds
```
{
    "global-vrouter-config": {
        "flow_aging_timeout_list": {
            "flow_aging_timeout": [
                {
                    "port": 0,
                    "protocol": "icmp",
                    "timeout_in_seconds": 180
                }
            ]
        },
        "uuid": "GLOBAL_UUID"
    }
}
```
3. Do a PUT operation, as below command
```
curl -X PUT -H "Content-Type: application/json; charset=UTF-8" -d @globaltemp.json \
http://<controller-ip>:8082/global-vrouter-config/<GLOBAL_UUID>
```
4. Check if its updated, using below command
```
curl  http://<controller-ip>:8082/global-vrouter-config/<GLOBAL_UUID> | python -mjson.tool
```
5. Create the payload file(globalnull.json), to remove all protocols
```
{
    "global-vrouter-config": {
        "flow_aging_timeout_list": null,
        "uuid": "GLOBAL_UUID"
    }
}
```
6. Do a PUT operation, as below command
```
curl -X PUT -H "Content-Type: application/json; charset=UTF-8" -d @globalnull.json \
http://<controller-ip>:8082/global-vrouter-config/<GLOBAL_UUID>
