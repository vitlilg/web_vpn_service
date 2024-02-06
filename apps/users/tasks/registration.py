from apps.users.models.statement_registration import CustomerStatementRegistration
from apps.users.services.registration import CustomerRegistrationService
from web_vpn_service import celery_app


@celery_app.task
def registration_from_statement(statement_id: int) -> bool:
    statement = CustomerStatementRegistration.objects.get(id=statement_id)
    CustomerRegistrationService.registration_from_statement(statement)
    return True
