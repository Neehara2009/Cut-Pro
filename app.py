from flask import Flask, render_template, request, redirect, url_for, flash
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

app = Flask(name)
app.secret_key = 'supersecretkey'

# SMTP server configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL = 'neeharadeemantha@gmail.com'
PASSWORD = '2009923.'

def send_email(recipients, subject, body, attachment_path=None):
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL, PASSWORD)

        msg = MIMEMultipart()
        msg['From'] = EMAIL
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        if attachment_path:
            with open(attachment_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={attachment_path.split("/")[-1]}')
                msg.attach(part)

        server.sendmail(EMAIL, recipients, msg.as_string())
        flash('Email sent successfully!', 'success')

    except Exception as e:
        flash(f'Failed to send email. Error: {e}', 'danger')
    
    finally:
        server.quit()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        recipients = request.form['recipients'].split(',')
        subject = request.form['subject']
        body = request.form['body']
        attachment_path = request.files['attachment'].filename if 'attachment' in request.files else None

        send_email(recipients, subject, body, attachment_path)
        return redirect(url_for('index'))

    return render_template('index.html')

if name == "main":
    app.run(debug=True)
