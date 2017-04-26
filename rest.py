import requests
import json


url = 'http://172.16.166.6/api/aaaLogin.json'
payload = { "aaaUser" : { "attributes" : { "name" : "admin", "pwd" : "cisco!123"}}}

header = {"content-type": "application/json"}

response = requests.post(url,data=json.dumps(payload), headers=header, verify=False)

header = {"content-type": "application/json", "Cookie":response.headers['Set-Cookie']}

interface_url = 'http://172.16.166.6/api/mo/sys/intf/aggr-[po2]/aggrif.json'

response = requests.get(interface_url, headers=header, verify=False).json()

#interface = response['imdata'][0]['l1PhysIf']['attributes']

print(json.dumps(response, indent=4, separators=(',', ':')))

'''
cdp_url = "http://172.16.166.6/api/mo/sys/cdp/inst/if-[eth1/1]/adj-1.json"

response = requests.get(cdp_url, headers=header, verify=False).json()

cdp = response['imdata'][0]['cdpAdjEp']['attributes']

print("Admin State: " + interface['adminSt'])
print("Layer: " + interface['layer'])
print("Switching Mode: " + interface['mode'])
print("Access VLAN: " + interface['accessVlan'])
print("CDP Neighbor: " + cdp['sysName'])
print("CDP Switch: " + cdp['platId'])
print("CDP Port ID: " + cdp['portId'])

payload = {"l1PhysIf" : {"attributes" : {"adminSt": "down"}}}

response = requests.post(interface_url,data=json.dumps(payload), headers=header, verify=False).json()
response = requests.get(interface_url, headers=header, verify=False).json()
interface = response['imdata'][0]['l1PhysIf']['attributes']


print("Admin State: " + interface['adminSt'])
print("Layer: " + interface['layer'])
print("Switching Mode: " + interface['mode'])
print("Access VLAN: " + interface['accessVlan'])

'''