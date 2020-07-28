from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# If modifying these scopes, delete the file token.pickle.
# SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

#TEST
#COVID_SPREADSHEET_ID = '1Sd-AFnUwAUsUSIbIloTQj5sFoRTjgB2kGHydqx5a0aI'

#REAL
COVID_SPREADSHEET_ID = '1HpfT0FWyhx1wjiOMwrvzprVWFPxFhBYJidevHMwOMyM'
SAMPLE_RANGE_NAME = 'RawData'


def main():
    now = datetime.now()
    data = [now.strftime("%Y/%m/%d %H:%M:%S")]

    r = requests.get("https://virusncov.com/")
    bs2 = BeautifulSoup(r.content, 'html.parser', from_encoding="utf-8")
    #print(bs2)

    for s in bs2.findAll('h2'):
        #print(s)
        h2 = s.get_text()
        if h2 != "Latest Updates:":
            print(h2)
            x = h2.split(" ")
            data.append(x[-1])

    for s in bs2.findAll('div', {'class': 'small-card'})[0:2]:
        # print(s)
        i = 0
        aux2 = ""
        for s2 in s.findAll('span'):
            # print(s2)
            if i % 2:
                print(s2.get_text() + ": " + aux2)
            else:
                aux2 = s2.get_text()
                if '(' in aux2:
                    data.append(aux2[0:aux2.index(' (')])
                else:
                    data.append(aux2)
            i += 1

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=COVID_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    print(data)
    values = [data]
    body = {
        'values': values
    }

    result = service.spreadsheets().values().append(
       spreadsheetId=COVID_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME,
       valueInputOption='USER_ENTERED', body=body).execute()
    print('{0} cells appended.'.format(result \
                                      .get('updates') \
                                      .get('updatedCells')))


if __name__ == '__main__':
    main()
