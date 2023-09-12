import os.path
import pickle
import json
import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

import sys, os

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)


flags = open("gmailFlags.txt", "r", encoding="utf-8").read().split("\n")
senders = [x for x in flags if "@" in x and len(x) != 0 and x[0] != "#"]
replies = [x for x in flags if "@" not in x and len(x) != 0 and x[0] != "#"]

def get_unread_emails():
    print("Getting emails")
    try:
        with open("newEmailsOlder.json", 'r') as file:
            processed_emails = json.load(file)
    except FileNotFoundError:
        processed_emails = []

    try:
        with open("newEmailsToday.json", 'r') as file:
            today_emails = json.load(file)
            if today_emails["date"] != str(datetime.date.today()):
                processed_emails.extend(today_emails["emails"])
                with open("newEmailsOlder.json", 'w') as file:
                    json.dump(processed_emails, file)
                today_emails = {"date": str(datetime.date.today()), "emails": []}
    except FileNotFoundError:
        today_emails = {"date": str(datetime.date.today()), "emails": []}

    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "supersecretstuff.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.pickle", 'wb') as token:
            pickle.dump(creds, token)

    try:
        service = build('gmail', 'v1', credentials=creds)
        
        senders_query = "is:unread " + " OR ".join([f"from:{sender}" for sender in senders])
        results = service.users().messages().list(userId='me', q=senders_query).execute()
        messages = results.get('messages', [])

        if not messages:
            return []

        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            email_data = msg['payload']['headers']

            from_name, subject, date = None, None, None
            for values in email_data:
                name = values['name']
                if name == 'From':
                    from_name = values['value']
                elif name == 'Subject':
                    subject = values['value']
                elif name == 'Date':
                    date = values['value']

            email_id = msg['id']
            if email_id not in [email['id'] for email in processed_emails] and \
               email_id not in [email['id'] for email in today_emails["emails"]]:
                new_email = {
                    'id': email_id,
                    'from': from_name,
                    'subject': subject,
                    'date': date,
                    'link': f"https://mail.google.com/mail/u/0/#inbox/{message['id']}"
                }

                today_emails["emails"].append(new_email)
                with open("newEmailsToday.json", 'w') as file:
                    json.dump(today_emails, file)

        for search_query in replies:
            results = service.users().messages().list(userId='me', q=search_query).execute()
            messages = results.get('messages', [])

            for message in messages:
                msg = service.users().messages().get(userId='me', id=message['id']).execute()
                if message['id'] not in [email['id'] for email in processed_emails] and \
                    message['id'] not in [email['id'] for email in today_emails["emails"]]:
                    if 'payload' in msg:
                        email_data = msg['payload']['headers']

                        from_name, subject, date = None, None, None
                        for values in email_data:
                            name = values['name']
                            if name == 'From':
                                from_name = values['value']
                            elif name == 'Subject':
                                subject = values['value']
                            elif name == 'Date':
                                date = values['value']

                        new_email = {
                            'id': message['id'],
                            'from': from_name,
                            'subject': subject,
                            'date': date,
                            'link': f"https://mail.google.com/mail/u/0/#inbox/{message['id']}"
                        }

                        today_emails["emails"].append(new_email)
                        with open("newEmailsToday.json", 'w') as file:
                            json.dump(today_emails, file)

        returned = []
        for x in today_emails["emails"]:
            try:
                From = str(x["from"])
            except:
                From = "None"
            
            try:
                subject = str(x["subject"])
            except:
                subject = "None"
            
            try:
                link = str(x["link"])
            except:
                link = "None"
            
            returned.append(From + ": " + subject + ":\n" + link)
        return returned

    except Exception as error:
        print(f'An error occurred: {error}')
        return f'An error occurred: {error}'

if __name__ == '__main__':
    new_emails = get_unread_emails()
    for v in new_emails:
        print(v)
    else:
        print("No new emails.")