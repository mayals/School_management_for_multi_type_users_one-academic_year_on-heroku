from django.db import models



class AbstractTimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False, null=True,blank=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True, null=True, blank=False)

    class Meta:
        abstract = True
        

       
