from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.forms.models import inlineformset_factory
from .forms import AcademicYearForm, LoginForm, ImageUserForm, SchoolAdminUserCreateForm, SchoolAdminUserExtentionCreateForm, TeacherUserCreateForm, StudentUserCreateForm, ParentUserCreateForm, MessageTeacherToStudentForm, MessageTeacherToGradeForm
from django.shortcuts import get_object_or_404, redirect, render
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import ImageUser, Teacher, Student, Parent, Employee, SchoolAdmin
import uuid
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from listings.models import Grade,Subject
from django.shortcuts import get_object_or_404
from .models import AcademicYear
from django.forms import inlineformset_factory

#####################################################################################################
############################### AcademicYear ##############################################################
######################################################################################################

'''permission only by webadmin'''
############## AcademicYear add #######################################################33
@login_required(login_url='users:login_user')
def academicyear_add(request):
    academicyear_form = AcademicYearForm()
    if request.user.is_superuser :
        # give permission for webadmin only
        academicyear = AcademicYear.objects.all()
        if not academicyear :
                ## add academic year
                if request.method == 'POST':
                    academicyear_form = AcademicYearForm(request.POST)
                    if academicyear_form.is_valid(): 
                        new_academicyear = academicyear_form.save(commit=False)
                        new_academicyear.is_done = True
                        new_academicyear.save()
                
                        messages.success(request,"New AcademicYear created successfully !")
                        return redirect('users:webadmin_dashboard', webadmin_username=request.user.username)
            

    else:
        messages.warning(request, "Sorry, page authentication not allowed for you !")
        return redirect('users:main_dashboard')
        
    context = {
        'form_y': academicyear_form,
        'title': 'Academic Year Add',
        'sub_title': 'Academic Year Create',
        
            
        }
    return render(request,'users/academicyear_add.html', context)



##permission only by webadmin
############## AcademicYear edit #######################################################33
@login_required(login_url='users:login_user')
def academicyear_edit(request,year_name):
    # give permission for webadmin only
    if not request.user.is_superuser:
        messages.warning(request, "Sorry, page authentication not allowed for you !")
        return redirect('users:main_dashboard')
 
    else:
        ## edit academic year by superuser 
        academicyear = get_object_or_404(AcademicYear,name=year_name)
        academicyear_form = AcademicYearForm(instance=academicyear)
        if request.method == 'POST':
            print('before valid request.posy=', request.POST)
            academicyear_form = AcademicYearForm(request.POST,instance=academicyear)
            
            if academicyear_form.is_valid():
                print('after valid request.posy=',request.POST)
                edited_form = academicyear_form.save() 
                print('cleaned start_date=', academicyear_form.cleaned_data.get('start_date'))
                print(' cleaned end_date=', academicyear_form.cleaned_data.get('end_date'))
                
                print('post is_done=', request.POST.get('is_done'))

                is_done = academicyear_form.cleaned_data.get('is_done')
                print('clean is_done=', is_done)
                
                messages.success(request,"AcademicYear edit successfully !")
                return redirect('users:webadmin_dashboard', webadmin_username=request.user.username)


    context = {
        'form_y': academicyear_form,
        'title': 'Academic Year Edit',
        'sub_title': 'Academic Year Edit',
    }
    return render(request, 'users/academicyear_edit.html', context)




'''permission only to web admin '''
#################################### academicyear_delete ###############################333
def academicyear_delete(request, year_name):
    # give permission for webadmin only
    if request.user.is_superuser:
        academicyear = get_object_or_404(AcademicYear, name=year_name)
        academicyear.delete()
        messages.success(request, "delete done successfully!")
        return redirect('users:academicyear_add')

    else:
        messages.warning(request, "Sorry, page authentication not allowed for you !")
        return redirect('users:main_dashboard')


''' No need permission'''
########################  login_user  #####################################
def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        # print(form)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if User.objects.all().filter(username=username).filter(is_active=True).exists():
                
                    login(request, user)
                    return redirect('users:main_dashboard')
                    
                    ################this way is also work ok ###################3
                    # if username.startswith('TT'):
                    #     messages.success(request, 'Welcome Teacher {} you are successfully login'.format(request.user.first_name))
                    #     return redirect('users:teacher_dashboard',teacher_username=request.user.username)
                        
                    
                    # elif username.startswith('ST'):
                    #     messages.success(request, 'Welcome Student {} you are successfully login'.format(
                    #         request.user.first_name))
                    #     return redirect('users:student_dashboard', student_username=request.user.username)

                    # elif username.startswith('PT'):
                    #     messages.success(request, 'Welcome Parent {} you are successfully login'.format(
                    #         request.user.first_name))
                    #     return redirect('users:parent_children', parent_username=request.user.username)


                    # elif username.startswith('ET'):
                    #     messages.success(request, 'Welcome Employee {} you are successfully login'.format(
                    #         request.user.first_name))
                    #     return redirect('users:employee_dashboard', employee_username=request.user.username)


                    # # here the user is webadmin
                    # elif request.user.is_superuser:
                    #     messages.success(request, 'Welcome Web Admin {} you are successfully login'.format(request.user.first_name))
                    #     return redirect('users:webadmin_dashboard',webadmin_username=request.user.username)
                    
                    # else:            
                    #     messages.success(request, 'Welcome School Admin {} you are successfully login'.format(
                    #         request.user.first_name))
                    #     return redirect('users:schadmin_dashboard', schadmin_username=request.user.username)
                        
                   
            else:
                form = LoginForm()
                messages.warning(request,'Please check your username and password')
                return redirect('users:login_user')
    
    else:
        form = LoginForm()
    
    
    context = {
        'form': form,
    }
    return render(request, 'users/login.html', context)




'''pemission any request user'''
####################### logout_user ####################################3
@login_required(login_url='users:login_user')
def logout_user(request):
    logout(request)
    return redirect('listings:index')


