def read(useremail_input, userpassword_input, mycursor):
    sql = 'SELECT * FROM scores WHERE useremail = %s AND userpassword = %s'
    val = (useremail_input, userpassword_input)
    mycursor.execute(sql, val)
    input_row = mycursor.fetchone()
    return input_row

def check(useremail_input, username_input, mycursor):
    sql = 'SELECT * FROM scores WHERE useremail = %s OR username = %s'
    val = (useremail_input, username_input)
    mycursor.execute(sql, val)
    input_row = mycursor.fetchone()
    return input_row