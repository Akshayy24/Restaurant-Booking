from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('restaurant.urls')),
    path('users/', include('users.urls')),
    path('menu/', include('menu.urls')),

]