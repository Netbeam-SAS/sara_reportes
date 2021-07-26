import smtplib
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders

class Email:
    """ Email class """
    def __init__(self, subject, message, files, settings):
        """Compose and send email with provided info and attachments.

        Args:
            subject (str): message title
            message (str): message body
            files (list[str]): list of file paths to be attached to email
            settings:
                FROM (str): from name
                TO (list[str]): to name(s)
                SERVER (str): mail server host name
                PORT (int): port number
                USERNAME (str): server auth username
                PASSWORD (str): server auth password
        """
        self.send_from = settings['FROM']
        self.send_to = settings['TO']
        self.server = settings['SERVER']
        self.port = settings['PORT']
        self.username = settings['USERNAME']
        self.password = settings['PASSWORD']
        self.subject = subject
        self.message = message
        self.files = files
        self.use_tls = True
    
    def send_email(self):
        """Compose and send email with provided info and attachments."""
        msg = MIMEMultipart()
        msg['From'] = self.send_from
        msg['To'] = COMMASPACE.join(self.send_to)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = self.subject

        msg.attach(MIMEText(self.message, 'html', 'utf-8'))

        for path in self.files:
            part = MIMEBase('application', "octet-stream")
            with open(path, 'rb') as file:
                part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            'attachment; filename={}'.format(Path(path).name))
            msg.attach(part)

        smtp = smtplib.SMTP(self.server, self.port)
        if self.use_tls:
            smtp.starttls()
        smtp.login(self.username, self.password)
        smtp.sendmail(self.send_from, self.send_to, msg.as_string())
        smtp.quit()