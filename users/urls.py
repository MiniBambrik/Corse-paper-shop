from django.urls import path, include
from . import views

app_name = 'users'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
]