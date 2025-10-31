from __future__ import print_function
import os.path
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Gmail API scope: full access to send emails
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

def get_gmail_service():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    service = build("gmail", "v1", credentials=creds)
    return service

def send_email(service, to_list, subject, body):
    """Send an email to multiple recipients using Gmail API."""
    message = MIMEText(body)
    message["to"] = ", ".join(to_list)
    message["subject"] = subject

    # Encode and send
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    send_message = {"raw": encoded_message}

    try:
        sent = service.users().messages().send(userId="me", body=send_message).execute()
        print(f"✅ Email sent successfully (ID: {sent['id']})")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
