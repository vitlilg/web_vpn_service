from rest_framework import routers

from apps.websites.api.v1.views.websites import WebsiteViewSet

app_name = 'websites'

router = routers.SimpleRouter()
router.register('', WebsiteViewSet)

urlpatterns = [

]

urlpatterns += router.urls
