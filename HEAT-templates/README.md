## Steps to RUN

1) Set up a HEAT client environment
```
sudo apt-get install python-pip python-virtualenv
virtualenv .venv
source .venv/bin/activate
pip install python-heatclient
```

2) clone this repository
```
git clone this repo
cd tungsten-fabric/HEAT-templates
```

3) Set the number of instances, instance name and network name in cluster.env

4) Run the stack create
```
source openstackrc
heat stack-create cluster -f multiple_instance_create.yaml -e cluster.env
```

5) Check status using **heat stack-list**. For more information do **heat stack-show clustera**
