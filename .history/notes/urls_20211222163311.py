from django.urls import path
from . import views

app_name = 'notes'

urlpatterns = [
    path('',views.index, name='index'),
    path('topics/', views.topics, name='topics'),
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    path('new_topic/', views.new_topic, name='new_topic'),
    path('delete_topic/<int:topic_id>/', views.delete_topic, name='delete_topic'),
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    path('edit_entry/<int:entry_id>/', views.edit_entry,name='edit_entry'),
    path('delete_entry/<int:entry_id>/', views.delete_entry, name='delete_entry'),
    path('groups/new_topic/<int:group_id>/', views.group_new_topic, name='group_new_topic'),

]
