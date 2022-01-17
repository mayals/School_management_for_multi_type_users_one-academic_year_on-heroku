from django.db.models import Avg
from django.db import models
from django.db.models.fields.related import ManyToManyField
from django.shortcuts import get_object_or_404
from helpers.models import AbstractTimeStamp
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
### circular import issues ### solving
# https://www.pythonpool.com/python-circular-import/
from users import models as users_model


######################## Grade ###################################
class Grade(AbstractTimeStamp):
    name = models.CharField(verbose_name ='Grade name',max_length=200, unique=True, null=True, blank=False)                 
    description = models.CharField(verbose_name='Describtion', max_length=200, null=True, blank=False)
    slug = models.CharField(verbose_name='Grade slug',max_length=200, unique=True, null=True, blank=True)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('listings:grade_detail', kwargs={'grade_slug': self.slug})

    class Meta:
        ordering = [ '-created_at']
        verbose_name_plural = 'Grades'

    def get_teachers_for_grade(self):
        teachers_grade = users_model.Teacher.objects.all().filter(grades=self)
        return teachers_grade
    
    def get_students_for_grade(self):
        students_grade = users_model.Student.objects.all().filter(grade=self)
        return students_grade

    def get_students_for_grade_count(self):
        students_grade_count = users_model.Student.objects.all().filter(grade=self).count()
        return students_grade_count
    
    def get_subjects_for_grade(self):
        subjects_grade = Subject.objects.all().filter(grade=self)
        return subjects_grade


    def save(self,*args,**kwargs):
        if not self.slug :
            self.slug = slugify(self.name)
        
        super(Grade,self).save(*args,**kwargs)
    
    
   

####################### grade attendance ##########################################
class GradeAttendance(AbstractTimeStamp):
    att_date = models.DateField(verbose_name='Date of Attendance', null=True, blank=False)
    grade = models.ForeignKey(Grade, null=True, on_delete=models.CASCADE)
    students = models.ManyToManyField('users.Student', blank=True, null=True, verbose_name="list of students")
    created_by = models.ForeignKey('users.Teacher', on_delete=models.CASCADE, null=True, blank=False, related_name='att_author')
                                  
   
    def get_absolute_url(self):
        return reverse("listings:grade_attendanc_create", kwargs={"grade_slug": self.grade})
    
    
    def __str__(self):
        return str('Attendace for grade ( {} ) - at {}'.format(self.grade,self.att_date))

    class Meta:
        ordering = ['-created_by']
     
    
    

    
    

######################## Subject ###################################
class Subject(AbstractTimeStamp):
    grade = models.ForeignKey(Grade, null=True, on_delete=models.CASCADE, related_name='g_subjects')
    title = models.CharField(max_length=200, null=True, blank=False)
    slug = models.CharField(max_length=50, verbose_name='Subject slug', unique=True, null=True, blank=True)
    description = models.CharField(max_length=200, unique=False, null=True, blank=True)
    note = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return '%s - %s' % (self.title, self.grade)


    class Meta:
        ordering = ['grade', 'title']
        verbose_name_plural = 'Subjects'
        unique_together = ['title','grade']
    

    def get_subject_full_title(self):
        "Returns the subject's full title."
        return '%s - %s' % (self.title,self.grade)


    def get_marks_for_subject(self):
        marks_subject = Mark.objects.all().filter(subject=self)
        return marks_subject

    def get_average_of_marks_for_subject(self):
        marks_subject_avarage = Mark.objects.all().filter(subject=self).aggregate(marks_average_of_subject=Avg('mark_value'))
        return marks_subject_avarage

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = str(slugify(self.title)+'-'+slugify(self.grade))
        super(Subject, self).save(*args, **kwargs)

   


    


########################  Mark  ###############################################33
ft = 'First Term'
st = 'Second Term'
final = 'Final'

EX_NAME_CHOICES = [
        (ft,'First Term'),
        (st,'Second Term'),
        (final,'Final'), 
        ]
class Mark(AbstractTimeStamp):
    subject = models.ForeignKey('Subject', null=True, on_delete=models.CASCADE, related_name='marks_sub')
    student = models.ForeignKey('users.Student', null=True, on_delete=models.CASCADE,related_name ='mark_set')
    exam_name = models.CharField(verbose_name='Exam Name', max_length=20, choices=EX_NAME_CHOICES, null=True, blank=False)
    mark_value = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    full_value = models.DecimalField(max_digits=4, decimal_places=1, null=True)
    exam_date = models.DateTimeField(null=True)
    note = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey('users.Teacher', null=True, on_delete=models.CASCADE, related_name='marks_created_by')
    # grade = models.ForeignKey('Grade', null=True, on_delete=models.CASCADE, related_name='marks_gr')
    
    
    def __str__(self):
        return str('{} - mark of -  {}/{}'.format(self.student, self.exam_name, self.subject))

    class Meta:
        ordering = [ 'student', '-exam_date']
        verbose_name_plural = 'Marks'
        unique_together = ['exam_name', 'subject','student']

    




# not used yet !
######################## Salary ###################################
class Salary(AbstractTimeStamp):
    teacher = models.ForeignKey('users.Teacher', verbose_name='Salary of Teacher', null=True,on_delete=models.CASCADE)
    date = models.DateField(verbose_name='Date of salary',null=True, blank=False, default=timezone.now)
    amount = models.DecimalField(verbose_name='amount of salary', max_digits=8, decimal_places=2, null=True, blank=False)

    def __str__(self):
        return str('{} - salary of -  {}/{}'.format(self.teacher, self.date.month, self.date.year))

    class Meta:
        ordering = [ '-created_at']
        verbose_name_plural = 'Salaries'
