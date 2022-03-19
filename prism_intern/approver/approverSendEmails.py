from django.core.mail import send_mail
from django.conf import settings

def apprsendemails(subject,message,to):
    send_mail(subject,message,
        'rangujyothisri@gmail.com',
        [to],
        fail_silently=False,
    )