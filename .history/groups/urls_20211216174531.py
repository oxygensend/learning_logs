from django.urls import path, include, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views

app_name = 'groups'

urlpatterns = [

    path('', views.GroupsView.as_view(), name='groups'),
    path('new_groups', views.NewGroupView.as_view(), name='new_group'),
    path('<int:group_id>/', views.group, name='group'),
    path('delete_group/<int:pk>/', views.DeleteGroupView.as_view(), name='delete_group'),
    path('add_to_group/<int:group_id>/', views.add_to_group , name='add_to_group'),
    path('delete_from_group/<int:group_id>/', views.delete_from_group,name='delete_from_group'),
    path('delete_user/<int:group_id>/<int:user_id>/', views.delete_user, name='delete_user')
]