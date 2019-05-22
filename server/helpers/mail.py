import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Mail():
    def __init__(self, login, password, host, port,mail_to):
        self.login = login
        self.password = password
        self.host = host
        self.port = port
        self.mail_to = mail_to

    def send(self, email_from, email_to, subject, html):
        msg = MIMEMultipart()
        msg['From'] = email_from
        msg['Subject'] = subject
        msg.attach(MIMEText(html, 'html'))
        s = smtplib.SMTP(self.host, self.port)
        s.starttls()
        s.login(self.login, self.password)
        text = msg.as_string()
        s.sendmail(email_from, [email_to], text)
        s.quit()
