import requests
import json
import datetime
import time
import os
def main():
    print("""
                                     _______  _______  _______  _______  _       _________
                                    (       )(  ____ \(  ____ )(  ___  )| \    /\\__   __/
                                    | () () || (    \/| (    )|| (   ) ||  \  / /   ) (
                                    | || || || (__    | (____)|| (___) ||  (_/ /    | |
                                    | |(_)| ||  __)   |     __)|  ___  ||   _ (     | |
                                    | |   | || (      | (\ (   | (   ) ||  ( \ \    | |
                                    | )   ( || (____/\| ) \ \__| )   ( ||  /  \ \___) (___
                                    |/     \|(_______/|/   \__/|/     \||_/    \/\_______/
*********************                                                                               ********************************
_________ _       _________ _______  _              _______  _______  _        _        _______  _______ _________ _______  _______
\__   __/( (    /|\__   __/(  ____ \( \            (  ____ \(  ___  )( \      ( \      (  ____ \(  ____ \\__   __/(  ___  )(  ____ )
   ) (   |  \  ( |   ) (   | (    \/| (            | (    \/| (   ) || (      | (      | (    \/| (    \/   ) (   | (   ) || (    )|
   | |   |   \ | |   | |   | (__    | |            | |      | |   | || |      | |      | (__    | |         | |   | |   | || (____)|
   | |   | (\ \) |   | |   |  __)   | |            | |      | |   | || |      | |      |  __)   | |         | |   | |   | ||     __)
   | |   | | \   |   | |   | (      | |            | |      | |   | || |      | |      | (      | |         | |   | |   | || (\ (
___) (___| )  \  |   | |   | (____/\| (____/\      | (____/\| (___) || (____/\| (____/\| (____/\| (____/\   | |   | (___) || ) \ \__
\_______/|/    )_)   )_(   (_______/(_______/      (_______/(_______)(_______/(_______/(_______/(_______/   )_(   (_______)|/   \__/
=====================================================================================================================================
                                ----    Leaveraging the Meraki Dashboard  API   ----
            Hastily thrown together with the power of coffee and frustration by Rogelio Dominguez (roy@dominguez.tech)


""")
    filename = "MerakiReport-{}.json".format(str(datetime.datetime.now()))
    f = open(filename,'a')
    class MerakiReport:
        def __init__(api):
            try:
                api.key = api_key
            except:
                api.key = input('API key: ')
            api.headers = {"Content-Type": "application/json","Accept": "application/json","X-Cisco-Meraki-API-Key":api.key}
            api.baseurl = "https://api.meraki.com/api/v1/"
            api.payload = {}
        def orgGetData(api):
            print("\n"+"="*80+"\n"+"  Organzation Data  "+"\n"+"="*80+"\n")
            print("[ ! Attempting to get organization ! ]\n")
            api.getOrgs = requests.request("GET",api.baseurl+"organizations",headers=api.headers,data=api.payload).json()
            timestamp = str("\nCollection started at {}\n").format(datetime.datetime.now())
            f.write(str("\n[ Number of Organizations | {} ]\n").format(len(api.getOrgs)))
            f.write(str(api.getOrgs))
#print(api.orgReport)
            for organization in api.getOrgs:
                orgId = organization['id']
                f.write("\n[ Org Id: {} | Org Name {} ]\n".format(organization['id'],organization['name']))
# Get Org Networks
                print("[ ! Attempting to get networks for this organization ! ]")
                url = str(api.baseurl+"organizations/{}/{}").format(orgId,'networks')
                api.getNetworks = requests.request("GET",str(api.baseurl+"organizations/{}/networks").format(orgId),headers=api.headers,data=api.payload).json()
                f.write("\n[ Number of Networks | {} ]\n".format(len(api.getNetworks)))
                f.write(str(api.getNetworks))
#Get Org Devices
                print("[ ! Attempting to get devices for this organization ! ]")
                url = str(api.baseurl+"organizations/{}/{}").format(orgId,"devices")
                api.getOrgDevices = requests.request("GET",url,headers=api.headers,data=api.payload).json()
                f.write("\n[ Number of Devices in  | {} ]\n".format(len(api.getOrgDevices)))
                f.write(str(api.getOrgDevices))
