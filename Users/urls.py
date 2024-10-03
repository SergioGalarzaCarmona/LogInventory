from django.urls import path
from . import views

urlpatterns = [
    path('sign up/',views.sign_up, name='sign_up'),
    path('log in/',views.log_in, name='log_in'),
    path('log out/',views.log_out, name='log_out'),
    path('',views.home, name = 'home')
] 