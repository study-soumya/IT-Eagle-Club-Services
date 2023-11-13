from django import forms
from froala_editor.widgets import FroalaEditor

from .models import *


class MemberForm(forms.ModelForm):
    class Meta:
        model = MembersModel
        fields = ['description']
        
class ServiceForm(forms.ModelForm):
    class Meta:
        model = ServicesModel
        fields = ['description']