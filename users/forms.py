from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import SchoolAdmin, Teacher, Student, Parent, ImageUser, AcademicYear, MessageTeacherToStudent, MessageTeacherToGrade
from django.forms import inlineformset_factory

## https: // pypi.org/project/django-bootstrap-datepicker-plus / 
## https: // monim67.github.io/django-bootstrap-datepicker-plus/configure / 
# from bootstrap_datepicker_plus import DatePickerInput
from bootstrap_datepicker_plus.widgets import DatePickerInput


class AcademicYearForm(forms.ModelForm):


    class Meta:
        model = AcademicYear
        fields = ['start_date','end_date']
        widgets = {
                    # specify date-format
                    'start_date': DatePickerInput(format='%Y-%m-%d'),
                    'end_date': DatePickerInput(format='%Y-%m-%d'),
                  }

    
   
######################################################################################3
class ImageUserForm(forms.ModelForm):
    class Meta:
        model = ImageUser
        fields = ['image']


class LoginForm(forms.ModelForm):
    username = forms.CharField(max_length=20,
                               required=True,
                               label='',
                               error_messages={
                                   'required': 'username must no be empty'},
                               widget=forms.TextInput(attrs={
                                   'placeholder': 'Enter username',
                                   'class': 'form-control'
                               })
                               )

    password = forms.CharField(required=True,
                               label='',
                               error_messages={
                                   'required': 'required password'},
                               widget=forms.PasswordInput(attrs={
                                   'placeholder': 'Enter password',
                                   'class': 'form-control',
                               })
                               )

    class Meta:
        model = User
        fields = ['username', 'password']





########################### SchoolAdminUserCreateForm ################################################################
class SchoolAdminUserCreateForm(UserCreationForm):
    username = forms.CharField(max_length=100, label='username', required=True,
                               help_text='no space allowed in username',
                               error_messages={'required': 'username must no be empty',
                                               'unique': 'OPS! this username is used before!'},
                               widget=forms.TextInput(attrs={
                                   'placeholder': 'username here ..',
                                   'class': 'form-control'})
                               )
    class Meta:
        model = User
        fields = ['username','password1','password2']

   

#################################### SchoolAdminUserExtentionCreateForm ############################################
class SchoolAdminUserExtentionCreateForm(forms.ModelForm):

        first_name = forms.CharField(max_length=15, label="First Name", required=True,
                                        help_text='please enter english alphabetics only for First name',
                                        error_messages={
                                            'required': 'reqired first name'},
                                        widget=forms.TextInput(attrs={
                                            'placeholder': 'First Name here ..',
                                            'class': 'form-control'})
                                        )

        last_name = forms.CharField(max_length=15, label="Last Name", required=True,
                                help_text='please enter english alphabetics only for Last Name',
                                error_messages={
                                    'required': 'reqired last name'},
                                widget=forms.TextInput(attrs={
                                    'placeholder': 'Last Name here ..',
                                    'class': 'form-control'})
                                )


        email = forms.EmailField(max_length=255, label="Email", required=True,
                                 error_messages={'required': 'required email'},
                                 widget=forms.TextInput(attrs={
                                     'placeholder': 'Email here ..',
                                     'class': 'form-control'})
                                 )
        
        second_name = forms.CharField(max_length=15, label="Second Name", required=True,
                                        help_text='please enter english alphabetics only for Second Name',
                                        error_messages={
                                          'required': 'reqired second name'},
                                        widget=forms.TextInput(attrs={
                                          'placeholder': 'second Name here ..',
                                          'class': 'form-control'})
                                        )

        mobile = forms.CharField(max_length=10, label="Mobile", required=True,
                                 help_text="Please enter mobile number long of 10 numbers and start with '050 or 055 or 053'",
                                 error_messages={
                                     'required': 'reqired mobile number'},
                                 widget=forms.TextInput(attrs={
                                     'placeholder': 'Mobile number here ..',
                                     'class': 'form-control'})
                                 )

        skills = forms.CharField(widget=forms.Textarea(attrs={'cols': '20',
                                                                   'rows': 10,
                                                      'placeholder': 'write your skills here ..',
                                                      'class': 'form-control',}
                                                           ))
 
      



        
        

        class Meta:
            model = SchoolAdmin
            fields = ['first_name', 'second_name', 'last_name',
                        'email', 'mobile','gender',
                        'date_born', 'country_born', 'nationality',
                        'passport_number', 'address', 'skills',
                        'is_schadmin', 'is_active', 'is_superuser', 'is_staff']

            
            widgets = {
                # specify date-frmat
                'date_born': DatePickerInput(format='%Y-%m-%d'),
            }




            



