from django.template.loader import render_to_string
from django.utils.html import strip_tags

from apps.services.email_services import EmailService
from apps.users.models import User
from apps.users.models.statement_registration import CustomerStatementRegistration
from generic.utils.email_sender import send_email
from web_vpn_service import celery_app


@celery_app.task
def get_and_send_security_code_to_email(email: str):
    security_code = EmailService.get_or_create_security_code_for_email(email)
    statement = CustomerStatementRegistration.objects.filter(
        status=CustomerStatementRegistration.Status.WAITING_CONFIRMATION_EMAIL.value,
        email=email,
    ).first()
    full_name = f'{statement.first_name} {statement.last_name}'
    html_message = render_to_string(
        'templates/email_confirmation_code.html', {
            'full_name': full_name.strip(),
            'security_code': security_code,
        },
    )
    plain_message = strip_tags(html_message)
    send_email(
        plain_message=plain_message,
        recipients=[email],
        html_message=html_message,
    )


@celery_app.task(serializer='pickle')
def send_email_about_successful_registration(user: User, password: str):
    full_name = f'{user.first_name} {user.last_name}'
    context = {
        'full_name': full_name.strip(),
        'password': password,
    }
    html_message = render_to_string('templates/successful_registration_email.html', context=context)
    plain_message = strip_tags(html_message)
    return send_email(
        plain_message,
        [user.email],
        html_message,
        'Successful registration on Jobs service',
    )


@celery_app.task(serializer='pickle')
def send_email_about_reset_password(user: User, password: str):
    full_name = f'{user.first_name} {user.last_name}'
    context = {
        'full_name': full_name.strip(),
        'password': password,
    }
    html_message = render_to_string('templates/password_reset_email.html', context=context)
    plain_message = strip_tags(html_message)
    return send_email(
        plain_message,
        [user.email],
        html_message,
        'Password reset',
    )
