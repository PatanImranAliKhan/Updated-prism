from django.contrib import admin

# Register your models here.
from .models import Photo, Feedback

admin.site.register(Photo)
admin.site.register(Feedback)