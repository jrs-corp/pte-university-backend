'''
main.py
Authors:
1. Jamelah Guimba
2. Ricardo Chacon
3. Sulabh Shrestha

Information for code and database
4 -> speaking
5 -> listening
6 -> writing
7 -> reading
'''

# # Importing Libraries
import os
import sys
import boto3
import random
import string
import hashlib
import subprocess
import configparser
import mysql.connector
from getpass import getpass

# # Importing from other py files
from insert import insert
from writing import writing
from reading import reading
from listening import listening
# from speaking import speaking
from read import read, check, get, set

# # Parsing the configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# # Connecting to MYSQL Database
mydb = mysql.connector.connect(
  host=config['DATABASE']['host'],
  user=config['DATABASE']['user'],
  password=config['DATABASE']['password'],
  database=config['DATABASE']['database']
)
mycursor = mydb.cursor()

# # Setting up Values for Simple Email Service (SES)
SENDER = config['EMAIL']['sender_email']
AWS_REGION = config['EMAIL']['aws_region']
SUBJECT = "PTE University"
SUCCESS_BODY_TEXT = ("Status of the Password\r\n"
            "Your password success status"
            )
FAILURE_BODY_TEXT = ("Status of the Password\r\n"
            "Your password failure status"
            )

# # The main function from which our program runs
def main():
    print('Welcome to PTE University')

    exit_system = False
    while exit_system == False:
        print('-'*30)
        first_input = input('''
                        What would you like to do?
                        1) Registration
                        2) Login
                        3) Forget Password
                        4) About Us
                        5) Exit the System
                    ''')
        print('-'*30)
        if int(first_input) ==  1:

            print('Registration')
            username_desired = input('Enter the username:  ')
            useremail_desired = input('Enter the useremail:  ')
            userpassword_desired = getpass('Enter the password: ')
            pass_hash = hashlib.md5(str(userpassword_desired).encode('utf-8')).hexdigest()

            # # Check if it already exists or not
            existing_row = check(useremail_desired, username_desired, mycursor)
            if existing_row == None:
                rowcount = insert(username_desired, useremail_desired, pass_hash, mycursor, mydb)
                if rowcount == 1:
                    print('Registration Successful')
                    first_input = 2
                else:
                    print('Registration Failed')
            else:
                print('Registration Failed, the name or email already exists')

        elif int(first_input) == 2:

            print('Login')
            useremail_input = input('Enter the useremail:  ')
            userpassword_input = getpass('Enter the password: ')
            pass_hash = hashlib.md5(str(userpassword_input).encode('utf-8')).hexdigest()

            internal_exit_status = False
            while internal_exit_status == False:
                # # Cause profile needs to be refreshed everytime
                input_row = read(useremail_input, pass_hash, mycursor)

                if input_row != None:
                    # print('Login Successful')
                    username_input = input_row[1]

                    # internal_exit_status = False
                    # while internal_exit_status == False:

                    print('-'*30)
                    print('Your Profile: ')
                    print(f'Your Name: {username_input}')
                    print(f'Your scores for speaking {input_row[4]}')
                    print(f'Your scores for listening {input_row[5]}')
                    print(f'Your scores for writing {input_row[6]}')
                    print(f'Your scores for reading {input_row[7]}')
                    print('-'*30)

                    print('-'*30)
                    user_input = input(''' 
                    
                    Select the module you would like to start:
                    1) Reading
                    2) Listening
                    3) Writing
                    4) Speaking
                    5) Your Profile
                    6) Log Out
                    7) Exit the System
                    ''')
                    print('-'*30)

                    if int(user_input) == 1:
                        reading(useremail_input, username_input, mycursor, mydb)
                    elif int(user_input) == 2:
                        listening(useremail_input, username_input, mycursor, mydb)
                    elif int(user_input) == 3:
                        writing(useremail_input, username_input, mycursor, mydb)
                    elif int(user_input) == 4:
                        my_env = os.environ.copy()
                        my_env["FLASK_APP"] = "speaking.py"
                        my_env["FLASK_EMAIL"] = useremail_input
                        my_env["FLASK_USR"] = username_input
                        my_command = "flask run"
                        subprocess.Popen(my_command, env=my_env)
                    elif int(user_input) == 5:
                        print('-'*30)
                        print('Your Profile from Profile: ')
                        print(f'Your Name: {username_input}')
                        print(f'Your scores for speaking {input_row[4]}')
                        print(f'Your scores for listening {input_row[5]}')
                        print(f'Your scores for writing {input_row[6]}')
                        print(f'Your scores for reading {input_row[7]}')
                        print('-'*30)   
                    elif int(user_input) == 6:
                        print('LogOut Successfully')
                        internal_exit_status = True
                    elif int(user_input) == 7:
                        internal_exit_status = True
                        exit_system = True
                    else:
                        print('Wrong Input, Better Luck Next Time')
                else:
                    internal_exit_status = True
                    print('Login failed')

        elif int(first_input) == 3:

            print('You forgot your password')
            letters = string.ascii_lowercase
            random_password=''.join(random.choice(letters) for i in range(10))
            pass_hash = hashlib.md5(str(random_password).encode('utf-8')).hexdigest()
            forgot_email = input('Enter the useremail:  ')
            input_row = set(pass_hash, forgot_email, mycursor, mydb)
            
            if input_row == 0:
                print('Liar, you dont have your email registered')
            else:
                RECIPIENT = forgot_email
                SUCCESS_BODY_HTML = f"""<html>
                <head></head>
                <body>
                <h1>PTE University</h1
                <p>Your password is {random_password}</p>
                </body>
                </html>
                            """            
                FAILURE_BODY_HTML = """<html>
                <head></head>
                <body>
                <h1>PTE University</h1>
                <p>Failure</p>
                </body>
                </html>
                            """            
                CHARSET = "UTF-8"
                
                # # Setting up boto3 client
                client = boto3.client('ses',
                aws_access_key_id=config['AWS']['aws_access_key_id'],
                aws_secret_access_key=config['AWS']['aws_secret_access_key'],
                region_name=AWS_REGION)

                # # Send Email to the recipient
                response = client.send_email(
                    Destination={
                        'ToAddresses': [
                            RECIPIENT,
                        ],
                    },
                    Message={
                        'Body': {
                            'Html': {
                                'Charset': CHARSET,
                                'Data': SUCCESS_BODY_HTML,
                            },
                            'Text': {
                                'Charset': CHARSET,
                                'Data': SUCCESS_BODY_TEXT,
                            },
                        },
                        'Subject': {
                            'Charset': CHARSET,
                            'Data': SUBJECT,
                        },
                    },
                    Source=SENDER,
                )
                print('Your new password has sent to your email')
                first_input = 2
        elif int(first_input) == 4:
            print('''
            Developed By:
                1. Jamelah Guimba: Our Description Here
                2. Ricardo Chacon: Our Description Here
                3. Sulabh Shrestha: Our Description Here
            ''')
        elif int(first_input) == 5:
            exit_system = True
        else:
            print('You entered the wrong key')

if __name__=="__main__":
    main()