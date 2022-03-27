from django.shortcuts import render, redirect
from approver.models import Approver
from .models import Photo,Feedback, hdrReview, beautyReview, lightReview, bokehReview
from approver.forms import ApproverForm
from django.contrib.auth.hashers import check_password, make_password
from .adminSendEmails import admsendemails

import re
import random
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
            if re.match(data, i.username, re.IGNORECASE) or re.match(data, i.email, re.IGNORECASE) or re.match(data, str(i.mobile), re.IGNORECASE):
                results.append(i)
                c=c+1
        if c!=0:
            return render(request,'approvers/approvers_list.html',{'approvers': results})
        return render(request,'approvers/approvers_list.html',{'approvers':approvers,'error': "no results found, so we are displaying all the results"})
    return render(request,'approvers/approvers_list.html',{'approvers':approvers})

def Add_approvers(request):
    form=ApproverForm()
    if request.method=="POST":
        sub="Added as Approver"
        mess="""Yuo have been added into SamsungPrism research as an approver. Once please verify your Details asmentioned below\n
                Email: {}\nUsername : {}\nMobile Number : {}\n
                We have given password as samsungprism to login. Once you login please reset your password in your profilepage"""
        to=[request.POST['email']]
        request.POST._mutable = True
        request.POST['password'] = make_password("samsungprism",None, 'default')
        appr=Approver(username=request.POST['username'],email=request.POST['email'],mobile=request.POST['mobile'],password=request.POST['password'],assign="True")
        try:
            appr.save()
            html_data = mess.format(request.POST['email'],request.POST['username'],request.POST['mobile'])
            # html_data='Hi '+request.POST['username']+', you have been added as an approver. use samsungprism as the password and change the password.'
            admsendemails('Successfully Registered',html_data,request.POST['email'])
            return render(request, 'approvers/add_approvers.html',{'form':form,'message':'Approver was Added Successfully'})
        except:
            return render(request, 'approvers/add_approvers.html',{'form':form,'error':'something entered wrong'})
    return render(request, 'approvers/add_approvers.html',{'form':form})

def getRandomNumber(count):
    return int(random.randint(0,count))

def Approvements_Inprogress(request):
    try:
        p=Photo.objects.filter()
        photos=[]
        appr = Approver.objects.all()
        for k in p:
            data=[]
            hdr=hdrReview.objects.filter(photo_id=k.id) or []
            beauty=beautyReview.objects.filter(photo_id=k.id) or []
            bokeh=bokehReview.objects.filter(photo_id=k.id) or []
            light=lightReview.objects.filter(photo_id=k.id) or []
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
            if count<4:
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
            if (re.match(data, str(i['id']), re.IGNORECASE) or re.match(data, i['email'], re.IGNORECASE) or re.match(data, i['approver1_email'], re.IGNORECASE) or re.match(data, i['approver2_email'], re.IGNORECASE) or re.match(data, i['approver3_email'], re.IGNORECASE) or re.match(data, i['approver4_email'], re.IGNORECASE)):
                res.append(i)
                c=c+1
        if c!=0:
            return render(request,'approvements/inprogress_approvements.html',{'photos':res})
        return render(request,'approvements/inprogress_approvements.html',{'photos':photos,'error': "no results found, so we are displaying all the results"})
    # print("Photos = ",photos)
    return render(request,'approvements/inprogress_approvements.html',{'photos':photos})

def Already_Approved_set(request):
    try:
        p=Photo.objects.filter()
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
                print("approvers data = ",approvers_data)
                random_generated_number = getRandomNumber(len(reviewed_comments))
                op_comment=""
                if random_generated_number>=len(reviewed_comments):
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

    except Exception as e: 
        photos=[]
        print("Exception ",e)
    if request.method=="POST":
        data=request.POST['search']
        res=[]
        c=0
        for i in photos:
            if (re.match(data, str(i['id']), re.IGNORECASE) or re.match(data, i['email'], re.IGNORECASE) or re.match(data, i['approver1_email'], re.IGNORECASE) or re.match(data, i['approver2_email'], re.IGNORECASE) or re.match(data, i['approver3_email'], re.IGNORECASE) or re.match(data, i['approver4_email'], re.IGNORECASE)):
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
    return render(request,'adm_ReportView.html',{'photo':p,'hdr':hdr,'beauty':beauty,'bokeh':bokeh,'light':light})

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