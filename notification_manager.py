import smtplib
import os

class NotificationManager:
    def __init__(self):
        self.smtp_address = os.environ["SMTP_EMAIL_PROVIDER"]
        self.my_email = os.environ["MY_EMAIL"]
        self.my_password = os.environ["MY_PASSWORD"]
        self.connection = smtplib.SMTP(os.environ["SMTP_EMAIL_PROVIDER"])

    def send_emails(self, email_list, email_body):
        with self.connection:
            self.connection.starttls()
            self.connection.login(self.my_email, self.my_password)
            for email in email_list:
                self.connection.sendmail(
                    from_addr=self.my_email,
                    to_addrs=email,
                    msg=f"Subject:New Low Price Flight!\n\n{email_body}".encode('utf-8')
                )