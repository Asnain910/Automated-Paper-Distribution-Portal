from flask import Flask, request, render_template_string, redirect, url_for
from werkzeug.utils import secure_filename
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string(open('form.html').read())

@app.route('/submit', methods=['POST'])
def submit():
    form_data = request.form.to_dict()
    file = request.files['file']
    if file:
        filename = os.path.join('uploads', secure_filename(file.filename))
        file.save(filename)

        # Read CSV, randomly select 3 faculty
        df = pd.read_csv(filename)
        selected_faculty = df.sample(n=3)

        # Construct email body from form data using the new function
        email_body = construct_email_body(form_data)

        # Path to the attachment in the project directory
        attachment_path = os.path.join('attachment', 'Combined.pdf')
        
        send_emails(selected_faculty['email'].tolist(), email_body,  attachment_path)

    return 'Emails sent successfully!'

def construct_email_body(form_data):
    email_body = "Dear Faculty,\n\n"
    email_body += "You have been selected to contribute to setting the upcoming exam papers. Below are the details provided by the examination department:\n\n"
    for key, value in form_data.items():
        email_body += f"{key}: {value}\n"
    email_body += "\nPlease ensure the papers are prepared according to the guidelines and submitted by the due dates.\n\n"
    email_body += "Thank you for your cooperation.\n"
    email_body += "Examination Department"
    return email_body

def send_emails(emails, content, attachment_path=None):
    sender_email = "asnainsdq12@gmail.com"  # Update with your email
    password ="xsmtpsib-f34776e5b8573841fb424a70ae118461f4bb019951c4c94d9a02d05276fa925c-nDaPFTOGw5Jmq6pv"  # Recommended: Use environment variable
    smtp_server = "smtp-relay.sendinblue.com"  # Update with your SMTP server
    port = 587  # For starttls

    message = MIMEMultipart("alternative")
    message["Subject"] = "Faculty Notification"
    message["From"] = sender_email

    part = MIMEText(content, "plain")
    message.attach(part)

    if attachment_path and os.path.isfile(attachment_path):
        # Prepare the attachment
        with open(attachment_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {os.path.basename(attachment_path)}",
        )

        message.attach(part)

    # Login to server and send the email
    server = smtplib.SMTP(smtp_server, port)
    server.starttls()
    server.login(sender_email, password)
    for email in emails:
        message["To"] = email
        server.sendmail(sender_email, email, message.as_string())

    server.quit()

if __name__ == '__main__':
    app.run(debug=True)
