from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_message(html_route, user):
    html_message = render_to_string(html_route, {"user": user})

    send_mail(
        "Test",
        html_message,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
        html_message=html_message
    )