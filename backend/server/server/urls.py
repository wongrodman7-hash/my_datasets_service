from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from apps.endpoints.urls import urlpatterns as endpoints_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='api/v1/', permanent=False)),
]

urlpatterns += endpoints_urlpatterns
