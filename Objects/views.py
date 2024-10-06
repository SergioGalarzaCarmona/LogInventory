from django.shortcuts import render,redirect
from Objects.forms import ObjectForm,ModifieObject
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
        stock_before = object_instance.stock
        form = ModifieObject(request.POST,instance=object_instance)
        form.save()
        if stock_before == int(request.POST['stock']):
            type_instance = Type_Transaction.objects.get(type_id = 4)
        elif stock_before < int(request.POST['stock']):
            type_instance = Type_Transaction.objects.get(type_id = 1)
        elif  stock_before > int(request.POST['stock']):
            type_instance = Type_Transaction.objects.get(type_id = 2)
        Transactions.objects.create(object_id = object_instance,user_id = request.user,type_transaction = type_instance,stock_before = stock_before,stock_after = request.POST['stock'])
        return redirect('main') 
def record(request):
    transactions = Transactions.objects.filter(user_id = request.user)
    return render(request,'record.html',{
        'record' : transactions,
    })