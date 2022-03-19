from django.urls import path
from . import views

urlpatterns = [
    path('',views.ApproverHomePage,name="appr_home"),
    path('about/',views.ApproverAboutPage,name="appr_about"),
    path('contact/',views.ApproverContactPage,name="appr_contact"),
    path('newreports/',views.NewReports,name="newreports"),
    path('verifiedreports/',views.AlreadyVerifiedReports,name="verified_reports"),
    path('profile',views.ProfilePage,name="appr_profile"),
    path('viewreport/<int:id>/',views.ViewBenchmarkingReport,name="apprviewreport")
]