from django.urls import path, include, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [

    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
]