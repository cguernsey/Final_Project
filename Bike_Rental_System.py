'''
EN.640.635 Software Carpentry
Final Project
Bike Rental System
Cameron Carter and Cameron Guernsey
'''

import math
import random
import numpy as np
import getpass
import xlsxwriter
from datetime import datetime

def is_prime(p):
    '''
    This function will return True if p is prime, or False if not.

    **Parameters**

        p: *int*
            The number you wish to determine whether it is prime or not

    **Returns**

        prime_answer: *bool*
            True if prime, False if not
    '''
    # This is not a prime number.
    if (p == 1):

        return False
    # This is a prime number.
    if (p == 2):

        return True
    # If the number is even it is not prime.
    if (p % 2 == 0):

        return False
    # Loops through to find prime factors.
    i = 3
    while i < math.sqrt(p) + 1:
        if p % i == 0:

            return False

        i += 2

    return True


def get_prime_divisors(N):
    '''
    This function will get all the prime divisors of a given integer N.

    **parameters**

        p: *int*
            The number you wish to find the prime divisors of.

    **Returns**

        primes: *int*
            The list of prime divisors of N.
    '''
    # Creates an empty list to hold the prime divisors of N.
    primes = []

    # Loops through divisors of N checking with is_prime function.
    i = 2
    while i < (N/2 + 1):
        if (N % i == 0):
            if (is_prime(i)):
                primes.append(i)

        i += 1

    return(primes)


def get_primes_in_range(low, high):
    '''
    This function will return the prime numbers in a given range.

    **Parameters**

        p: *int*
            The range that you wish to find the prime numbers within

    **Returns**

        primes_in_ramge: *int*
            The list of prime numbers within the range
    '''
    # Creates an empty list to add the prime values that are within the range.
    primes_in_range = []

    # Uses is_prime function to test values within range.
    for x in range(low, high + 1):
        if (is_prime(x)):

            primes_in_range.append(x)

    return(primes_in_range)


def generate_key():
    '''
    This will generate the key for encryption and decryption of a message.

    **Parameters**

        None

    **Returns**

        N, E, D: *int*
            The values of the key used for encryption
    '''
    # Gets all the prime values within the specified range.
    primes = get_primes_in_range(130, 555)

    # Randomly generates values for P and Q based on primes list.
    P = random.choice(primes)
    Q = random.choice(primes)

    N = P*Q
    X = (P - 1)*(Q-1)

    # Gets the prime divisors of X and primes within the range of X.
    divisors = get_prime_divisors(X)
    primes_in_range = get_primes_in_range(2, X)

    e = []

    # Adds the prime values that are not divisors of X to a list.
    i = 2
    while i < (len(primes_in_range)):
        if (primes_in_range[i] not in divisors):
            e.append(primes_in_range[i])

        i += 1

    E = random.choice(e)

    k = 1

    D = (k * X + 1) / E

    # As long as D is not an integer loop through k until D becomes integer.
    while D.is_integer() is not True:
        k += 1

        D = (k * X + 1) / E

    # Casts D as an integer.
    D = int(D)

    return(N, E, D)


def encrypt(message, N, E):
    '''
    This function will encrypt a given string message with N and D values.

    **Parameters**

        p: *str, int*
            The message and integers, N and D, used to encrypt the string

    **Returns**

        encryption: *int*
            The encrypted message as a list of integers
    '''

    # Creates the empty list to which the encrypted values will be added.
    encryption = []

    # Loops through every element in the string.
    for x in range(len(message)):
        M = ord(message[x])
        C = M**E % N

        # Adds the encrypted value as the next element of the list.
        encryption.append(C)

    return(encryption)


def decrypt(encrypted_message, N, D):
    '''
    This function will decrypt the encrypted message given with N and D values.

    **Parameters**

        p: *int*
            The numbers from the encrypted message as well as N and D integers

    **Returns**

        newmsg: *str*
            The decrypted message as a string
    '''

    # Creates an empty string for the new message to be constructed.
    newmsg = ""

    # Loops through every element in the encrypted list.
    for x in range(len(encrypted_message)):
        C = encrypted_message[x]
        M = C**D % N

        # Turns the decrypted M value back into the string value.
        decrypted = chr(M)

        # Builds the original string.
        newmsg += decrypted

    return(newmsg)


