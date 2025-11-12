import os
import base64
import ssl
import certifi
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Gmail send scope (not readonly)
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

def get_gmail_service():
    """Authorize and return a Gmail API service."""
    # creds = None

    # # Load saved credentials if they exist
    # if os.path.exists("token.json"):
    #     creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # # If credentials are invalid or missing, run login flow
    # if not creds or not creds.valid:
    #     if creds and creds.expired and creds.refresh_token:
    #         creds.refresh(Request())
    #     else:
    #         flow = InstalledAppFlow.from_client_secrets_file(
    #             "credentials.json", SCOPES
    #         )
    #         creds = flow.run_local_server(port=0)
    #     with open("token.json", "w") as token:
    #         token.write(creds.to_json())
    
    token_path = "token.json"

    if not os.path.exists(token_path):
        print("❌ token.json not found. Cannot refresh without existing token.")
        sys.exit(1)

    creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(token_path, "w") as token:
            token.write(creds.to_json())
        print("✅ Gmail token refreshed successfully!")
    elif creds and creds.valid:
        print("✅ Token is still valid — no need to refresh.")
    else:
        print("⚠️ Cannot refresh token. Missing refresh_token or invalid credentials.")


    # Build Gmail API client with certifi SSL fix
    service = build("gmail", "v1", credentials=creds, cache_discovery=False)

    return service



def send_email(service, recipients, subject, body, sender="me"):
    """Send a well-formatted email using Gmail API (plain text + HTML)."""
    try:
        # Create MIME message (supports both text & HTML)
        message = MIMEMultipart("alternative")
        message["To"] = ", ".join(recipients)
        message["From"] = sender
        message["Subject"] = subject

        # Plain text fallback (for non-HTML clients)
        text_part = MIMEText(body, "plain")

        # Optional HTML version for Gmail rendering
        html_body = f"""
        <html>
          <body style="font-family:Arial, sans-serif; line-height:1.6; color:#202124;">
            {body.replace('\n', '<br>')}
            <br><br>
            <p style="font-size:0.9em;color:#5f6368;">Sent automatically via ScholarSnap 🚀</p>
          </body>
        </html>
        """
        html_part = MIMEText(html_body, "html")

        # Attach both versions (HTML preferred)
        message.attach(text_part)
        message.attach(html_part)

        # Encode message as base64url
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        # Send message using Gmail API
        send_result = (
            service.users()
            .messages()
            .send(userId="me", body={"raw": raw_message})
            .execute()
        )

        print(f"✅ Email sent successfully! Message ID: {send_result['id']}")
        return send_result

    except HttpError as error:
        print(f"❌ Gmail API error: {error}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None



def email_summary(summary_text, paper_title, recipients):
    """Utility to send a summary email."""
    subject = f"{paper_title}"
    body = f"{summary_text}\n"

    service = get_gmail_service()
    send_email(service, recipients, subject, body)


if __name__ == "__main__":
    # Example test (you can remove or modify)
    recipients = ["example@gmail.com"]
    email_summary(
        "This paper discusses a new approach to computer vision reasoning.",
        "Are Video Models Ready as Zero-Shot Reasoners?",
        "https://arxiv.org/abs/2510.26802",
        recipients,
    )
