from django.urls import path
from Objects import views

urlpatterns = [
    path('',views.main,name='main')
]



