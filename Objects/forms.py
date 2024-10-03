from django.forms import ModelForm,Form

from django.contrib.auth.models import User
from Objects.models import Objects

class ObjectForm(ModelForm):
    class Meta:
        model = Objects
        fields = ['name','stock','description','image']
class ModifieObject(ModelForm):
    class Meta:
        model = Objects
        fields = ['name','stock','description','image','show_object']