class User:
    '''
    This class handles the creation and info of users to the
    rental system.
    '''

    def __init__(self):
        '''
        This initializes the attributes of new users.

        **Parameters**

            None

        **Returns**

            User Object
        '''

        # Allow user to input their name and username
        self.firstname = input('What is your FIRST NAME? ')
        self.lastname = input('What is your LAST NAME? ')
        self.username = input('Create a USERNAME: ')

        # Generate a new key for each user to encrypt their password
        key = generate_key()
        self.N = key[0]
        self.E = key[1]
        self.D = key[2]

        self.password = encrypt(getpass.getpass('Create a PASSWORD: '),
                                self.N, self.E)

        # Initialize the default rental status and bike rented
        self.status = "Not Renting"
        self.bike = "None"
        self.time_out = 0
        self.time_in = 0

        self.user_info = [self.firstname, self.lastname, self.username,
            self.password, self.status, self.bike, [self.N, self.E, self.D],
            self.time_out, self.time_in]

    def __str__(self):
        '''
        Makes the user refer to itself as its username
        '''
        return self.username

    def __repr__(self):
        '''
        Allows you to use print() or to write str(user)
        '''
        return str(self)

def create_account():
    '''
    This function creates a new user account for first time users
    and will create new User objects.

    **Parameters**

        None

    **Returns**

        user_list: *list of objects*
            The user_list is the master list of user objects that tracks
            their attributes
        new_user: *object*
            The User object in order to update rental information
    '''

    # Reference to user_list as global variable
    global user_list

    # Create a new user object when the new account is initiated
    print("Let's create a new account. ")
    new_user = User()

    if str(new_user) in str(user_list):
        print("Username already taken. Please choose another. ")
        new_user = User()

        
    # Append the users list to include the new user
    user_list.append(new_user)

    # Print the list of users
    print("User List: ")
    print(user_list)
    
    return user_list, new_user

def login():
    '''
    This function allows a user to login to their account if
    they have already created one and are renting a bike.

    **Parameters**

        None

    **Returns**

        user: *object*
            The user object and its attributes
    '''

    # Reference to user_list and available_bikes as global variables
    global user_list
    global available_bikes

    # Initialize user as not found
    user = "Not found"

    # Allow user to input username and password
    usrname = input("What is your username? ")
    pssword = getpass.getpass("What is your password? ")

    # Search for the user in the master list based on username and pass
    for i in range(len(user_list)):

        if str(user_list[i]) == usrname and decrypt(user_list[i].password,
            user_list[i].N, user_list[i].D) == pssword:

            # Record the found user and break the loop
            print("Welcome " + user_list[i].firstname + "!")
            user = user_list[i]
            break

    if user == "Not found":
        print("Username or Password incorrect ")
        if input("Try again? Y or N \n") == "Y":
            user = login()
        else:
            user_list, available_bikes = rent_or_return()

    return user


def rent_bike(user):
    '''
    This removes the rented bike from the available list and
    tracks the real time that the user rented the bike.

    **Parameters**

        user: *object*
            The user to record who rented the bike
    
    **Returns**
    
        user_list: *list of objects*
            The master list of users
    '''

    # Reference to user_list and available_bikes as global variables
    global user_list
    global available_bikes

    print("Choose a bike from the following:")
    print(available_bikes)
    bike_number = input("What is your bike number? \n")

    # Check if the bike number exists and user did not input "OUT"
    if bike_number in available_bikes and not bike_number == "OUT":
        print("Thanks for renting bike " + bike_number + "! \n")

        # List comprehension to replace rented bike
        available_bikes = ["OUT" if bik == bike_number else bik for \
            bik in available_bikes]
        print("Remaining bikes available: \n")
        print(available_bikes)

        for item in user_list:
            if user == item:
                # Update user attributes for rental
                user.status = "Renting"
                user.bike = bike_number
                user.time_out = datetime.now()
                item = user
                # Update the user_info attribute to reflect changes
                user.user_info = [user.lastname, user.firstname, user.username,
                    user.password, user.status, user.bike, [user.N, user.E, user.D],
                    user.time_out, user.time_in]
            else:
                pass

    else:
        print("Please choose a valid bike number from the list. \n")
        user_list = rent_bike(user)

    return user_list


def rental_check(user):
    '''
    This checks the rental status of a user.

    **Parameters**

        user: *object*
            The user looking to rent a bike

    **Returns**

        *bool*
            Return False if user is already renting
    '''

    if user.status == "Renting":
        print("You are already renting a bike. ")
        print("Please return your rented bike before renting another. ")
        
        return False
    else:
        return True


