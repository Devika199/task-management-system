from django.urls import path
from . import views  

urlpatterns = [
    path('', views.home, name='home'),  
    path('signup_page/',views.signup_page,name='signup_page'),
    path('register_user/',views.register_user,name='register_user'),
    path('check_phone/',views.check_phone,name='check_phone'),
    path('check_email/',views.check_email,name='check_email'),
    path('admin_home/',views.admin_home,name='admin_home'),
    path('login_page',views.login_page,name='login_page'),
    path('login_fun',views.login_fun,name='login_fun'),
    path('addtask',views.addtask,name='addtask'),
    path('task_save',views.task_save,name='task_save'),
    path('user_home',views.user_home,name='user_home'),
    path('user_tasks/',views.user_tasks,name='user_tasks'),
    path('update_task_status',views.update_task_status,name='update_task_status'),
    path('add_task_comment/',views.add_task_comment,name='add_task_comment'),
    path('admin_notification/',views.admin_notification,name='admin_notification'),
    path('view_users/',views.view_users,name='view_users'),
    path('viewtask',views.viewtask,name='viewtask'),
    path('delete_task',views.delete_task,name='delete_task'),
    path('task_update',views.task_update,name='task_update'),
    path('log_out',views.log_out,name='log_out'),
    path('task-detail/<int:task_id>/', views.task_detail,name='task_detail'),
    path('mark_task_comments_read/', views.mark_task_comments_read, name='mark_task_comments_read'),
]