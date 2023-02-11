from django.core.mail import send_mail
from django.conf import settings


def sign(reciever_email):
    send_mail(
        'Sign up for ZLATMAX newsletters',
        "You have been signed up for ZLATMAX newsletters. You can unsign your email address anytime at «https://github.com/MakStef/ecommerce». \n(this is just a demonstrative message and actually there won't be any actions later.)",
        settings.EMAIL_HOST_USER,
        [reciever_email, ],
    )


def unsign(reciever_email):
    send_mail(
        'Unsign for ZLATMAX newsletters',
        "You won't be recieving ZLATMAX newsletters anymore. You can sign up your email again at «https://github.com/MakStef/ecommerce». \n(this is just a demonstrative message and actually there won't be any actions later.)",
        settings.EMAIL_HOST_USER,
        [reciever_email, ],
    )
