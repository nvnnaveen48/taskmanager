from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.home, name='home'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add-user/', views.add_user, name='add_user'),
    path('bulk-add-users/', views.bulk_add_users, name='bulk_add_users'),
    path('assign-task/', views.assign_task, name='assign_task'),
    path('mark-task-done/<int:task_id>/', views.mark_task_done, name='mark_task_done'),
    path('add-note/<int:task_id>/', views.add_note, name='add_note'),
    path('send-alert/<int:user_id>/', views.send_alert, name='send_alert'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 