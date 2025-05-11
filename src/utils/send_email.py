import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import logging

def send_email_notification(to_email, username):
    sender_email = os.environ.get("SENDER_EMAIL")
    sender_password = os.environ.get("SENDER_PASSWORD")

    if not sender_email or not sender_password:
        logging.error("Missing email credentials in environment variables.")
        raise ValueError("Missing email credentials in environment variables.")

    subject = "New User Signup Notification"
    body = f"A new user has signed up: {username} ({to_email})"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = sender_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        logging.info("Connecting to SMTP server...")
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.set_debuglevel(1)  # 🔍 Show SMTP interaction in logs
            server.starttls()
            logging.info("Starting TLS and logging in...")
            server.login(sender_email, sender_password)
            logging.info("Login successful. Sending email...")
            server.sendmail(sender_email, sender_email, message.as_string())
            logging.info(f"Email sent successfully to {sender_email}")
            return True
    except Exception as e:
        logging.exception("Failed to send email.")
        return False
