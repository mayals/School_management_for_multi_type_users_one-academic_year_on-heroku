from django.db.models import Avg
from django.shortcuts import render,redirect, get_object_or_404
from users.models import AcademicYear, SchoolAdmin, Teacher, Student, Parent, MessageTeacherToStudent, MessageTeacherToGrade
from .models import Grade, Subject, Mark, GradeAttendance
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.models import User

from .forms import GradeForm, SubjectForm, MarkForm, GradeAttendanceForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail
from .forms import EmailForm


''' NO pemission'''
######################################################################################################
###################################### EMAIL US ############################################################
##########################################################################################################
def Email_us(request):    
    email_form = EmailForm()
    if request.method == 'POST':
        email_form = EmailForm(request.POST)
        if email_form.is_valid():
            subject = email_form.cleaned_data['subject']
            message = email_form.cleaned_data['message']
            sender = email_form.cleaned_data['sender']
            recipients = ['developer.web.dj@gmail.com']
            
            cc_myself = email_form.cleaned_data['cc_myself']
            if cc_myself:
                recipients.append(sender)

            send_mail(subject, message, sender, recipients)
            messages.success(request,'sending Email done')
            return redirect('listings:index')
    
    context = {
        'email_form': email_form,
    }
    return render(request, 'listings/email_us.html',context)


''' NO pemission'''
######################## index  #####################################
def index(request):
    title = 'Home'
    context = {
        'title': title,
    }
    return render(request, 'listings/index.html', context)


#####################################################################################################
############################### all users ##############################################################
######################################################################################################

'''pemission webadmin only'''
################################# all users list   ####################################
@login_required(login_url='users:login_user')
def user_list(request):
    sch_ufstname = None
    sch_ulstname = None
    sch_uusername = None

    all_users = User.objects.all()

    if 'sch_ufstname' in request.GET:
        sch_ufstname = request.GET.get('sch_ufstname')
        if sch_ufstname is not None:
            all_users = all_users.filter(first_name__icontains=sch_ufstname)

    if 'sch_ulstname' in request.GET:
        sch_ulstname = request.GET.get('sch_ulstname')
        if sch_ulstname is not None:
            all_users = all_users.filter(last_name__icontains=sch_ulstname)

    if 'sch_uusername' in request.GET:
        sch_uusername = request.GET.get('sch_uusername')
        print(sch_uusername)
        if sch_uusername is not None:
            all_users = all_users.filter(username__icontains = sch_uusername)

    # paginator
    paginator = Paginator(all_users, 10)
    page = request.GET.get('page')

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        users = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        users = paginator.page(paginator.num_pages)

    context = {
        'users': users,
        'page': page,
    }
    return render(request,'listings/user_list.html',context)




#####################################################################################################
############################### School admin  ##############################################################
######################################################################################################
'''pemission SCHOOL ADMIN only & web admin '''
################################# schadmin_list   ####################################
@login_required(login_url='users:login_user')
def schadmin_list(request):
    
    all_schadmins = SchoolAdmin.objects.all().filter(is_active=True)
    
    # paginator 
    paginator = Paginator(all_schadmins,5)
    page = request.GET.get('page')

    try:
        schadmins = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        schadmins = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        schadmins = paginator.page(paginator.num_pages)

    context = {
        
        'schadmins': schadmins,
        'page': page,
    }
    return render(request, 'listings/schadmin_list.html', context)




'''pemission SCHOOL ADMIN only & web admin '''
#################################  schadmin_detail  ####################################
@login_required(login_url='users:login_user')
def schadmin_detail(request, schadmin_username):
  
    user = get_object_or_404(User, username=schadmin_username)
    schadmin = get_object_or_404(SchoolAdmin, user=user)
    

    context = {
        
        'user': user,
        'schadmin': schadmin,
        
    }
    return render(request, 'listings/schadmin_detail.html', context)





#####################################################################################################
############################### teacher  ##############################################################
######################################################################################################