#Get Configuration Changes
                print("[ ! Attempting to get configuration changes for this organization ! ]")
                url = str(api.baseurl+"/organizations/{}/{}").format(orgId,"configurationChanges")
                api.getOrgConfigChanges = requests.request("GET",url,headers=api.headers,data=api.payload).json()
                f.write("\n[ Change Log Entries  | {} ]\n".format(len(api.getOrgConfigChanges)))
                fileName = "changeLog-{}-{}.json".format(orgId,datetime.datetime.now())
                changeLog = open(fileName,'a')
                print("[ ! Writing Log entries to {}  | {} ]\n".format(fileName,len(api.getOrgConfigChanges)))
                for entry in api.getOrgConfigChanges:
                    changeLog.write(str('\nTimestamp: {} \nChange made by: {} | Changes on: {} | New: {} \n').format(entry['ts'],entry['adminName'],entry['page'],entry['oldValue'],entry['newValue']))
                changeLog.close()
#Get Org Inventory Information
                print("[ ! Attempting to get inventory information for this organization ! ]")
                url = str(api.baseurl+"organizations/{}/{}").format(orgId,"inventoryDevices")
                api.getOrgInventory = requests.request("GET",url,headers=api.headers,data=api.payload).json()
                print(str("\n[ Number of inventory Devices found in | {}]\n").format(len(api.getOrgInventory)))
                f.write(str(api.getOrgInventory))
#Get Org Uplink Statuses
                print("[ ! Attempting to get uplink infomration for this organization ! ]")
                url = str(api.baseurl+"organizations/{}/{}").format(orgId,"uplinks/statuses")
                api.getOrgUplinkStats = requests.request("GET",url,headers=api.headers,data=api.payload).json()
                try:
                    f.write(str("\n[ Number of Devices in  | {} ]\n".format(len(api.getOrgUplinkStats))))
                    f.write(str(api.getOrgUplinkStats))
                except:
                    print("[ !! Error !! ]")
                    pass
        def networkGetData(api):
            print("\n"+"="*80+"\n"+"  Network Data  "+"\n"+"="*80+"\n")
            networks = api.getNetworks
            for network in networks:
#Get Network settings
                print("[ ! Attempting to get network settings ! ]")
                try:
                    url = str(api.baseurl+"networks/{}/{}").format(network['id'],"settings")
                    networkSettings = requests.request("GET",url,headers=api.headers,data=api.payload).json()
                    f.write(str("\n[ | Logging Configuarations for {}| ]\n").format(network['id']))
                    f.write(str(networkSettings))
                except:
                    print("[ !! Error !! ]")
                    pass
#Get Network Devices
                print("[ ! Attempting to get network devices ! ]")
                try:
                    url = str(api.baseurl+"networks/{}/{}").format(network['id'],"devices")
                    networkDevices = requests.request("GET",url,headers=api.headers,data=api.payload).json()
                    f.write(str("\n[ | {} Network Devices Found  on {} | ]\n").format(len(networkDevices),network['id']))
                    f.write(str(networkDevices))
                except:
                    print("[ !! Error !! ]")
                    pass
#Get Network Traffic Data if set in Network Settings
                print("[ ! Attempting to get network traffic data ! ]")
                try:
                    url = str(api.baseurl+"networks/{}/{}").format(network['id'],"traffic?timespan=608400&deviceType=wireless")
                    networkTraffic = requests.request("GET",url,headers=api.headers,data=api.payload).json()
                    f.write(str("\n[ | Wireless network traffic data for {} | {} days ]\n").format(network['id'],60480/24/60/60))
                    f.write(str(networkTraffic))
                except:
                    print("[ !! Error !! ]")
                    pass
#Get Network Traffic Floor Plans
                print("[ ! Attempting to get network floor plans ! ]")
                try:
                    url = str(api.baseurl+"networks/{}/{}").format(network['id'],"floorPlans")
                    networkFloorPlans = requests.request("GET",url,headers=api.headers,data=api.payload).json()
                    f.write(str("\n[ | Network floor plans for {} | ]\n").format(network['id']))
                    f.write(str(networkFloorPlans))
                except:
                    print("[ !! Error !! ]")
                    pass

#Get Network Clients
                print("[ ! Attempting to get network clients ! ]")
                url = str(api.baseurl+"networks/{}/{}").format(network['id'],"clients?timespan=604800&perpage=1000")
                networkClients = requests.request("GET",url,headers=api.headers,data=api.payload).json()
                f.write(str("\n[ | {} Network Clients Found  on {} | ]\n").format(len(networkClients),network['id']))
                for client in networkClients:
                    f.write("\n"+str(client)+"\n")

