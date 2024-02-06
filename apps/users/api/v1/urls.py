from rest_framework import routers

from apps.users.api.v1.views.user import UserViewSet

app_name = 'users'

router = routers.SimpleRouter()
router.register('', UserViewSet)

urlpatterns = [
]

urlpatterns += router.urls
