from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def welcome_messages(instance):
    """ For a welcome email upon registration
    """
    message = f"Hello, {instance.username}"
    html_message = render_to_string("gmail/hello_massage.html", {"user": instance})

    send_mail(
        message,
        html_message,
        settings.EMAIL_HOST_USER,
        [instance.email],
        fail_silently=False,
        html_message=html_message
    )


def key_message(instance, key):
    """ Sends a confirmation key by email to recover your password
    """
    message = "Ключ подтверждения"
    html_message = render_to_string("gmail/key_message.html", {'user': instance, "key": key})

    send_mail(
        message,
        html_message,
        settings.EMAIL_HOST_USER,
        [instance.email],
        fail_silently=False,
        html_message=html_message
    )
