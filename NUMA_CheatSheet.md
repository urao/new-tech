 ### Below are some of the commands related to NUMA on Ubuntu
 
1. Install required packages to check NUMA related configuration
```
apt install -y numactl
apt install -y hwloc
```
2. Check if NUMA is enabled or disabled
```
numactl --show
lscpu | grep -i numa
```
3. Check inventory of available nodes on the system
```
numactl --hardware
```
4. Check if the network interfaces are tied to NUMA
```
cat /sys/class/net/eth0/device/numa_node
lshw -short -c network
```
5. Check which NUMA the network card belongs to using lstopo
```
lstopo
lstopo --logical
lstopo --logical --ouput-format png > lstopo.png
```
