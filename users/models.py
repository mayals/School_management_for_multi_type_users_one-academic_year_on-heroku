from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from helpers.models import AbstractTimeStamp
from datetime import date
from sch_proj.utils import mobile_check
from django.urls import reverse


### circular import issues ### solving
# https://www.pythonpool.com/python-circular-import/
from listings import models as mod



######################### academic year #############################
class AcademicYear(models.Model):
    start_date = models.DateField(null=True, blank=False)
    end_date = models.DateField(null=True, blank=False)
    
    start_year = models.CharField(max_length=4, null=True, blank=True)
    end_year = models.CharField(max_length=4, null=True, blank=True)
    name = models.CharField(max_length=12, null=True, blank=True)
    is_done = models.BooleanField(default=False)
    
    def __str__(self):
           return str(self.name)
        
       
    def save(self, *args, **kwargs):
        
        self.start_year = self.start_date.strftime('%Y')
        print(self.start_year)
           
        self.end_year = self.end_date.strftime('%Y')
        print(self.end_year)

        if self.end_year > self.start_year:
            self.name = "{}-{}".format(self.start_year, self.end_year)
            print(self.name)
            if AcademicYear.objects.filter(name=self.name).exists():
                return # name must have unique name!
        
            super(AcademicYear, self).save(*args, **kwargs)
        

    class Meta:
        ordering = ['-start_date']
        
        

###################### user image ##################################
class ImageUser(AbstractTimeStamp):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    image = models.ImageField(verbose_name='User Image',upload_to='user-image/%Y/%m/%d/', null=True, blank=True)

    def __str__(self):
        return '{} image'.format(self.user.username)

    


########################################
class SchoolAdmin(AbstractTimeStamp):
    m = 'male'
    f = 'female'
    GENDER_CHOICES = [(m,'Male'), (f,'Female'),]
    
   
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(verbose_name='First Name', max_length=50, null=True, blank=False)
    second_name = models.CharField(verbose_name='Second Name', max_length=50, null=True, blank=False)
    last_name = models.CharField(verbose_name='Last Name', max_length=50,null=True, blank=False)
    email = models.EmailField(verbose_name='Email', max_length=254, null=True, blank=False)
    mobile = models.CharField(verbose_name="your mobile number",
                              max_length=10, null=True, blank=False, validators=[mobile_check])
    gender = models.CharField(verbose_name='Gender',max_length=10, choices=GENDER_CHOICES, blank=False)
    date_born = models.DateField(verbose_name='Date of Born', null=True, blank=False)
    country_born = models.CharField(verbose_name='Place of Born',max_length=200, null=True, blank=False)
    nationality = models.CharField(verbose_name='Nationality', max_length=200, null=True, blank=False)
    passport_number = models.CharField(verbose_name='Pawssport No.', max_length=50, null=True, blank=False)
    address = models.CharField(verbose_name='Current Address', max_length=200, null=True, blank=False)
    skills = models.TextField()
   
    is_schadmin = models.BooleanField(verbose_name='Is School Admin ?', default=True)
    is_active = models.BooleanField(verbose_name='is active ?', default=True, help_text='is this admin school user active ?')
    is_superuser = models.BooleanField(verbose_name='is superuser?', default=False, help_text='is this admin school user superuser ?')
    is_staff = models.BooleanField(verbose_name='is staff ?', default=False, help_text='is this admin school staff ?')
    
    created_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='schooladmins_created_by')
    updated_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='schooladmins_updated_by')

    @property
    def get_schadmin_full_name(self):
        '''Returns the SchoolAdmin's full name.'''
        return '%s %s %s' % (self.first_name, self.second_name, self.last_name)


    @property
    def get_schadmin_age(self):
        '''Returns the student's age.'''
        date_today = date.today()
        age = date_today.year - self.date_born.year
        return age
    
    @property
    def get_schadmin_username(self):
        schadmin_username = self.user.username
        return schadmin_username


    def __str__(self):
        return self.get_schadmin_full_name

    class Meta:
        ordering = ['first_name']
        verbose_name_plural = 'SchoolAdmins'
        unique_together = ['first_name', 'second_name', 'last_name']
        