'''pemission SCHOOL ADMIN only & web admin '''
############################  teacher_list  #######################################3
@login_required(login_url='users:login_user')
def teacher_list(request):
    sch_ttfstname = None
    sch_ttlstname = None
    sch_ttusername = None

    all_teachers = Teacher.objects.all().filter(is_active=True)
   
   
    if 'sch_ttfstname' in request.GET:
        sch_ttfstname = request.GET.get('sch_ttfstname')
        if not sch_ttfstname == None:
            all_teachers = all_teachers.filter(first_name__icontains = sch_ttfstname)

    if 'sch_ttlstname' in request.GET:
        sch_ttlstname = request.GET.get('sch_ttlstname')
        if not sch_ttlstname == None:
            all_teachers = all_teachers.filter(last_name__icontains = sch_ttlstname)

    if 'sch_ttusername' in request.GET:
        sch_ttusername = request.GET.get('sch_ttusername')
        if not sch_ttusername == None:
            all_teachers = all_teachers.filter(given_username__icontains = sch_ttusername)


    #pagination
    paginator = Paginator(all_teachers,10)
    page = request.GET.get('page')

    try:
        teachers = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        teachers = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        teachers = paginator.page(paginator.num_pages)
    
    context = {
        'teachers': teachers,
        'page': page,
    }
    return render(request,'listings/teacher_list.html',context)


'''pemission SCHOOL ADMIN only & web admin '''
#################################  teacher_detail  ####################################
@login_required(login_url='users:login_user')
def teacher_detail(request,teacher_username):
   
    teacher = get_object_or_404(Teacher, given_username=teacher_username)
    grades_for_teacher = teacher.grades.all()
    context = {
       
        'teacher': teacher,
        'grades_for_teacher': grades_for_teacher,
      
    }
    return render(request, 'listings/teacher_detail.html', context)


####################################################################################################
############################### student ##############################################################
######################################################################################################

'''pemission SCHOOL ADMIN only & web admin '''
#################################  student_list  ####################################
@login_required(login_url='users:login_user')
def student_list(request):
    sch_stfstname = None
    sch_stlstname = None
    sch_stgrade = None

    all_students = Student.objects.all().filter(is_active=True).filter(status='inprogress')
    
    if 'sch_stfstname' in request.GET:
        sch_stfstname = request.GET.get('sch_stfstname')
        if not sch_stfstname == None:
            all_students = all_students.filter(first_name__icontains=sch_stfstname)

    
    if 'sch_stlstname' in request.GET:
        sch_stfstname = request.GET.get('sch_stlstname')
        if not sch_stlstname == None:
            all_students = all_students.filter(last_name__icontains=sch_stlstname)

    
    if 'sch_stgrade' in request.GET:
        sch_stgrade = request.GET.get('sch_stgrade')
        if not sch_stgrade == None:
            all_students = all_students.filter(grade__name__icontains=sch_stgrade)

    #pagination
    paginator = Paginator(all_students,10)
    page = request.GET.get('page')
    
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        students = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        students = paginator.page(paginator.num_pages)
    
    context = {
        'students': students,
        'page': page,
    }
    return render(request, 'listings/student_list.html', context)


'''pemission SCHOOL ADMIN only & web admin '''
#################################  student_detail  ####################################
@login_required(login_url='users:login_user')
def student_detail(request, student_username):
    student = get_object_or_404(Student, given_username=student_username)
    subjects_for_grade = Subject.objects.all().filter(grade = student.grade)
    marks = Mark.objects.all().filter(student=student)
    subjects = Subject.objects.all()
    total_mark = Mark.objects.all().filter(student=student).aggregate(Avg('mark_value'))
    parent_for_student = Parent.objects.all().filter(students=student)
    ### 
    messageteachertostudent = MessageTeacherToStudent.objects.all().filter(student__given_username=student_username)
    
    context = {
        'student': student,
        'marks':marks,
        'subjects_for_grade': subjects_for_grade, 
        'subjects': subjects,
        'total_mark': total_mark,
        'parent_for_student' : parent_for_student,
        'message_teacher_to_student': messageteachertostudent,
    }
    return render(request,'listings/student_detail.html', context)



##########################  mark_student_create  ##########################################################
# def mark_student_create(request, student_username):

