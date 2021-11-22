from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('service.routers')),
    path('api/account/', include('src.accounts.api.urls')),
    path('api/music/', include('src.music.api.urls')),
    path('', include('src.accounts.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)