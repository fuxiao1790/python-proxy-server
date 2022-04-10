import smtplib
from email.message import EmailMessage
from getpass import getpass

addr = input("SMTP Server: ")
port = input("SMTP Server Port: ")
username = input("SMTP Server Username: ")
password = getpass("SMTP Server Password: ")

client = smtplib.SMTP(addr, port)
client.ehlo() 
client.starttls()
client.login(username, password)

email_from = input("From: ")
email_to = input("To: ")
email_subject = input("Subject: ")
email_content = input("Email Content: ")

msg = EmailMessage()
msg["From"] = email_from
msg["To"] = email_to
msg["Subject"] = email_subject
msg.set_content(email_content)

client.send_message(msg)
client.quit()