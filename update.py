def update(email, username, mycursor, mydb, module_number, module_name, temp_marks):
    sql = 'SELECT * FROM scores WHERE useremail = %s AND username = %s'
    val = (email, username)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchone()
    fromdb = myresult[module_number]

    # # Creating list
    forcode = fromdb.split(' ')
    forcode.append(str(temp_marks))

    # # Reverting back to string for db
    fordb = ' '.join(forcode)

    # # Update query
    if module_name == 'reading':
        sql = 'UPDATE scores SET reading = %s WHERE useremail = %s'
    elif module_name == 'speaking':
        sql = 'UPDATE scores SET speaking = %s WHERE useremail = %s'
    elif module_name == 'listening':
        sql = 'UPDATE scores SET listening = %s WHERE useremail = %s'
    elif module_name == 'writing':
        sql = 'UPDATE scores SET writing = %s WHERE useremail = %s'
    val = (fordb, email)
    mycursor.execute(sql, val)
    mydb.commit()
    # print(mycursor.rowcount, "Record Updated")
    print('\n')
    print(f"                        Record Updated: {mycursor.rowcount}")