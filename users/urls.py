from django.urls import path, include, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [

    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('password-change/', auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('users:password_change_done'), template_name='registration/password_change.html'), name='password_change'),
]