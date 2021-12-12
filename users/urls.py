from django.urls import path, include, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [

    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('password-change/', auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('users:password_change_done'), template_name='registration/password_change.html'), name='password_change'),
    path('groups', views.groups, name='groups'),
    path('new_groups', views.new_group, name='new_group'),
    path('groups/<int:group_id>/', views.group, name='group'),
    path('delete_group/<int:group_id>/', views.delete_group, name='delete_group'),
    path('add_to_group/<int:group_id>/', views.add_to_group , name='add_to_group')

]