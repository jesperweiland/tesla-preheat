#!/usr/bin/python3

# A script to preheat the Tesla Model S

import pytesla
from sys import exit
import time
import http.client, urllib

# Settings

# temperature to defrost car
defrost_temp = 30

# temperature for normal preheating
preheat_temp = 21

# Miles
minimal_range = 50

# Preheat if colder than
preheat_treshold = 10

# Defrost if colder
defrost_treshold = 0

tesla_login = ""
tesla_password = ""
vehicle_vin = ""

pushover_enable = True
pushover_token = ""
pushover_user = ""

# Teslamotors.com login
car = pytesla.Connection(tesla_login, tesla_password).vehicle(vehicle_vin)

# Wake up
car.wake_up()

def sendpush(push_message):
	conn = http.client.HTTPSConnection("api.pushover.net:443")
	conn.request("POST", "/1/messages.json",
  	urllib.parse.urlencode({
    		"token": pushover_token,
    		"user": pushover_user,
    		"message": push_message,
    		"html": 1,
  	}), { "Content-type": "application/x-www-form-urlencoded" })
	conn.getresponse()

# Loop and continue once the car is online
while True:
	try:
		if "vehicle_name" in car.vehicle_state:
			break
	except http.client.HTTPException:
		pass

# Start airco (needed to measure temperatures)
car.auto_conditioning_start()

# Wait for the temperature sensors to become ready
time.sleep(10)

# Get data from car
outside_temp = car.climate_state['outside_temp'] 
ideal_range = car.charge_state['ideal_battery_range']
ideal_rangekm = round(car.charge_state['ideal_battery_range'] * 1.6)

# Start preheating if the outside temperature is below the treshold and the range is more than 80km (50 miles)
if outside_temp >= defrost_treshold <= preheat_treshold and ideal_range > minimal_range:
	# Wait 5 minutes and start preheating
	time.sleep(600)
	car.set_temps(preheat_temp,preheat_temp)
	if pushover_enable:
		sendpush("<b>Started preheat</b>\nOutside temperature: %s degrees\nRange: %skm" % (outside_temp,ideal_rangekm))
elif outside_temp < defrost_treshold and ideal_range > minimal_range:
	car.set_temps(defrost_temp,defrost_temp)
	if pushover_enable:
		sendpush("<b>Started DEFROST</b>\nOutside temperature: %s degrees\nRange: %skm" % (outside_temp,ideal_rangekm))
	# Wait 10 minutes before going back to normal preheat temperatures
	time.sleep(600)
	if pushover_enable:
		sendpush("<b>Defrost stopped, preheat started</b>")
	car.set_temps(preheat_temp,preheat_temp)