#Get Network Bluetooth Clients
                print("[ ! Attempting to get network bluetooth clients ! ]")
                url = str(api.baseurl+"networks/{}/{}").format(network['id'],"bluetoothClients")
                networkBTClients = requests.request("GET",url,headers=api.headers,data=api.payload).json()
                f.write(str("\n[ | {} Bluetooth clients for {} | ]\n").format(len(networkBTClients),network['id']))
                f.write(str(networkBTClients))

#Get Wireless Connection stats
                print("[ ! Attempting to get wireless network device connection stats ! ]")
                try:
                    url = str(api.baseurl+"/networks/{}/wireless/connectionStats?timespan=604800").format(network['id'])
                    getwirelessNetworkConnectionStats = requests.request("GET",url,headers=api.headers,data=api.payload).json()
                    f.write(str("\n[ | Network device connections stats for  {} | {} days ]\n").format(network['id'],60480/24/60/60))
                    f.write(str(getwirelessNetworkConnectionStats))
                except:
                    print("[ !! Error !! ]")
                    pass
#Get AirMarshal Data
                print("[ ! Attempting to get wireless network AirMarshal data ! ]")
                try:
                    url = str(api.baseurl+"/networks/{}/wireless/airMarshal?timespan=604800").format(network['id'])
                    getairMarshal = requests.request("GET",url,headers=api.headers,data=api.payload).json()
                    f.write(str("\n[ | Air Marshal Stats {}  ]\n").format(network['id'],int(60480/24/60/60)))
                    f.write(str(getairMarshal))
                except:
                    print("[ !! Error !! ]")
                    pass
#Get Wireless Network Failed Connection stats
                print("[ ! Attempting to get wireless network failed connection stats ! ]")
                try:
                    url = str(api.baseurl+"/networks/{}/wireless/failedConnections?timespan=604800&band=2.4").format(network['id'])
                    failedConnections24 = requests.request("GET",url,headers=api.headers,data=api.payload).json()
                    f.write(str("\n[ | Failed connection stats {} | {} days| 2.4Ghz ]\n").format(network['id'],int(60480/24/60/60)))
                    f.write(str(failedConnections24))

                    url = str(api.baseurl+"/networks/{}/wireless/failedConnections?timespan=604800&band=5").format(network['id'])
                    failedConnections5 = requests.request("GET",url,headers=api.headers,data=api.payload).json()
                    f.write(str("\n[ | Failed connection stats {} | {} days| 5Ghz | ]\n").format(network['id'],int(60480/24/60/60)))
                    f.write(str(failedConnections5))
                except:
                    print("[ !! Error !! ]")
                    pass

#Get Wireless Channel utilzation
                print("[ ! Attempting to get network wireless channel utlization history! ]")
                try:
                    url = str(api.baseurl+"/networks/{}/wireless/channelUtilizationHistory?timespan=604800&band=2.4&autoResolution=True").format(network['id'])
                    channelUtilzation24 = requests.request("GET",url,headers=api.headers,data=api.payload).json()
                    f.write(str("\n[ | Wireless channel utilization history {} | {} days | 2.4Ghz | ]\n").format(network['id'],int(604800/24/60/60)))
                    f.write(str(channelUtilizationHistory24))

                    url = str(api.baseurl+"/networks/{}/wireless/channelUtilizationHistory?timespan=604800&band=5&autoResolution=True").format(network['id'])
                    channelUtilization5 = requests.request("GET",url,headers=api.headers,data=api.payload).json()
                    f.write(str("\n[ | Wireless channel utilization history {} | {} days | 5Ghz | ]\n").format(network['id'],int(604800/24/60/60)))
                    f.write(str(channelUtilizationHistory5))
                except:
                    print("[ !! Error !! ]")
                    pass
#Get Wireless Network Latency Stats
                print("[ ! Attempting to get wireless network latency stats ! ]")
                try:
                    url = str(api.baseurl+"/networks/{}/wireless/latencyStats?timespan=604800&band=2.4&autoResolution=True").format(network['id'])
                    getwirelessNetworkLatencyStats24 = requests.request("GET",url,headers=api.headers,data=api.payload).json()
                    f.write(str("\n[ | Latency stats for  {} | {} days ]\n").format(network['id'],604800/24/60/60))
                    f.write(str(getwirelessNetworkLatencyStats24))
                    url = str(api.baseurl+"/networks/{}/wireless/latencyStats?timespan=604800&band=2.4&autoResolution=True").format(network['id'])
                    getwirelessNetworkLatencyStats5 = requests.request("GET",url,headers=api.headers,data=api.payload).json()
                    f.write(str("\n[ | Latency stats for  {} | {} days ]\n").format(network['id'],604800/24/60/60))
                    f.write(str(getwirelessNetworkLatencyStats5))
                except:
                    print("[ !! Error !! ]")
