from django.shortcuts import render, redirect
from approver.models import Approver
from .models import Photo,Feedback, hdrReview, beautyReview, lightReview, bokehReview
from approver.forms import ApproverForm
from django.contrib.auth.hashers import check_password, make_password
from .adminSendEmails import admsendemails

import re
from django.db.models import Q
# Create your views here.

def AdminHome(request):
    return render(request,'adm_home.html')

def FeedbacksPage(request):
    feedbacks=Feedback.objects.all()
    return render(request,'feedbacks_list.html',{'feedbacks':feedbacks})

def ChangeWorkflow(request):
    return redirect('adm_home')

def AllApproversList(request):
    approvers=Approver.objects.filter(assign="True")
    if request.method=="POST":
        results = []
        data = str(request.POST['search'])
        c=0
        for i in approvers:
            if re.match(data, i.username, re.IGNORECASE) or re.match(data, i.email, re.IGNORECASE) or re.match(data, str(i.mobile), re.IGNORECASE) or re.match(data, str(i.category), re.IGNORECASE):
                results.append(i)
                c=c+1
        print(c)
        if c!=0:
            return render(request,'approvers/approvers_list.html',{'approvers': results})
        return render(request,'approvers/approvers_list.html',{'approvers':approvers,'error': "no results found, so we are displaying all the results"})
    return render(request,'approvers/approvers_list.html',{'approvers':approvers})

def Add_approvers(request):
    form=ApproverForm()
    if request.method=="POST":
        sub="Added as Approver"
        mess="""Yuo have been added into SamsungPrism research as an approver. Once please verify your Details asmentioned below\n
                Email: {}\nUsername : {}\nMobile Number : {}\nYou have been added into category : {}\n
                We have given password as samsungprism to login. Once you login please reset your password in your profilepage"""
        to=[request.POST['email']]
        request.POST._mutable = True
        request.POST['password'] = make_password("samsungprism",None, 'default')
        if(request.POST['category']==""):
            return render(request, 'approvers/add_approvers.html',{'form':form,'error':'Fill Category field'})
        appr=Approver(username=request.POST['username'],email=request.POST['email'],mobile=request.POST['mobile'],category=request.POST['category'],password=request.POST['password'],assign="True")
        try:
            appr.save()
            html_data='Hi '+request.POST['username']+', you have been added as an approver. use samsungprism as the password and change the password.'
            admsendemails('Successfully Registered',html_data,request.POST['email'])
            return render(request, 'approvers/add_approvers.html',{'form':form,'message':'Approver was Added Successfully'})
        except:
            return render(request, 'approvers/add_approvers.html',{'form':form,'error':'something entered wrong'})
    return render(request, 'approvers/add_approvers.html',{'form':form})

def Approvements_Inprogress(request):
    try:
        p=Photo.objects.all()
        photos=[]
        for i in p:
            data=[]
            hdr=hdrReview.objects.filter(photo_id=i.id) or []
            beauty=beautyReview.objects.filter(photo_id=i.id) or []
            bokeh=bokehReview.objects.filter(photo_id=i.id) or []
            light=lightReview.objects.filter(photo_id=i.id) or []
            if(len(hdr)==0 or len(beauty)==0 or len(bokeh)==0 or len(light)==0):
                    
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
    if request.method=="POST":
        data=request.POST['search']
        res=[]
        c=0
        for i in photos:
            if (re.match(data, str(i['id']), re.IGNORECASE) or re.match(data, i['email'], re.IGNORECASE) or re.match(data, i['hdr_appr_email'], re.IGNORECASE) or re.match(data, i['beauty_appr_email'], re.IGNORECASE) or re.match(data, i['bokeh_appr_email'], re.IGNORECASE) or re.match(data, i['light_appr_email'], re.IGNORECASE)):
                res.append(i)
                c=c+1
        if c!=0:
            return render(request,'approvements/inprogress_approvements.html',{'photos':res})
        return render(request,'approvements/inprogress_approvements.html',{'photos':photos,'error': "no results found, so we are displaying all the results"})
    return render(request,'approvements/inprogress_approvements.html',{'photos':photos})

def Already_Approved_set(request):
    try:
        p=Photo.objects.all()
        photos=[]
        for i in p:
            data=[]
            hdr=hdrReview.objects.filter(photo_id=i.id) or []
            beauty=beautyReview.objects.filter(photo_id=i.id) or []
            bokeh=bokehReview.objects.filter(photo_id=i.id) or []
            light=lightReview.objects.filter(photo_id=i.id) or []
            if(len(hdr)!=0 and len(beauty)!=0 and len(bokeh)!=0 and len(light)!=0):
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
    if request.method=="POST":
        data=request.POST['search']
        res=[]
        c=0
        for i in photos:
            if (re.match(data, str(i['id']), re.IGNORECASE) or re.match(data, i['email'], re.IGNORECASE) or re.match(data, i['hdr_appr_email'], re.IGNORECASE) or re.match(data, i['beauty_appr_email'], re.IGNORECASE) or re.match(data, i['bokeh_appr_email'], re.IGNORECASE) or re.match(data, i['light_appr_email'], re.IGNORECASE)):
                res.append(i)
                c=c+1
        if c!=0:
            return render(request,'approvements/approved_set.html',{'photos':res})
        return render(request,'approvements/approved_set.html',{'photos':photos,'error': "no results found, so we are displaying all the results"})
    return render(request,'approvements/approved_set.html',{'photos':photos})