def return_bike():
    '''
    This returns a bike based on the bike number and updates the
    appropriate user's information accordingly.

    **Parameters**

        None
    
    **Returns**

        user_list: *list of objects*
            The master list of users
        available_bikes: *list of str*
            The current bike list of available bikes
    '''

    # Reference to user_list and available_bikes as global variable
    global user_list
    global available_bikes

    # Set the bike and cost variables
    bike_number = input("What is your bike number? \n")
    flat_fee = 4
    rate = 0.10

    # Check to see if the inputted bike is correctly missing from the list
    if bike_number not in available_bikes:

        # Return bike if bike number matches user's rented bike
        for item in user_list:
            if bike_number == item.bike:
                # Update the user info after returning the bike
                item.status = "Not Renting"
                item.bike = "None"
                item.time_in = datetime.now()
                # Update the user_info attribute to reflect changes
                item.user_info = [item.lastname, item.firstname, item.username,
                    item.password, item.status, item.bike, [item.N, item.E, item.D],
                    item.time_out, item.time_in]

                # Calculate time the bike was rented and cost to user
                time_rented = item.time_in - item.time_out
                min_rented = time_rented.total_seconds()/60
                cost = float(flat_fee) + (rate * float(min_rented))
                print("Your cost for this ride is $", round(cost,2))

                # Replace the bike back into the list of available bikes
                let = bike_number[0]
                if let == "A":
                    num = int(bike_number[1]) - 1
                elif let == "B":
                    num = int(bike_number[1]) + 4
                elif let == "C":
                    num = int(bike_number[1]) + 9
                elif let == "D":
                    num = int(bike_number[1]) + 14
                elif let == "E":
                    num = int(bike_number[1]) + 19
                
                # Replace bike if the list item is labeled as "OUT"
                if available_bikes[num] == "OUT":
                    available_bikes[num] = bike_number
            
            else:
                pass
    
    else:
        print("This is not a valid bike number to return. ")
        user_list, available_bikes = rent_or_return()
    
    return user_list, available_bikes



def rent_or_return():
    '''
    This initializes the system and acts as the main screen.

    **Parameters**

        None

    **Returns**

        user_list: *list of objects*
            The master list of users
        available_bikes: *list of str*
            The current bike list of available bikes
    '''

    # Reference to user_list and available_bikes as global variables
    global user_list
    global available_bikes

    # Choose to rent or return a bike
    function = input("Would you like to 'Rent' (1) or 'Return' (2)? Or enter 'Exit' (0) to exit the program. \n")
    if function == '1' or function == 'Rent':
        
        f2 = input(" 'Login' (1) or 'Create an Account' (2) \n")
        if f2 == '1' or f2 == 'Login':
            # Check if any users have been created first
            if len(user_list) == 0:
                print("There are no existing users! ")
                user_list, available_bikes = rent_or_return()
            else:
                # Login if selected by user and users exist
                user = login()
                if rental_check(user):
                    user_list = rent_bike(user)
                else:
                    user_list, available_bikes = rent_or_return()

        elif f2 == '2' or f2 == 'Create an Account':
            # Create Account
            user_list, user = create_account()
            user_list = rent_bike(user)

        else:
            print("Invalid Input. Select Login (1) or Create an Account (2) ")
            # Send back to main login page if invalid input
            user_list, available_bikes = rent_or_return()
        
        print("Thanks for renting with us!")
    
    elif function == '2' or function == 'Return':
        
        # Return bike
        user_list, available_bikes = return_bike()
        print("Thanks for returning your bike! ")

    # Exit the program
    elif function == '0' or function == 'Exit':
        pass
    
    else:
        print("Please try again and input a valid command.")

    return user_list, available_bikes

def create_excel():
    '''
    This writes the user list to an excel document for reference.

    **Parameters**

        user_list: *list of objects*
            The list of users
    
    **Returns**

        None
    '''

    # Reference to user_list as global variable
    global user_list

    # Create the excel workbook
    workbook = xlsxwriter.Workbook('Bike_Rental_User_Data.xlsx')

    # Create the main user worksheet
    worksheet = workbook.add_worksheet("Users")

    # These column headers are the attributes of each User object
    headers = ["Lastname", "Firstname", "Username", "Enc Password", "Rental Status",
        "Bike Rented", "Encryption Key", "Time Out", "Time In"]

    row = 0
    column = 0

    # Add the headers to the sheet
    for item in headers:
        worksheet.write(row, column, item)
        column += 1

    # Reset row and column index to add users
    row = 1
    column = 0

    # Add users to the sheet
    for i in user_list:
        for j in range(len(headers)):
            print(i.user_info[j])
            worksheet.write(row, column, str(i.user_info[j]))
            column += 1
        row += 1

    workbook.close()


if __name__ == "__main__":
    # Initialize the user list outside of the functions
    user_list = []

    # Initialize the bike list outside of the functions
    available_bikes = ['A1', 'A2', 'A3', 'A4', 'A5',
                       'B1', 'B2', 'B3', 'B4', 'B5',
                       'C1', 'C2', 'C3', 'C4', 'C5',
                       'D1', 'D2', 'D3', 'D4', 'D5',
                       'E1', 'E2', 'E3', 'E4', 'E5']

    # Create an infinite loop to simulate user operating app
    while 1==1:
        # This is the main function to initiate the program
        user_list, available_bikes = rent_or_return()

        print("Users: ")
        print(user_list)
        print("User Info: ")
        for item in user_list:
            print(item.user_info)

        print("Bike List: ")
        print(available_bikes)

        # Allow user to break loop to simulate closing app
        if input("Continue? Y or N \n") == "N":
            create_excel()
            break
