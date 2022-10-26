#### Below are some of the useful commands for ESXi 7.0

* System
```
esxcli system version get
esxcli system hostname get
esxcli system boot device get
esxcli system syslog config get
esxcli network ip dns server list
```

* Network
```
esxcli network ip interface list
esxcli network ip interface ipv4 get
esxcli network ip route ipv4 list
esxcli network ip connection list
esxcli network ip neighbor list
```

* NUMA 
```
esxcfg-nics -l
esxcli hardware cpu global get
esxcli hardware memory get
esxcli network nic list
for X in 0 1; do echo -n "NUMA${X}: "; cpuList=`vsish -e ls /hardware/numa/${X}/pcpus`; echo $cpuList; done
vsish -e cat /net/pNics/vmnic4/properties | grep NUMA
for X in 0 1 2 3 4 5 6 7 8 9 10 11; do echo -n "${X}"; vsish -e cat /net/pNics/vmnic${X}/properties | grep NUMA; done
lspci
lspci -vvv
```

* Firmware version of the NIC
```
esxcli network nic get -n vmnic4
```

* Stats
```
esxcli network nic stats get -n vmnic0
```

* Storage
```
esxcli storage vmfs extent list
esxcli storage filesystem list
```


* ESXi VMs
```
esxcli network vm list
```
