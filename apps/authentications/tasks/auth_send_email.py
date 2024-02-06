from django.template.loader import render_to_string
from django.utils.html import strip_tags

from generic.utils.email_sender import send_email
from web_vpn_service import celery_app


@celery_app.task
def send_email_about_recovery_password(email, template_context):
    html_message = render_to_string('templates/recovery_password_email.html', template_context)
    plain_message = strip_tags(html_message)
    title = 'Recovery password on Simple VPN service'
    return send_email(
        plain_message,
        [email],
        html_message,
        title,
    )
