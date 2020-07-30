
### Debug commands based on the service

1. Controller
```
http://<controller_ip>:8083/Snh_IFMapTableShowReq?x=access-control-list
```

2. Schema
```
http://<controller_ip>:8087/Snh_SandeshUVECacheReq?x=NodeStatus
```

3. Config
```
```

4. Analytics
```
curl http://<analytics_ip>:5995/Snh_SandeshUVECacheReq?x=AlarmgenStatus | xmllint --format -
curl http://<analytics_ip>:5995/Snh_SandeshUVECacheReq?x=AlarmgenPartition | xmllint --format -
curl http://<analytics_ip>:5995/Snh_SandeshUVETypesReq? |  xmllint --format - 
curl http://<analytics_ip>:8089/Snh_SandeshTraceRequest?x=UveTrace | xmllint --format -
curl http://<analytics_ip>:5995/Snh_SandeshTraceRequest?x=UVEQTrace | xmllint --format - 
curl http://<analytics_ip>:8081/analytics/uves/virtual-networks | python -mjson.tool
curl http://<analytics_ip>:8081/analytics/uves/virtual-network/default-domain:default-domain:<vn-name>?flat | python -mjson.tool
curl http://<analytics_ip>:8090/Snh_SandeshUVECacheReq?x=NodeStatus | xmllint --format -
curl http://<analytics_ip>:5995/Snh_SandeshUVECacheReq?x=NodeStatus  | xmllint --format -

```

4. Compute
```
http://<compute_ip>:8085/Snh_FetchAllFlowRecords
http://<compute_ip>:8085/Snh_VnListReq?name=&uuid=&vxlan_id=&ipam_name=
http://<compute_ip>:8085/Snh_ItfReq
http://<compute_ip>:8085/Snh_AgentStatsReq
http://<compute_ip>:8085/Snh_CpuLoadInfoReq
http://<compute_ip>:8085/Snh_KDropStatsReq
http://<compute_ip>:8085/Snh_ShowAllInfo
```

