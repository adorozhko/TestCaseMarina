from django.contrib import admin
from django.urls import include, path

from subscriptions.urls import router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v0/', include(router.urls))
]