###################################################################################3


'''mark created only by teacher'''
############################################################################################
######################################### MARK ###########################################
###############################################################################################
@login_required(login_url='users:login_user')
def mark_create(request,student_username, subject_slug):
    
    if Teacher.objects.all().filter(is_active=True).filter(user=request.user).exists():
        print('yes it is teacher')
        auther = get_object_or_404(Teacher,user = request.user)
        
        mark_form = MarkForm()
        
        student = get_object_or_404(Student, given_username=student_username)
        subject = get_object_or_404(Subject,slug=subject_slug)
        if request.method == 'POST':
            mark_form = MarkForm(request.POST)
            if mark_form.is_valid():
                new_mark = mark_form.save(commit=False)
                exam_name = request.POST.get('exam_name')
                new_mark.student = student
                new_mark.subject = subject
                new_mark.created_by = auther
                if Mark.objects.filter(exam_name=exam_name).filter(subject=subject).filter(student=student).exists():
                    messages.warning(request, "exam name is add before for this student and subject!")
                    
                else:
                    mark_form.save_m2m
                    new_mark.save()

                    if 'saveandcontinue' in request.POST:
                        messages.success(request, "New mark add successfully !")
                        return redirect('listings:student_detail', student_username=student.given_username)

                    elif 'saveandaddanother' in request.POST:
                        messages.success(request, "New mark add successfully !")
                        return redirect('listings:mark_create', student_username=student.given_username,subject_slug=subject.slug)
    
           

    
    else:
        messages.warning(request, "Sorry, add mark not allowed for you !")
        student= get_object_or_404(Student,given_username=student_username)
        return redirect('listings:student_detail', student_username=student.given_username)

    context = {
     
        'form_mk': mark_form,
        'student': student,
        'subject': subject,
        'title': 'Mark Form',
        'sub_title': 'Add Mark',   
    }
    return render(request,'listings/mark_create.html',context)






########################### mark_edit ################################
@login_required(login_url='users:login_user')
def mark_edit(request,student_username, subject_slug,mark_id):

   
    if Teacher.objects.all().filter(is_active=True).filter(user=request.user).exists():
        print('yes it is teacher')
        auther = get_object_or_404(Teacher, user=request.user)

        student = get_object_or_404(Student, given_username=student_username)
        subject = get_object_or_404(Subject, slug=subject_slug)
        id = mark_id
        instance_mark = get_object_or_404(Mark, student=student, subject=subject, id=id)
        mark_form = MarkForm(instance=instance_mark)
        
        if request.method == 'POST':
            mark_form = MarkForm(request.POST, instance=instance_mark)
            if mark_form.is_valid():
                new_mark = mark_form.save(commit=False)

                new_mark.student = student

                new_mark.subject = subject
                
                new_mark.id = id
                
                new_mark.created_by = auther
                mark_form.save_m2m
                new_mark.save()

                messages.success(request, "mark edit successfully !")
                return redirect('listings:student_detail', student_username=student.given_username)

                

    else:
        messages.warning(request, "Sorry, edit mark not allowed for you !")
        student = get_object_or_404(Student, given_username=student_username)
        return redirect('listings:student_detail', student_username=student.given_username)

    context = {
      
        'form_mk': mark_form,
        'student': student,
        'subject': subject,
        'title': 'Mark Form',
        'sub_title': 'Edit Mark',
    }
    return render(request, 'listings/mark_edit.html', context)



################################ student_subject_mark_detail #############################################
@login_required(login_url='users:login_user')
def student_subject_mark_detail(request,student_username, subject_slug):
    
    student = get_object_or_404(Student, given_username=student_username)
    subject = get_object_or_404(Subject, slug=subject_slug)
    marks_for_student_subject = Mark.objects.all().filter(student=student).filter(subject=subject)
    context = {
        
        'student': student,
        'subject': subject,
        'marks_for_student_subject': marks_for_student_subject,
    }

    return render(request, 'listings/student_subject_mark_detail.html', context)







#####################################################################################################
############################### parent  ##############################################################
######################################################################################################


