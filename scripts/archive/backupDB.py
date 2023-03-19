import sqlite3
#import firebase_admin
#from firebase_admin import credentials
#from firebase_admin import db
import requests
import time
from datetime import datetime
from datetime import date
import random
from FBdataAdding import *

#Enter the UID of the rollator user here
UID = "4nIlD4s8Jdc2Uoa1q0DeONmmisH2"



# Define a function to send data to the Firebase database
def send_to_firebase(data):
	senName, val, time, date = data
	print(("To Firebase -> senName: "+str(senName)+", val:"+str(val)+", date: "+str(date)+", time: " + str(time)))
	if (senName == "heartRate"):
		addHRData(UID, date, time, val)
	elif (senName == "jerk"):
		addJerkData(UID, date, time, val)
	elif (senName == "seat"):
		addSeatData(UID, date, time, val)
	elif (senName == "speed"):
		addSpeedData(UID, date, time, val)
	elif (senName == "weightDistribution"):
		addWeightDistData(UID, date, time, val)
	return True

# Define a function to send data to the local SQLite database
def send_to_sqlite(data):
	senName, val, time, date = data
	# Initializing SQLite connection
	sqlite_conn = sqlite3.connect('/home/pi/Documents/rollsmart/scripts/localDB.db')
	sqlite_cursor = sqlite_conn.cursor()
	sqlite_cursor.execute("INSERT INTO sensor_data (sensor_name, value, timestamp, date) VALUES (?, ?, ?, ?)", data)
	sqlite_conn.commit()
	print("To SQLite-> senName: "+str(senName)+", val:"+str(val)+", date: "+str(date)+", time: " + str(time))

def uploadData(sensor_data):
	# Initializing SQLite connection
	sqlite_conn = sqlite3.connect('/home/pi/Documents/rollsmart/scripts/localDB.db')
	sqlite_cursor = sqlite_conn.cursor()

	# Check internet connection
	internet_status = True
	try:
		requests.get('https://www.google.com')
	except:
		internet_status = False

	# Send data to the appropriate database
	if internet_status:
		if sqlite_cursor.execute("SELECT COUNT(*) FROM sensor_data").fetchone()[0] > 0:
			data = sqlite_cursor.execute("SELECT * FROM sensor_data").fetchall()
			print("===UPLOAD TO FB===")
			for d in data:
				send_to_firebase(d)
			sqlite_cursor.execute("DELETE FROM sensor_data")
			sqlite_conn.commit()
			print("===END===")
		for data in sensor_data:
			send_to_firebase(data)
	else:
		for data in sensor_data:
			send_to_sqlite(data)

# Continuously monitor the sensor data and send it to the appropriate database
#while True:
	#now = datetime.now()
	#nowDate =  str(date.today())
	#nowTime = str(now.strftime("%H:%M:%S"))
	
	#sensor_data = [('heartRate', random.randint(55,75), nowTime, nowDate)]
	#uploadData(sensor_data)
	#ime.sleep(5)