###################### Teacher ##################################
class Teacher(AbstractTimeStamp):
    m = 'male'
    f = 'female'
    GENDER_CHOICES = [(m, 'Male'), (f, 'Female'),]

    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    grades = models.ManyToManyField(mod.Grade, null=True,blank=True)
    subjects = models.ManyToManyField(mod.Subject, null=True,blank=True)
    first_name = models.CharField(verbose_name='First Name', max_length=50, null=True, blank=False)
    second_name = models.CharField(verbose_name='Second Name', max_length=50, null=True, blank=False)
    last_name = models.CharField(verbose_name='Last Name', max_length=50, null=True, blank=False)
    email = models.EmailField(verbose_name='Email',max_length=254, null=True, blank=False)
    mobile = models.CharField(verbose_name="your mobile number",
                              max_length=10, null=True, blank=False, validators=[mobile_check])
    gender = models.CharField(verbose_name='Gender', max_length=10,choices=GENDER_CHOICES, null=True, blank=False)
    date_born = models.DateField(verbose_name='Date of Born', null=True, blank=False)
    country_born = models.CharField(verbose_name='Place of Born', max_length=200, null=True, blank=False)
    nationality = models.CharField(verbose_name='Nationality', max_length=200, null=True, blank=False)
    passport_number = models.CharField(verbose_name='Pawssport No.', max_length=50, null=True, blank=False)
    address = models.CharField(verbose_name='Current Address', max_length=200, null=True, blank=False)
    
    skills = models.TextField(verbose_name='Skills',null=True,blank=False)
    
    is_teacher = models.BooleanField(verbose_name='is teacher ?', default=True)
    is_active = models.BooleanField(verbose_name='is active ?', default=True, help_text='is this user active ?')
    
    is_user_done = models.CharField(max_length=20, null=True)
    
    given_username = models.CharField(max_length=20, null=True, blank=True)
    given_password = models.CharField(max_length=20,null=True,blank=True)
    
    created_by = models.ForeignKey(SchoolAdmin, null=True, on_delete=models.CASCADE, related_name='teachers_created_by')
    updated_by = models.ForeignKey(SchoolAdmin, null=True, blank=True,on_delete=models.CASCADE, related_name='teachers_updated_by')
    
    def __str__(self):
        return self.get_teacher_full_name


    @property
    def get_teacher_full_name(self):
        '''Returns the teacher's full name.'''
        return '%s %s %s' % (self.first_name, self.second_name, self.last_name) 
    
    
    @property
    def get_teacher_age(self):
        '''Returns the teachers age.'''
        date_today = date.today()
        age = date_today.year - self.date_born.year
        return age

    
    class Meta:
        ordering = ['first_name']
        verbose_name_plural = 'Teachers'
        unique_together = ['first_name', 'second_name', 'last_name']



    

########################### Parent ###############################################
class Parent(AbstractTimeStamp):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    students = models.ManyToManyField('Student', related_name='parent_set')  
    father_f_name = models.CharField(max_length=200, null=True, blank=False, verbose_name="Father's first name")
    father_l_name = models.CharField(max_length=200, null=True, blank=False,verbose_name="Father's last name")
    father_email = models.EmailField(verbose_name='Father Email', max_length=254, null=True, blank=False)
    father_mobile = models.CharField(verbose_name="Father mobile's number",
                                     max_length=10, null=True, blank=False, validators=[mobile_check])
    father_nationality = models.CharField(verbose_name='Father nationality', max_length=200, null=True, blank=False)
    father_passport_no = models.CharField(verbose_name='Pawssport No.', max_length=50, null=True, blank=False)
    father_address = models.CharField(verbose_name='Current Address', max_length=200, null=True, blank=False)
    

    mother_fl_name = models.CharField(max_length=200, null=True, blank=False, verbose_name="mother's fill name")
    mother_mobile = models.CharField(verbose_name="Mother's mobile number",
                                     max_length=10, null=True, blank=False, validators=[mobile_check])
    note = models.TextField(verbose_name='Note',blank=True, null=True)
    
    is_parent = models.BooleanField(verbose_name='is parent ?', default=True) 
    is_active = models.BooleanField(verbose_name='is active ?', default=True, help_text='is this user active ?')
    
    is_user_done = models.CharField(max_length=20, null=True)
    
    
    given_username = models.CharField(max_length=20, null=True, blank=True)
    given_password = models.CharField(max_length=20, null=True, blank=True)
    
    created_by = models.ForeignKey(SchoolAdmin, null=True, on_delete=models.CASCADE, related_name='parents_created_by')
    updated_by = models.ForeignKey(SchoolAdmin, null=True, blank=True,on_delete=models.CASCADE, related_name='parents_updated_by')


    @property
    def get_father_full_name(self):
        '''Returns the father's full name.'''
        return '%s %s' % (self.father_f_name, self.father_l_name)

    def __str__(self):
        return self.get_father_full_name

    
    
    class Meta:
        ordering = ['father_f_name']
        verbose_name_plural = 'Parents'
        unique_together = ['father_f_name','father_l_name']