################################################################################################
########################################## profile #############################################
################################################################################################
'''pemission any request user'''
@login_required(login_url='users:login_user')
def image_user_update(request,user_username):
    user = get_object_or_404(User, username=user_username)
    old_image = get_object_or_404(ImageUser, user=user)
    image_user_form = ImageUserForm(instance=old_image)
    
    if request.method == 'POST':
        image_user_form = ImageUserForm(request.POST, request.FILES, instance=old_image)
        if image_user_form.is_valid():
            updated_image = image_user_form.save(commit=False)
            updated_image.user = user
            updated_image.save()
            messages.success(request, 'image update done')
            return redirect('users:profile')

    context = {
        'user' : request.user,
        'image_user_form': image_user_form,
        'title': 'User Profile',
        'sub_title': 'Update User Image',
    }
    return render(request, 'users/image_user_update.html', context)


'''pemission any request user'''
################### profile ##############################
@login_required(login_url='users:login_user')
def profile(request):
    username_value = str(request.user.username)
    print(username_value)

    if username_value.startswith('ST'):
        return redirect('users:student_profile')

    elif username_value.startswith('TT'):
        return redirect('users:teacher_profile')

    elif username_value.startswith('PT'):
        return redirect('users:parent_profile')

    elif request.user.is_superuser :
        return redirect('users:webadmin_profile')
   
    else :
        return redirect('users:schadmin_profile')



'''pemission webadmin only'''
######################## webadmin_profile  #####################################
@login_required(login_url='users:login_user')
def webadmin_profile(request):
    context = {   
        'title': '',
        'sub_title': 'web admin Profile',
    }
    return render(request, 'users/webadmin_profile.html', context)


'''pemission schooladmin only'''
######################## schadmin_profile  #####################################
@login_required(login_url='users:login_user')
def schadmin_profile(request):
    user= request.user
    schadmin = get_object_or_404(SchoolAdmin, user=user)
    context = {
     
        'schadmin': schadmin,
        'title': 'School Admin Profile',
        'sub_title': '',
    }
    return render(request, 'users/schadmin_profile.html', context)


'''pemission teacher only'''
######################## teacher_profile  #####################################
@login_required(login_url='users:login_user')
def teacher_profile(request):
    user = request.user
    teacher = get_object_or_404(Teacher, user=user)
    grades_for_teacher = teacher.grades.all()
    subjects_for_teacher = teacher.subjects.all()
    # teacher_grades_subjects = Teacher.objects.all().filter(grades=grades_for_teacher).filter(subjects=subjects_for_teacher)
    context = {
        'user': user,
        'grades_for_teacher': grades_for_teacher,
        'subjects_for_teacher': subjects_for_teacher,
        # 'teacher_grades_subjects': teacher_grades_subjects,
        'title': 'Teacher Profile',
        'sub_title': '',

    }
    return render(request, 'users/teacher_profile.html', context)



'''pemission student only'''
######################## student_profile  #####################################
@login_required(login_url='users:login_user')
def student_profile(request):
    user = request.user
    student= get_object_or_404(Student,user=user)
    grade_for_student = student.grade
    subjects_for_student = Subject.objects.all().filter(grade=grade_for_student)
    parent_for_student = Parent.objects.all().filter(students=student)
    
    # teacher_grades_subjects = Teacher.objects.all().filter(grades=grades_for_teacher).filter(subjects=subjects_for_teacher)
    context = {
        'user': user,
        'grade_for_student': grade_for_student,
        'subjects_for_student': subjects_for_student,
        # 'teacher_grades_subjects': teacher_grades_subjects,
        'title': 'Student Profile',
        'sub_title': '',
        'parent_for_student':parent_for_student,
    }
    return render(request, 'users/student_profile.html', context)



'''pemission parent only'''
######################## parent_profile  #####################################
@login_required(login_url='users:login_user')
def parent_profile(request):
    user = request.user
    parent = get_object_or_404(Parent, user=user)
    students_for_parent = parent.students.all()
   
    # teacher_grades_subjects = Teacher.objects.all().filter(grades=grades_for_teacher).filter(subjects=subjects_for_teacher)
    context = {
        'user': user,
        'parent' :parent,
        'students_for_parent': students_for_parent,
        'title': 'Parent Profile',
        'sub_title': '',

        
    }
    return render(request, 'users/parent_profile.html', context)


