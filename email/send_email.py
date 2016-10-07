
from os.path import basename
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


def send_email(sender, recipient, subject, message, attachments):
  msg = MIMEMultipart()
  msg['To'] = recipient
  msg['From'] = sender
  msg['Subject'] = subject

  part = MIMEText('text', "plain")
  part.set_payload(message)
  msg.attach(part)

  for f in attachments:
    with open(f, "rb") as fd:
        part = MIMEApplication(
            fd.read(),
            Name=basename(f)
        )
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)

  session = smtplib.SMTP('127.0.0.1', 25)
  # session.set_debuglevel(1)
  session.ehlo()
  session.sendmail(sender, recipient, msg.as_string())
  print("You email is sent to {0}.".format(recipient))
  session.quit()

if __name__ == '__main__':
  sender = raw_input("What is the sender's email adress? ")
  recipient = raw_input("What is the recipient's email adress? ")
  subject = raw_input("What is the subject? ")
  
  message = ''
  msgline = raw_input('Enter the message. Empty line ends the message.\n')
  while msgline != '':
    message += msgline + '\n'
    msgline = raw_input('')

  attachments = []
  att = raw_input('Enter the file names of attachments. Empty line ends the list.\n')
  while att != '':
    attachments.append(att)
    att = raw_input('')

  send_email(sender, recipient, subject, message, attachments)