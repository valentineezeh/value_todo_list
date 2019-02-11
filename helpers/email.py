# using SendGrid's Python Library
import sendgrid
import os
from sendgrid.helpers.mail import *


def send_email(user_email, subject, template):
    """This function fires the Sendgrid configuration and setup that sends a mail to a user. You need internet connection for this to work. """

    # App default email address set in .env file
    config_email_address = os.getenv('MAIL_DEFAULT_SENDER')

    # Set up sendgrid with set-up API key gotten from sendgrid
    sg = sendgrid.SendGridAPIClient(apikey=os.getenv('SENDGRID_API_KEY'))

    from_email = Email(config_email_address)
    to_email = Email(user_email)
    subject = subject
    content = Content('text/html', template)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())

    print(response.status_code)
    print(response.body)
    print(response.headers)
