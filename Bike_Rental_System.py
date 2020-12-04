'''
EN.640.635 Software Carpentry
Final Project
Bike Rental System
Cameron Carter and Cameron Guernsey
'''

import math
import random
import hashlib
import pandas as pd
import numpy as np
import getpass

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

        self.user_info = [self.firstname, self.lastname, self.username,
            self.password, self.status, self.bike]

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

        name: *str*
            The name input by the user creating the account

    **Returns**

        user_list: *list of objects*
            The user_list is the master list of user objects that tracks
            their attributes
        new_user: *object*
            The User object in order to update rental information
    '''

    # Create a new user object when the new account is initiated
    print("Let's create a new account. ")
    new_user = User()

    print(new_user)
    print("Decrypted Password: ")
    print(decrypt(new_user.password, new_user.N, new_user.D))
    print("User List: ")
    print(user_list)

    # Append the users list to include the new user
    user_list.append(new_user)

    print("User List: ")
    print(user_list)
    
    return user_list, new_user

def login():
    '''
    This function allows a user to login to their account if
    they have already created one and are renting a bike.

    **Parameters**

        user_list: *list of objects*
            This takes in the master list of users that has already
            been created

    **Returns**

        None
    '''

    # Reference to user_list as global variable
    global user_list

    # Return to the main screen if no users have been created yet
    if len(user_list) == 0:
        print("There are no existing users! ")
        user_list = rent_or_return()

    else:
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
                user_list = rent_or_return()

    return user


def rent_or_return():
    '''
    This initializes the system and acts as the main screen.

    **Parameters**
    
        None
    
    **Returns**

        None
    '''

    # Reference to user_list as global variable
    global user_list

    function = input("Would you like to 'Rent' (1) or 'Return' (2)? \n")
    if function == '1' or function == 'Rent':
        
        #RENT Function Goes Here
        f2 = input(" 'Login' (1) or 'Create an Account' (2) \n")
        if f2 == '1' or f2 == 'Login':
            #LOGIN FUNCTION
            user = login()
            print(user)
        elif f2 == '2' or f2 == 'Create an Account':
            #CREATE ACCOUNT FUNCTION
            user_list, user = create_account()
            def rent_bike():
                print("Choose a bike from the following:")
                print(available_bikes)
                bike_number = input("What is your bike number? \n")
    
                if bike_number in available_bikes:
                    print("Thanks for renting bike number " + bike_number + "! \n")
                    available_bikes.remove(bike_number)
                    print("Remaining bikes available: \n")
                    print(available_bikes)
        
                else:
                    print("Please choose a valid bike number from the list. \n")
                    rent_bike()
        else:
            print("Invalid Input. Select Login (1) or Create an Account (2) ")
            # Send back to main login page if invalid input
            user_list = rent_or_return()
        
        print("Thanks for renting with us!")
    
    elif function == '2' or function == 'Return':
        
        #RETURN Function Goes Here
        
        print('Thanks for returning your bike!')
    else:
        print("Please try again and input a valid command.")

    return user_list

available_bikes = ['A1', 'A2', 'A3', 'A4', 'A5',
                   'B1', 'B2', 'B3', 'B4', 'B5',
                   'C1', 'C2', 'C3', 'C4', 'C5',
                   'D1', 'D2', 'D3', 'D4', 'D5',
                   'E1', 'E2', 'E3', 'E4', 'E5']

if __name__ == "__main__":
    # Initialize the user list outside of the functions
    user_list = []

    while 1==1:

        user_list = rent_or_return()
        print(user_list)
        if input("Continue? Y or N \n") == "N":
            break
        
