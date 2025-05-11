import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email_notification(to_email, username):
    sender_email = "ameyasutar1@gmail.com"
    sender_password = "ezep tiqc ttvq auol"

    subject = "New User Signup Notification"
    body = f"A new user has signed up: {username} ({to_email})"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = sender_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, sender_email, message.as_string())
            return True
    except Exception as e:
        print("Email send error:", e)
        return False
