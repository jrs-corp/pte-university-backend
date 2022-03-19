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
import subprocess
import configparser
import mysql.connector
from getpass import getpass

# # Importing from other py files
from reading import reading
from listening import listening
from writing import writing
# from speaking import speaking
from read import read, check
from insert import insert

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

def main():
    print('Welcome to PTE University')

    first_input = input('''
                    What would you like to do?
                    1) Registration
                    2) Login
                ''')

    if int(first_input) ==  1:
        print('Registration Begins')
        username_desired = input('Enter the username:  ')
        useremail_desired = input('Enter the useremail:  ')
        userpassword_desired = getpass('Enter the password: ')

        # # Check if it already exists or not
        existing_row = check(useremail_desired, username_desired, mycursor)
        if existing_row == None:
            rowcount = insert(username_desired, useremail_desired, userpassword_desired, mycursor, mydb)
            if rowcount == 1:
                print('Registration Successful')
            else:
                print('Registration Failed')
        else:
            print('Registration Failed, the name or email already exists')

    elif int(first_input) == 2:
        print('Login Begins')
        useremail_input = input('Enter the useremail:  ')
        userpassword_input = getpass('Enter the password: ')
        input_row = read(useremail_input, userpassword_input, mycursor)
        if input_row != None:
            print('Login Successful')
            username_input = input_row[1]

            user_input = input(''' 
            Select the module you would like to start:
            1) Reading
            2) Listening
            3) Writing
            4) Speaking
            ''')
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
            else:
                print('Wrong Input, Better Luck Next Time')
        else:
            print('Login failed')

if __name__=="__main__":
    main()

# # # Insert Type 1
# sql = 'INSERT INTO scores (username, useremail, userpassword, speaking, listening, writing, reading) VALUES (%s, %s, %s, %s, %s, %s, %s)'
# val = ('brock', 'brock@gmail.com', 'rick', '1 2 3', '4 3 5', '6 4 3', '7 6 6')
# mycursor.execute(sql, val)
# mydb.commit()
# print(mycursor.rowcount, "Record Inserted")

# # # Insert Type 2
# sql = 'INSERT INTO scores (username, useremail, userpassword, speaking, listening, writing, reading) VALUES (%s, %s, %s, %s, %s, %s, %s)'
# val = ('brock', 'broc@gmail.com', 'rick', '0', '0', '0', '0')
# mycursor.execute(sql, val)
# mydb.commit()
# print(mycursor.rowcount, "Record Inserted")

# # # Update Type 1
# sql = 'UPDATE scores SET speaking = %s WHERE useremail = %s'
# val = ('1 2 3','broc@gmail.com')
# mycursor.execute(sql, val)
# mydb.commit()
# print(mycursor.rowcount, "Record Updated")
#
# # # Update Type 2
# # # Reading the data
# sql = 'SELECT * FROM scores WHERE useremail = %s AND username = %s'
# val = ('brock@gmail.com', 'brock')
# mycursor.execute(sql, val)
# myresult = mycursor.fetchone()
# print(mycursor.rowcount, "Record Extracted")
# speaking_fromdb = myresult[4]
# # # Creating list
# speaking_forcode = speaking_fromdb.split(' ')
# speaking_forcode.append('65')
# # # Reverting back to string for db
# speaking_fordb = ' '.join(speaking_forcode)
# sql = 'UPDATE scores SET speaking = %s WHERE useremail = %s'
# val = (speaking_fordb,'broc@gmail.com')
# mycursor.execute(sql, val)
# mydb.commit()
# print(mycursor.rowcount, "Record Updated")
#
# # # Delete Type 1
# sql = 'DELETE FROM scores WHERE useremail = %s AND username = %s'
# val = ('brock@gmail.com', 'brock')
# mycursor.execute(sql, val)
# mydb.commit()
# print(mycursor.rowcount, "Record Deleted")