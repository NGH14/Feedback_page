import smtplib
from email.mime.text import MIMEText


def send_mail(customer, service, rating, comments):
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    login = '9cb838f112f332'
    password = '1181db9a98fd45'
    message = f"<h3>New Feedback Submission</h3><ul><li>Customer: {customer}</li><li>About Service: {service}</li><li>Rating: {rating}</li><li>Comments: {comments}</li></ul>"

    sender_email = 'customeremail@gmail.com'
    receiver_email = 'appleemail@apple.com'
    msg = MIMEText(message, 'html')
    msg['Subject'] = 'Apple Feedback'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Send email
    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
