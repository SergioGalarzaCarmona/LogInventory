from django import forms
from django.contrib.auth.models import User
from Objects.models import Objects

class Create_or_Modifie_Object(forms.Form):
    name = forms.CharField(label='Nombre',max_length=50,widget=forms.TextInput({'class' : 'object-name'}))
    stock = forms.IntegerField(label='Cantidad',max_value=10000,widget=forms.NumberInput({'class' : 'object-stock'}))
    description = forms.CharField(label='Descripcion',max_length=500,widget=forms.Textarea({'class' : 'object-description'}))
    image = forms.ImageField(label='Imagen')
    
class Untrack_Object(forms.Form):
    pass

class Reverse_Transaction(forms.Form):
    pass