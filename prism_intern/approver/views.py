from django.shortcuts import render, redirect
from administrator.models import Photo, Feedback, hdrReview,bokehReview, beautyReview,lightReview, editReview
from administrator.forms import PhotoForm, FeedbackForm
from django.contrib.auth.hashers import check_password, make_password
from .models import Approver
from .approverSendEmails import apprsendemails

from django.db.models import Q

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

def ApproverHomePage(request):
    return render(request, 'approverHome.html')

def ApproverAboutPage(request):
    return render(request, 'appr_about.html')

def ApproverContactPage(request):
    username=request.session['username']
    email=request.session['email']
    mobile=request.session['mobile']
    try:
        if request.method=="POST":
            fb=Feedback(name=username,email=email,mobile=mobile,rate=request.POST['rate'],feedback=request.POST['feedback'])
            try:
                fb.save()
                return render(request, 'appr_contact.html',{'username':username,'email':email,'mobile':mobile,'message':'Feedback has been sent successfull'})
            except:
                return render(request, 'appr_contact.html',{'username':username,'email':email,'mobile':mobile,'error':'Fill All the details correctly'})
        return render(request,'appr_contact.html',{'username':username,'email':email,'mobile':mobile})
    except:
        return render(request,'appr_contact.html',{'username':username,'email':email,'mobile':mobile})

def NewReports(request):
    email=request.session['email']
    if request.method=="POST":
        id=request.POST.get("addcomment")
        photo_details = Photo.objects.get(id=id)
        review=request.POST['review']

        if(request.session['category']=="hdr"):
            try:
                h=hdrReview.objects.get(email=request.session['email'],photo_id=id)
                if h.review!=review:
                    e=editReview(email=request.session['email'],photo_id=id,review=h.review)
                    e.save()
                    html_data='Hi '+photo_details.email+', your Report has been approved by the approvers. Once verify it.'
                    apprsendemails('report Approved',html_data,photo_details.email)
                    h.review=review
                    h.photo_edited=False
                    h.save()
            except:
                hdr=hdrReview(email=request.session['email'],review=review,photo_id=id)
                hdr.save()
                html_data='Hi '+photo_details.email+', your Report has been approved by the approvers. Once verify it.'
                apprsendemails('report Approved',html_data,photo_details.email)
        elif (request.session['category']=="beauty"):
            try:
                bea=beautyReview.objects.get(email=request.session['email'],photo_id=id)
                e=editReview(email=request.session['email'],photo_id=id,review=bea.review)
                e.save()
                html_data='Hi '+photo_details.email+', your Report has been approved by the approvers. Once verify it.'
                apprsendemails('report Approved',html_data,photo_details.email)
                bea.review=review
                bea.photo_edited=False
                bea.save()
            except:
                beauty=beautyReview(email=request.session['email'],review=review,photo_id=id)
                beauty.save()
                html_data='Hi '+photo_details.email+', your Report has been approved by the approvers. Once verify it.'
                apprsendemails('report Approved',html_data,photo_details.email)
        elif (request.session['category']=="bokeh"):
            try:
                bo=bokehReview.objects.get(email=request.session['email'],photo_id=id)
                e=editReview(email=request.session['email'],photo_id=id,review=bo.review)
                e.save()
                html_data='Hi '+photo_details.email+', your Report has been approved by the approvers. Once verify it.'
                apprsendemails('report Approved',html_data,photo_details.email)
                bo.review=review
                bo.photo_edited=False
                bo.save()
            except:
                bokeh=bokehReview(email=request.session['email'],review=review,photo_id=id)
                bokeh.save()
                html_data='Hi '+photo_details.email+', your Report has been approved by the approvers. Once verify it.'
                apprsendemails('report Approved',html_data,photo_details.email)
        else:
            try:
                li=lightReview.objects.get(email=request.session['email'],photo_id=id)
                e=editReview(email=request.session['email'],photo_id=id,review=li.review)
                e.save()
                html_data='Hi '+photo_details.email+', your Report has been approved by the approvers. Once verify it.'
                apprsendemails('report Approved',html_data,photo_details.email)
                li.review=review
                li.photo_edited=False
                li.save()
            except:
                light=lightReview(email=request.session['email'],review=review,photo_id=id)
                light.save()
                html_data='Hi '+photo_details.email+', your Report has been approved by the approvers. Once verify it.'
                apprsendemails('report Approved',html_data,photo_details.email)
        a=Approver.objects.get(email=email)
        a.assignments_done+=1
        a.save()
        return redirect('newreports')
    # try:
    ph=Photo.objects.all()
    photos=[]
    for i in ph:
        d=[]
        if(request.session['category']=="hdr"):
            d=hdrReview.objects.filter(email=request.session['email'],photo_id=i.id) or []
        elif (request.session['category']=="beauty"):
            d=beautyReview.objects.filter(email=request.session['email'],photo_id=i.id) or[]
        elif (request.session['category']=="bokeh"):
            d=bokehReview.objects.filter(email=request.session['email'],photo_id=i.id) or []
        else:
            d=lightReview.objects.filter(email=request.session['email'],photo_id=i.id) or []
        data=[]
        
        if len(d)==0:
            photos.append(i)
            print("data : ",data)
        else:
            for j in d:
                if j.photo_edited==True:
                    # k['edited_comment']=j.review
                    photos.append(i)
        # photos=data
    return render(request, 'new_reports.html',{'photos':photos,'email':email})
    # except:
    #     print("exception")
    #     return render(request, 'new_reports.html',{'photos':data,'email':email})

