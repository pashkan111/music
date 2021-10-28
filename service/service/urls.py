from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('service.routers')),
    path('account/api', include('src.accounts.api.urls')),
    path('', include('src.accounts.urls')),
]

