# authentication/send_email.py
import jwt
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.template.loader import render_to_string
# from django.conf.settings import SECRET_KEY, DOMAIN, SENDGRID_API_KEY
from django.conf import settings


def send_confirmation_email(email, username):

    token = jwt.encode({'user': username}, settings.SECRET_KEY,
                       algorithm='HS256').decode('utf-8')
    context = {
        'small_text_detail': 'Thank you for '
                             'creating an account. '
                             'Please verify your email '
                             'address to set up your account.',
        'email': email,
        'domain': settings.DOMAIN,
        'token': token,
    }

    # locates our email.html in the templates folder
    msg_html = render_to_string('users/email.html', context)
    message = Mail(
        # the email that sends the confirmation email
        from_email='business@propelytics.in',
        # from_email = "from@example.com",
        to_emails=[email],  # list of email receivers
        # to_emails = 'to@example.com',
        subject='Account activation',  # subject of your email
        html_content=msg_html)

    # sg = SendGridAPIClient(settings.EMAIL_HOST_PASSWORD)
    #
    # response = sg.send(message)
    # print(response.status_code)
    # print(response.body)


    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)

        # sg.send(message)
        response = sg.send(message)
        # print(response.status_code)
        # print(response.body)
        # print(response.headers)
    except Exception as e:
        return str(e)
