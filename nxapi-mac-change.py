#!/usr/bin/env python
'''
This script will dynamically change the access VLAN for a host connection given the host MAC address.

This will be done through the use of NXAPI calls through the use of json-rpc cli methods.

'''

import requests
import json
import getpass
import sys
import argparse
import re

mac_found = False

#setting json-rpc request type
myheaders={'content-type':'application/json-rpc'}

#Script can get arguments one of two ways

#Argument passed through script arguments
#order of arguments
#argv[0] script name, argv[1] ip, argv[2] switchuser, argv[3] mac address, argv[4] vlan
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("ip", help="SWITCH MGMT IP")
parser.add_argument("switchuser", help="Username")
parser.add_argument("mac_address", help="Host MAC to search for(expected in ####.####.####)")
parser.add_argument("new_vlan", type=int ,help="VLAN to change access to")
args = parser.parse_args()

#interactive prompt

#args.ip = raw_input("Switch IP: ")
#args.switchuser = raw_input("Username: ")
#args.mac_address = raw_input("MAC Address: ")
#args.new_vlan = raw_input("New VLAN: ")

#use getpass() to prompt user for password for switch without echoing on the term
switchpassword = getpass.getpass("User password for %s:"%(args.switchuser))

#NXAPI requests expect the URL for the switch to be in the form of 'http://#.#.#.#/ins'
url = 'http://%s/ins' %(args.ip)


#send request to switch to get outputs of show mac address

payload_show=[
  {
    "jsonrpc": "2.0",
    "method": "cli",
    "params": {
      "cmd": "show mac address-table",
      "version": 1
    },
    "id": 1
  }
]
try:
    response = requests.post(url,data=json.dumps(payload_show), headers=myheaders,auth=(args.switchuser,switchpassword)).json()
except Exception:
	print("Something failed during getting 'show mac address-table'")
	sys.exit(0)

#check for MAC address entry
#we will be able to check each row of mac address table output by checking following structure
#['result']['body']['TABLE_mac_address']['ROW_mac_address']
#we will interate through the ['disp_mac_addr'] values looking for provided MAC address
#if found we will set flag for found and track the interface
for item in response['result']['body']['TABLE_mac_address']['ROW_mac_address']:
    if item['disp_mac_addr'] == args.mac_address:
        interface = item['disp_port']
        current_vlan = item['disp_vlan']
        print("MAC '%s' found on '%s' in VLAN%s"%(args.mac_address,interface,current_vlan))
        mac_found = True

#if mac found we will send the config payload to change the vlan on the interface
if mac_found:
	payload_config=[
	  {
		"jsonrpc": "2.0",
		"method": "cli",
		"params": {
		  "cmd": "config t",
		  "version": 1
		},
		"id": 1
	  },
	  {
		"jsonrpc": "2.0",
		"method": "cli",
		"params": {
		  "cmd": "interface %s"%(interface),
		  "version": 1
		},
		"id": 2
	  },
	  {
		"jsonrpc": "2.0",
		"method": "cli",
		"params": {
		  "cmd": "switchport access vlan %s"%(args.new_vlan),
		  "version": 1
		},
		"id": 3
	  }
	]

	try:
		config_response = requests.post(url,data=json.dumps(payload_config), headers=myheaders,auth=(args.switchuser,switchpassword)).json()
		print("Access VLAN Changed on '%s' to %s\n")%(interface,args.new_vlan)
	except Exception:
		print("Something Failed during config request")
else:
	print("MAC Not Found")
