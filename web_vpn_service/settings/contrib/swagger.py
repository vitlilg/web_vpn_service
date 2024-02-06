from web_vpn_service.settings.environment import env

SPECTACULAR_SETTINGS = {
    'TITLE': 'Web VPN Service',
    'DESCRIPTION': 'Simple Web VPN Service',
    'VERSION': '1.0.0',
    'SCHEMA_PATH_PREFIX': '/api/v[0-9]',
    'COMPONENT_SPLIT_REQUEST': True,
    'AUTHENTICATION_WHITELIST': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'apps.services.authentication_services.TokenAuthentication',
    ],
    'SWAGGER_UI_SETTINGS': {
        'persistAuthorization': True,
    },
}

SWAGGER_URL = env.str('SWAGGER_URL', None)
