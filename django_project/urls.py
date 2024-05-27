from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)


urlpatterns = [
    path('', include('blogs.urls')),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('admin/', admin.site.urls),
    path('users/',include('users.urls')),
    path('articles/', include('articles.urls')),
    path("__debug__/", include("debug_toolbar.urls")),        
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    