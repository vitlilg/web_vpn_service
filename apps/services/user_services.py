from apps.users.exceptions import CustomerNotFoundError
from apps.users.models import User


class CustomerService:

    @staticmethod
    def get_customer_user_by_request(request, kwargs):
        request_user = request.user
        if request_user.type_user == User.TypeUserChoices.CUSTOMER:
            customer_user = request_user
        else:
            kwargs_param = 'customer_pk'
            customer_pk = kwargs.get(kwargs_param)
            if not customer_pk:
                return CustomerNotFoundError
            if isinstance(customer_pk, str) and not customer_pk.isdigit():
                raise CustomerNotFoundError
            try:
                customer_user = User.objects.get(id=customer_pk, type_user=User.TypeUserChoices.CUSTOMER)
            except User.DoesNotExist:
                raise CustomerNotFoundError
        return customer_user
