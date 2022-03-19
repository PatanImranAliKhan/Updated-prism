from PIL import Image
from django import forms
from django.core.files import File
from .models import Photo
from django.forms import TextInput,NumberInput,EmailInput
from .models import Feedback

class PhotoForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = Photo
        fields = ('file', 'x', 'y', 'width', 'height', 'email','uploaded_date','uploaded_time',)
        # form.fields['field_name'].widget = forms.HiddenInput()
        widgets={
            'email':forms.HiddenInput(),
            'uploaded_date':forms.HiddenInput(),
            'uploaded_time':forms.HiddenInput(),
        }

    def save(self):
        photo = super(PhotoForm, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(photo.file)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
        resized_image.save(photo.file.path)
        return photo


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
