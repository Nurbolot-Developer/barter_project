# barter_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

def root_view(request):
    return JsonResponse({"message": "Barter API: go to /api/ads/ or /api/proposals/"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ads/', include('ads.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/', include('ads.api_urls')),  # если есть отдельный файл с API роутингом
    # Редирект с корня сайта на /ads/
    path('', RedirectView.as_view(url='/ads/', permanent=False)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
