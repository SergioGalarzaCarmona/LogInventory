from django.urls import path
from . import views

urlpatterns = [
    path('sign up/',views.sign_up, name='sign_up'),
    path('log in/<int:code>',views.log_in, name='log_in'),
    path('log out/',views.log_out, name='log_out'),
    path('last password/',views.mail_sender,name='last_password'),
    path('change password/<str:passkey_config>/<str:passkey_link>',views.change_password,name='change_password'),
    path('',views.home, name = 'home')
] 