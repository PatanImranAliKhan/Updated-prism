from django.shortcuts import render, redirect
from administrator.models import Photo, Feedback, hdrReview, beautyReview, bokehReview,lightReview
from administrator.forms import PhotoForm
from .models import user
from django.contrib.auth.hashers import check_password, make_password
from approver.models import Approver

from datetime import date
import datetime
import re
import random
from .usersendEmails import usersendemails
# Create your views here.


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

def UserHomePage(request):
    return render(request, 'userHome.html')

def UserAboutPage(request):
    return render(request, 'user_about.html')

def UserContactPage(request):
    username=request.session['username']
    email=request.session['email']
    mobile=request.session['mobile']
    try:
        if request.method=="POST":
            fb=Feedback(name=username,email=email,mobile=mobile,rate=request.POST['rate'],feedback=request.POST['feedback'])
            try:
                fb.save()
                print(fb)
                return render(request, 'user_contact.html',{'username':username,'email':email,'mobile':mobile,'message':'Feedback has been sent successfull'})
            except:
                return render(request, 'user_contact.html',{'username':username,'email':email,'mobile':mobile,'error':'Fill All the details correctly'})
        return render(request,'user_contact.html',{'username':username,'email':email,'mobile':mobile})
    except:
        return render(request, 'user_contact.html',{'username':username,'email':email,'mobile':mobile})

def UserProfilePage(request):
    a=user.objects.get(email=request.session['email'])
    if request.method=="POST":
        if "updatedetails" in request.POST:
            name=request.POST['name']
            mobile=request.POST['mobile']
            bio=request.POST['bio']
            try:
                if name=="":
                    name=request.session['username']
                if mobile=="":
                    mobile=request.session['mobile']
                usr=user.objects.get(email=request.session['email'])
                usr.username=name
                usr.mobile=mobile
                usr.bio=bio
                usr.save()
                return render(request, 'user_profile.html',{'user':usr,'message':'data has been updated successfully'})
            except:
                return render(request, 'user_profile.html',{'user':a,'error':'some thing get wrong please try later'})
        elif "updatepassword" in request.POST:
            oldpass=request.POST['oldpass']
            newpass=request.POST['newpass']
            confirmpass=request.POST['confirmpass']
            try:
                a=user.objects.get(email=request.session['email'])
                pa=a.password
                if check_password(oldpass, pa):
                    if newpass!=confirmpass:
                        return render(request, 'user_profile.html',{'user':a,'error':'New password and cofirm password was not matching','errorcon':'not matching with new password'})
                    try:
                        password=make_password(newpass,None, 'default')
                        a.password=password
                        a.save()
                        return render(request, 'user_profile.html',{'user':a,'message':'data has been updated successfully'})
                    except:
                        return render(request, 'user_profile.html',{'user':a,'error':'some thing get wrong please try later'})
                else:
                    return render(request,'user_profile.html',{'user':a,'error':'Entered password was incorrect','errorp':'incorrect password'})
            except:
                return render(request,'user_profile.html',{'user':a,'error':'invalid email or password'})
    return render(request, 'user_profile.html',{'user':a})


def UploadPhoto(request):
    photos = Photo.objects.all()
    if request.method == 'POST':
        request.POST._mutable = True
        request.POST['email']=request.session['email']
        request.POST['uploaded_date']=date.today()
        request.POST['uploaded_time']=datetime.datetime.now().time()
        form = PhotoForm(request.POST, request.FILES)
        # print(request.POST['hdr'],request.POST['beauty'],request.POST['bokeh'],request.POST['light'])
        print(form.errors.as_data())
    
        if form.is_valid():
            form.save()
            form=PhotoForm()
            return redirect('viewuploads')
            # return render(request, 'user_upload_report.html', {'form': form, 'photos': photos,'success':"Photo was uploaded successfully"})
        else:
            return render(request, 'user_upload_report.html', {'form': form, 'photos': photos,'error':'Error Occured'})
    else:
        form = PhotoForm()
    return render(request, 'user_upload_report.html', {'form': form, 'photos': photos})

def getRandomNumber(count):
    return int(random.randint(0,count))

