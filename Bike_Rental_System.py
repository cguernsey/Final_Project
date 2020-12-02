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

        # user_list = user_list.append(self.user_info)

def create_account():
    '''
    This function creates a new user account for first time users
    and will create new User objects.

    **Parameters**

        None

    **Returns**

        None
    '''

    # Initialize the users list if it does not exist
    if 'user_list' in globals() or 'user_list' in locals():
        pass
    else:
        user_list = []

    # Create a new user object when the new account is initiated
    print("Let's create a new account. ")
    new_user = User()

    print(new_user.user_info)
    print("Decrypted Password: ")
    print(decrypt(new_user.password, new_user.N, new_user.D))
    print("User List: ")
    print(user_list)

    # Append the users list to include the new user
    user_list.append(new_user.user_info)

    print("User List: ")
    print(user_list)


def password(enc_msg, usr, passwd, N, D):
    '''
    This function decrypts an encrypted message if the given username
    and password match the information in the database.

    **Parameters**

        *list, str, int*
            The encrypted message list, the string username and password,
            and the integers values of N and D

    **Returns**

        *str*
            The decrypted message if username and password match
    '''

    def decrypt(enc_msg, N, D):
        '''
        This function will decrypt the encrypted message given with N and D
        values.

        **Parameters**

            *list, int*
                The encrypted message list as well as N and D integers

        **Returns**

            *str*
                The decrypted message as a string
        '''
        return ''.join([chr((s ** D) % N) for s in enc_msg])

    # These are the randomly generated salts for each password hash
    salt1 = b'\xf3\x1f\xca\xbb\xa5\x11\xada\xdc\x12\xe4\x9a\xf5+\xc0\x02'
    salt2 = b'<\xfb\x96\xcfz\xa7\xa9\xd2]\x8a?\x90\xf8!_#'

    # These are the salted password hashes added to the database
    pass1 = [b'\xf9y\r\xa99\xb0d)V\xd0\xecv_\xfc\xd1\x17(\xf0\xbe=T\xbe\xb1z'
             b'\xb0\xc0\xfc+\xd2,\xb4\x91\x98\x917\xf8\x1f\x05\x06?+\xcc\x0b]'
             b'\x0fB\xb5\x19\x88\xccS0x\r\x813\xc6\xe7\xab8\x8e\xc6\x1b%']

    pass2 = [b'\x04\xa9\x1e\x1fPo4OZ\xe6w0!F\xcc\xa8h\x0fM\xd7\xa9\x85p\x10'
             b'\xf9\x8a7\x08\xf4\xa4\xa5(A{\xb2\xf2~\xdf5\xa9\xb9x\x11\xebEb'
             b'\xf7\xceo<"v\x84\xdacG*\x92\x80\xef\xf9\x82\xf5\x0e']

    # Create a database of usernames, passwords, and salts
    df = pd.DataFrame(columns=['Username', 'Password', 'Salt'])
    new_users = pd.DataFrame([['hherbol1', pass1[0], salt1],
                              ['cvcarter', pass2[0], salt2]],
                             columns=['Username', 'Password', 'Salt'])
    df = df.append(new_users, ignore_index=True)

    # Check if username exists in the database and return row
    if df['Username'].str.contains(usr).any():
        ind = np.where(df['Username'] == usr)
        ind = int(ind[0])
    else:
        raise AssertionError("Username not found")

    # Create the salted hash of the password given by the user
    passwd = str.encode(passwd)
    hash_passwd = hashlib.pbkdf2_hmac('sha512', passwd, df.at[ind, 'Salt'],
                                      100000)

    # Loop through dataframe to check if hashed password matches
    if hash_passwd == df.Password[ind]:
        print("The password is accepted!")
        return(decrypt(enc_msg, N, D))
    else:
        raise AssertionError("Password is incorrect")

        
def rent_or_return():
    function = input("Would you like to Rent (1) or Return (2)? \n")
    if function == '1' or function == 'Rent':
        
        #RENT Function Goes Here
        
            #LOGIN FUNCTION
            
            #CREATE ACCOUNT FUNCTION (__init__(new_user))
        
            #RENT_BIKE FUNCTION    
            
        
    print("Thanks for renting with us!")
    
    elif function == '2' or function == 'Return':
        
        #RETURN Function Goes Here
        
        print('Thanks for returning your bike!')
    else:
        print("Please try again and input a valid command.")

if __name__ == '__main__':
    rent_or_return()
