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
        id=request.POST.get("addcomment") or request.POST.get("save")
        photo_details = Photo.objects.get(id=id)
        
        hdr_comment = request.POST['hdr']
        beauty_comment = request.POST['beauty']
        bokeh_comment = request.POST['bokeh']
        light_comment = request.POST['light']
        print(hdr_comment,beauty_comment,bokeh_comment,light_comment)
        save_mode=False
        if 'save' in request.POST:
            save_mode=True
            print("save_mode",save_mode)

        html_data='Hi '+photo_details.email+', your Report has been approved by the approvers. Once verify it.'
        apprsendemails('report Approved',html_data,photo_details.email)

        if(hdr_comment!=None):
            try:
                h=hdrReview.objects.get(email=request.session['email'],photo_id=id)
                if h.review!=hdr_comment or h.save_mode==True:
                    if(save_mode==False):
                        e=editReview(email=request.session['email'],photo_id=id,review=h.review,category='hdr')
                        e.save()
                    h.review=hdr_comment
                    h.save_mode=save_mode
                    h.photo_edited=False
                    h.save()
            except: 
                hdr=hdrReview(email=request.session['email'],review=hdr_comment,photo_id=id,save_mode=save_mode)
                hdr.save()

            
        if (beauty_comment!=None):
            try:
                bea=beautyReview.objects.get(email=request.session['email'],photo_id=id)
                if bea.review!=beauty_comment or bea.save_mode==True:
                    if(save_mode==False):
                        e=editReview(email=request.session['email'],photo_id=id,review=bea.review,category='beauty')
                        e.save()
                    bea.review=beauty_comment
                    bea.save_mode=save_mode
                    bea.photo_edited=False
                    bea.save()
            except:
                beauty=beautyReview(email=request.session['email'],review=beauty_comment,photo_id=id,save_mode=save_mode)
                beauty.save()
        if (bokeh_comment!=None):
            try:
                bo=bokehReview.objects.get(email=request.session['email'],photo_id=id)
                if bo.review!=bokeh_comment or bo.save_mode==True:
                    if (save_mode==False):
                        e=editReview(email=request.session['email'],photo_id=id,review=bo.review, category='bokeh')
                        e.save()
                    bo.review=bokeh_comment
                    bo.save_mode=save_mode
                    bo.photo_edited=False
                    bo.save()
            except:
                bokeh=bokehReview(email=request.session['email'],review=bokeh_comment,photo_id=id,save_mode=save_mode)
                bokeh.save()
        if (light_comment!=None):
            try:
                li=lightReview.objects.get(email=request.session['email'],photo_id=id)
                if li.review!=light_comment or li.save_mode==True:
                    if(save_mode==False):
                        e=editReview(email=request.session['email'],photo_id=id,review=li.review, category='light')
                        e.save()
                    li.review=light_comment
                    li.save_mode=save_mode
                    li.photo_edited=False
                    li.save()
            except:
                light=lightReview(email=request.session['email'],review=light_comment,photo_id=id,save_mode=save_mode)
                light.save()
        if save_mode==False:
            a=Approver.objects.get(email=email)
            a.assignments_done+=1
            a.save()
        return redirect('newreports')
    try:
        ph=Photo.objects.all()
        photos=[]
        for i in ph:
            d=[]
            hdr_rev=hdrReview.objects.filter(email=request.session['email'],photo_id=i.id) or []
            beauty_rev=beautyReview.objects.filter(email=request.session['email'],photo_id=i.id) or[]
            bokeh_rev=bokehReview.objects.filter(email=request.session['email'],photo_id=i.id) or []
            light_rev=lightReview.objects.filter(email=request.session['email'],photo_id=i.id) or []
            data={}
            print(hdr_rev)
            # print(hdr_rev[0].save_mode)
            if len(hdr_rev)!=0 or len(beauty_rev)!=0 or len(bokeh_rev)!=0 or len(light_rev)!=0:
                # if(hdr_rev[0].save_mode==True or beauty_rev[0].save_mode==True or bokeh_rev[0].save_mode==True or light_rev[0].save_mode==True):
                temp=0
                if(len(hdr_rev)!=0 and hdr_rev[0].save_mode==True):
                    temp=1
                    data['hdr_rev']=hdr_rev[0].review
                else:
                    data['hdr_rev']=""
                if(len(beauty_rev)!=0 and beauty_rev[0].save_mode==True):
                    temp=1
                    data['beauty_rev']=beauty_rev[0].review
                else:
                    data['beauty_rev']=""
                if(len(bokeh_rev)!=0 and bokeh_rev[0].save_mode==True):
                    temp=1
                    data['bokeh_rev']=bokeh_rev[0].review
                else:
                    data['bokeh_rev']=""
                if(len(light_rev)!=0 and light_rev[0].save_mode==True):
                    temp=1
                    data['light_rev']=light_rev[0].review
                else:
                    data['light_rev']=""
                if(temp==1):
                    photos.append({
                        'id':i.id,
                        'email':i.email,
                        'samsung_image': i.samsung_image,
                        'competator1_name': i.competator1_name,
                        'competator2_name': i.competator2_name,
                        'uploaded_date':i.uploaded_date,
                        'uploaded_time':i.uploaded_time,
                        'hdr_rev':data['hdr_rev'],
                        'beauty_rev':data['beauty_rev'],
                        'bokeh_rev':data['bokeh_rev'],
                        'light_rev':data['light_rev']
                    })
                print(data)
                continue
            else:
                photos.append(i)
        print("photos = ",photos)
        return render(request, 'new_reports.html',{'photos':photos,'email':email})
    except Exception as e:
        print("exception ",e)
        return render(request, 'new_reports.html',{'photos':ph,'email':email,'exception':e})

