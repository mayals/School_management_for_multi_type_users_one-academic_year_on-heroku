# https: // betterprogramming.pub/django-quick-tips-context-processors-da74f887f1fc

from django.shortcuts import get_object_or_404
from .models import AcademicYear


def add_variable_to_context(request):
    academicyears = AcademicYear.objects.all()
    
    return {
            'academicyears': academicyears,
            
        }
