from django.db import models

# Create your models here.
assignchoices=(('False','False'),('True','True'))
categories=(('hdr','hdr'),('beauty','beauty'),('bokeh','bokeh'),('light','light'))
class Approver(models.Model):
    username=models.CharField(max_length=60)
    email=models.CharField(max_length=60,primary_key=True)
    mobile=models.BigIntegerField()
    password=models.CharField(max_length=255)
    profilepic=models.ImageField(upload_to='profilepics/', default='profilepics\defaultpicimg.png')
    bio=models.TextField(blank=True)
    assign=models.CharField(max_length=10,choices=assignchoices,default="False",blank=True)
    assignments_done=models.IntegerField(blank=True,default=0)