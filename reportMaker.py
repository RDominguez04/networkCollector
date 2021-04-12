import os
import json
import csv
import main

a = main.APICaller()
a.organizations()
a.networks()
a.devices()
print(a.networks)
print(a.orgs)

class wordDoc():
    def __init__(dataIn):
        dataIn.jsonData = "a"
    def formatDoc(dataIn):
        os.system('clear')
        docHeader = "Organization Name:{orgName} - Organizations ID:{orgId} - Date of Report:{dateCreated} - \n {title:}"

        docOrgInventory = "MAC:{}|Name:{}|Model Number:{}|Serial:{}|Network:{}|Device Type:{}"


        print(docHeader.format(orgName=a.orgs['name'],orgId=a.orgs['id'],dateCreated="10-2-2020",title="This is a sample report"))
        for x in a.inventoryDevices:
            if 'MR' in x['model']:
                x.update({'deviceType': 'wap'})
            elif 'MS' in x['model']:
                x.update({'deviceType': 'switch'})
            elif 'MX' in x['model']:
                x.update({'deviceType': 'ngfw'})
            elif 'MG' in x['model']:
                x.update({'deviceType': 'lte'})
            elif 'MV' in x['model']:
                x.update({'deviceType': 'cam'})
            print(docOrgInventory.format(x['mac'],x['name'],x['model'],x['serial'],x['networkId'],x['deviceType']))
            
        switches()

wordDoc().formatDoc()
