from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import logout
from django.views.decorators.csrf import ensure_csrf_cookie
import pandas as pd
import json
from .models import CustomUser, Task, Notification
from .forms import CustomUserCreationForm, CSVUploadForm, TaskAssignmentForm, NoteForm
from django.contrib.auth.models import User
from django.db.models import Count
from datetime import datetime

def is_admin(user):
    return user.is_authenticated and user.is_admin

def is_staff_user(user):
    return user.is_staff

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
            task.status = 'in_progress'
            task.save()

            admin_user = CustomUser.objects.filter(is_admin=True).first()
            if admin_user:
                Notification.objects.create(
                    user=admin_user,
                    notification_type='task_noted',
                    message=f'Task {task_id} marked as in progress by {request.user.username}'
                )
                return JsonResponse({'status': 'success', 'message': 'Status updated to in progress.'})
            else:
                return JsonResponse({'status': 'success', 'message': 'Status updated to in progress, but no admin to notify.'})
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

@ensure_csrf_cookie
@user_passes_test(is_staff_user)
def admin_stats(request):
    stats = {
        'total_tasks': Task.objects.count(),
        'completed_tasks': Task.objects.filter(status='done').count(),
        'in_progress_tasks': Task.objects.filter(status='in_progress').count(),
        'pending_tasks': Task.objects.filter(status='pending').count()
    }
    return JsonResponse(stats)

@ensure_csrf_cookie
@user_passes_test(is_staff_user)
def admin_tasks(request):
    if request.method == 'GET':
        tasks = Task.objects.all().order_by('-created_at')
        tasks_data = [{
            'id': task.id,
            'username': task.user.username if task.user else 'Unassigned',
            'status': task.status,
            'created_at': task.created_at.isoformat(),
            'has_image': bool(task.image),
            'has_csv': bool(task.csv_data)
        } for task in tasks]
        return JsonResponse(tasks_data, safe=False)
    
    elif request.method == 'POST':
        try:
            # Get form data
            user_id = request.POST.get('assigned_to')
            
            if not user_id:
                return JsonResponse({'status': 'error', 'message': 'User assignment is required'}, status=400)
            
            # Create task
            task = Task.objects.create(
                user_id=user_id,
                status='pending'
            )
            
            # Handle file uploads
            image = request.FILES.get('image')
            csv_file = request.FILES.get('csv_file')
            csv_data = request.POST.get('csv_data')
            
            if image:
                task.image = image
                task.save()
            
            if csv_file:
                csv_content = csv_file.read().decode('utf-8')
                task.csv_data = csv_content
                task.save()
            elif csv_data:
                task.csv_data = csv_data
                task.save()
            
            # Create notification
            Notification.objects.create(
                user_id=user_id,
                notification_type='task_assigned',
                message=f'New task assigned: Task #{task.id}'
            )
            
            return JsonResponse({
                'status': 'success',
                'task_id': task.id,
                'message': 'Task created successfully'
            })
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@ensure_csrf_cookie
@user_passes_test(is_staff_user)
def admin_users(request):
    if request.method == 'GET':
        users = CustomUser.objects.all().order_by('-date_joined')
        users_data = [{
            'id': user.id,
            'username': user.username,
            'email': user.email or '',
            'is_active': user.is_active,
            'is_staff': user.is_staff,
            'date_joined': user.date_joined.isoformat()
        } for user in users]
        return JsonResponse(users_data, safe=False)
    
    elif request.method == 'POST':
        try:
            username = request.POST.get('username')
            email = request.POST.get('email', '')  # Make email optional
            password = request.POST.get('password')
            
            if not username or not password:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Username and password are required'
                }, status=400)
            
            # Check for unique username
            if CustomUser.objects.filter(username=username).exists():
                return JsonResponse({
                    'status': 'error',
                    'message': 'Username already exists'
                }, status=400)
            
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_staff=False  # Always create regular users
            )
            return JsonResponse({'status': 'success', 'user_id': user.id})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@ensure_csrf_cookie
@user_passes_test(is_staff_user)
def admin_task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'GET':
        return JsonResponse({
            'id': task.id,
            'status': task.status,
            'created_at': task.created_at.isoformat(),
            'assigned_to': task.user.username if task.user else None,
            'has_image': bool(task.image),
            'has_csv': bool(task.csv_data),
            'csv_data': task.csv_data if task.csv_data else None,
            'image_url': task.image.url if task.image else None
        })
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            task.status = data.get('status', task.status)
            if 'assigned_to' in data:
                task.user_id = data['assigned_to']
            task.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    elif request.method == 'DELETE':
        try:
            # Delete associated files
            if task.image:
                task.image.delete(save=False)
            task.delete()
            return JsonResponse({'status': 'success', 'message': 'Task deleted successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@ensure_csrf_cookie
@user_passes_test(is_staff_user)
def admin_user_detail(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'GET':
        return JsonResponse({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_active': user.is_active,
            'is_staff': user.is_staff,
            'date_joined': user.date_joined.isoformat()
        })
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            user.username = data.get('username', user.username)
            user.email = data.get('email', user.email)
            user.is_active = data.get('is_active', user.is_active)
            user.is_staff = data.get('is_staff', user.is_staff)
            if 'password' in data:
                user.set_password(data['password'])
            user.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    elif request.method == 'DELETE':
        try:
            # Check if user has any tasks
            if Task.objects.filter(assigned_to=user).exists():
                return JsonResponse({
                    'status': 'error',
                    'message': 'Cannot delete user with assigned tasks'
                }, status=400)
            
            user.delete()
            return JsonResponse({'status': 'success', 'message': 'User deleted successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
