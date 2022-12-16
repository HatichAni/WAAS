import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from src import app
from flask import render_template


def send_mail(recipient, subject, body):
    # Enviroment
    email_sender_address = os.environ.get('EMAIL_SENDER_ADDRESS')
    email_sender_password = os.environ.get('EMAIL_SENDER_PASSWORD')
    email_sender_host = os.environ.get('EMAIL_SENDER_HOST')

    # Construct the email message
    msg = MIMEMultipart()
    msg['From'] = email_sender_address
    msg['To'] = recipient
    msg['Subject'] = subject

    # Attach the body to the email message
    msg.attach(MIMEText(body, 'html'))

    # Connect to the Gmail SMTP server
    email_sender_host = os.environ.get('EMAIL_SENDER_HOST')
    if (email_sender_password):
        smtp_server = smtplib.SMTP_SSL(email_sender_host, 465)
    else:
        smtp_server = smtplib.SMTP(email_sender_host, 25)

    # Login to the Gmail server
    if (email_sender_password):
        smtp_server.login(email_sender_address, email_sender_password)

    # Send the email
    smtp_server.sendmail(email_sender_address, recipient, body)

    # Disconnect from the server
    smtp_server.quit()


def send_success_email(job, connection, result, *args, **kwargs):
    email = job.meta.get('email')
    subject = uploaded_filename + " has finished transcribing!"
    uploaded_filename = job.meta.get('uploaded_filename')

    disclaimer = os.environ.get('DISCLAIMER', '')

    subject = uploaded_filename + " is finished transcribing!"
    body = f'Your file is ready. Download it here: \n\n Text file with timecodes {download_url + "?output=timecode_txt"} \n Textfile without timecodes: {download_url + "?output=txt"} \n Captions file with timecodes(SRT) {download_url + "?output=srt"}'

    send_mail(email, subject, body)


def send_failure_email(job, connection, type, value, traceback):
    email = job.meta.get('email')
    subject = 'The transcription failed'

    body = "We're sorry, but we were unable to transcribe the file you uploaded. Please try again or contact the team for assistance."

    send_mail(email, subject, body)
