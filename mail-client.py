import smtplib
from email.message import EmailMessage

SMTP_SERVER_ADDR = "smtp.gmail.com"
SMTP_SERVER_PORT = 587
SENDER_EMAIL = ""
SENDER_PASSWORD = ""
RECEIVER_EMAIL = ""

msg = EmailMessage()
msg["From"] = SENDER_EMAIL
msg["To"] = RECEIVER_EMAIL
msg["Subject"] = "Test"
msg.set_content("THIS IS A TEST")

client = smtplib.SMTP(SMTP_SERVER_ADDR, SMTP_SERVER_PORT)
client.ehlo()
client.starttls()
client.login(SENDER_EMAIL, SENDER_PASSWORD)

client.send_message(msg)
client.quit()