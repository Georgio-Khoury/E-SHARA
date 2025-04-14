import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(subject, body):
    sender_email = "razan.hmede@lau.edu"
    receiver_emails = [
        "aya.jouni02@lau.edu",  
        "farah.alnassar@lau.edu",  
        "georgio.elkhoury@lau.edu",
        "razan.hmede@lau.edu"
    ]
    password = "pass" 

    try:
        server = smtplib.SMTP('smtp.office365.com', 587)
        server.starttls()
        server.login(sender_email, password)

        for receiver_email in receiver_emails:
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            server.sendmail(sender_email, receiver_email, msg.as_string())

        print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to send email. Error: {str(e)}")

    finally:
        server.quit()

if __name__ == "__main__":
    subject = "Sensor Data Update"
    body = "hello" 
    send_email(subject, body)
