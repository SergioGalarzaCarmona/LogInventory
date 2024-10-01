from django.shortcuts import render,redirect
from Objects.forms import ObjectForm
from Objects.models import Objects,Transactions,Type_Transaction
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