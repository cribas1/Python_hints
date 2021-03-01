#Basic imports
import pandas as pd

#imports for Google sheets libraries
import gspread
from oauth2client.service_account import ServiceAccountCredentials

#imports for slack
import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter

#Getting variables from .env
env_path = Path('.')/'.env'
load_dotenv(dotenv_path = env_path)
token=os.environ['SLACK_TOKEN']
secret=os.environ['SLACK_SECRET']
# define the scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('Learning python-0fa5acac5c94.json', scope)

# authorize the clientsheet
google_client = gspread.authorize(creds)

# get the instance of the spreadsheet where data is stored
spreadsheet = google_client.open('Slack_bot data')

# get instances of input and output sheets
input_sheet_instance = spreadsheet.get_worksheet(0)
output_sheet_instance = spreadsheet.get_worksheet(1)


#initializing slack
app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(secret,'/slack/events',app)
client = slack.WebClient(token)
BOT_ID = client.api_call("auth.test")['user_id']

##defining function to recieve slack command
@app.route('/candidates_available', methods =['POST'])
def candidates_available():
    data = request.form
    user_id = data.get('user_id')
    channel_id = data.get('channel_id')

    # get data from input sheet

    input_data = input_sheet_instance.get_all_records()

    # convert the json to dataframe
    input_df = pd.DataFrame.from_dict(input_data)

    # filtering invalid candidates
    available_candidates_df = input_df[input_df["Outcome of first interview"] == "Good"]
    available_candidates_df = available_candidates_df["Candidate name"]

    client.chat_postMessage(channel=channel_id, text="Find below the list of available candidates:")

    for x in available_candidates_df:
        text = x
        client.chat_postMessage(channel=channel_id, text=text )

    client.chat_postMessage(channel=channel_id, text="Remember to tag me with the name of the candidates that did well so we schedule the next interview ASAP!")

    return Response(), 200

@slack_event_adapter.on('app_mention')
def message(payload):
    event = payload.get('event', {})
    text=event.get('text')
    print(text)

if __name__ == "__main__":
    app.run(debug=True, port =5000)


