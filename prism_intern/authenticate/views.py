from sqlite3 import Date
from django.shortcuts import render
from django.shortcuts import redirect
from administrator.forms import FeedbackForm
from approver.models import Approver
from approver.forms import ApproverForm
from user.models import user
from user.forms import UserForm
from datetime import datetime
from django.core.mail import send_mail
from .sendingEmails import sendemails

from django.contrib.auth.hashers import make_password, check_password
import random
import string


def CheckData(request):
    try:
        a=request.session['username']
        print(a)
        if a is None:
            return None
        else:
            pro=request.session['profession']
            return pro
    except:
        return None

def HomePage(request):
    return render(request,'home.html')

def AboutPage(request):
    return render(request,'about.html')

def ContactPage(request):
    cform=FeedbackForm()
    if request.method=="POST":
        cform=FeedbackForm(request.POST)
        if cform.is_valid():
            cform.save()
            cform=FeedbackForm()
            return render(request, 'contact.html',{'form':cform,'message':'Feedback has been sent successfull'})
        return render(request, 'contact.html',{'form':cform,'error':'Fill All the details correctly'})
    return render(request,'contact.html',{'form':cform})

def LoginPage(request):
    if request.method=="POST":
        email=request.POST['email']
        password=request.POST['password']
        if email=="admin@gmail.com" and password=="admin":
            return redirect("adm_home")
        try:
            category=request.POST['category']
        except:
            return render(request,'login.html',{'error':'Please select the category'}) 
        if(category==None):
            return render(request,'login.html',{'error':'Please select the category'})
        if category=="user":
            try:
                u=user.objects.get(email=email)
                pa=u.password
                if check_password(password, pa):
                    AddSession(request, u)
                    request.session['profession']='user'
                    return redirect('user_home')
                else:
                    return render(request,'login.html',{'error':'invalid password'})
            except:
                return render(request,'login.html',{'error':'invalid email or password'})
        else:
            try:
                a=Approver.objects.get(email=email)
                pa=a.password
                if check_password(password, pa):
                    print(a)
                    if a.assign=="True":
                        AddSession(request, a)
                        request.session['profession']='approver'
                        return redirect('appr_home')
                    else:
                        return render(request, 'invaliduser.html')
                else:
                    return render(request,'login.html',{'error':'invalid password'})
            except:
                return render(request,'login.html',{'error':'invalid email or password'})
    return render(request,'login.html')

def AddSession(request,detail):
    request.session['username']=detail.username
    request.session['email']=detail.email
    request.session['mobile']=detail.mobile

def registerPage(request):
    return render(request,'register/registration.html')

def UserRegistration(request):
    uform=UserForm()
    if request.method=="POST":
        request.POST._mutable = True
        request.POST['password'] = make_password(request.POST['password'],None, 'default')
        uform=UserForm(request.POST)
        if uform.is_valid():
            uform.save()
            request.session['username']=request.POST['username']
            request.session['email']=request.POST['email']
            request.session['mobile']=request.POST['mobile']
            request.session['profession']='user'
            html_data='Hi '+request.POST['username']+', you have successfully registered'
            sendemails('Successfully Registered',html_data,request.POST['email'])
            uform=UserForm()
            return redirect('user_home')
        return render(request, 'register/user_register.html',{'form':uform,'error':'something entered wrong'})
    return render(request, 'register/user_register.html',{'form':uform})

def ApproverRegistration(request):
    form=ApproverForm()
    if request.method=="POST":
        request.POST._mutable = True
        request.POST['password'] = make_password(request.POST['password'],None, 'default')
        aform=ApproverForm(request.POST)
        if aform.is_valid():
            aform.save()
            html_data='Hi '+request.POST['username']+', you have been added as an approver'
            sendemails('Successfully Registered',html_data,request.POST['email'])
            return render(request, 'invaliduser.html')
        aform=ApproverForm()
        return render(request, 'register/appr_register.html',{'form':aform,'error':'something entered wrong'})
    return render(request, 'register/appr_register.html',{'form':form})

def Profile(request):
    return render(request,'profile.html')

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def ForgotPasswordPage(request):
    if request.method=="POST":
        email = request.POST['email']
        category = request.POST['category']
        if(email is None or category==""):
            return render(request, 'forgot-password-verify-email.html',{'error':'please fill all the details'})
        try:
            if category=="user":
                u = user.objects.get(email=email)
            else:
                app = Approver.objects.get(email=email)
            rndm_str = get_random_string(4)
            request.session['forgot_password_email']=email
            request.session['forgot_password_otp']=rndm_str
            request.session['forgot_password_category']=category

            now = datetime.now()
            current_time = now.strftime("%d/%m/%Y %H:%M:%S")
            request.session['forgot_password_time_allot'] = current_time

            send_mail(
                'OTP for change password',
                'Otp : '+rndm_str,
                'rangujyothisri@gmail.com',
                [email],
                fail_silently=False,
            )

            return redirect('changepassword')
        except Exception as e:
            print(e)
            return render(request, 'forgot-password-verify-email.html',{'error':'This Email has not created an account'})
    return render(request, 'forgot-password-verify-email.html')

def ChangePasswordPage(request):
    if request.method=="POST":
        now = datetime.now()
        current_time = now.strftime("%d/%m/%Y %H:%M:%S")
        allot_time = datetime.strptime(request.session['forgot_password_time_allot'],'%d/%m/%Y %H:%M:%S')
        print(current_time)
        print(allot_time)
        dif = now-allot_time
        dif_in_sec = dif.seconds
        if(dif_in_sec>1200):
            return render(request, 'forgot-password-verify-email.html',{'error':'Time out Please try again'})
        otp = request.POST['otp']
        category = request.POST['category']
        password = request.POST['password']
        if(otp is None or category is None or password is None):
            return render(request, 'change-password.html',{'error':'Please fill all the details'})
        original_otp = request.session['forgot_password_otp']
        original_category = request.session['forgot_password_category']
        if(otp!=original_otp):
            return render(request, 'change-password.html',{'error':'incorrect OTP'})
        if(category!=original_category):
            return render(request, 'change-password.html',{'error':'incorrect category'})
        original_email = request.session['forgot_password_email']
        try:
            if(category=="user"):
                u = user.objects.get(email=original_email)
                u.password = make_password(password,None, 'default')
                u.save()
                return render(request, 'change-password.html',{'message':'Password has been changed'})
            else:
                appr = Approver.objects.get(email=original_email)
                appr.password = make_password(password,None, 'default')
                appr.save()
                return render(request, 'change-password.html',{'message':'Password has been changed'})
        except Exception as e:
            return render(request, 'change-password.html',{'error':e})
    return render(request, 'change-password.html',{'message':'OTP has been sent to your mail.'})

def LogoutPage(request):
    try:
        del request.session['username']
        del request.session['email']
        del request.session['mobile']
        return redirect('home')
    except:
        return redirect('home')