################ Teacher form ############################################
class TeacherUserCreateForm(forms.ModelForm):
        first_name = forms.CharField(max_length=15, label="First Name", required=True,
                                     help_text='please enter english alphabetics only for First name',
                                     error_messages={
                                         'required': 'reqired first name'},
                                     widget=forms.TextInput(attrs={
                                         'placeholder': 'First Name here ..',
                                         'class': 'form-control'})
                                     )

        last_name = forms.CharField(max_length=15, label="Last Name", required=True,
                                help_text='please enter english alphabetics only for Last Name',
                                error_messages={
                                    'required': 'reqired last name'},
                                widget=forms.TextInput(attrs={
                                    'placeholder': 'Last Name here ..',
                                    'class': 'form-control'})
                                )


        email = forms.EmailField(max_length=255, label="Email", required=True,
                                 error_messages={'required': 'required email'},
                                 widget=forms.TextInput(attrs={
                                     'placeholder': 'Email here ..',
                                     'class': 'form-control'})
                                 )
        
        second_name = forms.CharField(max_length=15, label="Second Name", required=True,
                                      help_text='please enter english alphabetics only for Second Name',
                                      error_messages={
                                          'required': 'reqired second name'},
                                      widget=forms.TextInput(attrs={
                                          'placeholder': 'second Name here ..',
                                          'class': 'form-control'})
                                      )

        mobile = forms.CharField(max_length=10, label="Mobile", required=True,
                                 help_text="Please enter mobile number long of 10 numbers and start with '050 or 055 or 053'",
                                 error_messages={
                                     'required': 'reqired mobile number'},
                                 widget=forms.TextInput(attrs={
                                     'placeholder': 'Mobile number here ..',
                                     'class': 'form-control'})
                                 )

        skills = forms.CharField(widget=forms.Textarea(attrs={'cols': '20',
                                                                   'rows': 10,
                                                      'placeholder': 'write your skills here ..',
                                                      'class': 'form-control',}
                                                           ))
       
        
            
        
        
       
        

        class Meta:
            model = Teacher
            fields = ['first_name', 'second_name', 'last_name',
                        'email', 'mobile','gender',
                        'date_born', 'country_born', 'nationality',
                        'passport_number', 'address', 'skills',
                        'is_teacher', 'is_active','grades','subjects']
                        
            widgets = {
                # specify date-frmat
                'date_born': DatePickerInput(format='%Y-%m-%d'),
            }






################ Student form ############################################
class StudentUserCreateForm(forms.ModelForm): 
    first_name = forms.CharField(max_length=15, label="First Name", required=True,
                                 help_text='please enter english alphabetics only for First name',
                                 error_messages={
                                     'required': 'reqired first name'},
                                 widget=forms.TextInput(attrs={
                                     'placeholder': 'First Name here ..',
                                     'class': 'form-control'})
                                 )

    last_name = forms.CharField(max_length=15, label="Last Name", required=True,
                                help_text='please enter english alphabetics only for Last Name',
                                error_messages={
                                    'required': 'reqired last name'},
                                widget=forms.TextInput(attrs={
                                    'placeholder': 'Last Name here ..',
                                    'class': 'form-control'})
                                )

    email = forms.EmailField(max_length=255, label="Email", required=True,
                             error_messages={'required': 'required email'},
                             widget=forms.TextInput(attrs={
                                 'placeholder': 'Email here ..',
                                 'class': 'form-control'})
                             )

    second_name = forms.CharField(max_length=15, label="Second Name", required=True,
                                  help_text='please enter english alphabetics only for Second Name',
                                  error_messages={
                                      'required': 'reqired second name'},
                                  widget=forms.TextInput(attrs={
                                      'placeholder': 'second Name here ..',
                                      'class': 'form-control'})
                                  )

    mobile = forms.CharField(max_length=10, label="Mobile", required=True,
                             help_text="Please enter mobile number long of 10 numbers and start with '050 or 055 or 053'",
                             error_messages={
                                 'required': 'reqired mobile number'},
                             widget=forms.TextInput(attrs={
                                 'placeholder': 'Mobile number here ..',
                                 'class': 'form-control'})
                             )

    

    class Meta:
        model = Student
        fields = ['first_name', 'second_name', 'last_name', 'grade',
                  'email', 'mobile', 'gender','status','skills',
                  'date_born', 'country_born', 'nationality',
                  'passport_number', 'address',
                  'is_student', 'is_active']

        widgets = {
            # specify date-frmat
            'date_born': DatePickerInput(format='%Y-%m-%d'),
        }




