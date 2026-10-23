from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render,redirect
from django.contrib import messages
import re
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render

from django.db.models import Q
def admin_required(view):
    return login_required(user_passes_test(lambda u: u.is_superuser)(view))

# Create your views here.
def home(request):
    return render(request,'home.html')
def signup_page(request):
    return render(request,'signup_page.html')
def register_user(request):
    if request.method=='POST':
        name=request.POST.get('name')
        address= request.POST.get('address')
        phone= request.POST.get('phone')
        email= request.POST.get('email')
        password=request.POST.get('password')
        if User.objects.filter(email=email).exists():
                    return JsonResponse({
                  
                            'success':False,   
                            'message':'Email already exists'               
                           
        
            })
        if Registeration.objects.filter(phone=phone).exists():
                            return JsonResponse({
                          
                                    'success':False,   
                                    'message':'Phone already exists'               
                                   
                
                    })
        if not re.fullmatch(r'[6-9][0-9]{9}', phone):
         return JsonResponse({
            'success': False,
            'message': 'Enter a valid 10-digit mobile number.'
        })

        if not re.fullmatch(r'[^@\s]+@[^@\s]+\.com', email, re.IGNORECASE):
         return JsonResponse({
            'success': False,
            'message': 'Enter a valid email ending in .com.'
        })

        if not re.fullmatch(r'(?=.*[A-Za-z])(?=.*[0-9])(?=.*[^A-Za-z0-9\s])\S{8,}',password):
         return JsonResponse({
                    'success': False,
                    'message': 'Password must contain a letter, number, symbol, and at least 8 characters.'
                })

        user=User.objects.create_user(password=password,username=email,email=email)
        
        Registeration.objects.create(
            user=user,
                name=name,address=address,phone=phone,email=email
            )
        return JsonResponse({
          
                    'success':True,   
                    'message':'User Added successfully'               
                   

    })
def check_email(request):
    email = request.GET.get("email")
    exists = User.objects.filter(email=email).exists()
    return JsonResponse({"exists": exists})

def check_phone(request):
    phone = request.GET.get("phone")
    exists = Registeration.objects.filter(phone=phone).exists()
    return JsonResponse({"exists": exists})
def login_page(request):

    return render(request,'login_page.html')


def login_fun(request):
    if request.method == 'POST':
        email = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        try:
            user_obj = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            messages.error(request, 'Invalid email or password.')
            return redirect('login_page')

        user = authenticate(
            request,
            username=user_obj.username,
            password=password
        )

        if user is not None:
            login(request, user)

            if user.is_superuser:
                return redirect('admin_home')

            return redirect('user_home')

        messages.error(request, 'Invalid email or password.')
        return redirect('login_page')

    return redirect('login_page')
@login_required
@admin_required
def addtask(request):
    unread_notifications_count=TaskComment.objects.filter(is_read=False).count()

    members=Registeration.objects.all()
    return render(request,'addtask.html',{
          'members':members,
          'unread_notifications_count':unread_notifications_count
    })

@admin_required
def admin_home(request):
     profile=request.user
     unread_notifications_count=TaskComment.objects.filter(is_read=False).count()
     tasks=Task.objects.count()
     todo_count=Task.objects.filter(status='todo').count()
     in_progress_count=Task.objects.filter(status='in_progress').count()
     done_count=Task.objects.filter(status='completed').count()
     recent_tasks=Task.objects.order_by('-created_date')[:3]
     return render(request,'admin_home.html',{
           'profile':profile,
           'tasks':tasks,
           'todo_count':todo_count,
           'in_progress_count':in_progress_count,
           'done_count':done_count,
           'unread_notifications_count':unread_notifications_count,
           'recent_tasks':recent_tasks
     }) 
@login_required
@admin_required
def task_save(request):
    if request.method=='POST':
            name=request.POST.get('name')
            description= request.POST.get('des')
            priority= request.POST.get('priority')
            status= request.POST.get('status')
            assigned= request.POST.get('assigned_to')
            enddate=request.POST.get('enddate')
            assigned_to=User.objects.get(id=assigned)

            
            Task.objects.create(
                created_by=request.user,assigned_to=assigned_to,
                    title=name,description=description,priority=priority,status=status,
                    due_date=enddate
                    

                )
            return JsonResponse({
              
                        'success':True,   
                        'message':'Task Added successfully'               
                       
    
        })
from django.db.models import Case, When, Value, IntegerField
from django.utils import timezone

@login_required
def user_home(request):
    profile=Registeration.objects.get(user=request.user)
    total_tasks=Task.objects.filter(assigned_to=request.user.id).count()
    todo_count=Task.objects.filter(status='todo',assigned_to=request.user.id).count()
    in_progress_count=Task.objects.filter(status='in_progress',assigned_to=request.user.id).count()
    done_count=Task.objects.filter(status='completed',assigned_to=request.user.id).count()
    today = timezone.localdate()
    
    task=Task.objects.filter(assigned_to=request.user.id)
    smart_task = task.filter(
       due_date__isnull=False
    ).exclude(
        status='completed'
    ).annotate(
        priority_order=Case(
            When(priority='high', then=Value(1)),
            When(priority='medium', then=Value(2)),
            When(priority='low', then=Value(3)),
            default=Value(4),
            output_field=IntegerField()
        )
    ).order_by('due_date', 'priority_order').first()
    due_today_count = task.filter(
            due_date=today
        ).exclude(status='completed').count()
    
    overdue_count = task.filter(
            due_date__lt=today
        ).exclude(status='completed').count()
    return render(request,'user_home.html',{
          'profile':profile,
          'task':task,
          'smart_task':smart_task,
          'total_tasks':total_tasks,
          'todo_count':todo_count,
          'in_progress_count':in_progress_count,
          'done_count':done_count,
          'due_today_count':due_today_count,
          'overdue_count':overdue_count
    })
