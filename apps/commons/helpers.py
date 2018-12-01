import logging

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def email(context, subject, to_mail, html_template):
    """
    Send email
    :param context:
    :param subject:
    :param to_mail:
    :param html_template:
    :return:
    """
    html_content = render_to_string(html_template, context)
    try:
        send_mail(
            subject=subject,
            message='',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=to_mail,
            fail_silently=False,
            html_message=html_content)
    except Exception as exc:
        logging.error("Error enviando el correo")
        logging.error("Mensaje de error=> {}".format(exc))
        return False
    else:
        return True
