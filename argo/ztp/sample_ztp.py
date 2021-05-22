#!/usr/bin/python

from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.op.lldp import LLDPNeighborTable
from jnpr.junos.exception import *
import urllib
import jcs
import os
import json
import requests
import time

#root@ArgoMX1> show lldp neighbors
#Local Interface    Parent Interface    Chassis Id          Port info          System Name
#fxp0               -                   50:c7:09:a3:c5:9d   528                gw.pod3.cce
#xe-1/1/0           -                   50:c7:09:bb:64:dc   537                spine2.pod3.cce
#xe-1/1/1           -                   50:c7:09:c5:8b:0c   537                spine1.pod3.cce

def disable_interface(interface_name):
   try:
     with Device() as dev:
        with Config(dev, 'exclusive') as cu:
           cu.load('set interfaces {0} disable'.format(interface_name))
           cu.commit()
   except Exception as inst:
      jcs.syslog('external.warn', "{0}: Unable to disable interface.".format(interface_name))
      jcs.syslog('external.warn', "{0}.".format(inst))


def compare_lldp_info():
   expected_topology = {
       'fxp0':
           {'Chassis_ID': '50:c7:09:a3:c5:9d',
            'System_Name': 'gw.pod3.cce'},
       'xe-1/1/0':
           {'Chassis_ID': '50:c7:09:bb:64:dc',
            'System_Name': 'spine2.pod3.cce'},
       'xe-1/1/1':
           {'Chassis_ID': '50:c7:09:c5:8b:0c',
            'System_Name': 'spine1.pod3.cce'},
       'xe-1/1/2':
           {'Chassis_ID': 'abc123',
            'System_Name': 'unknown host'}
   }
   try:
       with Device() as dev:
           lldp = LLDPNeighborTable(dev)
           lldp.get()
           for item in lldp:
               if item['local_int'] in expected_topology.keys() \
                       and item['remote_chassis_id'] == expected_topology[item['local_int']['Chassis_ID']] \
                       and item['remote_sysname'] == expected_topology[item['local_int']['System_Name']]:
                   jcs.syslog('external.info', "{0}: Expected interface found.".format(item['local_int']))
               else:
                   jcs.syslog('external.warn', "{0}: Cabling mismatch detected.".format(item['local_int']))
                   jcs.syslog('external.warn', "{0}: Disabling interface.".format(item['local_int']))
                   disable_interface(item['local_int'])
   except Exception as inst:
       jcs.syslog('external.warn', "{0}: Unable to verify LLDP information.".format(inst))

# Main program defined
def main():

   script = os.path.basename(__file__)
   jcs.syslog("external.info", "{0}: Python script triggered via ZTP to push configuration".format(script))

   run_dir = "/var/db/scripts/event/"
   port_num = 30017
   web_srvr_ip = '10.85.95.136'
   ztp_server = 'http://{0}:{1}/'.format(web_srvr_ip,port_num)
   conf_file = 'juniper.conf'
   storage_check = False

   jcs.syslog("external.info", "{0}: Downloading the configuration".format(script))
   urllib.urlretrieve (ztp_server+conf_file, run_dir+conf_file)

   # Create a device object
   dev = Device(gather_facts=True)
   # Opens a connection
   dev.open()

   # Get system storage
   if storage_check:
      rsp = dev.rpc.get_system_storage()
      var_location_percent = rsp.xpath(".//filesystem[normalize-space(mounted-on)='/var']/used-percent")[0].text
      strip_percent = int(var_location_percent.strip())

      if strip_percent > 75:
         syslog_message = "Warning: /var utilization is at " + str(strip_percent) + "%"
         jcs.syslog("external.warning", "{0}: {1}".format(script,syslog_message))
      else:
         jcs.syslog("external.info", "{0}: var location storage size {1}".format(script,strip_percent))

   try:
      # Create configuration object
      with Config(dev, mode="exclusive") as cu:
         jcs.syslog("external.info", "{0}: Loading the configuration".format(script))
         cu.load(path=run_dir+conf_file, overwrite=True)
         jcs.syslog("external.info", "{0}: Committing the configuration".format(script))
         cu.commit()
   except Exception as err:
      jcs.syslog("external.error", "{0}: Unable to commit the configuration {1}".format(script,err))
      #print (err)
      dev.close()
      return
   jcs.syslog("external.info", "{0}: Successfully committed the configuration".format(script))
   dev.close()

   jcs.syslog("external.info", "{0}: Python script triggered to push config via ZTP is COMPLETED!!!!".format(script))


   # Check cabling
   jcs.syslog("external.info", "{0}: Sleeping for 60 secs before checking cabling connections!".format(script))
   time.sleep(60)
   jcs.syslog("external.info", "{0}: Starting Cabling Verification.".format(script))
   #compare_lldp_info()
   jcs.syslog("external.info", "{0}: Finished Cabling Verification.".format(script))


   # Post end-ztp process webhook message
   jcs.syslog("external.info", "{0}: Post end-ztp process webhook message".format(script))
   headers = { 'Accept': 'application/json' }
   port_num = 32100
   url = 'http://{0}:{1}/ztp-end-process'.format(web_srvr_ip,port_num)
   data = {"message": "ZTP process finished"}
   r = requests.post(url, data=json.dumps(data), headers=headers)
   jcs.syslog("external.info", "{0}: Post message output {1}".format(script, r.text))

# main program starts here
if __name__ == "__main__":
    main()