##############################  parent_list  ##################################
@login_required(login_url='users:login_user')
def parent_list(request):
    sch_ptfathfname = None
    sch_ptfathusername = None
    sch_ptstusername = None
    
    all_parents = Parent.objects.all().filter(is_active=True)

    if 'sch_ptfathfname' in request.GET:
        sch_ptfathfname = request.GET.get('sch_ptfathfname')
        if not sch_ptfathfname == None:
            all_parents = all_parents.filter(father_f_name__icontains=sch_ptfathfname)
    
    if 'sch_ptfathusername' in request.GET:
        sch_ptfathusername = request.GET.get('sch_ptfathusername')
        if not sch_ptfathusername == None:
            all_parents = all_parents.filter(given_username__icontains=sch_ptfathusername)

    if 'sch_ptstusername' in request.GET:
        sch_ptstusername = request.GET.get('sch_ptstusername')
        if not sch_ptstusername == None:
            all_parents = all_parents.filter(students__given_username__icontains=sch_ptstusername)

    #pagination
    paginator = Paginator(all_parents,10)
    page = request.GET.get('page')

    try:
        parents = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        parents = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        parents = paginator.page(paginator.num_pages)
    context = {

        'parents': parents ,
        'page':page,
    }
    return render(request, 'listings/parent_list.html', context)


#################################  parent_detail  ####################################
@login_required(login_url='users:login_user')
def parent_detail(request, parent_username):
    parent = get_object_or_404(Parent, given_username=parent_username)
    
    context = {
        'parent': parent,
        
    }
    return render(request, 'listings/parent_detail.html', context)



#####################################################################################################
############################### Grade ##############################################################
######################################################################################################
'''only permission to schooladmin ''' 
############## grade signup #######################################################33
@login_required(login_url='users:login_user')
def grade_signup(request):
    # give permission to school admin only
    if SchoolAdmin.objects.all().filter(is_active=True).filter(user=request.user).exists():
        print('yes it is school admin')
       
       
        grade_form = GradeForm()
        if request.method == 'POST':
            grade_form = GradeForm(request.POST)
            if grade_form.is_valid():
                new_grade = grade_form.save()  
                # https://docs.djangoproject.com/en/3.2/topics/forms/modelforms/#the-save-method
                # no need because not need to (commit=False)
                # grade_form.save_m2m()
                # new_grade.save()

                if 'saveandcontinue' in request.POST:
                    messages.success(request, "New grade created successfully !")
                    return redirect('listings:grade_list')

                elif 'saveandaddanother' in request.POST:
                    messages.success(request, "New grade created successfully !")
                    return redirect('listings:grade_signup')

    else:
        messages.warning(request, "Sorry, add grade not allowed for you !")
        return redirect('users:main_dashboard')

    context = {
        'form_gr' : grade_form,
        'title': 'Grade Signup',
        'sub_title': 'Grade Create',
    }
    return render(request,'listings/grade_signup.html',context)



############################  grade_list  ###########################################################
@login_required(login_url='users:login_user')
def grade_list(request):
    all_grades = Grade.objects.all()
    # paginator
    paginator = Paginator(all_grades, 10)
    page = request.GET.get('page')

    try:
        grades = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        grades = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        grades = paginator.page(paginator.num_pages)
    
    
    context = {
        'grades': grades,
        'page': page,
    }
    return render(request, 'listings/grade_list.html', context)


############################  grade_detail  #######################################3
@login_required(login_url='users:login_user')
def grade_detail(request,grade_slug):
    grade = get_object_or_404(Grade, slug=grade_slug)
   
    teachers_for_grade = Teacher.objects.all().filter(grades=grade)
    
    context = {
        
        'grade': grade,
        'teachers_for_grade': teachers_for_grade ,
    }
    return render(request, 'listings/grade_detail.html', context)