def AlreadyVerifiedReports(request):
    email=request.session['email']
    # data=hdrReview.objects.all(email=request.session['email'],review="").exclude(review="")
    photos=[]
    if request.method=="POST":
        print()
        review=request.POST['editedreview']
        id=request.POST.get('edit')
        photo_details = Photo.objects.get(id=id)
        h=hdrReview.objects.get(email=request.session['email'],photo_id=id)
        if h.review!=review:
            e=editReview(email=request.session['email'],photo_id=id,review=h.review)
            e.save()
            h.review=review
            h.save()
            html_data='Hi '+photo_details.email+', your Report status has been updated by the approvers. Once verify it.'
            apprsendemails('Updated report Status',html_data,photo_details.email)
    try:
        if(request.session['category']=="hdr"):
            d=hdrReview.objects.filter(email=request.session['email']) or []
        elif (request.session['category']=="beauty"):
            d=beautyReview.objects.filter(email=request.session['email']) or[]
        elif (request.session['category']=="bokeh"):
            d=bokehReview.objects.filter(email=request.session['email']) or []
        else:
            d=lightReview.objects.filter(email=request.session['email']) or []
        for i in d:
            try:
                p=Photo.objects.get(id=i.photo_id)
                abc = {
                    "id":p.id,
                    "file":p.file,
                    "comment":i.review
                }
                photos.append(abc)
            except Exception as e:
                print(e)
        return render(request, 'appr_verified_reports.html',{'photos':photos,'email':email})
    except:
        return render(request, 'appr_verified_reports.html',{'photos':photos,'email':email})

def ProfilePage(request):
    a=Approver.objects.get(email=request.session['email'])
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
                appr=Approver.objects.get(email=request.session['email'])
                appr.username=name
                appr.mobile=mobile
                appr.bio=bio
                appr.save()
                return render(request, 'appr_profile.html',{'approver':appr,'message':'data has been updated successfully'})
            except:
                return render(request, 'appr_profile.html',{'approver':a,'error':'some thing get wrong please try later'})
        elif "updatepassword" in request.POST:
            oldpass=request.POST['oldpass']
            newpass=request.POST['newpass']
            confirmpass=request.POST['confirmpass']
            try:
                a=Approver.objects.get(email=request.session['email'])
                pa=a.password
                if check_password(oldpass, pa):
                    if newpass!=confirmpass:
                        return render(request, 'appr_profile.html',{'approver':a,'error':'New password and cofirm password was not matching','errorcon':'not matching with new password'})
                    try:
                        password=make_password(newpass,None, 'default')
                        a.password=password
                        a.save()
                        return render(request, 'appr_profile.html',{'approver':a,'message':'data has been updated successfully'})
                    except:
                        return render(request, 'appr_profile.html',{'approver':a,'error':'some thing get wrong please try later'})
                else:
                    return render(request,'appr_profile.html',{'approver':a,'error':'Entered password was incorrect','errorp':'incorrect password'})
            except:
                return render(request,'appr_profile.html',{'approver':a,'error':'invalid email or password'})
    return render(request, 'appr_profile.html',{'approver':a})

def ViewBenchmarkingReport(request,id):
    p=Photo.objects.get(id=id)
    hdr=hdrReview.objects.filter(photo_id=id)
    beauty=beautyReview.objects.filter(photo_id=id)
    bokeh=bokehReview.objects.filter(photo_id=id)
    light=lightReview.objects.filter(photo_id=id)
    return render(request,'appr_BenchmarkingReport.html',{'photo':p,'hdr':hdr,'beauty':beauty,'bokeh':bokeh,'light':light})