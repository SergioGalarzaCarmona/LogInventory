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
            'message' : 'Los cambios hechos en los campos de "nombre","descripcion" y "imagen", no podrán ser retrocedidos.¡CUIDADO!.'
        })
    else:
        object_instance_before = Objects.objects.get(object_id = id)
        stock_before = object_instance_before.stock
        form = ModifieObject(request.POST,instance=object_instance_before)
        object_instance_after = Objects.objects.get(object_id = id)
        form.save()
        if  (object_instance_before.name != object_instance_after.name) or (object_instance_before.description != object_instance_after.description) or (object_instance_before.image != object_instance_after.image):
            type_instance = Type_Transaction.objects.get(type_id = 4)
        elif stock_before < int(request.POST['stock']):
            type_instance = Type_Transaction.objects.get(type_id = 1)
        elif  stock_before > int(request.POST['stock']):
            type_instance = Type_Transaction.objects.get(type_id = 2)
        else: 
            return render(request,'objects.html',{
            'form' : form,
            'object' : object_instance_after,
            'message' : 'Los cambios hechos en los campos de "nombre","descripcion" y "imagen", no podrán ser retrocedidos.¡CUIDADO!.',
            'change_invalid' : 'No se ha realizado ningún cambio, realiza almenos un cambio.'
        })
        Transactions.objects.create(object_id = object_instance_before,user_id = request.user,type_transaction = type_instance,stock_before = stock_before,stock_after = request.POST['stock'])
        return redirect('main') 
def record(request):
    if request.method =='GET':
        transactions = Transactions.objects.filter(user_id = request.user)
        return render(request,'record.html',{
            'record' : transactions,
        })
    else: 
        object_instance = Objects.objects.get(object_id = request.POST['object'])
        transaction_instance = Transactions.objects.get(transaction_id = request.POST['transaction'])
        object_instance.stock = transaction_instance.stock_before
        if object_instance.show_object == 0:
            object_instance.show_object = 1
        object_instance.save()
        return redirect('record')
        