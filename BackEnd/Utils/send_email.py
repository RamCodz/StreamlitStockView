import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(sender_email, sender_password, recipient_email, subject, body, smtp_server='smtp.gmail.com', smtp_port=587):
    try:
        # Create a multipart message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        
        # Add the email body
        msg.attach(MIMEText(body, 'plain'))
        
        # Connect to the mail server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Start TLS for security
        
        # Login to the email account
        server.login(sender_email, sender_password)
        
        # Send the email
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        
        # Close the server connection
        server.quit()
        
        print("Email sent successfully!")
        
    except Exception as e:
        print(f"Failed to send email: {e}")

# Example usage
# send_email('your_email@gmail.com', 'your_password', 'recipient_email@example.com', 'Subject', 'Email body content')