import asyncio
from email.message import EmailMessage
from typing import List, Tuple
import aiosmtplib
from dotenv import load_dotenv
import os

load_dotenv()

HOST = "smtp.gmail.com"

async def send_email(to_email: str, subject: str, body: str) -> Tuple[dict, str]:
    sender_email = os.getenv('GMAIL_EMAIL')
    sender_password = os.getenv('GMAIL_PASSWORD')

    # build message
    message = EmailMessage()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(body)

    # send
    send_kws = dict(username=sender_email, password=sender_password, hostname=HOST, port=587, start_tls=True)
    try:
        res = await aiosmtplib.send(message, **send_kws)
        print(f"Email sent successfully to {to_email}")
        return res
    except Exception as e:
        print(f"Failed to send email to {to_email}: {str(e)}")
        return ({}, str(e))

async def send_emails(to_emails: List[str], subject: str, body: str) -> List[Tuple[dict, str]]:
    tasks = [send_email(email, subject, body) for email in to_emails]
    return await asyncio.gather(*tasks)

# Synchronous wrapper for compatibility
def send_emails_sync(to_emails: List[str], subject: str, body: str) -> List[Tuple[dict, str]]:
    return asyncio.run(send_emails(to_emails, subject, body))