@login_required
@admin_required
def viewtask(request):
    unread_notifications_count=TaskComment.objects.filter(is_read=False).count()

    task=Task.objects.filter(created_by=request.user)
    members=User.objects.all().exclude(is_superuser=True)
    search=request.GET.get('search')
    priority=request.GET.get('priority')
    status=request.GET.get('status')
    
    if  search: 
          task=task.filter(title__icontains=search)
                           
    if priority:
          task=task.filter(priority=priority)
    if status:
              task=task.filter(status=status)
    


    return render(request,'viewtask.html',{
        'task':task,
        'members':members,
        'unread_notifications_count':unread_notifications_count
    })
@login_required
@admin_required

def delete_task(request):
    id=request.POST.get('id')
    task=Task.objects.get(id=id)
    task.delete()
    return JsonResponse({
        'success':True
    })

@login_required
@admin_required

def task_update(request):
    if request.method=='POST':
            id=request.POST.get('id')
            name=request.POST.get('name')
            description= request.POST.get('des')
            priority= request.POST.get('priority')
            status= request.POST.get('status')
            assigned_to= request.POST.get('assigned_to')
            assigned=User.objects.get(id=assigned_to)   
            enddate=request.POST.get('enddate')
            task=Task.objects.get(id=id)
            task.title=name
            task.description=description
            task.priority=priority
            task.status=status
            task.due_date=enddate
            task.assigned_to=assigned
            task.save()
            
            return JsonResponse({
              
                        'success':True,   
                        'message':'Task Updated successfully'               
                       
    
        })
@login_required
def user_tasks(request):
      tasks=Task.objects.filter(assigned_to=request.user)
      profile=Registeration.objects.get(user=request.user)
      total_tasks=Task.objects.filter(assigned_to=request.user.id).count()
      todo_count=Task.objects.filter(status='todo',assigned_to=request.user.id).count()
      in_progress_count=Task.objects.filter(status='in_progress',assigned_to=request.user.id).count()
      done_count=Task.objects.filter(status='completed',assigned_to=request.user.id).count()
      for task in tasks:
        task.has_new_comment = task.comments.filter(
            user__is_staff=True,
            is_read_by_assignee=False
        ).exists()
      
      return render(request,'user_tasks.html',{
            'tasks':tasks,
            'profile':profile,
            'todo_count':todo_count,
                      'in_progress_count':in_progress_count,
                      'done_count':done_count
      })
def log_out(request):
    logout(request)
    return redirect('login_page')

@login_required

def update_task_status(request):
     
      if request.method=='POST':
            status=request.POST.get('status')
            task_id=request.POST.get('task_id')
            task=Task.objects.get(id=task_id, assigned_to=request.user)
            task.status=status
            task.save()
            return JsonResponse({
            'success': True,
            'status_display': task.get_status_display()
        })
@login_required

def add_task_comment(request):
      if request.method=='POST':
              task_id=request.POST.get('task_id')
              comment= request.POST.get('comment')
              task=Task.objects.get(id=task_id)
              TaskComment.objects.create(comment=comment,task=task,user=request.user,is_read=request.user.is_superuser)
              return JsonResponse({
                'success': True,
                
            })

@login_required
@admin_required

def admin_notification(request):
      unread_notifications_count=TaskComment.objects.filter(is_read=False).count()
      profile=request.user

       
      comments=TaskComment.objects.order_by('-created_at')
      TaskComment.objects.filter(is_read=False).update(is_read=True)
      return render(request,'admin_notification.html',{
            'comments':comments,
            'unread_notifications_count':unread_notifications_count,
            'profile':profile
      })
@login_required
@admin_required

def view_users(request):
      unread_notifications_count=TaskComment.objects.filter(is_read=False).count()

      users = User.objects.all().order_by('-id').exclude(is_superuser=True)

      return render(request,'view_users.html',{
            'users':users,
            'unread_notifications_count':unread_notifications_count
      })
from django.shortcuts import render, get_object_or_404
@login_required
@admin_required
def task_detail(request, task_id):
    unread_notifications_count=TaskComment.objects.filter(is_read=False).count()
    profile=request.user
    task = get_object_or_404(Task, id=task_id)

    return render(request, 'task_detail.html', {
        'task': task,
        'unread_notifications_count':unread_notifications_count,
        'profile':profile,
    })















from django.views.decorators.http import require_POST

@login_required
@require_POST
def mark_task_comments_read(request):
    task = get_object_or_404(
        Task, id=request.POST.get('task_id'), assigned_to=request.user
    )
    task.comments.filter(
        user__is_staff=True, is_read_by_assignee=False
    ).update(is_read_by_assignee=True)
    return JsonResponse({'success': True})