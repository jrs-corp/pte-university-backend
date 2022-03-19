# # Importing Libraries
import configparser
import mysql.connector
from azure.data.tables import TableClient

# # Importing from other py files
from update import update

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

# # Setting up the connection
connection_string = config['TABLEAPI']['connection_string']
table_name = config['TABLEAPI']['table_name']
my_filter = "PartitionKey eq 'Speaking'"
table_client = TableClient.from_connection_string(conn_str=connection_string, table_name=table_name)
entities = table_client.query_entities(my_filter)

# # Libraries for Speaking API
import os
import json
import time
import base64
import random
import requests
import azure.cognitiveservices.speech as speechsdk
from flask import Flask, jsonify, render_template, request, make_response
app = Flask(__name__)

# # Setting up the configuration for Speaking
subscription_key = config['SPEAKING']['subscription_key']
region = config['SPEAKING']['region']
language = "en-US"
voice = "Microsoft Server Speech Text to Speech Voice (en-US, JennyNeural)"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/gettoken", methods=["POST"])
def gettoken():
    fetch_token_url = 'https://%s.api.cognitive.microsoft.com/sts/v1.0/issueToken' %region
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key
    }
    response = requests.post(fetch_token_url, headers=headers)
    access_token = response.text
    return jsonify({"at":access_token})

@app.route("/gettonguetwister", methods=["POST"])
def gettonguetwister():
    tonguetwisters = []
    for entity in entities:
        tonguetwisters.append(entity['Question'])
    print(tonguetwisters)
    return jsonify({"tt":random.choice(tonguetwisters)})

@app.route("/ackaud", methods=["POST"])
def ackaud():
    # # Get the audio file and return score
    f = request.files['audio_data']
    reftext = request.form.get("reftext")
    #    f.save(audio)
    #print('file uploaded successfully')

    # a generator which reads audio data chunk by chunk
    # the audio_source can be any audio input stream which provides read() method, e.g. audio file, microphone, memory stream, etc.
    def get_chunk(audio_source, chunk_size=1024):
        while True:
            #time.sleep(chunk_size / 32000) # to simulate human speaking rate
            chunk = audio_source.read(chunk_size)
            if not chunk:
                #global uploadFinishTime
                #uploadFinishTime = time.time()
                break
            yield chunk

    # build pronunciation assessment parameters
    referenceText = reftext
    pronAssessmentParamsJson = "{\"ReferenceText\":\"%s\",\"GradingSystem\":\"HundredMark\",\"Dimension\":\"Comprehensive\",\"EnableMiscue\":\"True\"}" % referenceText
    pronAssessmentParamsBase64 = base64.b64encode(bytes(pronAssessmentParamsJson, 'utf-8'))
    pronAssessmentParams = str(pronAssessmentParamsBase64, "utf-8")

    # build request
    url = "https://%s.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?language=%s" % (region, language)
    headers = { 'Accept': 'application/json;text/xml',
                'Connection': 'Keep-Alive',
                'Content-Type': 'audio/wav; codecs=audio/pcm; samplerate=16000',
                'Ocp-Apim-Subscription-Key': subscription_key,
                'Pronunciation-Assessment': pronAssessmentParams,
                'Transfer-Encoding': 'chunked',
                'Expect': '100-continue' }

    #audioFile = open('audio.wav', 'rb')
    audioFile = f
    # send request with chunked data
    response = requests.post(url=url, data=get_chunk(audioFile), headers=headers)
    #getResponseTime = time.time()
    audioFile.close()

    #latency = getResponseTime - uploadFinishTime
    #print("Latency = %sms" % int(latency * 1000))
    # print('response.json()')
    # print(response.json())
    temp_data = response.json()
    # print('temp_data')
    # print(temp_data)
    accuracy_score = temp_data['NBest'][0]['AccuracyScore']
    fluency_score = temp_data['NBest'][0]['FluencyScore']
    completeness_score = temp_data['NBest'][0]['CompletenessScore']
    pron_score = temp_data['NBest'][0]['PronScore']
    temp_score = (accuracy_score + fluency_score + completeness_score + pron_score ) / 4
    email = os.environ.get('FLASK_EMAIL')
    username = os.environ.get('FLASK_USR')
    update(email, username, mycursor, mydb, 4, 'speaking', temp_score)

    return response.json()

# print('Test')
# print(os.environ.get('FLASK_USR'))

if __name__ == '__main__':
    app.run()