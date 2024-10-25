from django.forms import ModelForm
from Objects.models import Objects


#Creating form to create the "Objects"
class ObjectForm(ModelForm):
    class Meta:
        model = Objects
        fields = ['name','stock','description','image']
        
#Creating form to modifie the "Objects"
class ModifieObject(ModelForm):
    class Meta:
        model = Objects
        fields = ['name','stock','description','image','show_object']
