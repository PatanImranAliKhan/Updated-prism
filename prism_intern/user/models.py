from django.db import models

# Create your models here.

class user(models.Model):
    username=models.CharField(max_length=60)
    email=models.CharField(max_length=60,primary_key=True)
    mobile=models.BigIntegerField()
    profilepic=models.ImageField(upload_to='profilepics/', default='profilepics\defaultpicimg.png')
    bio=models.TextField(blank=True,default="")
    password=models.CharField(max_length=255)