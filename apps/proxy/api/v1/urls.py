from django.urls import path

from apps.proxy.api.v1.views.proxy import ProxyView

app_name = 'proxy'

urlpatterns = [
    path(
        r'',
        ProxyView.as_view(),
        name='proxy',
    ),
]
