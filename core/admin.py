from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import CustomUser, Task, Notification
import csv
import json
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import StringIO
from django import forms
import base64
from django.core.files.base import ContentFile

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_admin', 'profile_image_display')
    list_filter = ('is_admin',)
    search_fields = ('username', 'email')
    ordering = ('username',)
    
    def profile_image_display(self, obj):
        if obj.profile_image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />', obj.profile_image.url)
        return "No Image"
    profile_image_display.short_description = 'Profile Image'

class TaskAdminForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        widgets = {
            'csv_data': forms.Textarea(attrs={'class': 'vLargeTextField', 'rows': 10}),
        }

class TaskAdmin(admin.ModelAdmin):
    form = TaskAdminForm
    list_display = ('user', 'status', 'created_at', 'image_display')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username',)
    ordering = ('-created_at',)
    
    def image_display(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "No Image"
    image_display.short_description = 'Task Image'

    def save_model(self, request, obj, form, change):
        if 'csv_file' in request.FILES:
            csv_file = request.FILES['csv_file']
            if isinstance(csv_file, InMemoryUploadedFile):
                decoded_file = csv_file.read().decode('utf-8')
                obj.csv_data = decoded_file
        # Handle pasted image from clipboard (base64 in POST)
        pasted_image_data = request.POST.get('pasted_image_data')
        if pasted_image_data and pasted_image_data.startswith('data:image'):
            format, imgstr = pasted_image_data.split(';base64,')
            ext = format.split('/')[-1]
            obj.image = ContentFile(base64.b64decode(imgstr), name=f'pasted_image.{ext}')
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        if obj.image:
            obj.image.delete(save=False)
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            if obj.image:
                obj.image.delete(save=False)
        super().delete_queryset(request, queryset)

    class Media:
        js = ('admin/js/task_admin.js',)

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_type', 'message', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('user__username', 'message')
    ordering = ('-created_at',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Notification, NotificationAdmin)
