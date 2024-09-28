from django import forms
from django.contrib.auth.models import User

class Create_Objects(forms.Form):
    name = forms.CharField(label='Nombre',max_length=50,widget=forms.TextInput({'class' : 'object-name'}))
    stock = forms.IntegerField(label='Cantidad',max_value=10000,widget=forms.Select({'class' : 'object-stock'}))
    description = forms.CharField(label='Descripcion',max_length=500,widget=forms.Textarea({'class' : 'object-description'}))
    image = forms.ImageField(label='Imagen',widget=forms.Select({'class' : 'object-image'}))