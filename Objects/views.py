from django.shortcuts import render
from Objects import forms,models
# Create your views here.
def main(request):
    return render(request,'main.html')