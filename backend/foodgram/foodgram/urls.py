from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users_api.urls')),
    path('api/', include('recipes_api.urls')),
]
