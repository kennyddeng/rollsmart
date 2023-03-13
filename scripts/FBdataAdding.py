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
	


def main():
	# Define the UID to search for
	uid_to_find = "pbB9DkQHjqdAWmiGIdxK8XNVOLj1"

	# Get a reference to the loginInfo directory
	login_info_ref = db.child("loginInfo")

	# Get all the user profiles in the loginInfo directory
	user_profiles = login_info_ref.get()

	# Loop through each user profile to find the one with the matching UID
	for user_profile in user_profiles.each():
		# Get the UID field value for the current user profile
		user_uid = user_profile.val().get("UID")
		# Check if the UID matches the one we're searching for
		if user_uid == uid_to_find:
			# Return the user profile associated with the matching UID
			print(user_profile.key(), user_profile.val())
			break

	

if __name__ == "__main__":
	main()
