from django.contrib import admin
from django.urls import path, include
from car_service.views import index
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = ([
    path('admin/', admin.site.urls),
    path('car_service/', include('car_service.urls')),
    path('', RedirectView.as_view(url='car_service/', permanent=True)),
    path('tinymcre', include('tinymce.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))

urlpatterns += [
    path("accounts/", include('django.contrib.auth.urls')),
]