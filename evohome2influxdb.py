#!/usr/bin/python3
# encoding=utf-8

from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS
import json
import os
import sys
import requests


# debug enviroment variables
showraw = False
debug_str=os.getenv("DEBUG", None)
if debug_str is not None:
    debug = debug_str.lower() == "true"
else:
    debug = False


# evohome envionment variables
evohome_username=os.getenv('EVOHOME_EMAIL', "")
evohome_password=os.getenv('EVOHOME_PASSWORD', "")
evohome_application_id=os.getenv('EVOHOME_APP_ID',"")


# influxDBv2 environment variables
influxdb2_host=os.getenv('INFLUXDB2_HOST', "localhost")
influxdb2_port=int(os.getenv('INFLUXDB2_PORT', "8086"))
influxdb2_org=os.getenv('INFLUXDB2_ORG', "org")
influxdb2_token=os.getenv('INFLUXDB2_TOKEN', "token")
influxdb2_bucket=os.getenv('INFLUXDB2_BUCKET', "netatmo")


# hard encoded environment variables


# report debug status
if debug:
    print ( " debug: TRUE" )


# evohome
url = 'https://tccna.honeywell.com/WebAPI/api/Session'
payload = {'username': evohome_username, 'password': evohome_password, 'ApplicationId': evohome_application_id}

r = requests.post(url, data=payload)
response = r.json()

sessionID = response["sessionId"]
userID = response["userInfo"]["userID"]

url = "https://tccna.honeywell.com/WebAPI/api/locations?userId="+str(userID)+"&allData=True"
header = {'Content-Type': 'application/json', 'sessionID': sessionID}

if debug:
    print ( "  raw API: " )
    print (json.dumps(response,indent=4))
    print ( "sessionID: "+sessionID )
    print ( "   userID: "+str(userID) )
    print ( "      URL: "+url )

r = requests.get(url, headers=header)
raw = r.json()

if debug:
    print ( " raw JSON: " )
    print (json.dumps(raw,indent=4))


# influxDBv2
influxdb2_url="http://" + influxdb2_host + ":" + str(influxdb2_port)
if debug:
    print ( "influx: "+influxdb2_url )
    print ( "bucket: "+influxdb2_bucket )

client = InfluxDBClient(url=influxdb2_url, token=influxdb2_token, org=influxdb2_org)
write_api = client.write_api(write_options=SYNCHRONOUS)


# pass devices
devices = raw[0]['devices']

for d in devices:

    host=d['name']
    hardware=d['deviceID']
    temperature=d['thermostat']['indoorTemperature']
    setpoint=d['thermostat']['changeableValues']['heatSetpoint']['value']

    senddata={}
        
    senddata["measurement"]="Temperature"
    senddata["tags"]={}
    senddata["tags"]["source"]="Evohome"
    senddata["tags"]["host"]=host
    senddata["tags"]["hardware"]=hardware
    senddata["fields"]={}
    senddata["fields"]["value"]=temperature
    
    if debug:
        print ("INFLUX: "+influxdb2_bucket)
        print (json.dumps(senddata,indent=4))
    write_api.write(bucket=influxdb2_bucket, org=influxdb2_org, record=[senddata])
        
    senddata["measurement"]="Temperature-Setpoint"
    senddata["tags"]={}
    senddata["tags"]["source"]="Evohome"
    senddata["tags"]["host"]=host
    senddata["tags"]["hardware"]=hardware
    senddata["fields"]={}
    senddata["fields"]["value"]=setpoint
    
    if debug:
        print ("INFLUX: "+influxdb2_bucket)
        print (json.dumps(senddata,indent=4))
    write_api.write(bucket=influxdb2_bucket, org=influxdb2_org, record=[senddata])

    print ( host.ljust(11)+" = "+str(temperature)+" cf. "+str(setpoint))
