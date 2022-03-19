from django.shortcuts import render, redirect
from administrator.models import Photo, Feedback, hdrReview, beautyReview, bokehReview,lightReview
from administrator.forms import PhotoForm
from .models import user
from django.contrib.auth.hashers import check_password, make_password
from approver.models import Approver

from datetime import date
import datetime
import re
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
    # sendEmails.sendemails("jvhd", "message", "to")
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
        # print(form.errors.as_data())

        if form.is_valid():
            form.save()
            # appr1=Approver.objects.filter(category="hdr",assign="True")
            # for i in appr1:
            #     i.assignments_given+=1
            #     i.save()
            # appr2=Approver.objects.filter(category="beauty",assign="True")
            # for i in appr2:
            #     i.assignments_given+=1
            #     i.save()
            # appr3=Approver.objects.filter(category="bokeh",assign="True")
            # for i in appr3:
            #     i.assignments_given+=1
            #     i.save()
            # appr4=Approver.objects.filter(category="light",assign="True")
            # for i in appr4:
            #     i.assignments_given+=1
            #     i.save()
            form=PhotoForm()
            return render(request, 'user_upload_report.html', {'form': form, 'photos': photos,'success':"Photo was uploaded successfully"})
        else:
            return render(request, 'user_upload_report.html', {'form': form, 'photos': photos,'error':'Error Occured'})
    else:
        form = PhotoForm()
    return render(request, 'user_upload_report.html', {'form': form, 'photos': photos})

def ViewUploadsPage(request):
    try:
        p=Photo.objects.filter(email=request.session['email'])
        photos=[]
        print(p)
        for i in p:
            data=[]
            hdr=hdrReview.objects.filter(photo_id=i.id) or []
            beauty=beautyReview.objects.filter(photo_id=i.id) or []
            bokeh=bokehReview.objects.filter(photo_id=i.id) or []
            light=lightReview.objects.filter(photo_id=i.id) or []
            data.append(i.id)
            data.append(i.email)
            data.append(i.uploaded_date)
            data.append(i.uploaded_time)
            data.append(i.file)
            if len(hdr)!=0:
                data.append(hdr[0].review)
            elif len(beauty)!=0:
                data.append(beauty[0].review)
            elif len(bokeh)!=0:
                data.append(bokeh[0].review)
            elif len(light)!=0:
                data.append(light[0].review)
            else:
                data.append(False)
            print(data)
            # approver status
            if len(hdr)!=0:
                data.append(True)
            else:
                data.append(False)
            if len(beauty)!=0:
                data.append(True)
            else:
                data.append(False)
            if len(bokeh)!=0:
                data.append(True)
            else:
                data.append(False)
            if len(light)!=0:
                data.append(True)
            else:
                data.append(False)

            # approver details

            if len(hdr)!=0:
                data.append(hdr[0].email)
            else:
                hdr_appr=Approver.objects.filter(category="hdr")
                data.append(hdr_appr[0].email)
            if len(beauty)!=0:
                data.append(beauty[0].email)
            else:
                beauty_appr=Approver.objects.filter(category="beauty")
                data.append(beauty_appr[0].email)
            if len(bokeh)!=0:
                data.append(bokeh[0].email)
            else:
                bokeh_appr=Approver.objects.filter(category="bokeh")
                data.append(bokeh_appr[0].email)
            if len(light)!=0:
                data.append(light[0].email)
            else:
                light_appr=Approver.objects.filter(category="light")
                data.append(light_appr[0].email)
            abc = {
                "id":data[0],
                "email":data[1],
                "uploaded_date":data[2],
                "uploaded_time":data[3],
                "file":data[4],
                "comment":data[5],
                "hdrstatus":data[6],
                "beautystatus":data[7],
                "bokehstatus":data[8],
                "lightstatus":data[9],
                "hdr_appr_email":data[10],
                "beauty_appr_email":data[11],
                "bokeh_appr_email":data[12],
                "light_appr_email":data[13]
            }
            photos.append(abc)
    except Exception as e: 
        photos=[]
        print("Exception ",e)
    if request.method=="POST":
        data=request.POST['search']
        res=[]
        c=0
        for i in photos:
            if (re.match(data, str(i['id']), re.IGNORECASE) or re.match(data, i['email'], re.IGNORECASE) or re.match(data, i['hdr_appr_email'], re.IGNORECASE) or re.match(data, i['beauty_appr_email'], re.IGNORECASE) or re.match(data, i['bokeh_appr_email'], re.IGNORECASE) or re.match(data, i['light_appr_email'], re.IGNORECASE)):
                res.append(i)
                c=c+1
        if c!=0:
            return render(request,'user_view_uploaded_reports.html',{'photos':res})
        return render(request,'user_view_uploaded_reports.html',{'photos':photos,'error': "no results found, so we are displaying all the results"})
    print("Photos = ",photos)
    return render(request,'user_view_uploaded_reports.html',{'photos':photos})


def SharedViewForUserPage(request,email,file):
    p=Photo.objects.get(email=email,file=file)
    id=p.id
    abc= {
        "id":p.id,
        "file":p.file,
        "email":email
    }
    hdr=hdrReview.objects.filter(photo_id=id) or []
    beauty=beautyReview.objects.filter(photo_id=id) or []
    bokeh=bokehReview.objects.filter(photo_id=id) or []
    light=lightReview.objects.filter(photo_id=id) or []
    return render(request, 'SharedUserView.html',{'photo':abc,'hdr':hdr,'beauty':beauty,'bokeh':bokeh,'light':light})

def ViewReportPage(request,id):
    ph=Photo.objects.get(id=id)
    abc= {
        "id":id,
        "file":ph.file,
        "email":request.session['email']
    }
    hdr=hdrReview.objects.filter(photo_id=id) or []
    beauty=beautyReview.objects.filter(photo_id=id) or []
    bokeh=bokehReview.objects.filter(photo_id=id) or []
    light=lightReview.objects.filter(photo_id=id) or []
    return render(request, 'user_ReportView.html',{'photo':abc,'hdr':hdr,'beauty':beauty,'bokeh':bokeh,'light':light})

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
