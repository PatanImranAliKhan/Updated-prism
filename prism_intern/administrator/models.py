from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

hdr_choice = (('shade','shade'),('building','building'),('bright_light','bright_light'),('back_light','back_light'))
beauty_choice = (("female","female"),('male','male'))
bokeh_choice = (('default','default'),('Max','Max'))
low_choice = (('flash_ON','flash_ON'),('Flash_OFF','Flash_OFF'))


class hdrReview(models.Model):
    email=models.CharField(max_length=100)
    review=models.TextField()
    photo_id=models.IntegerField()
    save_mode=models.BooleanField(default=False)
    photo_edited=models.BooleanField(default=False)

class beautyReview(models.Model):
    email=models.CharField(max_length=100)
    review=models.TextField()
    photo_id=models.IntegerField()
    save_mode=models.BooleanField(default=False)
    photo_edited=models.BooleanField(default=False)

class bokehReview(models.Model):
    email=models.CharField(max_length=100)
    review=models.TextField()
    photo_id=models.IntegerField()
    save_mode=models.BooleanField(default=False)
    photo_edited=models.BooleanField(default=False)

class lightReview(models.Model):
    email=models.CharField(max_length=100)
    review=models.TextField()
    photo_id=models.IntegerField()
    save_mode=models.BooleanField(default=False)
    photo_edited=models.BooleanField(default=False)

class Review(models.Model):
    email=models.CharField(max_length=100)
    review=models.TextField()
    photo_id=models.IntegerField()
    save_mode=models.BooleanField(default=False)
    photo_edited=models.BooleanField(default=False)

class editReview(models.Model):
    email=models.CharField(max_length=100)
    review=models.TextField()
    category=models.CharField(max_length=100)
    photo_id=models.IntegerField()

class FileEditable(models.Model):
    samsung_image = models.ImageField()
    apple_image = models.ImageField()
    oneplus_image = models.ImageField()
    uploaded_date=models.DateField()
    review=models.TextField(blank=True)
    photo_id=models.IntegerField()

class Photo(models.Model):
    samsung_image = models.ImageField(upload_to='samsung_images/')
    competator1_name=models.CharField(max_length=100)
    apple_image = models.ImageField(upload_to='competator1_images/')
    competator2_name=models.CharField(max_length=100)
    oneplus_image = models.ImageField(upload_to='competator2_images/')
    email=models.CharField(max_length=60)
    uploaded_date=models.DateField()
    uploaded_time=models.TimeField()
    is_edited=models.BooleanField(default=False)
    is_deleted=models.BooleanField(default=False)

    class Meta:
        verbose_name = 'photo'
        verbose_name_plural = 'photos'

class Feedback(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    mobile=models.BigIntegerField()
    rate=models.IntegerField(default=1)
    feedback=models.TextField()
