from django.urls import path
from rest_framework.routers import SimpleRouter

from apps.authentications.api.v1.views.login import LoginView, LogoutView
from apps.authentications.api.v1.views.password import (
    ChangePasswordAPIView, ChangePasswordByTokenView, SendPasswordRecoveryEmailView,
)
from apps.authentications.api.v1.views.token import TokenView

app_name = 'auth'

router = SimpleRouter()

router.register('token', TokenView)

urlpatterns = [
    path('login/', LoginView.as_view(), name='auth_login'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('change_password/', ChangePasswordAPIView.as_view(), name='auth_password_change'),
    path('send_password_recovery_email/', SendPasswordRecoveryEmailView.as_view(), name='auth_password_reset_email'),
    path('change_password_by_token/', ChangePasswordByTokenView.as_view(), name='auth_change_password_by_token'),
]

urlpatterns += router.urls
