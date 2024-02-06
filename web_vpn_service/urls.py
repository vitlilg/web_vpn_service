"""
URL configuration for web_vpn_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from web_vpn_service import settings

urlpatterns = [
    path('api/v1/admin/', admin.site.urls),
    path('api/v1/auth/', include('apps.authentications.api.v1.urls')),
    path('api/v1/proxy/', include('apps.proxy.api.v1.urls')),
    path('api/v1/users/', include('apps.users.api.v1.urls')),
    path('api/v1/web_cabinet/', include('apps.web_cabinet.api.v1.urls')),
    path('api/v1/websites/', include('apps.websites.api.v1.urls')),
]

if settings.SWAGGER_URL:

    urlpatterns += [
        path('api/v1/swagger_schema/', SpectacularAPIView.as_view(api_version='v1'), name='schema'),
        path(f'api/v1/{settings.SWAGGER_URL}/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
    ]
