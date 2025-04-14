import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(subject, body):
    
    sender_email = "aya.jouni02@lau.edu"  
    receiver_emails = [
        "razan.hmede@lau.edu",  
        "farah.alnassar@lau.edu",  
        "georgio.elkhoury@lau.edu"  
    ]
    password = "your_password" # put your pass here!!!!

    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
      
        server = smtplib.SMTP('smtp.office365.com', 587)  
        server.starttls()  
        server.login(sender_email, password)  

      
        for receiver_email in receiver_emails:
            msg['To'] = receiver_email
            server.sendmail(sender_email, receiver_email, msg.as_string())

        print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to send email. Error: {str(e)}")

    finally:
        server.quit()

if __name__ == "__main__":
    subject = "Sensor Data Update"
    body = "This is an update with the real-time sensor data from the gloves."
    send_email(subject, body)
