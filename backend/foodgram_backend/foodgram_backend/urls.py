from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from .views import ShortLinkRedirectView

urlpatterns = [
    path("api/", include("api.urls")),
    path('admin/', admin.site.urls),
    path('s/<str:short_code>/', ShortLinkRedirectView.as_view(), name='short-link'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
