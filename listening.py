# # Importing Libraries
import configparser
from playsound import playsound
from azure.data.tables import TableClient

# # Importing from other py files
from update import update

# # Parsing the configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# # Setting up the connection
connection_string = config['TABLEAPI']['connection_string']
table_name = config['TABLEAPI']['table_name']
my_filter = "PartitionKey eq 'Listening'"
table_client = TableClient.from_connection_string(conn_str=connection_string, table_name=table_name)
entities = table_client.query_entities(my_filter)

def listening(email, username, mycursor, mydb):
    temp_marks = 0
    # # Looping through the listening questions
    for entity in entities:
        temp_answers = entity['Answers'].split(',')
        # # Showing the question
        playsound('Audio1.mp3')
        print(entity['Question'])
        print(temp_answers)
        pass_status = True

        # # Listing question from ListQuestion
        temp_questions = entity['ListQuestion'].split(',')

        for i in range(int(entity['Blanks'])):
            # # Asking for answers
            input_answer = input(f'{temp_questions[i]} ')
            # # We will only give full marks if all the blanks of a certain questions are fullfilled
            if input_answer == temp_answers[i]:
                pass_status = True
            else:
                pass_status = False
        if pass_status == True:
            temp_marks += 1
        quit_status = input('Do you want to take a break? ')
        if quit_status == 'Y' or quit_status == 'y':
            break
        print('-'*30)
    print('The final marks: ', temp_marks)
    update(email, username, mycursor, mydb, 7, 'reading', temp_marks)
