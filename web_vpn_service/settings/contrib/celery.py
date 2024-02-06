from web_vpn_service.settings.contrib.redis import REDIS_URL

CELERY_BROKER_URL = REDIS_URL + '/3'
CELERY_RESULT_BACKEND = REDIS_URL + '/4'
CELERY_ACCEPT_CONTENT = ['application/json', 'pickle']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
