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
from email_validator import validate_email, EmailNotValidError
from password_validator import PasswordValidator

# Create a schema
schema = PasswordValidator()

# Add properties to it
schema\
.min(8)\
.max(32)\
.has().uppercase()\
.has().lowercase()\
.has().digits()\
.has().symbols()\
.has().no().spaces()\

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
    print(' '+'-' * 150)
    print(' '+'*' * 150)
    print('\n')
    print('\n')
    print('                                                              Welcome to PTE University')
    print('\n')
    print('\n')
    print(' '+'*' * 150)
    #print('-' * 150)

    exit_system = False
    while exit_system == False:
        print(' ╔'+('-' * 149)+'╗')
        print(' ¦                                                                  MAIN MENU'+(' ' * 74)+'¦')
        print(' ¦'+('-' * 149)+'¦')
        print(' ¦' + (' ' * 149) + '¦')
        print(' ¦                [1] Registration        [2] Login               [3] Forget Password     [4] About Us            [5] Exit the System                  ¦')
        print(' ¦' + (' ' * 149) + '¦')
        print(' ╚'+('-' * 149)+ '╝')
        print('\n')
        first_input = input('                        What would you like to do? ')

        # # Validate for input
        check_first_input = True
        while check_first_input == True:
            if first_input.isnumeric() == True:
                check_first_input = False
            else:
                # first_input = input('      Invalid!          What would you like to do? ')
                first_input = input(f'''\n                        Invalid!  

                        What would you like to do? ''')
        # # Validate for input

        print('\n' * 10)
        # print('-'*30)
        #first_input = input('''
        #                What would you like to do?
        #                    [1] Registration
        #                    [2] Login
        #                    [3] Forget Password
        #                    [4] About Us
        #                    [5] Exit the System
        #
        #
        #                I want to: ''')
        #print('-'*30)
        print('\n')
        if int(first_input) ==  1:
            print(' ╔'+('-' * 149)+'╗')
            print(' ¦' + (' ' * 65) + 'REGISTRATION' + (' ' * 72) + '¦')
            print(' ╚'+('-' * 149)+ '╝')
            print('\n')
            # print('Registration')
            username_desired = input('                        Enter the User Name  :  ')
            useremail_desired = input('                        Enter the User Email :  ')

            # # Validate the Email
            check_email_status1 = True
            while check_email_status1 == True:
                try:
                    # Validate.
                    valid = validate_email(useremail_desired)

                    # Update with the normalized form.
                    # email = valid.email
                    check_email_status1 = False
                except EmailNotValidError as e:
                    # email is not valid, exception message is human-readable
                    print(f'\n                        {str(e)}')
                    # print('The email is invalid')
                    # useremail_desired = input('Invalid!                Enter the User Email :  ')
                    useremail_desired = input(f'''\n                        Invalid!  
                               
                        Enter the User Email :  ''')
            # # Validate the Email

            userpassword_desired = getpass('                        Enter the Password   : ')

            # # Validate the password
            check_password_status1 = True
            while check_password_status1 == True:
                if schema.validate(userpassword_desired) == True:
                    check_password_status1 = False
                else:
                    print(f'''\n                        Your password must contain:
                                1) Minimum of 8 Characters
                                2) Has Uppercase and Lowercase
                                3) Has digits
                                4) Has no spaces
                                5) Has special characters''')
                    print('\n')
                    userpassword_desired = getpass(f'''\n                        Invalid!  
                               
                        Enter the Password   : ''')
                    print('\n')
            # # Validate the password

            print('\n')
            pass_hash = hashlib.md5(str(userpassword_desired).encode('utf-8')).hexdigest()

            # # Check if it already exists or not
            existing_row = check(useremail_desired, username_desired, mycursor)
            if existing_row == None:
                rowcount = insert(username_desired, useremail_desired, pass_hash, mycursor, mydb)
                if rowcount == 1:
                    print('                        Registration Successful!')
                    first_input = 2
                else:
                    print('                        Registration Failed!')
            else:
                print('                        Registration Failed, the name or email already exists!')
            print('\n')
            print('\n' * 10)
        elif int(first_input) == 2:
            print(' ╔' + ('-' * 149) + '╗')
            print(' ¦' + (' ' * 69) + 'LOGIN' + (' ' * 75) + '¦')
            print(' ╚' + ('-' * 149) + '╝')
            #print('Login')
            print('\n')
            useremail_input = input('                        Enter the Email        :  ')
            userpassword_input = getpass('                        Enter the Password     : ')
            print('\n')

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

                    #print('-'*30)
                    print('\n')
                    print(' ╔' + ('-' * 149) + '╗')
                    print(' ¦' + (' ' * 63) + 'PROFILE SUMMARY' + (' ' * 71) + '¦')
                    print(' ╚' + ('-' * 149) + '╝')
                    print('\n')
                    # print('                        Your Profile: ')
                    print(f'                        Your Name: {username_input}')
                    print('\n')
                    print('                        SCORES:')
                    print(f'                                Speaking    : {input_row[4]}')
                    print(f'                                Listening   : {input_row[5]}')
                    print(f'                                Writing     : {input_row[6]}')
                    print(f'                                Reading     : {input_row[7]}')
                    #print('-'*30)
                    print('\n')
                    print('\n')

                    #print('-'*30)
                    print(' ╔' + ('-' * 149) + '╗')
                    print(' ¦                                                                  MAIN MENU' + (
                                ' ' * 74) + '¦')
                    print(' ¦' + ('-' * 149) + '¦')
                    print(' ¦' + (' ' * 149) + '¦')
                    print(
                        ' ¦        [1] Reading        [2] Listening      [3] Writing        [4] Speaking       [5] Profile        [6] Log Out        [7] Exit the System        ¦')
                    print(' ¦' + (' ' * 149) + '¦')
                    print(' ╚' + ('-' * 149) + '╝')
                    print('\n')
                    user_input = input('                        What do you want to do next? ')
                    # print('\n' * 10)

                    # # Validate for user_input            
                    check_user_input = True
                    while check_user_input == True:
                        if user_input.isnumeric() == True:
                            check_user_input = False
                        else:
                            user_input = input(f'''\n                        Invalid!  

                        What do you want to do next? ''')
                            # user_input = input('      Invalid!          What do you want to do next? ')
                    # # Validate for user_input

                    #user_input = input('''
                    #
                    #Select the module you would like to start:
                    #1) Reading
                    #2) Listening
                    #3) Writing
                    #4) Speaking
                    #5) Your Profile
                    #6) Log Out
                    #7) Exit the System
                    #''')
                    #print('-'*30)

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
                        print('\n') # skip below processing
                        # print('-'*30)
                        # print('Your Profile from Profile: ')
                        # print(f'Your Name: {username_input}')
                        # print(f'Your scores for speaking {input_row[4]}')
                        # print(f'Your scores for listening {input_row[5]}')
                        # print(f'Your scores for writing {input_row[6]}')
                        # print(f'Your scores for reading {input_row[7]}')
                        # print('-'*30)
                    elif int(user_input) == 6:
                        print(' ' + '-' * 150)
                        print(' ' + '*' * 150)
                        print('\n')
                        print('\n')
                        print('                                                              Welcome to PTE University')
                        print('\n')
                        print('\n')
                        print(' ' + '*' * 150)
                        print(' ' + '-' * 150)
                        print('\n')
                        print('                        LogOut Successfully!')
                        print('\n')
                        internal_exit_status = True
                    elif int(user_input) == 7:
                        internal_exit_status = True
                        exit_system = True
                    else:
                        print('Wrong Input, Better Luck Next Time')
                else:
                    internal_exit_status = True
                    print('                        Login failed! ')
                    print('\n')
                    print('\n' * 10)

        elif int(first_input) == 3:
            print('\n')
            print(' ╔' + ('-' * 149) + '╗')
            print(' ¦' + (' ' * 65) + 'RESET PASSWORD' + (' ' * 70) + '¦')
            print(' ╚' + ('-' * 149) + '╝')
            print('\n')
            # print('You forgot your password')
            letters = string.ascii_lowercase
            random_password=''.join(random.choice(letters) for i in range(10))
            pass_hash = hashlib.md5(str(random_password).encode('utf-8')).hexdigest()
            forgot_email = input('                        Enter the useremail:  ')
            print('\n')
            input_row = set(pass_hash, forgot_email, mycursor, mydb)
            
            if input_row == 0:
                # print('Liar, you dont have your email registered') #lol
                print('                        The email address don''t exist in our database.')
                print('\n' * 10)
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
                print('                        Your new password was sent to your email.')
                print('\n')
                print('\n' * 10)
                first_input = 2
        elif int(first_input) == 4:
            print('\n')
            print(' ╔' + ('-' * 149) + '╗')
            print(' ¦' + (' ' * 67) + 'ABOUT US' + (' ' * 74) + '¦')
            print(' ╚' + ('-' * 149) + '╝')
            print('\n')
            print('''
                        Developed By:
                                        1. Jamelah Guimba
                                        2. Ricardo Chacon
                                        3. Sulabh Shrestha
            ''')
            print('\n')
            print('\n' * 10)
        elif int(first_input) == 5:
            exit_system = True
        else:
            print('                        You entered the wrong key! Please try again.')
            print('\n')

if __name__=="__main__":
    main()