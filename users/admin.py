from django.contrib import admin
from .models import SchoolAdmin, Teacher, Student, Parent, ImageUser, AcademicYear, MessageTeacherToStudent, MessageTeacherToGrade

admin.site.register(SchoolAdmin)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Parent)
admin.site.register(ImageUser)
admin.site.register(AcademicYear)
admin.site.register(MessageTeacherToStudent)
admin.site.register(MessageTeacherToGrade)

