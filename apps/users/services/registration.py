from datetime import datetime, timedelta

from apps.history.models.email_history import EmailSendingHistory
from apps.users.models import User, UserProfile
from apps.users.models.statement_registration import CustomerStatementRegistration


class CustomerRegistrationService:

    @classmethod
    def registration_from_statement(
            cls,
            statement: CustomerStatementRegistration,
    ) -> int:
        customer_user = cls._create_customer_user(statement)
        cls._create_customer_profile(statement, customer_user)
        statement.user = customer_user
        statement.status = CustomerStatementRegistration.Status.APPROVED.value
        statement.save(update_fields=['user', 'status'])
        return customer_user.id

    @staticmethod
    def _create_customer_user(statement: CustomerStatementRegistration) -> User:
        user = User.objects.create_user(
            email=statement.email,
            first_name=statement.first_name,
            last_name=statement.last_name,
        )
        user.password = statement.password
        user.save(update_fields=['password'])
        return user

    @staticmethod
    def _create_customer_profile(
            statement: CustomerStatementRegistration,
            customer_user: User,
    ) -> UserProfile:
        return UserProfile.objects.create(
            user=customer_user,
            middle_name=statement.middle_name,
        )

    @staticmethod
    def check_when_last_email_was_sent(email: str, lifetime: int = 30) -> bool:
        time_end_mail = datetime.now() - timedelta(seconds=lifetime)
        return EmailSendingHistory.objects.filter(
            recipients__overlap=[email],
            send_time__gt=time_end_mail,
        ).exists()
