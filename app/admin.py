from django.contrib import admin
from .models import MembersModel, ServicesModel

admin.site.register(MembersModel)
admin.site.register(ServicesModel)