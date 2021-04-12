import json
import pandas as pd
import numpy
import os
import datetime as dt
import requests as rq


class APICaller():
    def __init__(api):
        api.url = 'https://api.meraki.com/api/v1'
        try:
            api.headers = {'X-Cisco-Meraki-API-Key': api.key}
        except:
            api.key = '37a10db07204cb50ae8a39d4b4772f5ba21b572d'
            api.headers = {'X-Cisco-Meraki-API-Key': api.key}

    def organizations(api):
        url = api.url+"/organizations/"
        orgs = rq.get(url,headers=api.headers).json()
        for x in orgs:
            try:
                api.orgs.append(x)
            except:
                api.orgs = x
        try:
            orgs = pd.DataFrame(orgs)
        except:
            orgs = pd.Series(orgs)
        #print('\n\nOrganizations\n')
        #print(orgs)

    def networks(api):
        try:
            orgId = api.orgs['id']
        except:
            #print("No Orgs found, will request now")
            api.organizations()
            orgId = api.orgs['id']
        url = str(api.url+'/organizations/{}/networks/').format(api.orgs['id'])
        api.networks = rq.get(url,headers=api.headers).json()
        try:
            api.dfnetworks = pd.DataFrame(api.networks)
        except:
            api.dfnetworks = pd.Series(api.networks)
        #print('\n\nNetworks\n')
        #print(api.dfnetworks)

    def devices(api):
        try:
            orgId = api.orgs['id']
        except:
            api.organizations()
            orgId = api.orgs['id']

        url = str(api.url+'/organizations/{}/inventoryDevices').format(orgId)
        api.inventoryDevices = rq.get(url,headers=api.headers).json()
        api.dfinventoryDevices = pd.DataFrame(api.inventoryDevices)
        #print("\n\nDevices\n")
        #print(api.dfinventoryDevices)

    def switches(api, serial):
        try:
            url = str(api.url+'/devices/{}/switch/{}').format(serial,'ports/statuses')
            switchPortStatus= rq.get(url,headers=api.headers).json()
            return switchPortStatus
            url = str(api.url+'/devices/{}/switch/{}').format(serial,'ports/statuses/packets')
            switchPortPackets= rq.get(url,headers=api.headers).json()
            return switchPortPackets
            #switchPort
        except:
            pass
    def wireless(api,serial):
        pass
APICaller().switches('Q2HP-P28Q-BDFR')
#APICaller().devices()
