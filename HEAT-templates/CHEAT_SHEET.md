## Cheat sheet commands for HOT (Heat Orchestration Template)

1) Heat Orchestration templates (HOT) are declarative configurations for the Heat orchestration tool, 
   used to automate the creation of many OpenStack resources
```
openstack stack create -t <template_file> -e <env_file> <stack_name>
openstack stack show <stack_name>
openstack stack update -t <template_file> -e <env_file> <stack_name>
openstack stack create --parameter <parameter_name>=<value> -t <template_file> -e <env_file> <stack_name>
openstack orchestration resource type list  #List of all resource types
openstack orchestration resource type show <resource_name> 
openstack stack list
openstack stack create -t <template_file> -e <env_file> <stack_name> --dry-run
openstack stack delete <stack_name> -y
openstack stack event list <stack_name>
openstack stack failures list --long <stack_name>
openstack stack resource list <stack_name>
openstack stack update <stack_name> --existing
```
