#!/usr/local/bin/ruby -w

require "evohome"
require 'influxdb-client'
require 'httparty'


# debug
DEBUG = ENV["DEBUG"]

if DEBUG=="true"
	debug = true
else
	debug = false
end

puts "debug="+DEBUG if debug


# evohome envionment variables
evohome_username = ENV["EVOHOME_EMAIL"]
evohome_password = ENV["EVOHOME_PASSWORD"]
evohome_application_id = ENV["EVOHOME_APP_ID"]


# influxDBv2 envionment variables
influxdb2_host = ENV["INFLUXDB2_HOST"]
influxdb2_port = ENV["INFLUXDB2_PORT"]
influxdb2_org = ENV["INFLUXDB2_ORG"]
influxdb2_bucket = ENV["INFLUXDB2_BUCKET"]
influxdb2_token = ENV["INFLUXDB2_TOKEN"]

influxdb2_url = "http://" + influxdb2_host + ":" + influxdb2_port.to_s


# evohome
evohome = Evohome.new(username: evohome_username, password: evohome_password, application_id: evohome_application_id)
evohome.connect!


# influxDBv2
puts "influxdb2_url = "+influxdb2_url if debug

client = InfluxDB2::Client.new(influxdb2_url, influxdb2_token, bucket: influxdb2_bucket, org: influxdb2_org, use_ssl: false, precision: InfluxDB2::WritePrecision::NANOSECOND)	
write_api = client.create_write_api

puts "Write Points" if debug
evohome.thermostats.map do |thermostat|
	point = InfluxDB2::Point.new(name: 'Temperature')
		.add_tag('host', thermostat.name)
		.add_tag('source', 'Evohome')
		.add_field('value', thermostat.temperature)
	puts point.to_line_protocol if debug
	write_api.write(data: point)

	point = InfluxDB2::Point.new(name: 'Temperature-Setpoint')
		.add_tag('host', thermostat.name)
		.add_tag('source', 'Evohome')
		.add_field('value', thermostat.temperature_setpoint)
	puts point.to_line_protocol if debug
	write_api.write(data: point)
end
puts 'DONE'
