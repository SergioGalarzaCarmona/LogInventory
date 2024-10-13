from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate
from random import randint

#To send email
import os
from dotenv import load_dotenv
from email.message import EmailMessage
import ssl
import smtplib




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
                'error' : "El nombre de usuario ya existe."
                })
        else:
            return render(request,'sign_up.html',{
                'error' : "Las contraseñas no coinciden."
                })
            
            
def log_in(request):
    if request.method == 'GET':
        return render(request,'log_in.html')
    else:
        user = authenticate(email=request.POST['user'],password=request.POST['password'])
        if user is None:
            return render(request,'log_in.html',{
            'error' : "El usuario o la contraseña son incorrectos."
        })
        else:
            login(request,user)
            return redirect('main')

def log_out(request):
    logout(request)
    return redirect('home')
    
def home(request):
    return render(request,'home.html')


def mail_sender(request):
    if request.method == 'GET':
        return render(request,'last_password.html')
    else:
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

        http://127.0.0.1:8000/change%20password/{passkey}


        '''
        #config of EmailMessage
        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = request.POST['email']
        em['Subject'] = subject
        em.set_content = body


        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
            smtp.login(email_sender,app_password)
            smtp.sendmail(email_sender,request.POST['email'],em.as_string())



        return render(request,'last_password.html')