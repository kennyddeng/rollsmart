########
# Functions for adding data into Firebase Database
# Nov.8 2022
# Corbin G.
########


# import all used libraries
import pyrebase

# Create new Firebase config and database object
config = {
  'apiKey': "AIzaSyB8YyKlyoarYSiAfS6ZpbmfFHmW5xLIhYg",
  'authDomain': "sysc4907rollsmart.firebaseapp.com",
  'databaseURL': "https://sysc4907rollsmart-default-rtdb.firebaseio.com",
  'projectId': "sysc4907rollsmart",
  'storageBucket': "sysc4907rollsmart.appspot.com",
  'messagingSenderId': "937699780579",
  'appId': "1:937699780579:web:c626a608dc7a2f0b51a2d6",
  'measurementId': "G-HHFNCNF4NP"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
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

def login():
    print("Log in...")
    email=input("Enter email: ")
    password=input("Enter password: ")
    try:
        login = auth.sign_in_with_email_and_password(email, password)
        print("Successfully logged in!")
        # print(auth.get_account_info(login['idToken']))
       # email = auth.get_account_info(login['idToken'])['users'][0]['email']
       # print(email)
    except:
        print("Invalid email or password")
    return

#Signup Function

def signup():
    print("Sign up...")
    email = input("Enter email: ")
    password=input("Enter password: ")
    try:
        user = auth.create_user_with_email_and_password(email, password)
        ask=input("Do you want to login?[y/n]")
        if ask=='y':
            login()
    except: 
        print("Email already exists")
    return

def addUserDB():
	firebase.database().ref("users/" + firebase.auth().currentUser.uid)


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
	
#Main

#ans=input("Are you a new user?[y/n]")

#if ans == 'n':
    #login()
    
#elif ans == 'y':
    #signup()
    
#newName = input("Enter new name: ")
#newRole = input("Enter new role: ")
#newUsername = input("Enter new username: ")
#newPassword = input("Enter new password: ")
#addUserLogin(newName, newRole, newUsername, newPassword)
#def main():

	

#if __name__ == "__main__":
#	main()
