from django import forms
from django.contrib.auth.models import User

class Create_Objects(forms.Form):
    user = forms.ChoiceField(User)