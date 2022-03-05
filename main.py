'''
main.py
Author:
2. Ricardo Chacon
3. Sulabh Shrestha
'''

# # Importing Libraries
import mysql.connector
import configparser

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

# # Insert Type 1
sql = 'INSERT INTO scores (username, useremail, userpassword, speaking, listening, writing, reading) VALUES (%s, %s, %s, %s, %s, %s, %s)'
val = ('brock', 'brock@gmail.com', 'rick', '1 2 3', '4 3 5', '6 4 3', '7 6 6')
mycursor.execute(sql, val)
mydb.commit()
print(mycursor.rowcount, "Record Inserted")

# # Insert Type 2
sql = 'INSERT INTO scores (username, useremail, userpassword) VALUES (%s, %s, %s)'
val = ('brock', 'broc@gmail.com', 'rick')
mycursor.execute(sql, val)
mydb.commit()
print(mycursor.rowcount, "Record Inserted")

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
# val = ('broc@gmail.com', 'brock')
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
