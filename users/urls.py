from django.urls import path
from django.contrib.auth.views import LogoutView,LoginView
from .views import register_view,profile_view,change_password_view

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/',profile_view, name='profile'),
    path('change-password/', change_password_view, name='change_password'),
]