 ### Below are some of the commands related to NUMA on Ubuntu

0. Install required packages to check NUMA related configuration
```
apt install -y numactl
apt install -y hwloc
apt install -y hwinfo
apt install -y inxi
```
1. Check hardware/memory/cpu information
```
lscpu
cat /proc/meminfo
cat /proc/cpuinfo
dmidecode | less
hwinfo
inxi -Fx
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
6. numatop, tool for memory access and analysis
```
apt install numatop -y
numatop -s high
```
7. Get PCI device address
```
lspci -nn
```
8. Show how many allocations were satisfied from the local node
```
numastat
```
