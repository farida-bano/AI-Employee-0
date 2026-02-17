import smtplib
import os
import argparse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(to_email, subject, body):
    sender_email = os.getenv('EMAIL_ADDRESS')
    sender_password = os.getenv('EMAIL_PASSWORD')

    if not sender_email or not sender_password:
        print("Error: EMAIL_ADDRESS and EMAIL_PASSWORD environment variables must be set.")
        return

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print(f"Success: Email sent to {to_email}")
    except Exception as e:
        print(f"Error: Failed to send email. {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send an email via SMTP.")
    parser.add_argument("--to", required=True, help="Recipient's email address.")
    parser.add_argument("--subject", required=True, help="Subject of the email.")
    parser.add_argument("--body", required=True, help="Body of the email.")
    args = parser.parse_args()

    send_email(args.to, args.subject, args.body)
