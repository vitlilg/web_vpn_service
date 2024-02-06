from django.urls import path
from rest_framework import routers

from apps.web_cabinet.api.v1.views.confirm_registration import ConfirmCustomerRegistrationView
from apps.web_cabinet.api.v1.views.registration import CustomerRegistrationView
from apps.web_cabinet.api.v1.views.web_user_profile import GetUserInfoView, UploadUserPhotoView
from apps.web_cabinet.api.v1.views.websites import CabinetWebsiteView
from apps.websites.api.v1.views.statistic import WebsiteStatisticView

app_name = 'web_cabinet'

router = routers.SimpleRouter()
router.register('websites', CabinetWebsiteView)

urlpatterns = [
    path('registration/', CustomerRegistrationView.as_view()),
    path('confirm_registration/', ConfirmCustomerRegistrationView.as_view()),
    path('my/', GetUserInfoView.as_view()),
    path('my/upload_photo/', UploadUserPhotoView.as_view()),
    path(
        'websites/statistic/',
        WebsiteStatisticView.as_view(),
        name='websites_statistic',
    ),
]

urlpatterns += router.urls