def AlreadyVerifiedReports(request):
    email=request.session['email']
    # data=hdrReview.objects.all(email=request.session['email'],review="").exclude(review="")
    photos=[]
    if request.method=="POST":
        id=request.POST.get("edit")
        photo_details = Photo.objects.get(id=id)
        
        hdr_comment = request.POST['hdr']
        beauty_comment = request.POST['beauty']
        bokeh_comment = request.POST['bokeh']
        light_comment = request.POST['light']

        html_data='Hi '+photo_details.email+', your Report has been approved by the approvers. Once verify it.'
        apprsendemails('report Approved',html_data,photo_details.email)

        if(hdr_comment!=None):
            try:
                h=hdrReview.objects.get(email=request.session['email'],photo_id=id)
                if hdr_comment!=None and h.review!=hdr_comment:
                    e=editReview(email=request.session['email'],photo_id=id,review=h.review,category='hdr')
                    e.save()
                    h.review=hdr_comment
                    h.save_mode=False
                    h.photo_edited=False
                    h.save()
            except: 
                hdr=hdrReview(email=request.session['email'],review=hdr_comment,photo_id=id)
                hdr.save()
        if (beauty_comment!=None):
            try:
                bea=beautyReview.objects.get(email=request.session['email'],photo_id=id)
                if bea.review!=beauty_comment:
                    e=editReview(email=request.session['email'],photo_id=id,review=bea.review,category='beauty')
                    e.save()
                    bea.review=beauty_comment
                    bea.save_mode=False
                    bea.photo_edited=False
                    bea.save()
            except:
                beauty=beautyReview(email=request.session['email'],review=beauty_comment,photo_id=id)
                beauty.save()
        if (bokeh_comment!=None):
            try:
                bo=bokehReview.objects.get(email=request.session['email'],photo_id=id)
                if bo.review!=bokeh_comment:
                    e=editReview(email=request.session['email'],photo_id=id,review=bo.review, category='bokeh')
                    e.save()
                    bo.review=bokeh_comment
                    bo.save_mode=False
                    bo.photo_edited=False
                    bo.save()
            except:
                bokeh=bokehReview(email=request.session['email'],review=bokeh_comment,photo_id=id)
                bokeh.save()
        if (light_comment!=None):
            try:
                li=lightReview.objects.get(email=request.session['email'],photo_id=id)
                if li.review!=light_comment:
                    e=editReview(email=request.session['email'],photo_id=id,review=li.review, category='light')
                    e.save()
                    li.review=light_comment
                    li.save_mode=False
                    li.photo_edited=False
                    li.save()
            except:
                light=lightReview(email=request.session['email'],review=light_comment,photo_id=id)
                light.save()
        return redirect('verified_reports')
    try:
        ph=Photo.objects.all()
        photos=[]
        data={}
        for i in ph:
            d=[]
            hdr_rev=hdrReview.objects.filter(email=request.session['email'],photo_id=i.id) or []
            beauty_rev=beautyReview.objects.filter(email=request.session['email'],photo_id=i.id) or[]
            bokeh_rev=bokehReview.objects.filter(email=request.session['email'],photo_id=i.id) or []
            light_rev=lightReview.objects.filter(email=request.session['email'],photo_id=i.id) or []
            
            if len(hdr_rev)!=0 or len(beauty_rev)!=0 or len(bokeh_rev)!=0 or len(light_rev)!=0:
                photos.append(i)
            if(len(hdr_rev)!=0):
                data['hdr_rev']=hdr_rev[0].review
            if(len(beauty_rev)!=0):
                data['beauty_rev']=beauty_rev[0].review
            if(len(bokeh_rev)!=0):
                data['bokeh_rev']=bokeh_rev[0].review
            if(len(light_rev)!=0):
                data['light_rev']=light_rev[0].review
        print("photos = ",photos)
        print("data = ",data)
        return render(request, 'appr_verified_reports.html',{'photos':photos,'email':email,'rev_data':data})
    except Exception as e:
        return render(request, 'appr_verified_reports.html',{'photos':data,'email':email,'exception':e})

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
        return render(request,'appr_BenchmarkingReport.html',{'photo':p,'hdr':hdr_data,'beauty':beauty_data,'bokeh':bokeh,'light':light})
    except Exception as e:
        print("Exception ",e)
        return render(request,'appr_BenchmarkingReport.html',{'photo':p,'hdr':[],'beauty':[],'bokeh':[],'light':[]})
