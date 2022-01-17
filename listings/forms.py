from django import forms 
from listings.models import Grade, Subject, Mark, Salary, GradeAttendance
from users.models import Student
from bootstrap_datepicker_plus.widgets import DatePickerInput



############################ grade form to add grade  #######################################
class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['name', 'description']
#################################################################







########### form as student list to  multiplechoice only attendace students for selected grade ################################################
class GradeAttendanceForm(forms.ModelForm):
    students = forms.ModelMultipleChoiceField(queryset=Student.objects.all(),required=True)
    class Meta:
        model = GradeAttendance
        fields = ['att_date', 'students']
        widgets = {
            # specify date-format
            'att_date': DatePickerInput(format='%Y-%m-%d'),
        }
#################################################################






###################################### SubjectForm #######################################################
class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['title', 'grade', 'description', 'note']
#################################################################






###################################### MarkForm #################################
class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ['exam_name','mark_value','full_value', 'exam_date', 'note']
        widgets = {
            # specify date-format
            'exam_date': DatePickerInput(format='%Y-%m-%d'),
        }

   





###################################### EmailForm #################################
# https://docs.djangoproject.com/en/3.2/topics/forms/#more-on-fields
class EmailForm(forms.Form):
    # subject = forms.CharField(label='', max_length=100,placeholder='Subject')
    # message = forms.CharField(widget=forms.Textarea)
    # sender = forms.EmailField()
    # cc_myself = forms.BooleanField(required=False)

    subject = forms.CharField(max_length=100, label="", required=True,
                                # help_text='please enter Email Subject',
                                error_messages={
                                            'required': 'reqired Subject'},

                                widget=forms.TextInput(attrs={
                                            'placeholder': 'Subject here ..',
                                            'class': 'form-control'})
                                )

    sender = forms.EmailField(max_length=255, label="", required=True,
                              error_messages={'required': 'required email'},
                              widget=forms.TextInput(attrs={
                                  'placeholder': 'Your Email here ..',
                                  'class': 'form-control'})
                              )


    message = forms.CharField(label="", widget=forms.Textarea(attrs={'cols':'15',
                                                                      'rows': 5,
                                                                'placeholder': 'Explain your problem here ..',
                                                                'class': 'form-control', })
                                                                 )
    
    cc_myself = forms.BooleanField(required=False)
#################################################################
                                                                                        
