from apps.history.models.history import History
from web_vpn_service import celery_app


@celery_app.task(serializer='pickle')
def create_history(**kwargs):
    History.objects.create(**kwargs)
