from django import forms
from .models import Approver
from django.forms import TextInput, PasswordInput,NumberInput,EmailInput, FileInput, IntegerField, Select

class ApproverForm(forms.ModelForm):
    class Meta:
        model=Approver
        fields='__all__'
        widgets={
            'username': TextInput(attrs={'type':'text','placeholder':'User Name','class':'form-control','name':'username'}),
            'email': EmailInput(attrs={'type':'email','placeholder':'example@gmail.com','class':'form-control','name':'email'}),
            'mobile': NumberInput(attrs={'type':'tel','placeholder':'PhoneNumber','class':'form-control','name':'mobile'}),
            'password': PasswordInput(attrs={'type':'password','placeholder':'Password','class':'form-control','name':'password'}),
            'category': Select(attrs={'class':'form-control','name':'category'})
        }