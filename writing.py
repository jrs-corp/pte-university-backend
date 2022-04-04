# # Importing Libraries
import configparser
from azure.data.tables import TableClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

# # Importing from other py files
from update import update

# # Parsing the configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# # Setting up the connection
connection_string = config['TABLEAPI']['connection_string']
table_name = config['TABLEAPI']['table_name']
my_filter = "PartitionKey eq 'Writing'"
table_client = TableClient.from_connection_string(conn_str=connection_string, table_name=table_name)
entities = table_client.query_entities(my_filter)
endpoint = config['WRITING']['endpoint']
key = config['WRITING']['key']
text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

def writing(email, username, mycursor, mydb):
    # header
    print('\n')
    print(' ╔' + ('-' * 149) + '╗')
    print(' ¦' + (' ' * 60) + 'PTE PRACTICE - WRITING' + (' ' * 67) + '¦')
    print(' ╚' + ('-' * 149) + '╝')
    print('\n')

    temp_marks = 0
    # # Looping through the writing questions
    for entity in entities:
        temp_answers = entity['Answers'].split(',')
        total_score = entity['Blanks']
        # # Showing the question
        # print(entity['Question'])   # hide for testing
        # print(temp_answers)         # hide for testing
        pass_status = True

        # # Asking for answers - One time as this in an essay
        input_answer = input(f"                        {entity['Question']}: ")
        articles = [ input_answer ]
        result = text_analytics_client.extract_key_phrases(articles)

        for i in range(len(result[0]['key_phrases'])):
            if result[0]['key_phrases'][i] in temp_answers:  # # Check is entity is in db answer or now
                pass_status = True
                temp_marks += 1
            else:
                pass_status = False
        # quit_status = input('Do you want to take a break? ')
        # if quit_status == 'Y' or quit_status == 'y':
        break
        print('-'*30)
    print('\n')
    final_marks = temp_marks * 100 / total_score
    print('                        The final marks: ', final_marks)
    update(email, username, mycursor, mydb, 6, 'writing', final_marks)
