from django.urls import path
from . import views

app_name = 'tasks'
urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('task/<int:pk>/', views.task_detail, name='task_detail'),
    path('task/new/', views.task_new, name='task_new'),
    path('task/<int:pk>/edit/', views.task_edit, name='task_edit'),
    path('task/<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('task/<int:pk>/history/', views.task_history, name='task_history'),
    path('task_stats/', views.task_stats, name='task_stats'),

]