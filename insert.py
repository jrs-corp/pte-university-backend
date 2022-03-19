def insert(username_desired, useremail_desired, userpassword_desired, mycursor, mydb):
    sql = 'INSERT INTO scores (username, useremail, userpassword, speaking, listening, writing, reading) VALUES (%s, %s, %s, %s, %s, %s, %s)'
    val = (username_desired, useremail_desired, userpassword_desired, '0', '0', '0', '0')
    mycursor.execute(sql, val)
    mydb.commit()
    return mycursor.rowcount