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
esxcli hardware pci list
```

* Firmware version of the NIC
```
esxcli network nic list
esxcli network nic get -n vmnic4
esxcli software vib list | grep i40en
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

* Upgrade NIC firmware
```
Download the firmware package from VMware Connect
Upload the package onto ESXi datastore, using datastore browser
Extract the contents of the driver zip file
Enter the host into maintenance mode
esxcli software vib install -v <PATH_TO_VIB_FILE>
Restart the ESXi host
Check the firmware
esxcli network nic get -n vmnicX
```

* Stop and Reboot Host
```
esxcli system shutdown poweroff --reason "shutting down"
esxcli system shutdown reboot --reason "restarting.."
```
