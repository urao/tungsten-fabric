## Create project object 
#### Tested on CN 5.x

1. Create project using RESTAPI
```
cat > body.json << EOM
{
    "project": {
        "fq_name": [
            "default-domain",
            "project1"
        ],
        "parent_type": "domain",
        "quota": {
            "defaults": -1
        }
    }
}
EOM
curl -i -s -X POST -H "Content-Type: application/json" \
                   -d @./body.json http://<IP_ADDRESS>:8082/projects 
curl -X GET http://<IP_ADDRESS>:8082/projects
```
