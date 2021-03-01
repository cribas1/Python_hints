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

# get data from input sheet

input_data = input_sheet_instance.get_all_records()
df = pd.DataFrame.from_dict(input_data)
df_output = df[["Candidate name","Candidate email","Linkedin link", "Availability for next interview"]]
print(df_output)
print([df.columns.values.tolist()]+df_output.values.tolist())

output_sheet_instance.insert_rows([df.columns.values.tolist()]+df_output.values.tolist())