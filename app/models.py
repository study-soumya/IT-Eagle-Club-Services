from django.db import models
from django.contrib.auth.models import User
from froala_editor.fields import FroalaField
from .helpers import *

class MembersModel(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Full Name')
    username = models.CharField(max_length=20, default="")
    company_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Company')
    job_title = models.CharField(max_length=100, blank=True, null=True, verbose_name='Job Title')
    job_designation = models.CharField(max_length=100, blank=True, null=True, verbose_name='Designation')
    work_experience = models.CharField(max_length=100, blank=True, null=True, verbose_name="Experience")
    email = models.EmailField(max_length=254, verbose_name='email address')
    description = FroalaField()
    profile_image = models.ImageField(upload_to='profile')
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    def get_short_name(self):
        return self.username
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = generate_slug(self.name)
        super(MembersModel, self).save(*args, **kwargs)
        

class ServicesModel(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    icon = models.CharField(max_length=100, blank=True, null=True)
    description = FroalaField()
    image = models.ImageField(upload_to='services')
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = generate_slug(self.title)
        super(ServicesModel, self).save(*args, **kwargs)