from django.urls import path
from . import views

urlpatterns = [
    path('sign up/',views.sign_up, name='sign_up'),
    path('log in/',views.log_in, name='log_in'),
    path('log out/',views.log_out, name='log_out'),
    path('lost password/',views.mail_sender,name='lost_password'),
    path('change password/<str:passkey>',views.change_password,name='change_password'),
    path('',views.home, name = 'home')
] 