################################################################################################
############################### dashboard #####################################################
################################################################################################
""" no authentication """
def main_dashboard(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('users:webadmin_dashboard',webadmin_username=request.user.username)

        elif SchoolAdmin.objects.all().filter(is_active=True).filter(user=request.user).exists():
            return redirect('users:schadmin_dashboard', schadmin_username=request.user.username)
            
        elif Teacher.objects.all().filter(is_active=True).filter(user=request.user).exists():
            return redirect('users:teacher_dashboard', teacher_username=request.user.username)

        elif Student.objects.all().filter(is_active=True).filter(user=request.user).exists():
            return redirect('users:student_dashboard', student_username=request.user.username)

        elif Parent.objects.all().filter(is_active=True).filter(user=request.user).exists():
            return redirect('users:parent_children', parent_username=request.user.username)
  
    
    else:
        return redirect('listings:index')




'''pemission shooladmin only'''
######################## schadmin_pdashboard  #####################################
@login_required(login_url='users:login_user')
def schadmin_dashboard(request,schadmin_username):
    # give permission to school admin only
    if SchoolAdmin.objects.all().filter(is_active=True).filter(user=request.user).exists():
        auther = request.user
        print('yes it is school admin')
        
        schadmin = get_object_or_404(SchoolAdmin, user=request.user)
        user=request.user

        academicyear = None 
        academicyear = AcademicYear.objects.all().order_by('-end_date')[:1]
        if academicyear:
            academicyear = academicyear
    
        all_schadmins = SchoolAdmin.objects.all().filter(is_active=True)
        all_teachers = Teacher.objects.all().filter(is_active=True)
        all_students = Student.objects.all().filter(is_active=True)
        all_parents = Parent.objects.all().filter(is_active=True)
        # all_employees = Employee.objects.all()
        all_grades = Grade.objects.all()
        all_subjects = Subject.objects.all()
        

        # pagination for schooladmin tabel 
        paginator = Paginator(all_schadmins, 5)
        page = request.GET.get('page')

        try:
            schadmins = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver the first page
            schadmins = paginator.page(1)
        except EmptyPage:
            # If page is out of range deliver last page of results
            schadmins = paginator.page(paginator.num_pages)

        title = 'School Admin Dashboard'

        context = {
           
            'academicyear' : academicyear,
            'title': title,
            'schadmins': schadmins,
            'page': page,

            'all_teachers': all_teachers,
            'all_students': all_students,
            'all_parents':  all_parents,
            # 'all_employees': all_employees,
            'all_grades' : all_grades,
            'all_subjects' : all_subjects,
        }
        return render(request, 'users/schadmin_dashboard.html', context)
    
    else:
        messages.warning(request, "Sorry, page authentication not allowed for you !")
        return redirect('users:main_dashboard')


'''pemission webadmin only'''
######################## webadmin_dashboard  #####################################
@login_required(login_url='users:login_user')
def webadmin_dashboard(request,webadmin_username):
    # give permission for webadmin only
    webadmin = get_object_or_404(User, username=webadmin_username)
    if  not request.user.is_superuser and not request.user == webadmin:
        messages.warning( request, "Sorry, page authentication not allowed for you !")
        return redirect('users:main_dashboard')

    else :
        academicyear = None
        all_users = User.objects.all()
        all_schadmins = SchoolAdmin.objects.all()
        all_teachers = Teacher.objects.all()
        all_students = Student.objects.all()
        all_parents = Parent.objects.all()
        all_employees = Employee.objects.all()
        academicyear = AcademicYear.objects.all()
        if academicyear:
            academicyear = academicyear.first()

    context = {
        'title':'Web Admin Dashboard',
        'all_users': all_users,
        'academicyear': academicyear,
        'all_schadmins': all_schadmins,
        'all_teachers': all_teachers,
        'all_students': all_students,
        'all_parents':  all_parents,
        'all_employees': all_employees,
    }
    return render(request, 'users/webadmin_dashboard.html', context)
    


'''pemission teacher only'''
######################## teacher_pdashboard  #####################################
@login_required(login_url='users:login_user')
def teacher_dashboard(request,teacher_username):
    # give permission to teacher only
    if Teacher.objects.all().filter(is_active=True).filter(user=request.user).exists():
        auther = request.user
        print('yes it is Teacher')
    
        
        title = 'Teacher Dashboard'
        all_users = User.objects.all()
        all_schadmins = SchoolAdmin.objects.all()
        all_teachers = Teacher.objects.all()
        all_students = Student.objects.all()
        all_parents = Parent.objects.all()
        all_employees = Employee.objects.all()

        academicyear = None 
        academicyear = AcademicYear.objects.all()
        if academicyear:
            academicyear = academicyear.first()

    else:
        messages.warning(request, "Sorry, page authentication not allowed for you !")
        return redirect('users:main_dashboard')


    context = {
        'title': title,
        'all_users': all_users,
        'all_schadmins': all_schadmins,
        'all_teachers': all_teachers,
        'all_students': all_students,
        'all_parents':  all_parents,
        'all_employees': all_employees,
        'academicyear' : academicyear,
    }
    return render(request, 'users/teacher_dashboard.html', context)



'''only teacher cand send message to student'''
 ##############################################
@login_required(login_url='users:login_user')
def message_t_student_send(request, student_username):
    # give permission to teacher only
    if Teacher.objects.all().filter(is_active=True).filter(user=request.user).exists():
        print('yes it is Teacher')

        student = get_object_or_404(Student, given_username=student_username)
        message_t_sudent_form = MessageTeacherToStudentForm()
        if request.method == 'POST':
            message_t_sudent_form = MessageTeacherToStudentForm(request.POST)
            if message_t_sudent_form.is_valid():
               new_message = message_t_sudent_form.save(commit = False)
               
               teacher = get_object_or_404(Teacher,user=request.user)
               new_message.teacher = teacher
               
               
               new_message.student = student
               
               new_message.save()
               messages.success(request, f'Message sent to  {student.get_student_full_name}  successfully !')
               return redirect('listings:student_list')


    else:
        messages.warning(request, "Sorry, page authentication not allowed for you !")
        return redirect('users:main_dashboard')
    

    context = {
        'title': 'to student',
        'student': student,
        'message_form' : message_t_sudent_form,
        'student': student,
    }
    return render(request,'users/message_t_student.html',context)
 ###############################################


'''only teacher cand send message to grade'''
##############################################
@login_required(login_url='users:login_user')
def message_t_grade_send(request, grade_slug):
    # give permission to teacher only
    if Teacher.objects.all().filter(is_active=True).filter(user=request.user).exists():
        print('yes it is Teacher')

        grade = get_object_or_404(Grade, slug=grade_slug)
        message_t_grade_form = MessageTeacherToGradeForm()
        if request.method == 'POST':
            message_t_grade_form = MessageTeacherToGradeForm(request.POST)
            if message_t_grade_form.is_valid():
               new_message = message_t_grade_form.save(commit=False)

               teacher = get_object_or_404(Teacher, user=request.user)
               new_message.teacher = teacher

               new_message.grade = grade

               new_message.save()
               messages.success(request, f'Message sent to  {grade.name}  successfully !')
               return redirect('listings:grade_list')

    else:
        messages.warning(request, "Sorry, page authentication not allowed for you !")
        return redirect('users:main_dashboard')
    

    context = {
        'title': 'to grade',
        'student': grade,
        'message_form': message_t_grade_form,
        'grade': grade,
    }
    return render(request, 'users/message_t_grade.html', context)
 ###############################################




'''pemission student only'''
######################## student_pdashboard  #####################################
@login_required(login_url='users:login_user')
def student_dashboard(request,student_username):
    # give permission to student only
    if Student.objects.all().filter(is_active=True).filter(user=request.user).exists():
        auther = request.user
        print('yes it is Student')

        user = request.user 
        student = get_object_or_404(Student,user=user)
        if student :
            student_username = student.given_username
            grade = student.grade

    else:
        messages.warning(request, "Sorry, page authentication not allowed for you !")
        return redirect('users:main_dashboard')

    academicyear = None 
    academicyear = AcademicYear.objects.all()
    if academicyear:
        academicyear = academicyear.first()
    
    context = {
        'student':student,
        'student_username' : student_username,
        'academicyear' : academicyear,
    }
    return render(request, 'users/student_dashboard.html', context)





'''pemission parent only'''
######################## student_pdashboard  #####################################
@login_required(login_url='users:login_user')
def parent_student_dashboard(request,student_username):
    # give permission to student only
    if Parent.objects.all().filter(is_active=True).filter(user=request.user).exists():
        auther = request.user
        print('yes it is parent')

        user = request.user 
        parent = get_object_or_404(Parent, user=user)
        student = get_object_or_404(Student,given_username=student_username)
        if parent:
            parent_username = parent.given_username
           
            
        academicyear = None 
        academicyear = AcademicYear.objects.all()
        if academicyear:
            academicyear = academicyear.first()

    else:
        messages.warning(request, "Sorry, page authentication not allowed for you !")
        return redirect('users:main_dashboard')


    context = {
        'student': student,
        'parent':parent,
        'parent_username': parent_username,
        'academicyear' :  academicyear,

    }
    return render(request, 'users/parent_student_dashboard.html', context)




'''pemission parent only'''
######################## student_pdashboard  #####################################
@login_required(login_url='users:login_user')
def parent_children(request, parent_username):
    # give permission to student only
    if Parent.objects.all().filter(is_active=True).filter(user=request.user).exists():
        auther = request.user
        print('yes it is parent')

        user = request.user
        parent = get_object_or_404(Parent, user=user)
        parent_username = parent.given_username


    else:
        messages.warning(request, "Sorry, page authentication not allowed for you !")
        return redirect('users:main_dashboard')


    academicyear = None
    academicyear = AcademicYear.objects.all()
    if academicyear:
        academicyear = academicyear.first()


    context = {
    'academicyear': academicyear,
    'parent': parent,
    'parent_username': parent_username,

    }
    return render(request, 'users/parent_children.html', context)




################################################################################################
################################## schooladmin ####################################################
################################################################################################
'''pemission webadmin only'''
'''Note : schooladmin only created by superuser'''
######################## schooladmin_signup #########################################
@login_required(login_url='users:login_user')
def schadmin_signup(request):
    # give permission for webadmin only
    auther = request.user
    schadmin_user_form = SchoolAdminUserCreateForm()
    schadmin_ext_form = SchoolAdminUserExtentionCreateForm()
    image_user_form = ImageUserForm()
    if request.user.is_superuser:
        if request.method == 'POST':
            schadmin_user_form = SchoolAdminUserCreateForm(request.POST)
            schadmin_ext_form = SchoolAdminUserExtentionCreateForm(request.POST)
            image_user_form = ImageUserForm(request.POST, request.FILES)
               
            if schadmin_user_form.is_valid() and schadmin_ext_form.is_valid() and image_user_form.is_valid():
                username = schadmin_user_form.cleaned_data.get('username')
                email = schadmin_ext_form.cleaned_data.get('email')
                first_name = schadmin_ext_form.cleaned_data.get('first_name')
                last_name = schadmin_ext_form.cleaned_data.get('last_name')
                is_active = schadmin_ext_form.cleaned_data.get('is_active')
                is_superuser = schadmin_ext_form.cleaned_data.get('is_superuser') 
                is_staff = schadmin_ext_form.cleaned_data.get('is_staff')
                
                user = schadmin_user_form.save(commit=False)
                user.username = username
                user.email = email
                user.first_name = first_name
                user.last_name = last_name
                user.is_active = is_active
                user.is_superuser = is_superuser
                user.is_staff = is_staff
                user.save()
                
                schadmin_ext = schadmin_ext_form.save(commit=False)
                schadmin_ext.user = user
                schadmin_ext.created_by = auther
                schadmin_ext.save()

                # https://docs.djangoproject.com/en/3.2/topics/forms/modelforms/#the-save-method
                    # save data in many to many fields(grades,subjects)_Calling save_m2m() is only required if you use save(commit=False)
                schadmin_ext_form.save_m2m()

                image_user = image_user_form.save(commit=False)
                image_user.user = user 
                image_user.save()
                
                messages.success( request, "New School Admin created successfully !")
                return redirect('listings:schadmin_list')
    
    else:
        messages.warning( request, "Sorry, add new School Admin not allowed for you !")
        return redirect('users:main_dashboard')


    context = {
        'form1' : schadmin_user_form ,
        'form2': schadmin_ext_form,
        'form3':image_user_form,
        'title': 'Sign Up',
        'sub_title': 'School Admin Create',
    }
    return render(request, 'users/schadmin_signup.html', context)



'''pemission webamin only'''
''' Note : schooladmin only updated by superuser'''
######################## schooladmin_edit #########################################
@login_required(login_url='users:login_user')
def schadmin_edit(request, schadmin_username):
    # give permission for webadmin only
    if request.user.is_superuser:
        auther = request.user
        user = get_object_or_404(User, username=schadmin_username)
        schadmin = get_object_or_404(SchoolAdmin,user=user)
        schadmin_ext_form = SchoolAdminUserExtentionCreateForm(instance=schadmin)
        if request.method == 'POST':
            schadmin_ext_form = SchoolAdminUserExtentionCreateForm(request.POST, request.FILES,instance=schadmin)
               
            if  schadmin_ext_form.is_valid():
                email = schadmin_ext_form.cleaned_data.get('email')
                first_name = schadmin_ext_form.cleaned_data.get('first_name')
                last_name = schadmin_ext_form.cleaned_data.get('last_name')
                is_active = schadmin_ext_form.cleaned_data.get('is_active')
                is_superuser = schadmin_ext_form.cleaned_data.get('is_superuser')
                is_staff = schadmin_ext_form.cleaned_data.get('is_staff')
                  
                user.email = email
                user.first_name = first_name
                user.last_name = last_name
                user.is_active = is_active
                user.is_superuser = is_superuser
                user.is_staff = is_staff
                user.save()
               
                schadmin_ext = schadmin_ext_form.save(commit=False)
                schadmin_ext.user = user

                schadmin_ext.updated_by = auther

                # https://docs.djangoproject.com/en/3.2/topics/forms/modelforms/#the-save-method
                # save data in many to many fields(grades,subjects)_Calling save_m2m() is only required if you use save(commit=False)
                schadmin_ext_form.save_m2m()

                
                schadmin_ext.save()
                messages.success(request, "Edit done successfully !")
                return redirect('listings:schadmin_list')
   
    else:
        messages.warning(request, "Sorry,edit School Admin not allowed for you !")
        return redirect('users:main_dashboard')

    context = {
        'title': 'Edit',
        'sub_title': 'School Admin Edit',
        'form2': schadmin_ext_form,
    }
    return render(request, 'users/schadmin_edit.html', context)




'''pemission webadmin only'''
'''Note : schooladmin only delete by superuser'''
####################### schadmin_delete_ask #########################################
@login_required(login_url='users:login_user')
def schadmin_delete_ask(request, schadmin_username):
    # give permission for webadmin only
    if request.user.is_superuser:
        user = get_object_or_404(User, username=schadmin_username)
        schadmin = get_object_or_404(SchoolAdmin, user=user)
        

    
    else:
        messages.warning(request,"Sorry, delete School Admin register not allowed for you !") 
        return redirect('users:main_dashboard')


    context = {
            'schadmin': schadmin,
        }
    return render(request, 'users/schadmin_delete_ask.html', context)




'''pemission webadmin only'''
'''Note : schooladmin only delete by admin(superuser)'''
####################### schadmin_delete #########################################
@login_required(login_url='users:login_user')
def schadmin_delete(request, schadmin_username):
    # give permission for webadmin only
    if request.user.is_superuser:
        user = get_object_or_404(User, username=schadmin_username)
        schadmin = get_object_or_404(SchoolAdmin, user=user)
        schadmin.delete()
        image = get_object_or_404(ImageUser,user=user)
        image.delete()
        user.delete()
        messages.success(request,"delete done successfully!") 
        return redirect('listings:schadmin_list')

    else:
        messages.warning(request, "Sorry, delete School Admin register not allowed for you !")
        return redirect('users:main_dashboard')









################################################################################################
################################### teacher ####################################################
################################################################################################
'''pemission SchoolAdmin only'''
'''Note : created by SchoolAdmin objects'''
####################### teacher_signup #########################################
@login_required(login_url='users:login_user')
def teacher_signup(request):
    # give permission to school admin only
    if SchoolAdmin.objects.all().filter(is_active=True).filter(user=request.user).exists():
        auther = request.user
        print('yes it is school admin')
        
        teacher_form = TeacherUserCreateForm()
        image_user_form = ImageUserForm()
        
        if request.method == 'POST':
            teacher_form = TeacherUserCreateForm(request.POST)
            image_user_form = ImageUserForm(request.POST,request.FILES)
            
            if teacher_form.is_valid() and image_user_form.is_valid():
                new_teacher = teacher_form.save(commit=False)
                
                is_user_done = teacher_form.cleaned_data.get('is_user_done')
                print('is_user_done=', is_user_done)
                
                if is_user_done == None :
                    given_username = 'TT_' + str(uuid.uuid4().hex[:8])
                    given_password = uuid.uuid4().hex[:8]
                    user = User.objects.create_user(username=given_username, password=given_password)
                    
                    # add new data in User model and save
                    user.username = given_username
                    
                    user.set_password = given_password
                    
                    first_name = teacher_form.cleaned_data.get('first_name')
                    user.first_name = first_name
                    
                    last_name = teacher_form.cleaned_data.get('last_name')
                    user.last_name = last_name
                    
                    email = teacher_form.cleaned_data.get('email')
                    user.email = email
                    
                    user.save()


                    # add new data in Teacher model and save
                    new_teacher.given_password = given_password
                    new_teacher.given_username = given_username
                    
                    new_teacher.is_user_done = 'DONE'
                    
                    auther = SchoolAdmin.objects.get(user=auther)
                    new_teacher.created_by = auther

                    new_teacher.is_teacher = True
                    new_teacher.id = user.id
                    new_teacher.user = user
                    new_teacher.save()
                    
                    
                    

                    # https://docs.djangoproject.com/en/3.2/topics/forms/modelforms/#the-save-method
                    # save data in many to many fields(grades,subjects)_Calling save_m2m() is only required if you use save(commit=False)
                    teacher_form.save_m2m()
                   

                    image_user = image_user_form.save(commit=False)
                    image_user.user = user
                    image_user.save()


                    if 'saveandcontinue' in request.POST:
                        messages.success(request, "New teacher created successfully !")
                        return redirect('listings:teacher_list')

                    elif 'saveandaddanother' in request.POST:
                        messages.success(request, "New teacher created successfully !")
                        return redirect('users:teacher_signup')
                    
                    
                else:
                    messages.warning(request,'you cant do this again because this teacher is done before')
                    return redirect('users:teacher_signup')

    else:
        messages.warning(request, "Sorry, add new teacher not allowed for you !")
        return redirect('users:main_dashboard')

    context = {
        'form_tch': teacher_form,
        'form3': image_user_form,
        'title': 'Sign Up',
        'sub_title': 'Teacher Create',
    }
    return render(request, 'users/teacher_signup.html', context)

    

'''pemission SchoolAdmin only'''
''' Note : teacher edit only by SchoolAdmin objects'''
####################### teacher_edit #########################################
@login_required(login_url='users:login_user')
def teacher_edit(request, teacher_username):
    # give permission to school admin only
    if SchoolAdmin.objects.all().filter(is_active=True).filter(user=request.user).exists():
        print('yes it is school admin')
        auther = request.user

        teacher = get_object_or_404(Teacher, given_username=teacher_username)
        teacher_form = TeacherUserCreateForm(instance=teacher)
        if request.method == 'POST':
            teacher_form = TeacherUserCreateForm(request.POST,instance=teacher)
            if teacher_form.is_valid():
                new_teacher = teacher_form.save(commit=False)
                user = get_object_or_404(User, username=teacher_username)

                # add edit new data in User model and save
                first_name = teacher_form.cleaned_data.get('first_name')
                user.first_name = first_name
                last_name = teacher_form.cleaned_data.get('last_name')
                user.last_name = last_name
                email = teacher_form.cleaned_data.get('email')
                user.email = email
                user.save()
     
                # add edit new data in Teacher model and save
                auther = SchoolAdmin.objects.get(user=auther)
                new_teacher.is_teacher = True
                # grades = teacher_form.cleaned_data.get('grades')
                # subjects = teacher_form.cleaned_data.get('subjects')
                new_teacher.id = user.id
                # new_teacher.grades = grades
                # new_teacher.subjects = subjects
                
                new_teacher.user = user
                new_teacher.save()

                # https://docs.djangoproject.com/en/3.2/topics/forms/modelforms/#the-save-method
                # save data in many to many fields(grades,subjects)_Calling save_m2m() is only required if you use save(commit=False)
                teacher_form.save_m2m()

                messages.success(request, 'Update done successfully')
                return redirect("listings:teacher_list")

        

    else:
        messages.warning(request, "Sorry, edit teacher not allowed for you !")
        return redirect('users:main_dashboard')

    context = {
        'form_tch': teacher_form,
        'title':    'Edit',
        'sub_title': 'Teacher Edit',
    }
    return render(request, 'users/teacher_edit.html', context)




'''pemission SchoolAdmin only'''
''' Note : teacher_delete_ask  only permission for SchoolAdmin objects'''
####################### teacher_delete_ask #########################################
@login_required(login_url='users:login_user')
def teacher_delete_ask(request, teacher_username):
    # give permission to school admin only
    if SchoolAdmin.objects.all().filter(is_active=True).filter(user=request.user).exists():
        print('yes it is school admin')
        auther = request.user

        teacher = get_object_or_404(Teacher, given_username = teacher_username)
        context = {
            'teacher': teacher,
        }
        return render(request, 'users/teacher_delete_ask.html', context)


    else:
        messages.warning(request, "Sorry, delete teacher register not allowed for you !")
        return redirect('users:main_dashboard')



'''pemission SchoolAdmin only'''
''' Note : teacher delete only by SchoolAdmin objects'''
####################### teacher_delete #########################################
@login_required(login_url='users:login_user')
def teacher_delete(request, teacher_username):
    # give permission to school admin only
    if SchoolAdmin.objects.all().filter(is_active=True).filter(user=request.user).exists():
        print('yes it is school admin')
        auther = request.user

        teacher = get_object_or_404(Student, given_username=teacher_username)
        user = get_object_or_404(User, username=teacher_username)
        teacher.delete()
        image = get_object_or_404(ImageUser,user=user)
        image.delete()
        user.delete()
        messages.success(request, "delete done successfully!")
        return redirect('listings:student_list')

    else:
        messages.warning(request, "Sorry, delete teacher register not allowed for you !")
        return redirect('users:main_dashboard')


################################################################################################
#################################### student ####################################################
################################################################################################

'''pemission SchoolAdmin only'''
''' Note : signup by SchoolAdmin'''
####################### student_signup #########################################
@login_required(login_url='users:login_user')
def student_signup(request):
    # give permission to school admin only
    if SchoolAdmin.objects.all().filter(is_active=True).filter(user=request.user).exists():
        print('yes it is school admin')
        auther = request.user
        
        auther = request.user
        student_form = StudentUserCreateForm()
        image_user_form = ImageUserForm()

        if request.method == 'POST':
            student_form = StudentUserCreateForm(request.POST)
            image_user_form = ImageUserForm(request.POST, request.FILES)

            if student_form.is_valid() and image_user_form.is_valid():
                new_student = student_form.save(commit=False)

                is_user_done = student_form.cleaned_data.get('is_user_done')
                print('is_user_done=', is_user_done)
                
                if is_user_done == None :
                    given_username = 'ST_' + str(uuid.uuid4().hex[:8])
                    given_password = uuid.uuid4().hex[:8]
                    user = User.objects.create_user(username=given_username, password=given_password)

                    # add new data in User model and save
                    user.username = given_username
                    user.set_password = given_password
                    first_name = student_form.cleaned_data.get('first_name')
                    user.first_name = first_name
                    last_name = student_form.cleaned_data.get('last_name')
                    user.last_name = last_name
                    email = student_form.cleaned_data.get('email')
                    user.email = email
                    user.save()

                    # add new data in Teacher model and save
                    new_student.given_password = given_password
                    new_student.given_username = given_username

                    
                    new_student.is_user_done = 'DONE'
                    auther = SchoolAdmin.objects.get(user=auther)
                    new_student.created_by = auther

                    new_student.is_student = True
                    new_student.user = user
                    new_student.save()

                    image_user = image_user_form.save(commit=False)
                    image_user.user = user
                    image_user.save()

                    


                    # https://docs.djangoproject.com/en/3.2/topics/forms/modelforms/#the-save-method
                    # save data in many to many fields(grades,subjects)_Calling save_m2m() is only required if you use save(commit=False)
                    # student_form.save_m2m()

                    if 'saveandcontinue' in request.POST:
                        messages.success(request, "New student created successfully !")
                        return redirect('listings:student_list')

                    elif 'saveandaddanother' in request.POST:
                        messages.success(request, "New student created successfully !")
                        return redirect('users:student_signup')

                else:
                    messages.warning(request, 'you cant do again because this student is done before')
                    return redirect('users:student_signup')

    else:
        messages.warning(request, "Sorry, add new student not allowed for you !")
        return redirect('users:main_dashboard')

    context = {
        'title': 'Sign Up',
        'sub_title': 'Student Create',
        'form': student_form,
        'form3': image_user_form,
    }
    return render(request, 'users/student_signup.html', context)


'''pemission SchoolAdmin only'''
''' Note : student edit only by SchoolAdmin objects '''
####################### student_edit #########################################
@login_required(login_url='users:login_user')
def student_edit(request, student_username):
    # give permission to school admin only
    if SchoolAdmin.objects.all().filter(is_active=True).filter(user=request.user).exists():
        print('yes it is school admin')
        auther = request.user
        
        student = get_object_or_404(Student, given_username=student_username)
        student_form = StudentUserCreateForm(instance = student)
        if request.method == 'POST':
            student_form = StudentUserCreateForm(request.POST,request.FILES,instance=student)
            if student_form.is_valid():
                new_student = student_form.save(commit=False)
                user = get_object_or_404(User, username=student_username)
                
                # add edit new data in User model and save
                first_name = student_form.cleaned_data.get('first_name')
                user.first_name = first_name
                last_name = student_form.cleaned_data.get('last_name')
                user.last_name = last_name
                email = student_form.cleaned_data.get('email')
                user.email = email
                user.save()

                # add edit new data in Teacher model and save
                auther = SchoolAdmin.objects.get(user=auther)
                new_student.updated_by = auther

                # new_student.is_student = True
                new_student.user = user
                new_student.save()

                
                # https://docs.djangoproject.com/en/3.2/topics/forms/modelforms/#the-save-method
                # save data in many to many fields(grades,subjects)_Calling save_m2m() is only required if you use save(commit=False)
                student_form.save_m2m()

                messages.success( request,'Update done successfully')
                return redirect("listings:student_list")
            
            else:
                student_form = StudentUserCreateForm(request.POST, request.FILES, instance=student)
    
    else:
        messages.warning(request, "Sorry, edit student not allowed for you !")   
        return redirect('users:main_dashboard')
        

    context = {
        'form': student_form,
        'title': 'Edit',
        'sub_title': 'Student Create',
    }
    return render(request,'users/student_edit.html',context)


'''pemission SchoolAdmin only'''
''' Note : student_delete_ask  only permission for SchoolAdmin objects '''
####################### student_delete_ask #########################################
@login_required(login_url='users:login_user')
def student_delete_ask(request, student_username):
    # give permission to school admin only
    if SchoolAdmin.objects.all().filter(is_active=True).filter(user=request.user).exists():
        print('yes it is school admin')
        student = get_object_or_404(Student, given_username=student_username)
        

    else:
        messages.warning(request, "Sorry, delete student register not allowed for you !")   
        return redirect('users:main_dashboard')


    context = {
        'student': student,
    }
    return render(request,'users/student_delete_ask.html', context)



'''pemission SchoolAdmin only'''
''' Note : student delete only by SchoolAdmin objects '''
####################### student_delete #########################################
@login_required(login_url='users:login_user')
def student_delete(request, student_username):
    # give permission to school admin only
    if SchoolAdmin.objects.all().filter(is_active=True).filter(user=request.user).exists():
        print('yes it is school admin')
      

        student = get_object_or_404(Student, given_username=student_username)
        user = get_object_or_404(User, username=student_username)
        student.delete()
        image = get_object_or_404(ImageUser,user=user)
        image.delete()
        user.delete()
        messages.success(request, "delete done successfully !")
        return redirect('listings:student_list')      

    else:
        messages.warning(request, "Sorry, delete student register not allowed for you !")
        return redirect('users:main_dashboard')



################################################################################################
###################################### parent ##################################################
################################################################################################

'''pemission SchoolAdmin only'''
''' Note : parent sign up only by SchoolAdmin objects '''
####################### parent_signup #########################################
@login_required(login_url='users:login_user')
def parent_signup(request):
    # give permission to school admin only
    if SchoolAdmin.objects.all().filter(is_active=True).filter(user=request.user).exists():
        auther = request.user
        print('yes it is school admin')

        parent_form = ParentUserCreateForm()
        image_user_form = ImageUserForm()
        if request.method == 'POST':
            parent_form = ParentUserCreateForm(request.POST)
            image_user_form = ImageUserForm(request.POST,request.FILES)

            if parent_form.is_valid() and image_user_form.is_valid():
                new_parent = parent_form.save(commit=False)

                is_user_done = parent_form.cleaned_data.get('is_user_done')
                print('is_user_done=', is_user_done)

                if is_user_done == None:
                    given_username = 'PT_' + str(uuid.uuid4().hex[:8])
                    given_password = uuid.uuid4().hex[:8]
                    user = User.objects.create_user(username=given_username, password=given_password)

                    # add new data in User model and save
                    user.username = given_username
                    user.set_password = given_password
                    first_name = parent_form.cleaned_data.get('father_f_name')
                    user.first_name = first_name
                    last_name = parent_form.cleaned_data.get('father_l_name')
                    user.last_name = last_name
                    email = parent_form.cleaned_data.get('father_email')
                    user.email = email
                    user.save()

                    # add new data in Parent model and save
                    new_parent.given_password = given_password
                    new_parent.given_username = given_username

                    new_parent.is_user_done = 'DONE'
                    auther = SchoolAdmin.objects.get(user=auther)
                    new_parent.created_by = auther

                    new_parent.is_parent = True
                    new_parent.user = user
                    new_parent.save()

                    image_user = image_user_form.save(commit=False)
                    image_user.user = user
                    image_user.save()

                    # https://docs.djangoproject.com/en/3.2/topics/forms/modelforms/#the-save-method
                    # save data in many to many fields(students)_Calling save_m2m() is only required if you use save(commit=False)
                    parent_form.save_m2m()

                    if 'saveandcontinue' in request.POST:
                        messages.success(request, "New parent created successfully !")
                        return redirect('listings:parent_list')

                    elif 'saveandaddanother' in request.POST:
                        messages.success(request, "New parent created successfully !")
                        return redirect('users:parent_signup')

                else:
                    messages.warning(request, 'you cant do again because this parent is done before')
    
    else:
        messages.warning(request, "Sorry, add new parent not allowed for you !")
        return redirect('users:main_dashboard')

    context = {
        'form_pa': parent_form,
        'form3': image_user_form,
        'title': 'Sign Up',
        'sub_title': 'Parent Create',
    }
    return render(request, 'users/parent_signup.html', context)




'''pemission SchoolAdmin only'''
''' Note : parent edit only by SchoolAdmin objects '''
####################### parent_edit #########################################
@login_required(login_url='users:login_user')
def parent_edit(request, parent_username):
    #give permission to school admin only
    if SchoolAdmin.objects.all().filter(is_active=True).filter(user=request.user).exists():
        print('yes it is school admin')
        auther = request.user

        parent = get_object_or_404(Parent, given_username=parent_username)
        parent_form = ParentUserCreateForm(instance=parent)
        if request.method == 'POST':
            parent_form = ParentUserCreateForm(request.POST, request.FILES, instance=parent)
            if parent_form.is_valid():
                new_parent = parent_form.save(commit=False)
                user = get_object_or_404(User, username=parent_username)

                # add edit new data in User model and save
                first_name = parent_form.cleaned_data.get('father_f_name')
                user.first_name = first_name
                last_name = parent_form.cleaned_data.get('father_l_name')
                user.last_name = last_name
                email = parent_form.cleaned_data.get('father_email')
                user.email = email
                user.save()

                # add  new data in Parent model and save
                auther = SchoolAdmin.objects.get(user=auther)
                new_parent.updated_by = auther

                # new_student.is_student = True
                new_parent.user = user
                new_parent.save()

                # https://docs.djangoproject.com/en/3.2/topics/forms/modelforms/#the-save-method
                # save data in many to many fields(grades,subjects)_Calling save_m2m() is only required if you use save(commit=False)
                parent_form.save_m2m()

                messages.success(request, 'Update done successfully')
                return redirect("listings:parent_list")

            else:
                parent_form = ParentUserCreateForm(request.POST, request.FILES, instance=parent)

    else:
        messages.warning(request, "Sorry, edit parent not allowed for you !")
        return redirect('users:main_dashboard')

    context = {
        'title': 'Edit',
        'sub_title': 'Parent Edit',
        'form_pa': parent_form,
    }
    return render(request, 'users/parent_edit.html', context)


'''pemission SchoolAdmin only'''
''' Note : parent_delete_ask  only permission for SchoolAdmin objects '''
####################### parent_delete_ask #########################################
@login_required(login_url='users:login_user')
def parent_delete_ask(request, parent_username):
    #give permission to school admin only
    if SchoolAdmin.objects.all().filter(is_active=True).filter(user=request.user).exists():
        print('yes it is school admin')

        parent = get_object_or_404(Parent, given_username=parent_username)
       
    else:
        messages.warning(request, "Sorry, delete parent register not allowed for you !")
        return redirect('users:main_dashboard')


    context = {
        'parent': parent,
    }
    return render(request, 'users/parent_delete_ask.html', context)




'''pemission SchoolAdmin only'''
''' Note : parent delete only by SchoolAdmin objects'''
####################### parent_delete #########################################
@login_required(login_url='users:login_user')
def parent_delete(request, parent_username):
    #give permission to school admin only
    if SchoolAdmin.objects.all().filter(is_active=True).filter(user=request.user).exists():
        print('yes it is school admin')

        parent = get_object_or_404(Parent, given_username=parent_username)
        user = get_object_or_404(User, username=parent_username)
        parent.delete()
        image = get_object_or_404(ImageUser, user=user)
        image.delete()
        user.delete()
        messages.success(request, "delete done successfully !")
        return redirect('users:main_dashboard')

    else:
        messages.warning(request, "Sorry, delete parent register not allowed for you !")
        return redirect('listings:parent_list')


















# THIS TRY  NOT USED #####
################################################################################################
################################################################################################
################################################################################################
# https://docs.djangoproject.com/en/4.0/topics/forms/modelforms/#using-an-inline-formset-in-a-view
# https://docs.djangoproject.com/en/4.0/ref/forms/models/#inlineformset-factory
# https://docs.djangoproject.com/en/4.0/topics/forms/formsets/#formsets
# def attendace_student_create(request,student_username):
#     student = get_object_or_404(Student,given_username = student_username)
#     AttendanceFormset = inlineformset_factory(parent_model=Student,
#                                               model=,
#                                             #   form=AttendanceStudentForm,
#                                               fields=('date_attend','is_attend'), 
#                                               can_delete=False,
                                              
#                                               # max_num=5,
#                                               # fk_name=None,
#                                               # fields=None, exclude=None, can_order=False,
#                                               # can_delete=True, max_num=None, formfield_callback=None,
#                                               # widgets=None, validate_max=False, localized_fields=None,
#                                               # labels=None, help_texts=None, error_messages=None,
#                                               # min_num=None, validate_min=False, field_classes=None,
#                                              )
   
#     if request.method == 'POST':
#         formset = AttendanceFormset(request.POST,instance=student)
#         if formset.is_valid():
#             new_formset = formset.save(commit = False)
#             for fs in new_formset :
#                 fs.creatd_by = get_object_or_404(Teacher,user=request.user)
#                 fs.save()
#             messages.success(request,f'you add attendance for {student.get_student_full_name}  successfully.')
#             return redirect(student.get_absolute_url())

#     else:
#         formset = AttendanceFormset(instance=student)
    
#     context = {
#         'formset' : formset,
#         'student':student,
#     }
#     return render(request,'users/attendance_stud_create.html', context)
    
    

    
    
