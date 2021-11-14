import firebase_admin
from firebase_admin import credentials, initialize_app
from firebase_admin import firestore
import os

def initialize_firestore():
    """
    Create database connection
    """

    # Setup Google Cloud Key - The json file is obtained by going to 
    # Project Settings, Service Accounts, Create Service Account, and then
    # Generate New Private Key
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]  = "cloud_database_start/fencing-attendance-firebase-adminsdk-5go47-4f6cd6f504.json"

    # Use the application default credentials.  The projectID is obtianed 
    # by going to Project Settings and then General.
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
        'projectId': 'fencing-attendance',
    })

    # Get reference to database
    db = firestore.client()
    return db

def increment_attendance(name, db):
    #gets that name from the database
    attendee = db.collection("fencers").document(name).get()

    #quick error check, should never fire as the previous statement in the handle_input funtion shoudln't send a nonexistent person this way
    if not attendee.exists:
        print("This is very bad. You should never have gotten here.")
        return
    
    #switch to dictionary
    new_data = attendee.to_dict()

    ##increases the attendance
    new_data["total_attendance"] += 1

    #makes the attendance the new document
    db.collection("fencers").document(name).set(new_data)



def get_first_name():
    #Gets first name
    name = input("What is your first name? ")
    return name

def get_last_name():
    #Gets last name from user
    name = input("What is your last name? ")
    return name

def get_email():
    #gets the email from the user
    email = input("What is your email? ")
    return email

def display_attendance(db):
    #once I am able to implement the attendace by day, this function will display it to the admin
    pass

def display_fencers(db):
    """Displays the fencer list with information to the admin"""
    fencers_db = db.collection("fencers").get()


    print("All Fencers")
    print(f"{'Name':<30}   {'Email':<30}  {'Total Attendance':<10}")

    #For each fencer in the database, print them out
    for fencer in fencers_db:

        person = fencer.to_dict()
        print(f"{fencer.id:<30}   {person['email']:<30}  {person['total_attendance']:<10}")
    print()   

def admin_sign_in(db):
    """An admin sign in function to keep the people who want to sign in from our special admins"""
    password_attempt = get_user_pass()

    #get password that is in the database, I'd like to have a little more robust password system
    actual_pass = db.collection("super_secret_password").document("password").get()

    #if the password doesn't exist... hoo boy
    if not actual_pass.exists:
        print("Check database, something bad has happened.")
        return
    
    pass_dict = actual_pass.to_dict()

    #if the password is correct, the admin may see the admin actions!
    if password_attempt == pass_dict["pass"]:
        print("Welcome!")
        admin_actions(db)
        return
    else:
        print("That password was not recognized")
        return

def admin_actions(db):
    """Handles super cool actions that are only for admins"""

    print("Hello important admin! What would you like to do today?")
    print("\t1) Get fencer list")
    print("\t2) Get attendance for a day")
    print("\t3) Quit admin")

    # Similar input error checking to normal actions
    admin_interacting = True

    while (admin_interacting):
        bad_choice = True
        while(bad_choice):
            try:
                user_choice = int(input("Please select an option: "))
            except:
                print("Input not recognized")
            
            if user_choice > 3 or user_choice < 1:
                print("Not an option! Try again")
                continue

            if user_choice == 1:
                display_fencers(db)
            elif user_choice == 2:
                display_attendance(db)
            elif user_choice == 3:
                admin_interacting = False
                return
            else:
                print("This should never have happened")


def get_user_pass():
    return input("Please enter a password: ")

def create_new_person(name, email, db):
    """If this is the person's first time here, the program creates a new spot in the database for them"""
    #first creates the data for the user
    data = {
        'email': email,
        'total_attendance' : 0
    }

    #Adds the data to the user in firestore
    db.collection("fencers").document(name).set(data)
    increment_attendance(name, db)

def handle_input(db):
    """This function handles the input that the program gets from the user on startup"""
    first_name = get_first_name().lower()
    last_name = get_last_name().lower()

    full_name = first_name + " " + last_name

    result = db.collection("fencers").document(full_name).get()
    #if person already in database 
    if result.exists:
        #increase their total attendance
        increment_attendance(full_name, db)
        print("Thanks for signing in!")
        return
    else:
        #create a new spot in the database for them2
        
        print("Welcome to Fencing! Just a few more details to get you all set up.\n")
        email = get_email()
        create_new_person(full_name, email, db)
        print("Sign in successful! Enjoy your day!")
        return

db = initialize_firestore()

user_interacting = True

print("Hello! Welcome to the Rexburg fencing workshop!")

while(user_interacting):
    print("Please select an option")
    print("\t1) Sign in")
    print("\t2) Sign in as admin")
    print("\t3) Quit")

    bad_choice = True
    user_choice = 0
    while(bad_choice):
        try:
            user_choice = int(input(" > "))

            if (user_choice > 3 or user_choice < 1):
                print("That option doesn't exist, try again!")
            else:
                bad_choice = False
        except:
            print("Input not recognized, try again!")
    
    if user_choice == 1:
        handle_input(db)
    elif user_choice == 2:
        admin_sign_in(db)
    elif user_choice == 3:
        user_interacting = False
    else:
        print("You shouldn't be here.")
