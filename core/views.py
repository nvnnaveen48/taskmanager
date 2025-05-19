from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import logout
import pandas as pd
import json
from .models import CustomUser, Task, Notification
from .forms import CustomUserCreationForm, CSVUploadForm, TaskAssignmentForm, NoteForm

def is_admin(user):
    return user.is_authenticated and user.is_admin

@login_required
def home(request):
    if request.user.is_admin:
        return redirect('admin_dashboard')
    
    tasks = request.user.tasks.all()[:10]  # Get latest 10 tasks
    # Parse CSV/TSV data for each task using pandas
    for task in tasks:
        if task.csv_data:
            try:
                from io import StringIO
                sep = '\t' if '\t' in task.csv_data else ','
                df = pd.read_csv(StringIO(task.csv_data), sep=sep)
                task.csv_table = df.to_html(classes='table table-bordered table-striped align-middle text-center', index=False, border=0)
            except Exception:
                task.csv_table = '<pre>' + task.csv_data + '</pre>'
        else:
            task.csv_table = '<span>No data</span>'
    return render(request, 'core/user_dashboard.html', {'tasks': tasks})

@user_passes_test(is_admin)
def admin_dashboard(request):
    users = CustomUser.objects.filter(is_admin=False)
    return render(request, 'core/admin_dashboard.html', {'users': users})

@user_passes_test(is_admin)
def add_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_admin = False
            user.save()
            messages.success(request, 'User added successfully!')
            return redirect('admin_dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/add_user.html', {'form': form})

@user_passes_test(is_admin)
def bulk_add_users(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            df = pd.read_csv(csv_file)
            
            for _, row in df.iterrows():
                if not CustomUser.objects.filter(username=row['username']).exists():
                    user = CustomUser.objects.create_user(
                        username=row['username'],
                        email=row.get('email', ''),
                        password=row['password']
                    )
            
            messages.success(request, 'Users added successfully!')
            return redirect('admin_dashboard')
    else:
        form = CSVUploadForm()
    return render(request, 'core/bulk_add_users.html', {'form': form})

@user_passes_test(is_admin)
def assign_task(request):
    if request.method == 'POST':
        form = TaskAssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save()
            # Enforce 10-task limit per user
            user_tasks = Task.objects.filter(user=task.user).order_by('-created_at')
            if user_tasks.count() > 10:
                for old_task in user_tasks[10:]:
                    if old_task.image:
                        old_task.image.delete(save=False)
                    old_task.delete()
            Notification.objects.create(
                user=task.user,
                notification_type='admin_alert',
                message='New task assigned to you'
            )
            messages.success(request, 'Task assigned successfully!')
            return redirect('admin_dashboard')
    else:
        form = TaskAssignmentForm()
    return render(request, 'core/assign_task.html', {'form': form})

@login_required
def mark_task_done(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.status = 'done'
    task.save()

    admin_user = CustomUser.objects.filter(is_admin=True).first()
    if admin_user:
        Notification.objects.create(
            user=admin_user,
            notification_type='task_done',
            message=f'Task {task_id} marked as done by {request.user.username}'
        )
        return JsonResponse({'status': 'success', 'message': 'Task marked as done and admin notified.'})
    else:
        return JsonResponse({'status': 'success', 'message': 'Task marked as done, but no admin to notify.'})

@login_required
def add_note(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            task.status = 'noted'
            task.save()

            admin_user = CustomUser.objects.filter(is_admin=True).first()
            if admin_user:
                Notification.objects.create(
                    user=admin_user,
                    notification_type='task_noted',
                    message=f'Note from {request.user.username}: {form.cleaned_data["note"]}'
                )
                return JsonResponse({'status': 'success', 'message': 'Note sent to admin.'})
            else:
                return JsonResponse({'status': 'success', 'message': 'Note saved, but no admin to notify.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})

@user_passes_test(is_admin)
def send_alert(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    Notification.objects.create(
        user=user,
        notification_type='admin_alert',
        message='Alert from admin'
    )
    return JsonResponse({'status': 'success'})