'''only permission to school admin'''
############################  grade_edit  #######################################3
@login_required(login_url='users:login_user')
def grade_edit(request,grade_slug):
    # give permission to school admin only
    if SchoolAdmin.objects.all().filter(is_active=True).filter(user=request.user).exists():
        print('yes it is school admin')
        auther = request.user

        
        grade = get_object_or_404(Grade, slug=grade_slug)
        grade_form = GradeForm(instance=grade)
        if request.method == 'POST':
            grade_form = GradeForm(request.POST,instance=grade)
            if grade_form.is_valid():
                new_grade = grade_form.save()
                new_grade.save()
                # https://docs.djangoproject.com/en/3.2/topics/forms/modelforms/#the-save-method
                # no need because not need to (commit=False)
                # grade_form.save_m2m()
                # new_grade.save()

                messages.success(request,"grade edit successfully !")
                return redirect('listings:grade_list')
                
    else:
        messages.warning(request, "Sorry, edit grade not allowed for you !")
        return redirect('users:main_dashboard')
    
    
    context = {
        'form_gr': grade_form,
    }
    return render(request, 'listings/grade_edit.html', context)




# Note : grade only delete by scchool admin
####################### grade_delete_ask #########################################
@login_required(login_url='users:login_user')
def grade_delete_ask(request,grade_slug):
    # give permission to school admin only
    if SchoolAdmin.objects.all().filter(is_active=True).filter(user=request.user).exists():
        print('yes it is school admin')
        
        grade = get_object_or_404(Grade, slug=grade_slug)
   

    else:
        messages.warning(request, "Sorry, delete grade not allowed for you !")
        return redirect('users:main_dashboard')
    
    context = {
        'grade': grade,
    }
    return render(request, 'listings/grade_delete_ask.html', context)




# Note : grade only delete by school admin
####################### grade_delete #########################################
@login_required(login_url='users:login_user')
def grade_delete(request,grade_slug):
    # give permission to school admin only
    if SchoolAdmin.objects.all().filter(is_active=True).filter(user=request.user).exists():
        print('yes it is school admin')
        auther = request.user

        grade = get_object_or_404(Grade,slug=grade_slug)
        grade.delete()
        messages.success(request, "delete done successfully!")
        return redirect('listings:grade_list')


    else:
        messages.warning(request, "Sorry, delete grade not allowed for you !")
        return redirect('users:main_dashboard')

#####################################################################################################
############################### Subject ##############################################################
######################################################################################################
'''only permission to school admin'''
############## subject signup #######################################################33
@login_required(login_url='users:login_user')
def subject_signup(request):
    # give permission to school admin only
    if SchoolAdmin.objects.all().filter(is_active=True).filter(user=request.user).exists():
        print('yes it is school admin')
        auther = request.user

        subject_form = SubjectForm()
        if request.method == 'POST':
            subject_form = SubjectForm(request.POST)
            if subject_form.is_valid():
                
                new_subject = subject_form.save()

            

                if 'saveandcontinue' in request.POST:
                    messages.success(request, "New subject created successfully !")
                    return redirect('listings:subject_list')

                elif 'saveandaddanother' in request.POST:
                    messages.success(request, "New subject created successfully !")
                    return redirect('listings:subject_signup')
                
            
            
            else :
                messages.warning(request,"title of subject for The Grade must be unique, please use small letters for title !")

    else:
        messages.warning(request, "Sorry, add subject not allowed for you !")
        return redirect('users:main_dashboard')

             
    context = {
        'form_sub': subject_form,
        'title': 'Subject Signup',
        'sub_title': 'Subject Create',
    }
    return render(request, 'listings/subject_signup.html', context)





############################  subject_list  ###########################################################
@login_required(login_url='users:login_user')
def subject_list(request):
    all_subjects = Subject.objects.all()
    

    # paginator
    paginator = Paginator(all_subjects, 10)
    page = request.GET.get('page')

    try:
        subjects = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        subjects = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        subjects = paginator.page(paginator.num_pages)

    context = {
        
        'teachers' : Teacher.objects.all().filter(is_active=True),
        'subjects': subjects,
        'page': page,
    }
    return render(request, 'listings/subject_list.html', context)


