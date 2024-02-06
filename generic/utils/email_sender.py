from collections.abc import Sequence

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from apps.history.models.email_history import EmailSendingHistory


def send_email(
        plain_message,
        recipients: Sequence,
        html_message,
        title: str = settings.EMAIL_SUBJECT,
        from_email: str = settings.INFO_EMAIL_SENDER,
):
    email_status = EmailSendingHistory.Status.SUCCESS
    error_type = None
    try:
        send_mail(
            title,
            plain_message,
            from_email,
            recipients,
            html_message=html_message,
        )
    except Exception as exc:
        email_status = EmailSendingHistory.Status.ERROR
        error_type = exc.__class__.__name__
        raise
    finally:
        EmailSendingHistory.objects.create(
            title=title,
            from_email=from_email,
            recipients=recipients,
            status=email_status,
            error_type=error_type,
        )


def send_html_message(
    template: str,
    context: dict,
    recipients: Sequence,
):
    html_message = render_to_string(template, context)
    plain_message = strip_tags(html_message)
    send_email(
        plain_message=plain_message,
        recipients=recipients,
        html_message=html_message,
    )
