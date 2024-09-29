from django.forms import ModelForm,Form

from django.contrib.auth.models import User
from Objects.models import Objects

class ObjectForm(ModelForm):
    class Meta:
        model = Objects
        fields = ['name','stock','description','image']
    
class Untrack_Object(Form):
    pass

class Reverse_Transaction(Form):
    pass