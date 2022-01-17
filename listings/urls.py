from django.urls import path
from .import views


app_name ='listings'
urlpatterns =[
    
    # email_us 
    path('Email_us/',views.Email_us, name='Email_us'),
    
    # index
    path('', views.index, name='index'),
    
    # grade 
    path('grade_signup/',views.grade_signup, name='grade_signup'),
    path('grade_list/', views.grade_list, name='grade_list'),
    path('grade_list/detail/<slug:grade_slug>/',views.grade_detail, name='grade_detail'),
    path('grade_list/edit/<slug:grade_slug>/',views.grade_edit, name='grade_edit'),
    path('grade_list/delete_ask/<slug:grade_slug>/',views.grade_delete_ask, name='grade_delete_ask'),
    path('grade_list/delete/<slug:grade_slug>/',views.grade_delete, name='grade_delete'),
    # grade attendance students
    path('grade_attendance/<slug:grade_slug>/create/',views.grade_attendanc_create, name='grade_attendanc_create'),
    path('grades_dashboard/', views.grade_dashboard, name='grade_dashboard'),
    path('grade_attendance/<slug:grade_slug>/list/',views.attendance_list, name='attendance_list'),
    # path('grade_attendance/<slug:grade_slug>/',views.grade_attendanc, name='grade_attendanc'),
   
   # subject 
    path('subject_signup/',views.subject_signup, name='subject_signup'),
    path('subject_list/',views.subject_list, name='subject_list'),
    path('subject_list/detail/<slug:subject_slug>/',views.subject_detail, name='subject_detail'),
    path('subject_list/edit/<slug:subject_slug>/',views.subject_edit, name='subject_edit'),
    path('subject_list/delete_ask/<slug:subject_slug>/',views.subject_delete_ask, name='subject_delete_ask'),
    path('subject_list/delete/<slug:subject_slug>/',views.subject_delete, name='subject_delete'),
    path('subject_grade_dashboard/', views.subject_grade_dashboard, name='subject_grade_dashboard'),
    path('subject_mark_student_list/<slug:grade_slug>/<slug:subject_slug>/', views.subject_mark_student_list,
         name='subject_mark_student_list'),
    path('subject_mark_student_detail/<slug:grade_slug>/<slug:subject_slug>/<str:student_username>/', views.subject_mark_student_detail,
         name='subject_mark_student_detail'),

    # mark
    path('student_list/detail/<str:student_username>/<slug:subject_slug>/mark_add/',views.mark_create, name='mark_create'),
    path('student_list/detail/<str:student_username>/<slug:subject_slug>/<int:mark_id>/mark_edit/',views.mark_edit, name='mark_edit'),
    # path('mark/<str:student_username>/create/',views.mark_student_create, name="mark_student_create"),

    # user
    path('user_list/', views.user_list,name='user_list'),
    
    # school admin
    path('schadmin_list/',views.schadmin_list,name='schadmin_list'),
    path('schadmin_list/detail/<str:schadmin_username>/',views.schadmin_detail, name='schadmin_detail'),
    
    # teacher
    path('teacher_list/',views.teacher_list,name='teacher_list'),
    path('teacher_list/detail/<str:teacher_username>/',views.teacher_detail, name='teacher_detail'),
  
    # student
    path('student_list/',views.student_list,name='student_list'),
    path('student_list/detail/<str:student_username>/',views.student_detail, name='student_detail'),
    path('student_list/detail/<str:student_username>/<slug:subject_slug>/mark/',views.student_subject_mark_detail, name='student_subject_mark_detail'),
   
    path('student_list/detail/<str:student_username>/marks',views.student_detail_marks, name='student_detail_marks'),
    path('student_list/detail/<str:student_username>/attendance',views.student_detail_attendance, name='student_detail_attendance'),
    path('student_list/detail/<str:student_username>/messages',
         views.student_detail_messages, name='student_detail_messages'),
    
    # parent
    path('parent_list/', views.parent_list, name='parent_list'),
    path('parent_list/detail/<str:parent_username>/',views.parent_detail, name='parent_detail'),
    
    # charts
    path('charts_all/', views.charts_all, name='charts_all'),
 
]
