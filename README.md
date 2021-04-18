# evohome-influxdbv2

This is a docker container that pushes data from the Honeywell Evohome API to InfluxDB. Based on work of jankeesvw [evohome-to-influxdb] (https://github.com/jankeesvw/evohome-to-influxdb).

Updated for InfluxDBv2 and python.

## How to run
```
$ docker run -d \
 -e EVOHOME_APP_ID="91db1612-73fd-4500-91b2-e63b069b185c" \
 -e EVOHOME_EMAIL="<evohome email>" \
 -e EVOHOME_PASSWORD="<evohome password>" \
 -e INFLUXDB2_HOST="<INFLUXDBv2 SERVER>" \
 -e INFLUXDB2_PORT="8086" \
 -e INFLUXDB2_ORG="Home" \
 -e INFLUXDB2_TOKEN="" \
 -e INFLUXDB2_BUCKET="DEV" \
 --name "evohome-influxdbv2" \
dbsqp/evohome-influxdbv2:latest
```

## Evohome Application ID

Unsure where and how to register for an API access for Honeywell Home | Total Connect Comfort. However using the following ID found online works combined with user email and password used to access https://international.mytotalconnectcomfort.com.

APP_ID = 91db1612-73fd-4500-91b2-e63b069b185c



