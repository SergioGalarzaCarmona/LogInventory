from django.shortcuts import render,redirect
from Objects.forms import ObjectForm,ModifieObject
from Objects.models import Objects
# Create your views here.
def main(request):
    if request.method == 'GET':
        object_instance = Objects.objects.filter(user_id = request.user)
        return render(request,'main.html',{
            'create_or_modifie_form' : ObjectForm ,
            'objects' : object_instance,
        })
    else: 
        form = ObjectForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user_id = request.user
            post.save()
            return redirect('main')
        else:
            object_instance = Objects.objects.filter(user_id = request.user)
            return render(request,'main.html',{
                'create_or_modifie_form' : ObjectForm,
                'objects' : object_instance,          
                'is_not_valid' : 'Los datos ingresados no son validos'
            }) 
            
            
def object_instance(request,id):
    if request.method == 'GET':
        object_instance = Objects.objects.get(object_id = id)
        form = ModifieObject(instance=object_instance)
        return render(request,'objects.html',{
            'form' : form,
            'object' : object_instance,
        })
    else:
        object_instance = Objects.objects.get(object_id = id)
        form = ModifieObject(request.POST,instance=object_instance)
        form.save()
        return redirect('main')
        