import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailNotifier:
        def __init__(self, smtp_server, smtp_port, sender_email, sender_password, recipient_emails):
                self.smtp_server = smtp_server
                self.smtp_port = smtp_port
                self.sender_email = sender_email
                self.sender_password = sender_password
                self.recipient_emails = recipient_emails

        def send_email(self, subject, body):
                try:
                        # Prepare the email
                        msg = MIMEMultipart()
                        msg['From'] = self.sender_email
                        msg['To'] = ", ".join(self.recipient_emails)
                        msg['Subject'] = subject

                        msg.attach(MIMEText(body, 'plain'))

                        # Send the email
                        with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                                server.login(self.sender_email, self.sender_password)
                                server.sendmail(self.sender_email, self.recipient_emails, msg.as_string())

                        print("Mesage sent successfully.")
                except Exception as e:
                        print(f"Failed to send error notification: {e}")