def ApprovementEditPage(request,id):
    try:
        # if request.method=="POST":
        #     appr1=request.POST['approver1']
        #     appr2=request.POST['approver2']
        #     appr3=request.POST['approver3']
        #     p=Photo.objects.get(id=id)
        #     if(p.approver1!=appr1):
        #         a1=Approver.objects.get(email=p.approver1)
        #         a1.assignments_given-=1
        #         a1.save()

        #         e1=EditableApprover1.objects.create(email=p.approver1,review=p.rev1,status=p.appr1status)
        #         e1.save()
        #         p.oldAppr1.add(e1)

        #         a11=Approver.objects.get(email=appr1)
        #         a11.assignments_given+=1
        #         a11.save()
        #     if(p.approver2!=appr2):
        #         a2=Approver.objects.get(email=p.approver3)
        #         a2.assignments_given-=1
        #         a2.save()

        #         e2=EditableApprover2.objects.create(email=p.approver2,review=p.rev2,status=p.appr2status)
        #         e2.save()

        #         p.oldAppr2.add(e2)

        #         a22=Approver.objects.get(email=appr2)
        #         a22.assignments_given+=1
        #         a22.save()
        #     if(p.approver3!=appr3):
        #         a2=Approver.objects.get(email=p.approver3)
        #         a2.assignments_given-=1
        #         a2.save()

        #         e3=EditableApprover3.objects.create(email=p.approver3,review=p.rev3,status=p.appr3status)
        #         e3.save()

        #         p.oldAppr3.add(e3)

        #         a33=Approver.objects.get(email=appr3)
        #         a33.assignments_given+=1
        #         a33.save()
        #     p.edited=True
        #     p.approver1=appr1
        #     p.approver2=appr2
        #     p.approver3=appr3
        #     p.save()

        #     return redirect('new_approvements')
        p=Photo.objects.get(id=id)
        level1appr=Approver.objects.filter(level=1)
        level2appr=Approver.objects.filter(level=2)
        level3appr=Approver.objects.filter(level=3)
        return render(request, 'approvements/Edit_set.html',{'photo':p,'Level1appr':level1appr,'Level2appr':level2appr,'Level3appr':level3appr})
    except:
        print("exception")
        return render(request, 'approvements/Edit_set.html',{'error': 'Something went wrong'})

def ApproverDetails(request,email):
    appr=Approver.objects.get(email=email)
    p=Photo.objects.all() or []
    if request.method=="POST":
        appr.delete()
        return redirect('approvers')
    assignments=[len(p),appr.assignments_done]
    return render(request,'view_approver.html',{'approver':appr,'assignments':assignments})

def ViewReport(request,id):
    p=Photo.objects.get(id=id)
    hdr=hdrReview.objects.filter(photo_id=id)
    beauty=beautyReview.objects.filter(photo_id=id)
    bokeh=bokehReview.objects.filter(photo_id=id)
    light=lightReview.objects.filter(photo_id=id)
    abc=Photo.objects.all()
    t=0
    klu=[]
    for i in abc:
        if i.id!=id and t<2:
            klu.append(i.file)
            t+=1
    return render(request,'adm_ReportView.html',{'photo':p,'file2':klu[0],'file3':klu[1],'hdr':hdr,'beauty':beauty,'bokeh':bokeh,'light':light})

def getHDRPhotos(request,hdrobj,id):
    ph=Photo.objects.filter(hdr=hdrobj)
    photos=[]
    for i in ph:
        if i.id!=id:
            photos.append(i)
    # print(photos)
    return render(request,'hdr.html',{'photos':photos})
    

def getBeautyPhotos(request,beautyobj,id):
    ph=Photo.objects.filter(beauty=beautyobj)
    photos=[]
    for i in ph:
        if i.id!=id:
            photos.append(i)
    # print(photos)
    return render(request,'beauty.html',{'photos':photos})

def getBokehPhotos(request,bokehobj,id):
    ph=Photo.objects.filter(bokeh=bokehobj)
    photos=[]
    for i in ph:
        if i.id!=id:
            photos.append(i)
    # print(photos)
    return render(request,'bokeh.html',{'photos':photos})

def getLightPhotos(request,lightobj,id):
    ph=Photo.objects.filter(light=lightobj)
    photos=[]
    for i in ph:
        if i.id!=id:
            photos.append(i)
    # print(photos)
    return render(request,'light.html',{'photos':photos})