################ Teacher form ############################################
class ParentUserCreateForm(forms.ModelForm):
    father_f_name = forms.CharField(max_length=15, label="Father First Name", required=True,
                                 help_text='please enter english alphabetics only for First name',
                                 error_messages={
                                     'required': 'reqired first name'},
                                 widget=forms.TextInput(attrs={
                                     'placeholder': 'Father First Name here ..',
                                     'class': 'form-control'})
                                 )

    father_l_name = forms.CharField(max_length=15, label="Father Last Name", required=True,
                                help_text='please enter english alphabetics only for Last Name',
                                error_messages={
                                    'required': 'reqired last name'},
                                widget=forms.TextInput(attrs={
                                    'placeholder': 'Father Last Name here ..',
                                    'class': 'form-control'})
                                )

    father_email = forms.EmailField(max_length=255, label="Father Email", required=True,
                             error_messages={'required': 'required email'},
                             widget=forms.TextInput(attrs={
                                 'placeholder': 'Father Emai here ..',
                                 'class': 'form-control'})
                             )

    father_mobile = forms.CharField(max_length=10, label="Father Mobile", required=True,
                                             help_text="Please enter mobile number long of 10 numbers and start with '050 or 055 or 053'",
                                             error_messages={
                                                 'required': 'reqired mobile number'},
                                             widget=forms.TextInput(attrs={
                                                 'placeholder': 'Father Mobile here ..',
                                                 'class': 'form-control'})
                                             )

    mother_mobile = forms.CharField(max_length=10, label="Mother Mobile", required=True,
                                    help_text="Please enter mobile number long of 10 numbers and start with '050 or 055 or 053'",
                                    error_messages={
                                        'required': 'reqired mobile number'},
                                    widget=forms.TextInput(attrs={
                                        'placeholder': 'Mother Mobile here ..',
                                        'class': 'form-control'})
                                    )
    
    note = forms.CharField(widget=forms.Textarea(attrs={'cols': '20',
                                                          'rows': 10,
                                                          'placeholder': 'write parent notes here ..',
                                                          'class': 'form-control', }
                                                   ))

    

    class Meta:
        model = Parent
        fields = ['students', 'father_f_name', 'father_l_name',
                  'father_email','father_mobile', 'father_nationality',
                  'father_passport_no', 'father_address', 'mother_fl_name',
                  'mother_mobile', 'note', 'is_active',
                  'is_parent']

        
######################## MessageTeacherToStudent #######################################
class MessageTeacherToStudentForm(forms.ModelForm):
    message_text = forms.CharField(label ='',widget=forms.Textarea(attrs={'cols': '20',
                                                         'rows': 10,
                                                         'placeholder': 'Your message here ..',
                                                         'class': 'form-control', }
                                                  ))
    class Meta:
        model = MessageTeacherToStudent
        fields = ['message_subject','message_text']


######################## MessageTeacherToStudent #######################################
class MessageTeacherToGradeForm(forms.ModelForm):
    message_text = forms.CharField(label='', widget=forms.Textarea(attrs={'cols': '20',
                                                                          'rows': 10,
                                                                          'placeholder': 'Your message here ..',
                                                                          'class': 'form-control', }
                                                                   ))

    class Meta:
        model = MessageTeacherToGrade
        fields = ['message_subject', 'message_text']
