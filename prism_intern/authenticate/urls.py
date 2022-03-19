from django.urls import path
from . import views

urlpatterns = [
    path('',views.HomePage,name="home"),
    path('about/',views.AboutPage,name="about"),
    path('contact/',views.ContactPage,name="contact"),
    path('login/',views.LoginPage,name="login"),
    path('register/',views.UserRegistration,name="register"),
    path('profile/',views.Profile,name="profile"),
    path('forgot-password/',views.ForgotPasswordPage,name="forgotpassword"),
    path('change-password/',views.ChangePasswordPage,name="changepassword"),
    path('logout/',views.LogoutPage,name="logout"),
]