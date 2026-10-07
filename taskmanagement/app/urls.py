from django.urls import path
from . import views  

urlpatterns = [
    path('', views.home, name='home'),  
    path('registeration',views.registeration,name='registeration'),
    path('user_save',views.user_save,name='user_save'),
    path('login_page',views.login_page,name='login_page'),
    path('login_fun',views.login_fun,name='login_fun'),
    path('addtask',views.addtask,name='addtask'),
    path('task_save',views.task_save,name='task_save'),
    path('user_home',views.user_home,name='user_home'),
    path('viewtask',views.viewtask,name='viewtask'),
    path('delete_task',views.delete_task,name='delete_task'),
    path('task_update',views.task_update,name='task_update'),
    path('log_out',views.log_out,name='log_out'),
    #Api
    path('viewtaskapi',views.viewtaskapi,name='viewtaskapi'),
    path('task_saveapi',views.task_saveapi,name='task_saveapi'),
    path('task_updateapi',views.task_updateapi,name='task_updateapi'),
    path('delete_taskapi',views.delete_taskapi,name='delete_taskapi'),
]