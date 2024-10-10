from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate

# Create your views here.
def sign_up(request):
    if request.method == 'GET':
        return render(request,'sign_up.html',{
    })
    else:
        if  request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'],password=request.POST['password1'],email=request.POST['email_adress'])
                user.save()
                login(request,user)
                return redirect('main')
            except IntegrityError:
                return render(request,'sign_up.html',{
                'error' : "User already exists"
                })
        else:
            return render(request,'sign_up.html',{
                'error' : "Password don't match"
                })
            
            
def log_in(request):
    if request.method == 'GET':
        return render(request,'log_in.html')
    else:
        user = authenticate(username=request.POST['user'],password=request.POST['password'])
        if user is None:
            return render(request,'log_in.html',{
            'error' : "User doesn't exists"
        })
        else:
            login(request,user)
            return redirect('main')

def log_out(request):
    logout(request)
    return redirect('home')
    
def home(request):
    return render(request,'home.html')