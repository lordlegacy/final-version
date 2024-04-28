import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Email content
sender_email = 'your_email@example.com'
recipient_email = 'recipient_email@example.com'
subject = 'Email Verification'
verification_code = '123456'  # Replace with actual verification code

# Read the HTML content from the file
with open('index.html', 'r') as file:
    html_content = file.read()

# Replace placeholders with actual data
html_content = html_content.replace('[RECIPIENT]', recipient_email)
html_content = html_content.replace('[Enter verification code here]', verification_code)

# Create a multipart message and set headers
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = recipient_email
msg['Subject'] = subject

# Attach HTML content to the email
msg.attach(MIMEText(html_content, 'html'))

# SMTP server details
smtp_server = 'smtp.example.com'
smtp_port = 587
smtp_username = 'your_smtp_username'
smtp_password = 'your_smtp_password'

# Start SMTP session
server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()

# Login to SMTP server
server.login(smtp_username, smtp_password)

# Send email
server.sendmail(sender_email, recipient_email, msg.as_string())

# Close SMTP session
server.quit()

print("Email sent successfully")
