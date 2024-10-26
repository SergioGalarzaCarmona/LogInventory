from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate,get_user
from random import randint

#Send email
import os
from dotenv import load_dotenv
from email.message import EmailMessage
import ssl
import smtplib







def sign_up(request):
    
    #Filter the method
    if request.method == 'GET':
        return render(request,'sign_up.html',{
    })
    else:
        users = User.objects.filter(email = request.POST['email_adress'],is_superuser = 0)
        
        if len(users) == 0:
            #Checking passwords matching 
            if  request.POST['password1'] == request.POST['password2']:
                try:
                    #Create user, save, and login new user
                    user = User.objects.create_user(username=request.POST['username'],password=request.POST['password1'],email=request.POST['email_adress'],is_superuser = 0)
                    user.save()
                    login(request,user)
                    return redirect('main')
                #If the name already exists print "error"
                except IntegrityError:
                    return render(request,'sign_up.html',{
                    'error' : "El nombre de usuario ya existe."
                    })
            else:
                #If the password doesn't match print "error"
                return render(request,'sign_up.html',{
                    'error' : "Las contraseñas no coinciden."
                    })
                
        else:
            return render(request,'sign_up.html',{
                'error' : "El email ingresado ya pertenece a una cuenta"
                }) 
                
            
def log_in(request):
    #Filter method
    if request.method == 'GET':
        return render(request,'log_in.html')
    else:
        #If the caracter "@" is in "user", It's an email
        if '@' in request.POST['user']:
            try:
                #Create an user intance using email
                user_instance = User.objects.get(email = request.POST['user'],is_superuser = 0)
            except:
                return render(request,'log_in.html',{
                'error' : 'El usuario o la contraseña son incorrectas'
            })
        else:
            #Create an user instance using name
            user_instance = request.POST['user']
        #Authenticate user with the user instance and password
        user = authenticate(username=user_instance,password=request.POST['password'])
        if user is None:
            return render(request,'log_in.html',{
            'error' : "El usuario o la contraseña son incorrectos."
        })
        else:
            login(request,user)
            return redirect('main')
#Log out
def log_out(request):
    logout(request)
    return redirect('home')
#Send into server the html "home.html" 
def home(request):
    return render(request,'home.html')

#Send email for reset password
def mail_sender(request):
    if request.method == 'GET':
        return render(request,'lost_password.html')
    else:
        users = User.objects.filter(email = request.POST['email'],is_superuser = 0)
        if len(users) == 1:
            
            user = users[0]
            #Passkey for reset password
            #This passkey is for validate email sending
            caracters = [
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
            'k', 'l', 'm', 'n', 'ñ', 'o', 'p', 'q', 'r', 's',
            't', 'u', 'v', 'w', 'x', 'y', 'z', '1', '2', '3',
            '4', '5', '6', '7', '8', '9'
            ]
            passkey = ''
            for x in range(25):
                indice = randint(0,35)
                caracter = caracters[indice]
                passkey += caracter
            passkey_config = str(user) + ',' + str(passkey)
            #Load the enviroment variables
            load_dotenv()
            app_password = os.getenv('APP_PASSWORD')
            #Email adress that is going to send the email
            email_sender = 'Log.Inventory2406@gmail.com'
            #Subject and body of the email
            subject = 'Email para cambiar la contraseña.'
            body = f'''En este email se adjunta un link para restablecer tu contraseña.
            NO COMPARTAS ESTE LINK CON NADIE.
            Si has recibido este mensaje y no lo solicitaste, ps preocupese pq no tenemos forma de cambiar la contraseña de otra manera. 
            http://127.0.0.1:8000/change%20password/{passkey_config}/{passkey}
            '''
            #Config EmailMessage
            em = EmailMessage()
            em['From'] = email_sender
            em['To'] = request.POST['email']
            em['Subject'] = subject
            em.set_content(body)
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
                smtp.login(email_sender,app_password)
                smtp.sendmail(email_sender,request.POST['email'],em.as_string())
            return render(request,'lost_password.html')
        else:
            return render(request,'lost_password.html',{
                'error' : 'El email ingresado no concuerda con ningún usuario. '
            })
        
       
def change_password(request,passkey_config,passkey_link):
    user_link,passkey = passkey_config.split(',')
    user = User.objects.get(username = user_link)
    if request.method == 'GET':
            if passkey == passkey_link:
                return render(request,'change_password.html')
            else:
                return render(request,'error_passkey.html',{
                    'error' : 'Error de passkey'
                })
    else:
        if  request.POST['password1'] == request.POST['password2']: 
            user.set_password(str(request.POST['password1']))
            user.save()
            return redirect('log_in')
        else: 
            return render(request,'change_password.html',{
                'error' : 'Las contraseñas no coinciden.'
            })