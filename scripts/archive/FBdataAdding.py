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
COLLECTED_DATA = "collectedData"
LOGIN_INFO = "loginInfo"
NAME = "name"
HR_DATA = "heartRate"
JERK_DATA = "jerk"
SEAT_DATA = "seat"
SPEED_DATA = "speed"
WEIGHT_DIST_DATA = "weightDistribution"

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


def addUserLogin(NAME, role, username, password):
    db.child(LOGIN_INFO).child(NAME).child("role").set(role)
    db.child(LOGIN_INFO).child(NAME).child("username").set(username)
    db.child(LOGIN_INFO).child(NAME).child("password").set(password)

def newUDT(NAME):
    db.child(COLLECTED_DATA).child(NAME)

def addHRData(NAME, date, time, HR):
    db.child(COLLECTED_DATA).child(NAME).child(HR_DATA).child(date).child(time).set(HR)

def addJerkData(NAME, date, time, jerk):
    db.child(COLLECTED_DATA).child(NAME).child(JERK_DATA).child(date).child(time).set(jerk)

def addSeatData(NAME, date, time, seat):
    db.child(COLLECTED_DATA).child(NAME).child(SEAT_DATA).child(date).child(time).set(seat)

def addSpeedData(NAME, date, time, speed):
    db.child(COLLECTED_DATA).child(NAME).child(SPEED_DATA).child(date).child(time).set(speed)

def addWeightDistData(NAME, date, time, side):
    db.child(COLLECTED_DATA).child(NAME).child(WEIGHT_DIST_DATA).child(date).child(time).set(side)

#Main

#ans=input("Are you a new user?[y/n]")

#if ans == 'n':
    #login()

#elif ans == 'y':
    #signup()

#newNAME = input("Enter new NAME: ")
#newRole = input("Enter new role: ")
#newUserNAME = input("Enter new userNAME: ")
#newPassword = input("Enter new password: ")
#addUserLogin(newNAME, newRole, newUserNAME, newPassword)
#def main():


#if __NAME__ == "__main__":
#	main()
