import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import config
import time


class MassMailer(object):
    def __init__(self):
        # reading target list and message files
        with open("target_list.txt", encoding="utf-8") as target_list:
            self.target_list = target_list.read().replace(" ", "").split(config.target_list_separator)
        with open("message.json", encoding="utf-8") as message:
            self.message = json.loads(message.read())
        # connecting and logging in to server
        print("Connecting to smtp server...")
        self.server = smtplib.SMTP(config.smtp_url, config.smtp_port)
        self.server.login(config.smtp_username, config.smtp_password)

    def start_mass_mailer(self):
        print("starting mass mailer...")
        for target_email in self.target_list:
            print(f"Sending email to {target_email}")
            try:
                # Prepare message
                msg = MIMEMultipart()

                msg['From'] = config.smtp_email
                msg['To'] = target_email
                msg['Subject'] = self.message["subject"]

                message_body = self.message["body"]

                # Add Message To Email Body
                msg.attach(MIMEText(message_body, 'html'))
            except:
                print("There was unknown error with your message.")
                return
            try:
                self.server.sendmail(config.smtp_email, target_email, msg.as_string())
                print("email sent successfully")
            except:
                print("there was unknown error sending email... continuing")
            print(f"Waiting {config.email_delay} seconds")
            time.sleep(config.email_delay)
        print("Done.")
