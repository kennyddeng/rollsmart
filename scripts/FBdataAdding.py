########
# Functions for adding data into Firebase Database
# Nov.8 2022
# Corbin G.
########


# import all used libraries
import pyrebase

# Create new Firebase config and database object
config = {
  "apiKey": "AIzaSyB8YyKlyoarYSiAfS6ZpbmfFHmW5xLIhYg",
  "authDomain": "sysc4907rollsmart.firebaseapp.com",
  "databaseURL": "https://sysc4907rollsmart-default-rtdb.firebaseio.com/",
  "storageBucket": "sysc4907rollsmart.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

# define the names of tables used in Firebase database
collectedData = "collectedData"
loginInfo = "loginInfo"
name = "name"
hrData = "heartRate"
jerkData = "jerk"
seatData = "seat"
speedData = "speed"
weightDistData = "weightDistribution"

def addUserLogin(name, role, username, password):
	db.child(loginInfo).child(name).child("role").set(role)
	db.child(loginInfo).child(name).child("username").set(username)
	db.child(loginInfo).child(name).child("password").set(password)

def newUDT(name):
	db.child(collectedData).child(name)	
      
def addHRData(name, date, time, HR):
	db.child(collectedData).child(name).child(hrData).child(date).child(time).set(HR)
	
def addJerkData(name, date, time, jerk):
	db.child(collectedData).child(name).child(jerkData).child(date).child(time).set(jerk)
	
def addSeatData(name, date, time, seat):
	db.child(collectedData).child(name).child(seatData).child(date).child(time).set(seat)
	
def addSpeedData(name, date, time, speed):
	db.child(collectedData).child(name).child(speedData).child(date).child(time).set(speed)
	
def addWeightDistData(name, date, time, side):
	db.child(collectedData).child(name).child(weightDistData).child(date).child(time).set(side)
	


#def main():

	

#if __name__ == "__main__":
#	main()
