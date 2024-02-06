REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'apps.services.authentication_services.TokenAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DATETIME_FORMAT': '%H:%M:%S %d.%m.%Y',
    'DATE_INPUT_FORMATS': [
        '%Y-%m-%d',
        '%d-%m-%Y',
    ],
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),
    'DEFAULT_PAGINATION_CLASS': 'mixins.page_mixin.ShortLinkResultPagination',
    'DEFAULT_SCHEMA_CLASS': 'web_vpn_service.schemas.SwaggerSchema',
    # other settings
    'EXCEPTION_HANDLER': 'drf_standardized_errors.handler.exception_handler',
}
