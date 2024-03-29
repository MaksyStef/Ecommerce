from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls', 'store')),
    path('account/', include('account.urls', 'account')),
    path('api/', include('api.urls', 'api')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # Serve Media files