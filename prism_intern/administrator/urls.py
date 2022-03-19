from django.urls import path
from . import views

urlpatterns = [
    path('',views.AdminHome,name="adm_home"),
    path('feedbacks/',views.FeedbacksPage,name="feedbacks"),
    path('approvers/',views.AllApproversList,name="approvers"),
    path('add_approvers/',views.Add_approvers,name="add_approver"),
    path('inprogress_reportss/',views.Approvements_Inprogress,name="new_approvements"),
    path('verified_reports/',views.Already_Approved_set,name="approved_set"),
    path('edit/<int:id>',views.ApprovementEditPage,name="editapprovement"),
    path('approverdetails/<email>/',views.ApproverDetails,name="approverdetails"),
    path('viewreport/<int:id>/',views.ViewReport,name="admviewreport"),
    path('hdrphotos/<hdrobj>/<int:id>/',views.getHDRPhotos,name="hdrphotos"),
    path('beautyphotos/<beautyobj>/<int:id>/',views.getBeautyPhotos,name="beautyphotos"),
    path('bokehphotos/<bokehobj>/<int:id>/',views.getBokehPhotos,name="bokehphotos"),
    path('lightphotos/<lightobj>/<int:id>/',views.getLightPhotos,name="lightphotos"),
]