import json
import pandas as pd
import numpy
import os
import datetime as dt
import requests as rq

def main():
    #print(uiLayout)
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
            print(api.orgs)
        def networks(api):
            try:
                orgId = api.orgs['id']
            except:
                #print("No Orgs found, will request now")
                api.organizations()
                orgId = api.orgs['id']
            url = str(api.url+'/organizations/{}/networks/').format(api.orgs['id'])
            api.networks = rq.get(url,headers=api.headers).json()
            for x in api.networks:
                print("[ {} | {} : Device types Present - {}".format(x['id'],x['name'],*x['productTypes']))


        def devices(api):
            try:
                orgId = api.orgs['id']
            except:
                api.organizations()
                orgId = api.orgs['id']

            url = str(api.url+'/organizations/{}/inventoryDevices').format(orgId)
            api.inventoryDevices = rq.get(url,headers=api.headers).json()
            api.inventoryDevices = pd.DataFrame(api.inventoryDevices)
            print(api.inventoryDevices)
            """
            for x in api.inventoryDevices:
                outputFormat = "[ | Name: {name} | {serial} | {mac} | {model} ]".format(model = x['model'], serial = x['serial'], mac = x['mac'],name =x['name'])

                print(outputFormat)"""



    APICaller().networks()
    APICaller().devices()

main()