############################  subject_detail  #######################################3
@login_required(login_url='users:login_user')
def subject_detail(request,subject_slug):
    subject = get_object_or_404(Subject,slug=subject_slug)
    teachers = Teacher.objects.all().filter(is_active=True).filter(subjects= subject)
    students = Student.objects.all().filter(is_active=True).filter(grade=subject.grade)
  
    
    context = {
        
        'subject': subject ,
        'teachers_for_subject':  teachers,
        'students_for_subject':  students,
    }
    return render(request, 'listings/subject_detail.html', context)




'''only permission to school admin'''
############################  subject_edit  #######################################3
@login_required(login_url='users:login_user')
def subject_edit(request,subject_slug):
    # give permission to school admin only
    if SchoolAdmin.objects.all().filter(is_active=True).filter(user=request.user).exists():
        print('yes it is school admin')
        auther = request.user

        
        subject = get_object_or_404(Subject, slug=subject_slug)
        subject_form = SubjectForm(instance=subject)
        if request.method == 'POST':
            subject_form = SubjectForm(request.POST, instance=subject)
            if subject_form.is_valid():
                new_subject = subject_form.save()

                # https://docs.djangoproject.com/en/3.2/topics/forms/modelforms/#the-save-method
                # no need the next steps because not need to (commit=False)
                #new_subject = subject_form.save(commit=False)
                # subject_form.save_m2m()

                messages.success(request, "subject edit successfully !")
                return redirect('listings:subject_list')

    else:
        messages.warning(request, "Sorry, edit subject not allowed for you !")
        return redirect('users:main_dashboard')
    

    context = {
        'form_sub': subject_form,
    }
    return render(request, 'listings/subject_edit.html', context)


# Note : subject only delete by scchool admin
####################### subject_delete_ask #########################################
@login_required(login_url='users:login_user')
def subject_delete_ask(request,subject_slug):
    # give permission to school admin only
    if SchoolAdmin.objects.all().filter(is_active=True).filter(user=request.user).exists():
        print('yes it is school admin')
        auther = request.user
        
        subject = get_object_or_404(Subject, slug=subject_slug)
        context = {
            
            'subject': subject,
        }
        return render(request, 'listings/subject_delete_ask.html', context)

    else:
        messages.warning(request, "Sorry, delete subject not allowed for you !")
        return redirect('users:main_dashboard')



# Note : subject only delete by school admin
####################### subject_delete #########################################
@login_required(login_url='users:login_user')
def subject_delete(request,subject_slug):
    # give permission to school admin only
    if SchoolAdmin.objects.all().filter(is_active=True).filter(user=request.user).exists():
        print('yes it is school admin')
        auther = request.user

        subject = get_object_or_404(Subject,slug=subject_slug)
        subject.delete()
        messages.success(request, "delete done successfully!")
        return redirect('listings:subject_list')

    
    else:
        messages.warning(request, "Sorry, delete subject not allowed for you !")
        return redirect('users:main_dashboard')


######################################





'''https://www.titanwolf.org/Network/q/312661f6-1b33-4d15-9fee-9803be88700f/y'''
####################### grade_attendanc_create #########################################
@login_required(login_url='users:login_user')
def grade_attendanc_create(request, grade_slug):
    if Teacher.objects.all().filter(is_active=True).filter(user=request.user).exists():
        print('yes it is teacher')
    
        grade = get_object_or_404(Grade, slug=grade_slug)
        # instance = GradeAttendance.objects.get(grade=grade)
        if request.method == 'POST':

            form_att = GradeAttendanceForm(request.POST)
            form_att.fields['students'].queryset = Student.objects.filter(grade__slug=grade_slug)
        
            if form_att.is_valid():
                    new_att = form_att.save(commit=False)
                    user = request.user
                    teacher_author= get_object_or_404(Teacher,user=user)
                    if teacher_author :
                        new_att.created_by = teacher_author
                        new_att.grade = grade
                        new_att.save()
                        form_att.save_m2m()

                        messages.success(request, "Attendance students add to attendance grade successfully !")
                        return redirect('listings:grade_dashboard')
                    


        else:
            form_att = GradeAttendanceForm()
            form_att.fields['students'].queryset = Student.objects.filter(grade__slug=grade_slug)

    else:
        messages.warning(request, "Sorry, add attendance for students not allowed for you !")
        return redirect('users:main_dashboard')
    
    
    context = {
        'form_att': form_att,
        'title': 'Attendance add',
        'grade': grade,
    }
    return render(request, 'listings/grade_attendance_create.html', context)




