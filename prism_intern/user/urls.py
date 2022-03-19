from django.urls import path
from . import views

urlpatterns = [
    path('',views.UserHomePage,name="user_home"),
    path('about/',views.UserAboutPage,name="user_about"),
    path('contact/',views.UserContactPage,name="user_contact"),
    path('upload/',views.UploadPhoto,name="upload_image"),
    path('viewuploads/',views.ViewUploadsPage,name="viewuploads"),
    path('profile/',views.UserProfilePage,name="user_profile"),
    path('viewreport/<int:id>/',views.ViewReportPage,name="userviewreport"),
    path('updateprofilepic',views.UpdateProfilePic,name="updateprofilepic")
]