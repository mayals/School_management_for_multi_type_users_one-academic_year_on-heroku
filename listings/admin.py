from django.contrib import admin
from .models import Grade, Subject, Salary, Mark, GradeAttendance

admin.site.register(GradeAttendance)
admin.site.register(Grade)
admin.site.register(Salary)
admin.site.register(Mark)

class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'grade']
    list_display_links = ['grade']
    search_fields = ['title', 'grade']
    class Meta:
       model = Subject
        
admin.site.register(Subject, SubjectAdmin)