##################### Student ##################################
class Student(AbstractTimeStamp):
    m = 'male'
    f = 'female'
    GENDER_CHOICES = [(m, 'Male'), (f, 'Female'), ]

    pr = 'inprogress'
    fin = 'finished'
    STATUS_CHOICES = [(pr, 'In progress'), (fin, 'Finished'), ]

   
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    grade = models.ForeignKey('listings.Grade', verbose_name='Current grade',on_delete=models.CASCADE, null=True, related_name='student_set')
    first_name = models.CharField(verbose_name='First Name', max_length=50, null=True, blank=False)
    second_name = models.CharField(verbose_name='Second Name', max_length=50, null=True, blank=False)
    last_name = models.CharField(verbose_name='Last Name', max_length=50, null=True, blank=False)
    email = models.EmailField(verbose_name='Email',max_length=254, null=True, blank=False)
    mobile = models.CharField(verbose_name="your mobile number",max_length=10, null=True, blank=False, validators=[mobile_check])
    gender = models.CharField(verbose_name='Gender', max_length=10,choices=GENDER_CHOICES, null=True, blank=False)
    status = models.CharField(verbose_name='Status', max_length=10,choices=STATUS_CHOICES, null=True, blank=False)
    date_born = models.DateField(verbose_name='Date of Born', null=True, blank=False)
    country_born = models.CharField(verbose_name='Place of Born', max_length=200, null=True, blank=False)
    nationality = models.CharField(verbose_name='Nationality', max_length=200, null=True, blank=False)
    passport_number = models.CharField(verbose_name='Pawssport No.', max_length=50, null=True, blank=False)
    address = models.CharField(verbose_name='Current Address', max_length=200, null=True, blank=False)
    skills = models.TextField(verbose_name='Skills', null=True, blank=False)
    
    is_student = models.BooleanField(verbose_name='is Student ?', default=True)
    is_active = models.BooleanField(verbose_name='is active ?', default=True, help_text='is this user active ?')
    
    is_user_done = models.CharField(max_length=20,null=True)
    
    given_username = models.CharField(max_length=20, null=True, blank=True)
    given_password = models.CharField(max_length=20, null=True, blank=True)
    
    created_by = models.ForeignKey(SchoolAdmin, null=True, on_delete=models.CASCADE, related_name='students_created_by')
    updated_by = models.ForeignKey(SchoolAdmin, null=True, blank=True,on_delete=models.CASCADE, related_name='students_updated_by')

    

    @property
    def get_student_full_name(self):
        '''Returns the student's full name.'''
        return '%s %s %s' % (self.first_name, self.second_name, self.last_name)

    @property
    def get_student_age(self):
        '''Returns the student's age.'''
        date_today = date.today()
        age = date_today.year - self.date_born.year
        return age
    
    def __str__(self):
        return self.get_student_full_name

    def get_absolute_url(self):
        return reverse('listings:student_detail', kwargs={'student_username': self.given_username})
    
    


    class Meta:
        ordering = ['first_name','grade']
        verbose_name_plural = 'Students'
        unique_together = ['first_name', 'second_name', 'last_name']



######################## TEACHER Message TO STUDENT ############
class MessageTeacherToStudent(AbstractTimeStamp):
    teacher = models.ForeignKey(Teacher, verbose_name='Teacher',on_delete=models.CASCADE, null=True, blank=False)
    student = models.ForeignKey(Student,verbose_name='Student', on_delete=models.CASCADE, null=True, blank=False)
    message_subject = models.CharField(verbose_name='Message Subject', max_length=50, null=True, blank=False)
    message_text = models.TextField(verbose_name='',null=True, blank=False)
 
    def __str__(self):
        return "Message from {}".format(self.teacher)

    class Meta :
        ordering = ['-created_at']

##############################################################


######################## TEACHER Message TO STUDENT ############
class MessageTeacherToGrade(AbstractTimeStamp):
    teacher = models.ForeignKey(Teacher, verbose_name='Teacher', on_delete=models.CASCADE, null=True, blank=False)
    grade = models.ForeignKey('listings.Grade', verbose_name='Grade', on_delete=models.CASCADE, null=True, blank=False)
    message_subject = models.CharField(verbose_name='Message Subject', max_length=50, null=True, blank=False)
    message_text = models.TextField(verbose_name='', null=True, blank=False)

    def __str__(self):
        return "Message from {}".format(self.teacher)

    class Meta:
        ordering = ['-created_at']

##############################################################




##################### Employee ##################################
class Employee(AbstractTimeStamp):
     pass