'''pemission teacher only '''
#################################  grade_dashboard  ####################################
@login_required(login_url='users:login_user')
def grade_dashboard(request):
    students = Student.objects.all().filter(is_active=True).filter(status='inprogress')
    grades = Grade.objects.all().order_by('created_at')
    
    context = {
        'students' : students ,
        'grades': grades,
    }
    return render(request, 'listings/grade_dashboard.html', context)




#################################  attendance_list  ####################################
@login_required(login_url='users:login_user')
def attendance_list(request,grade_slug):
    grade = get_object_or_404(Grade,slug=grade_slug)
    all_student_in_grade = Student.objects.all().filter(grade__slug=grade_slug)
    gradeattendances = GradeAttendance.objects.all().filter(grade__slug=grade_slug).order_by('-att_date')

    context = {
        'all_student': all_student_in_grade,
        'title':'Attendance of Students',
        'grade': grade ,
        'gradeattendances': gradeattendances,
        'parents' : Parent.objects.all(),

    }
    return render(request, 'listings/gradeattendance_list.html', context)





'''pemission teacher only '''
#################################  suject_grade_dashboard  ####################################
@login_required(login_url='users:login_user')
def subject_grade_dashboard(request):
    students = Student.objects.all().filter(is_active=True).filter(status='inprogress')
    grades = Grade.objects.all().order_by('created_at')
    
    context = {
        'students' : students ,
        'grades': grades,
    }
    return render(request, 'listings/subject_grade_dashboard.html', context)


################################ student_subject_mark_detail #############################################
@login_required(login_url='users:login_user')
def subject_mark_student_list(request, grade_slug ,subject_slug):

    grade = get_object_or_404(Grade,slug=grade_slug)
    subject = get_object_or_404(Subject, slug=subject_slug)
    students = Student.objects.filter(grade=grade)
    # marks_for_subject = Mark.objects.all().filter(student=student).filter(subject=subject)
    context = {

        'grade': grade,
        'subject': subject,
        'students': students,
        # 'marks_for_student_subject': marks_for_student_subject,
    }

    return render(request,'listings/subject_mark_student_list.html', context)


################################### subject_mark_student_detail ############################################333333
def subject_mark_student_detail(request, grade_slug, subject_slug, student_username):
    student = get_object_or_404(Student, given_username=student_username)
    subject = get_object_or_404(Subject, slug=subject_slug)
    marks_for_student_subject = Mark.objects.all().filter(student=student).filter(subject=subject)
    context = {
        'student': student,
        'subject': subject,
        'marks_for_student_subject': marks_for_student_subject,
    }

    return render(request, 'listings/subject_mark_student_detail.html', context)
##############################################################################3333


'''pemission teacher only '''
#################################  student_detail_marks  ####################################
@login_required(login_url='users:login_user')
def student_detail_marks(request, student_username):
    student = get_object_or_404(Student, given_username=student_username)
    subjects_for_grade = Subject.objects.all().filter(grade=student.grade)
    marks = Mark.objects.all().filter(student=student)
    subjects = Subject.objects.all()
    total_mark = Mark.objects.all().filter(
        student=student).aggregate(Avg('mark_value'))
    parent_for_student = Parent.objects.all().filter(students=student)
    ###
    messageteachertostudent = MessageTeacherToStudent.objects.all().filter(
        student__given_username=student_username)

    context = {
        'student': student,
        'marks': marks,
        'subjects_for_grade': subjects_for_grade,
        'subjects': subjects,
        'total_mark': total_mark,
        'parent_for_student': parent_for_student,
        'message_teacher_to_student': messageteachertostudent,
    }
    return render(request, 'listings/student_detail_marks.html', context)


