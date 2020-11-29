'''
EN.640.635 Software Carpentry
Final Project
Bike Rental System
Cameron Carter and Cameron Guernsey
'''

import hashlib
import pandas as pd
import numpy as np
import getpass


def encrypt(msg, N, E):
    '''
    This function will encrypt a given string message with N and D values.

    **Parameters**

        *str, int*
            The message and integers, N and D, used to encrypt the string

    **Returns**

        *int*
            The encrypted message as a list of integers
    '''

    return[(ord(s) ** E) % N for s in msg]


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


