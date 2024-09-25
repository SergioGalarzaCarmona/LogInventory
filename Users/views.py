from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate
# Create your views here.
def sign_up(request):
    if request.method == 'GET':
        return render(request,'sign_up.html',{
        'form' : UserCreationForm
    })
    else:
        if  request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('welcome')
            except IntegrityError:
                return render(request,'sign_up.html',{
                'form' : UserCreationForm,
                'error' : "User already exists"
                })
        else:
            return render(request,'sign_up.html',{
                'form' : UserCreationForm,
                'error' : "Password don't match"
                })
            
            
def log_in(request):
    if request.method == 'GET':
        return render(request,'log_in.html',{ 
            'form' : AuthenticationForm
        })
    else:
        user = authenticate(username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request,'log_in.html',{
            'form' : AuthenticationForm,
            'error' : "User doesn't exists"
        })
        else:
            login(request,user)
            return redirect('home')

def log_out(request):
    logout(request)
    return redirect('welcome')
    
def welcome(request):
    return render(request,'welcome.html')