from web_vpn_service.settings.environment import env

EMAIL_BACKEND = 'django_ses.SESBackend'
AWS_SES_ACCESS_KEY_ID = env.str('AWS_SES_ACCESS_KEY_ID', '')
AWS_SES_SECRET_ACCESS_KEY = env.str('AWS_SES_SECRET_ACCESS_KEY', '')
AWS_SES_REGION_NAME = 'eu-central-1'
AWS_SES_REGION_ENDPOINT = 'email.eu-central-1.amazonaws.com'
INFO_EMAIL_SENDER = env.str('INFO_EMAIL_SENDER', '')
DEFAULT_FROM_EMAIL = env.str('INFO_EMAIL_SENDER', '')
EMAIL_SUBJECT = 'Simple VPN Service'
