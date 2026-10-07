from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render,redirect
from django.contrib import messages



# Create your views here.
def home(request):
    return render(request,'home.html')
def registeration(request):
    return render(request,'registeration.html')
def user_save(request):
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
        user=User.objects.create_user(password=password,username=email,email=email)
        
        Registeration.objects.create(
            user=user,
                name=name,address=address,phone=phone,email=email
            )
        return JsonResponse({
          
                    'success':True,   
                    'message':'User Added successfully'               
                   

    })
def login_page(request):
    return render(request,'login_page.html')

def login_fun(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)

            return redirect('user_home')
            
        else:
            messages.info(request,"Invalid username or password...")
            return redirect('login_page')
def addtask(request):
    return render(request,'addtask.html')
def task_save(request):
    if request.method=='POST':
            name=request.POST.get('name')
            description= request.POST.get('des')
            priority= request.POST.get('priority')
            status= request.POST.get('status')
           
            enddate=request.POST.get('enddate')
            
            Task.objects.create(
                user=request.user,
                    title=name,description=description,priority=priority,status=status,
                    due_date=enddate
                    

                )
            return JsonResponse({
              
                        'success':True,   
                        'message':'Task Added successfully'               
                       
    
        })
def user_home(request):
    profile=Registeration.objects.get(user=request.user)
    return render(request,'user_home.html',{
          'profile':profile
    })

def viewtask(request):
    task=Task.objects.filter(user=request.user)
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
        'task':task
    })

def delete_task(request):
    id=request.POST.get('id')
    task=Task.objects.get(id=id)
    task.delete()
    return JsonResponse({
        'success':True
    })


def task_update(request):
    if request.method=='POST':
            id=request.POST.get('id')
            name=request.POST.get('name')
            description= request.POST.get('des')
            priority= request.POST.get('priority')
            status= request.POST.get('status')
           
            enddate=request.POST.get('enddate')
            task=Task.objects.get(id=id)
            task.title=name
            task.description=description
            task.priority=priority
            task.status=status
            task.due_date=enddate
            task.save()
            
            return JsonResponse({
              
                        'success':True,   
                        'message':'Task Updated successfully'               
                       
    
        })

def log_out(request):
    logout(request)
    return redirect('login_page')


from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializer import TaskSerializer
@api_view(['GET'])
def viewtaskapi(request):
    task=Task.objects.filter(user=request.user)
    search=request.GET.get('search')
    priority=request.GET.get('priority')
    status=request.GET.get('status')
    if  search: 
          task=task.filter(title__icontains=search)
    if priority:
          task=task.filter(priority=priority)
    if status:
              task=task.filter(status=status)
          


    serailizer=TaskSerializer(task,many=True) 
    return Response(serailizer.data)
@api_view(['POST'])

def task_saveapi(request):
            name=request.data.get('name')
            description= request.data.get('des')
            priority= request.data.get('priority')
            status= request.data.get('status')
           
            enddate=request.data.get('enddate')
            
            task=Task.objects.create(
                user=request.user,
                    title=name,description=description,priority=priority,status=status,
                    due_date=enddate
                    

                )
            serailizer=TaskSerializer(task) 
            return Response(serailizer.data, status=201)
@api_view(['PUT'])

def task_updateapi(request):
            id=request.data.get('id')
            name=request.data.get('name')
            description= request.data.get('des')
            priority= request.data.get('priority')
            status= request.data.get('status')
           
            enddate=request.data.get('enddate')
            task=Task.objects.get(id=id)
            task.title=name
            task.description=description
            task.priority=priority
            task.status=status
            task.due_date=enddate
            task.save()
            serailizer=TaskSerializer(task) 
            return Response(serailizer.data, status=200)
@api_view(['DELETE'])
           
def delete_taskapi(request):
    id=request.data.get('id')
    task=Task.objects.get(id=id)
    task.delete()
    return Response({
          
           'success':True,
                 'message': 'Task deleted successfully'

       },status=200)
   
