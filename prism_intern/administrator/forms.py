from PIL import Image
from django import forms
from django.core.files import File
from .models import Photo
from django.forms import TextInput,NumberInput,EmailInput
from .models import Feedback

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('samsung_image','apple_image','oneplus_image', 'email','uploaded_date','uploaded_time','competator1_name','competator2_name')
        # form.fields['field_name'].widget = forms.HiddenInput()
        widgets={
            'email':forms.HiddenInput(),
            'uploaded_date':forms.HiddenInput(),
            'uploaded_time':forms.HiddenInput(),
        }


class FeedbackForm(forms.ModelForm):
    class Meta:
        model=Feedback
        fields='__all__'
        widgets={
            'name':TextInput(attrs={'type':'text','placeholder':'Username','class':'form-control form-control-md','name':'name'}),
            'email':EmailInput(attrs={'type':'email','placeholder':'example@gmail.com','class':'form-control form-control-md','name':'email'}),
            'mobile': NumberInput(attrs={'type':'tel','placeholder':'PhoneNumber','class':'form-control form-control-md','name':'mobile'}),
            'feedback':forms.Textarea(attrs={'type':'text','placeholder':'Enter your Feedback...','class':'form-control form-control-md','name':'feedback','rows':'5'}),
        }
