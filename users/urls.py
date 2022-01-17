from django.urls import path
from.import views


app_name = 'users'
urlpatterns = [
    # login
    path('login/', views.login_user, name='login_user'),
    # logout
    path('logout/', views.logout_user, name='logout_user'),
    # profile
    path('profile/',views.profile,name='profile'),
    # image update
    path('image_update/<str:user_username>/',views.image_user_update, name='image_user_update'),
    
    # main dashboard
    path('main_dashboard/', views.main_dashboard, name='main_dashboard'),

    # webadmin 
    path('webadmin_profile/', views.webadmin_profile, name='webadmin_profile'),
    path('webadmin_dashboard/<str:webadmin_username>/',views.webadmin_dashboard, name='webadmin_dashboard'),

    # Academic Year
    path('academicyear_add/', views.academicyear_add, name='academicyear_add'),
    path('academicyear_edit/<str:year_name>/',views.academicyear_edit, name='academicyear_edit'),
    path('academicyear_delete/<str:year_name>/',views.academicyear_delete, name='academicyear_delete'),
   

    # schooladmin
    path('schadmin_profile/', views.schadmin_profile, name='schadmin_profile'),
    path('schadmin_dashboard/<str:schadmin_username>/',views.schadmin_dashboard, name='schadmin_dashboard'),
    path('schooladmin_signup/', views.schadmin_signup, name='schadmin_signup'),
    path('schooladmin_list/<str:schadmin_username>/edit',views.schadmin_edit, name='schadmin_edit'),
    path('schooladmin_list/<str:schadmin_username>/delete_ask/',views.schadmin_delete_ask, name='schadmin_delete_ask'),
    path('schooladmin_list/<str:schadmin_username>/delete',views.schadmin_delete, name='schadmin_delete'),

    # teacher
    path('teacher_profile/', views.teacher_profile, name='teacher_profile'),
    path('teacher_dashboard/<str:teacher_username>/', views.teacher_dashboard,name='teacher_dashboard'),
    path('teacher_signup/', views.teacher_signup, name='teacher_signup'),
    path('teacher_list/<str:teacher_username>/edit',views.teacher_edit, name='teacher_edit'),
    path('teacher_list/<str:teacher_username>/delete_ask',views.teacher_delete_ask, name='teacher_delete_ask'),
    path('teacher_list/<str:teacher_username>/delete',views.teacher_delete, name='teacher_delete'),
    path('teacher_smessage/<str:student_username>/',views.message_t_student_send, name='message_t_student'),
    path('teacher_gmessage/<slug:grade_slug>/',views.message_t_grade_send, name='message_t_grade'),
    
    # student
    path('student_profile/', views.student_profile, name='student_profile'),
    path('student_dashboard/<str:student_username>/',views.student_dashboard, name='student_dashboard'),
    path('student_signup/', views.student_signup, name='student_signup'),
    path('student_list/<str:student_username>/edit',views.student_edit, name='student_edit'),
    path('student_list/<str:student_username>/delete_ask',views.student_delete_ask, name='student_delete_ask'),
    path('student_list/<str:student_username>/delete',views.student_delete, name='student_delete'),
    
    
    # parent
    path('parent_profile/', views.parent_profile, name='parent_profile'),
    
    path('parent_student_dashboard/<str:student_username>/',
         views.parent_student_dashboard, name='parent_student_dashboard'),
    path('parent_children/<str:parent_username>/',views.parent_children, name='parent_children'),
    path('parent_signup/', views.parent_signup, name='parent_signup'),
    
    path('parent_list/<str:parent_username>/edit',views.parent_edit, name='parent_edit'),
    path('parent_list/<str:parent_username>/delete_ask',views.parent_delete_ask, name='parent_delete_ask'),
    path('parent_list/<str:parent_username>/delete',views.parent_delete, name='parent_delete'),

    
    
   
]
