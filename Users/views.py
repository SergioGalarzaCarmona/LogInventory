from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate,get_user
from random import randint

#To send email
import os
from dotenv import load_dotenv
from email.message import EmailMessage
import ssl
import smtplib






# Create your views here.
def sign_up(request):
    
    #filter the method
    if request.method == 'GET':
        return render(request,'sign_up.html',{
    })
    else:
        #Checking passwords to be same 
        if  request.POST['password1'] == request.POST['password2']:
            try:
                #Create user, save, and login new user
                user = User.objects.create_user(username=request.POST['username'],password=request.POST['password1'],email=request.POST['email_adress'])
                user.save()
                login(request,user)
                return redirect('main')
            #If the name already exist, must be print "error"
            except IntegrityError:
                return render(request,'sign_up.html',{
                'error' : "El nombre de usuario ya existe."
                })
        else:
            #If the password don't match. print "error"
            return render(request,'sign_up.html',{
                'error' : "Las contraseñas no coinciden."
                })
            
            
def log_in(request,code):
    #Filter method
    if request.method == 'GET':
        if code == 0: 
            return render(request,'log_in.html')
        else: 
            return render(request,'log_in.html',{
                'first_session' : 'Primero inicia sesion para poder recuperar la contraseña.'
            })
    else:
        #If the caracter "@" is in "user", It's a email
        if '@' in request.POST['user']:
            #Create a user intance using email
            user_instance = User.objects.get(email = request.POST['user'])
        else:
            #Create a user instance using name
            user_instance = request.POST['user']
        #Authenticate user with the user instance and password
        user = authenticate(username=user_instance,password=request.POST['password'])
        if user is None:
            return render(request,'log_in.html',{
            'error' : "El usuario o la contraseña son incorrectos."
        })
        else:
            login(request,user)
            if code == 0:
                return redirect('main')
            else:
                return redirect('last_password')
#To log out
def log_out(request):
    logout(request)
    return redirect('home')
#To send into server the html "home.html" 
def home(request):
    return render(request,'home.html')

#To send email for reset password
def mail_sender(request):
    if request.method == 'GET':
        if str(request.user) == "AnonymousUser":
            ruta = reverse(viewname='log_in',args=[1])
            return redirect(ruta)
        else:
            return render(request,'last_password.html')
    else:
            #passkey to reset password
            #This passkey is to validate email sent
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
            passkey_config = str(request.user) + ',' + str(passkey)
            #Load the variables of enviroment
            load_dotenv()
            app_password = os.getenv('APP_PASSWORD')
            #Email adress with that send email
            email_sender = 'Log.Inventory2406@gmail.com'
            #subject and body of email
            subject = 'Email para cambiar la contraseña.'
            body = f'''En este email se adjunta un link para restablecer tu contraseña.
            NO COMPARTAS ESTE LINK CON NADIE.
            Si has recibido este mensaje y no lo solicitaste, ps preocupese pq no tenemos forma de cambiar la contraseña de otra manera. 
            http://127.0.0.1:8000/change%20password/{passkey_config}/{passkey}
            '''
            #config of EmailMessage
            em = EmailMessage()
            em['From'] = email_sender
            em['To'] = request.POST['email']
            em['Subject'] = subject
            em.set_content(body)
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
                smtp.login(email_sender,app_password)
                smtp.sendmail(email_sender,request.POST['email'],em.as_string())
            return render(request,'last_password.html')
        
def change_password(request,passkey_config,passkey_link):
    user,passkey = passkey_config.split(',')
    
    if request.method == 'GET':
        if str(request.user) == user:
            if passkey == passkey_link:
                return render(request,'change_password.html')
            else:
                return render(request,'error_passkey.html',{
                    'error' : 'Eror de passkey'
                })
        else:
            return render(request,'error_passkey.html',{
                'error' : 'Error de user'
            })
    else:
        if  request.POST['password1'] == request.POST['password2']: 
            user = get_user(request)
            user.set_password(str(request.POST['password1']))
            user.save()
            return render(request,'change_password.html')
        else: 
            return render(request,'change_password.html',{
                'error' : 'Las contraseñas no coinciden.'
            })