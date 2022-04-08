# # Importing Libraries
import configparser
from azure.data.tables import TableClient

# # Importing from other py files
from update import update

# # Parsing the configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# # Setting up the connection
connection_string = config['TABLEAPI']['connection_string']
table_name = config['TABLEAPI']['table_name']
my_filter = "PartitionKey eq 'Reading'"
table_client = TableClient.from_connection_string(conn_str=connection_string, table_name=table_name)
entities = table_client.query_entities(my_filter)


def reading(email, username, mycursor, mydb):
    # header
    print('\n')
    print(' ╔' + ('-' * 149) + '╗')
    print(' ¦' + (' ' * 60) + 'PTE PRACTICE - READING' + (' ' * 67) + '¦')
    print(' ╚' + ('-' * 149) + '╝')
    print('\n')

    temp_marks = 0
    total_marks = 0
    percent_marks = 0
    # # Looping through the reading questions
    for entity in entities:
        temp_answers = entity['Answers'].split(',')
        # Showing the question
        # print(entity['Question'])
        counter_word = 0
        counter = 0
        wrapped = ' '
        string = entity['Question']
        print("         ╔" + "-" * 126 + "╗")
        print("         ¦" + " " * 126 + "¦")
        for word in string.split():
            counter_word += 1
            counter += 1
            wrapped = wrapped + word + ' '
            if counter == 13 or counter_word == len(string.split()):   # display 18 words per line
                pad = 121 - len(wrapped)
                print(f"         ¦   {wrapped} {' ' * pad} ¦")
                counter = 0
                wrapped = ' '
        # print(f"         {temp_answers}") # hide for screenshot later
        pass_status = True
        print("         ¦" + " " * 126 + "¦")
        print("         ╚" + "-" * 126 + "╝")
        print('\n')
        for i in range(int(entity['Blanks'])):
            # # Asking for answers
            input_answer = input(f'                        Enter the answer for blank number ({i + 1}): ')
            # # We will only give full marks if all the blanks of a certain questions are fullfilled
            if input_answer == temp_answers[i]:
                pass_status = True
            else:
                pass_status = False
        if pass_status == True:
            temp_marks += 1
        total_marks += 1
        print('\n')
        quit_status = input('                        Do you want to take a break(Y/N)? ')
        print('\n')
        # print('\n' * 10)
        check_status = True
        exit_status = True
        while check_status == True:
            if quit_status == 'Y' or quit_status == 'y':
                check_status = False
                exit_status = False
            elif quit_status == 'N' or quit_status == 'n':
                check_status = False
            else:
                # quit_status = input('                   Wrong Command, Please Try Again(Y/N)? ')
                quit_status = input(f'''\n                        Wrong Command.  

                        Please Try Again(Y/N)? ''')
        if check_status == False and exit_status == False:
            break
        # print('-'*30)
    print('\n')
    print('                        The final marks      : ', temp_marks)
    percent_marks = int((temp_marks / total_marks) * 100)
    print('                        The percent marks    : ', percent_marks)
    update(email, username, mycursor, mydb, 7, 'reading', percent_marks)
