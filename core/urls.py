from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.home, name='home'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add-user/', views.add_user, name='add_user'),
    path('bulk-add-users/', views.bulk_add_users, name='bulk_add_users'),
    path('assign-task/', views.assign_task, name='assign_task'),
    path('mark-task-done/<int:task_id>/', views.mark_task_done, name='mark_task_done'),
    path('add-note/<int:task_id>/', views.add_note, name='add_note'),
    path('send-alert/<int:user_id>/', views.send_alert, name='send_alert'),
    path('api/admin/stats/', views.admin_stats, name='admin_stats'),
    path('api/admin/tasks/', views.admin_tasks, name='admin_tasks'),
    path('api/admin/users/', views.admin_users, name='admin_users'),
    path('api/admin/tasks/<int:task_id>/', views.admin_task_detail, name='admin_task_detail'),
    path('api/admin/users/<int:user_id>/', views.admin_user_detail, name='admin_user_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 