#get Wireless Network Latency History
                print("[ ! Attempting to get network wireless latency history ! ]")
                try:

                    url = str(api.baseurl+"/networks/{}/wireless/latencyHistory?timespan=604800&band=2.4&autoResolution=True").format(network['id'])
                    latencyHistory24 = requests.request("GET",url,headers=api.headers,data=api.payload).json()
                    f.write(str("\n[ | Wireless latency history {} | {} days | 2.4Ghz | ]\n").format(network['id'],int(604800/24/60/60)))
                    f.write(str(channelUtilizationHistory24))
                    url = str(api.baseurl+"/networks/{}/wireless/latencyHistory?timespan=604800&band=5&autoResolution=True").format(network['id'])
                    latencyHistory5 = requests.request("GET",url,headers=api.headers,data=api.payload).json()
                    f.write(str("\n[ | Wireless latency history {} | {} days | 5Ghz | ]\n").format(network['id'],int(604800/24/60/60)))
                    f.write(str(channelUtilizationHistory5))
                except:
                    print("[ !! Error !! ]")
                    pass
#Get Wireless Network Data Rate History
                print("[ ! Attempting to get network wireless data rate history ! ]")
                try:
                    url = str(api.baseurl+"/networks/{}/wireless/dataRateHistory?timespan=604800&band=2.4").format(network['id'])
                    dataRateHistory24 = requests.request("GET",url,headers=api.headers,data=api.payload).json()
                    f.write(str("\n[ | Wireless data rate history {} | {} days | 2.4Ghz | ]\n").format(network['id'],int(604800/24/60/60)))
                    f.write(str(channelUtilizationHistory24))
                    url = str(api.baseurl+"/networks/{}/wireless/dataRateHistory?timespan=604800&band=5&autoResolution=True").format(network['id'])
                    dataRateHistory5 = requests.request("GET",url,headers=api.headers,data=api.payload).json()
                    f.write(str("\n[ | Wireless data rate history {} | {} days | 5Ghz | ]\n").format(network['id'],int(604800/24/60/60)))
                    f.write(str(channelUtilizationHistory5))
                except:
                    print("[ !! Error !! ]")
                    pass
#Get Wireless Mesh Status
                print("[ ! Attempting to wireless mesh status! ]")
                try:
                    url = str(api.baseurl+"/networks/{}/wireless/meshStatus").format(network['id'])
                    meshStatus = requests.request("GET",url,headers=api.headers,data=api.payload).json()
                    f.write(str("\n[ | Wireless mesh status| ]\n").format(network['id'],int(604800/24/60/60)))
                    f.write(str(meshStatus))
                except:
                    print("[ !! Error !! ]")
                    pass

#Get Wireless Network Events
                print("[ ! Attempting to get wireless network events ! ]")
                try:

                    url = str(api.baseurl+"networks/{}/{}").format(network['id'],"events?productType=wireless&perPage=1000")
                    networkevents = requests.request("GET",url,headers=api.headers,data=api.payload).json()
                    f.write(str("\n[ | Wireless Network events for  {} | ]\n").format(network['id']))
                    f.write(str(getwirelessNetworkConnectionStats))
                except:
                    print("[ !! Error !! ]")
                    pass

#Get Wireless Network Event Types
                print("[ ! Attempting to get wireless network event types! ]")
                try:
                    url = str(api.baseurl+"networks/{}/{}").format(network['id'],"events/eventTypes")
                    networkEventTypes = requests.request("GET",url,headers=api.headers,data=api.payload).json()
                    f.write(str("\n[ | Getting wireless network events {} | ]\n").format(network['id']))
                    f.write(str(networkEventTypes))
                except:
                    pass
        def orgDevicesGet(api):
                print("\n"+"="*80+"\n"+"  Organzation Devices  "+"\n"+"="*80+"\n")
                for orgDevice in api.getOrgDevices:
#Get LLDP and CDP information for each device
                    print("[ | Getting LLDP/CDP Stats for {} {} | ]\n".format(orgDevice['serial'],orgDevice['name']))
                    try:
                        url = str(api.baseurl+"/devices/{}/lldpCdp").format(orgDevice['serial'])
                        lldpCdp = requests.request("GET",url,headers=api.headers,data=api.payload).json()
                        f.write(str("\n[ | LLDP/CDP stats for {} | ]\n").format(orgDevice['serial'],orgDevice['name']))
                        f.write(str(lldpCdp))
                    except:
                        print("[ !! Error !! ]")
                        pass