def ViewUploadsPage(request):
    try:
        p=Photo.objects.filter(email=request.session['email'])
        photos=[]
        appr = Approver.objects.all()
        for k in p:
            data=[]
            hdr=hdrReview.objects.filter(photo_id=k.id) or []
            beauty=beautyReview.objects.filter(photo_id=k.id) or []
            bokeh=bokehReview.objects.filter(photo_id=k.id) or []
            light=lightReview.objects.filter(photo_id=k.id) or []
            print(hdr,beauty,bokeh,light)
            reviewed_appr = set()
            reviewed_comments=[]
            for i in hdr:
                if i.save_mode==False:
                    reviewed_appr.add(i.email)
                    reviewed_comments.append(i.review)
            for i in beauty:
                if i.save_mode==False:
                    reviewed_appr.add(i.email)
                    reviewed_comments.append(i.review)
            for i in bokeh:
                if i.save_mode==False:
                    reviewed_appr.add(i.email)
                    reviewed_comments.append(i.review)
            for i in light:
                if i.save_mode==False:
                    reviewed_appr.add(i.email)
                    reviewed_comments.append(i.review)

            print("reviewd app = ",reviewed_appr)
            l=list(reviewed_appr)
            count=len(reviewed_appr)
            approvers_data=[]
            if count>=4:
                for j in range(count):
                    approvers_data.append({
                        'email':l[j],
                        'status':True
                    })
            else:
                for j in range(count):
                    approvers_data.append({
                        'email':l[j],
                        'status':True
                    })
                for j in appr:
                    if j.email not in l and count<4:
                        approvers_data.append({
                            'email':j.email,
                            'status':False
                        })
                        count+=1
            print("approvers data = ",approvers_data)
            random_generated_number = getRandomNumber(len(reviewed_comments))
            op_comment=""
            if(len(reviewed_comments)==0):
                op_comment=""
            elif random_generated_number>=len(reviewed_comments):
                op_comment=reviewed_comments[random_generated_number-1]
            else:
                op_comment=reviewed_comments[random_generated_number]
            photos.append({
                'id':k.id,
                'email':k.email,
                'file': k.samsung_image,
                'competator1_name':k.competator1_name,
                'competator2_name':k.competator2_name,
                'uploaded_date':k.uploaded_date,
                'uploaded_time':k.uploaded_time,
                'comment':op_comment,
                'approver1_status':approvers_data[0]['status'],
                'approver1_email':approvers_data[0]['email'],
                'approver2_status':approvers_data[1]['status'],
                'approver2_email':approvers_data[1]['email'],
                'approver3_status':approvers_data[2]['status'],
                'approver3_email':approvers_data[2]['email'],
                'approver4_status':approvers_data[3]['status'],
                'approver4_email':approvers_data[3]['email'],
            })
            print("photos = ",photos)
    except Exception as e: 
        photos=[]
        print("Exception ",e)
    if request.method=="POST":
        data=request.POST['search']
        res=[]
        c=0
        for i in photos:
            if (re.match(data, str(i['id']), re.IGNORECASE) or re.match(data, i['email'], re.IGNORECASE) or re.match(data, i['approver1_email'], re.IGNORECASE) or re.match(data, i['approver2_email'], re.IGNORECASE) or re.match(data, i['approver3_email'], re.IGNORECASE) or re.match(data, i['approver4_email'], re.IGNORECASE) or re.match(data, i['file'].url, re.IGNORECASE)):
                res.append(i)
                c=c+1
        if c!=0:
            return render(request,'user_view_uploaded_reports.html',{'photos':res})
        return render(request,'user_view_uploaded_reports.html',{'photos':photos,'error': "no results found, so we are displaying all the results"})
    # print("Photos = ",photos)
    return render(request,'user_view_uploaded_reports.html',{'photos':photos})


def SharedViewForUserPage(request,email,file):
    p=Photo.objects.get(email=email,file=file)
    id=p.id
    abc= {
        "id":p.id,
        "file":p.samsung_image,
        "email":email
    }
    hdr=hdrReview.objects.filter(photo_id=id) or []
    beauty=beautyReview.objects.filter(photo_id=id) or []
    bokeh=bokehReview.objects.filter(photo_id=id) or []
    light=lightReview.objects.filter(photo_id=id) or []
    return render(request, 'SharedUserView.html',{'photo':abc,'hdr':hdr,'beauty':beauty,'bokeh':bokeh,'light':light})

def ViewReportPage(request,id):
    try:
        p=Photo.objects.get(id=id)
        hdr=hdrReview.objects.filter(photo_id=id) or []
        beauty=beautyReview.objects.filter(photo_id=id) or  []
        bokeh=bokehReview.objects.filter(photo_id=id) or []
        light=lightReview.objects.filter(photo_id=id) or []
        hdr_data=[]
        for i in hdr:
            if i.save_mode==False:
                hdr_data.append(i)
        beauty_data=[]
        for i in beauty:
            if i.save_mode==False:
                beauty_data.append(i)
        bokeh_data=[]
        for i in bokeh:
            if i.save_mode==False:
                bokeh_data.append(i)
        light_data=[]
        for i in light:
            if i.save_mode==False:
                light_data.append(i)
        print(hdr_data,beauty_data,bokeh_data,light_data)
        return render(request,'user_ReportView.html',{'photo':p,'hdr':hdr_data,'beauty':beauty_data,'bokeh':bokeh,'light':light})
    except Exception as e:
        print("Exception ",e)
        return render(request,'user_ReportView.html',{'photo':p,'hdr':[],'beauty':[],'bokeh':[],'light':[]})

def UpdateProfilePic(request):
    try:
        u = user.objects.get(email=request.session['email'])
        u.profilepic = request.FILES['profilepic']
        u.save()
        return redirect('user_profile')
    except:
        return redirect('login')

# import datetime
# from datetime import date

# x = str(datetime.datetime.now().time()).split(":")
# y = datetime.datetime.now()
# print(date.today())

# print(x,"           ",y)
