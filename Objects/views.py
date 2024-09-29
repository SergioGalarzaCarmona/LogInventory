from django.shortcuts import render
from Objects.forms import ObjectForm
from Objects.models import Objects,Transactions,Type_Transaction
# Create your views here.
def main(request):
    if request.method == 'GET':
        object_instance = Objects.objects.filter(user_id = request.user)
        print(object_instance)
        return render(request,'main.html',{
            'create_or_modifie_form' : ObjectForm ,
            'objects' : object_instance,
        })
    else: 
        new_object = Objects.objects.create(user_id = request.user, name = request.POST['name'],stock = request.POST['stock'],description = request.POST['description'],image = request.POST['image'])
        return render(request,'main.html',{
            'create_or_modifie_form' : ObjectForm,
        })