#Get loss and latency information for each device
                    print("\n[ | Getting Loss and Latency Stats for {} {} | ]\n".format(orgDevice['serial'],orgDevice['name']))
                    try:
                        url = str(api.baseurl+"/devices/{}/lossAndLatencyHistory?timespan=604800&ip=8.8.8.8").format(orgDevice['serial'])
                        lossAndLatency = requests.request("GET",url,headers=api.headers,data=api.payload).json()
                        f.write(str("\n[ | Loss and Latency Stats for {} | ]\n").format(orgDevice['serial'],orgDevice['name']))
                        write(str(lossAndLatency))
                    except:
                        print("[ !! Error !! ]")
                        pass
                    if 'MR' in orgDevice['model']:


#Get MR Connection Stats
                        print("[ !! AP Found | Attempting to get wireless device connection stats ! ]")
                        try:
                            url = str(api.baseurl+"/devices/{}/wireless/connectionStats?timespan=604800&band=2.4").format(orgDevice['serial'])
                            mrConnectionStats24= requests.request("GET",url,headers=api.headers,data=api.payload).json()
                            f.write(str("\n[ | Wireless AP Connection stats {} | {} | {} | ]\n").format(orgDevice['serial'],orgDevice['name'],orgDevice['mac']))
                            f.write(str(mrConnectionStats24))

                            url = str(api.baseurl+"/devices/{}/wireless/connectionStats?timespan=604800&band=5").format(orgDevice['serial'])
                            mrConnectionStats5= requests.request("GET",url,headers=api.headers,data=api.payload).json()
                            f.write(str("\n[ | Wireless AP Connection stats {} | {} | {} | ]\n").format(orgDevice['serial'],orgDevice['name'],orgDevice['mac']))
                            f.write(str(mrConnectionStats5))

                        except:
                            print("[ !! Error !! ]")
                            pass
                        try:
                            url = str(api.baseurl+"/devices/{}/wireless/clients/connectionStats?timespan=604800&band=2.4").format(orgDevice['serial'])
                            clientConnectionStats24= requests.request("GET",url,headers=api.headers,data=api.payload).json()
                            f.write(str("\n[ | Wireless Clients Connection stats {} | {} | {} | ]\n").format(orgDevice['serial'],orgDevice['name'],orgDevice['mac']))
                            f.write(str(clientConnectionStats24))
                            url = str(api.baseurl+"/devices/{}/wireless/clients/connectionStats?timespan=604800&band=5").format(orgDevice['serial'])
                            clientConnectionStats5= requests.request("GET",url,headers=api.headers,data=api.payload).json()
                            f.write(str("\n[ | Wireless Clients Connection stats {} | {} | {} | ]\n").format(orgDevice['serial'],orgDevice['name'],orgDevice['mac']))
                            f.write(str(clientConnectionStats5))
                        except:
                            print("[ !! Error !! ]")
                            pass
    #Get MR Latency Stats
                        print("[ ! Attempting to get wireless device latency stats ! ]")
                        try:
                            url = str(api.baseurl+"/devices/{}/wireless/latencyStats?timespan=604800").format(orgDevice['serial'])
                            f.write(str("\n[ | Wireless Latency stats {} | {} | {} | ]\n").format(orgDevice['serial'],orgDevice['name'],orgDevice['mac']))
                            mrlatencyStats24 = requests.request("GET",url,headers=api.headers,data=api.payload).json()
                            f.write(str(mrlatencyStats24))

                            url = str(api.baseurl+"/devices/{}/wireless/latencyStats?timespan=604800").format(orgDevice['serial'])
                            f.write(str("\n[ | Wireless Latency stats {} | {} | {} | ]\n").format(orgDevice['serial'],orgDevice['name'],orgDevice['mac']))
                            mrlatencyStats5 = requests.request("GET",url,headers=api.headers,data=api.payload).json()
                            f.write(str(mrlatencyStats5))
                        except:
                            print("[ !! Error !! ]")
                            pass
                        else:
                            pass
    a = MerakiReport()
    a.orgGetData()
    a.networkGetData()
    a.orgDevicesGet()
    f.close()
    print("\nCollection Complete\n")
main()