'''pemission student only '''
#################################  student_detail_marks  ####################################
@login_required(login_url='users:login_user')
def student_detail_attendance(request, student_username):
    student = get_object_or_404(Student, given_username=student_username)
    grade = student.grade
   
    all_att = GradeAttendance.objects.filter(grade=grade).order_by('-att_date')
    request.session['all_att_count'] = all_att.count()
    all_att_count = request.session['all_att_count']

    stud_att = GradeAttendance.objects.filter(grade=grade).filter(students=student)
    request.session['stud_att_count'] = stud_att.count()
    stud_att_count = request.session['stud_att_count']
    
    count_of_absence = all_att_count - stud_att_count
    
    context = {
        'student': student,
        'all_att' : all_att,
        'stud_att': stud_att,
        'all_att_count': all_att_count,
        'stud_att_count' : stud_att_count,
        'count_of_absence' : count_of_absence ,
    }
    return render(request, 'listings/student_detail_attendance.html', context)


'''pemission student only '''
#################################  student_detail  ####################################
@login_required(login_url='users:login_user')
def student_detail_messages(request, student_username):
    student = get_object_or_404(Student, given_username=student_username)
    messageteachertostudent = MessageTeacherToStudent.objects.all().filter(student__given_username=student_username)
        
    grade = student.grade
    messageteachertograde = MessageTeacherToGrade.objects.all().filter(grade=grade)

    context = {
        'student': student,
        'message_teacher_to_student': messageteachertostudent,
        
        'grade': grade,
        'message_teacher_to_grade': messageteachertograde,
    }
    return render(request, 'listings/student_detail_messages.html', context)

###########################################################




################## gr_st_chart ##################################
def charts_all(request):
    # Area Chart Number of Students vs Grade
    grade_names = []
    grade_students_count = []
    
    grades = Grade.objects.all().order_by('created_at')
    
    for grade in grades : 
        # print(grade.name)
        grade_names.append(grade.name)
        
        # print(grade.student_set.count())
        grade_students_count.append(grade.student_set.count())

    grades_last_updated = Grade.objects.all().order_by('-updated_at')[:1]
    
    ############################################    
    # Bar Chart teaher name vs age
    teacher_names = []
    teacher_ages = []
    
    teachers = Teacher.objects.all().filter(is_active=True)
    for teacher in teachers :
        print(teacher.get_teacher_full_name)
        teacher_names.append(teacher.get_teacher_full_name)
        print(teacher.get_teacher_age)
        teacher_ages.append(teacher.get_teacher_age)

    teachers_last_updated = Teacher.objects.all().filter(is_active=True).order_by('-updated_at')[:1]
    ############################################    
    # Pi Chart student name vs age
    student_names = []
    student_ages = []

    students = Student.objects.all().filter(is_active=True).filter(status__contains ='inprogress')[:7]
    for student in students:
        print(student.get_student_full_name)
        student_names.append(student.get_student_full_name)
        
        print(student.get_student_age)
        student_ages.append(student.get_student_age)

    students_last_updated = Student.objects.all().filter(is_active=True).filter(status__contains='inprogress').order_by('-updated_at')[:1]
    ############################################

    context={
        # Area Chart Number of Students vs Grade
        'grade_names': grade_names,
        'grade_students_count': grade_students_count,
        'grades_last_updated': grades_last_updated,
        
        # Bar Chart teaher name vs age
        'teacher_names': teacher_names,
        'teacher_ages': teacher_ages,
        'teachers_last_updated':teachers_last_updated,

        # Pi Chart student name vs age
        'student_names': student_names,
        'student_ages': student_ages,
        'students_last_updated':students_last_updated,
    }
    return render(request, 'listings/charts_all.html', context)
#################################################
    
    # not used__ only try
    # teacher_join_names = []
    # teacher_join_current_year_month = []
    # for teacher in teachers :
    #     print(teacher.get_teacher_full_name)
    #     teacher_join_names.append(teacher.get_teacher_full_name)
        
        
    #     teacher_cr_month_name = teacher.created_at.strftime("%B")
    #     print(teacher_cr_month_name)
    #     teacher_join_current_year_month.append(teacher.created_at.strftime("%B"))
