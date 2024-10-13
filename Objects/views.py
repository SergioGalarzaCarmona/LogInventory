from django.shortcuts import render,redirect
from Objects.forms import ObjectForm,ModifieObject
from Objects.models import Objects,Transactions,Type_Transaction
# Create your views here.
def main(request):
    object_instance = Objects.objects.filter(user_id = request.user)
    if request.method == 'GET':
        return render(request,'main.html',{
            'create_or_modifie_form' : ObjectForm ,
            'objects' : object_instance,
            'show' : False
        })
    else:
        form = ObjectForm(request.POST,request.FILES)
        instance_valid = Objects.objects.filter(name = request.POST['name'], user_id = request.user)
        if int(request.POST['stock']) < 0:
            return render(request,'main.html',{
                    'create_or_modifie_form' : ObjectForm,
                    'objects' : object_instance,          
                    'number_invalid' : 'El stock no puede ser negativo.',
                    'show' : True
                }) 
        if len(instance_valid) == 0:
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
                    'is_not_valid' : 'Algunos de los datos ingresados no son válidos',
                    'show' : True
                }) 
        else: 
            return render(request,'main.html',{
                    'create_or_modifie_form' : ObjectForm,
                    'objects' : object_instance,
                    'name_invalid' : 'El nombre ya está en uso, ingrese otro por favor',
                    'show' : True
                }) 
            
            
def object_instance(request,id):
    record_object = Transactions.objects.filter(user_id = request.user, object_id = id)
    if request.method == 'GET':
        object_instance = Objects.objects.get(object_id = id)
        form = ModifieObject(instance=object_instance)
        return render(request,'objects.html',{
            'form' : form,
            'object' : object_instance,
            'message' : 'Los cambios hechos en los campos de "nombre","descripción" y "imagen", no podrán ser retrocedidos.¡CUIDADO!.',
            'record_object' : record_object
        })
    else:
        try:
            validation_record = request.POST['object']
        except:
            validation_record = None
        if validation_record != None:
            object_instance = Objects.objects.get(object_id = request.POST['object'])
            transaction_instance = Transactions.objects.get(transaction_id = request.POST['transaction'])
            object_instance.stock = transaction_instance.stock_before
            if object_instance.show_object == 0:
                object_instance.show_object = 1
            object_instance.save()
            return redirect('main')
        else:
            object_instance_before = Objects.objects.get(object_id = id)
            stock_before = object_instance_before.stock
            form = ModifieObject(request.POST,instance=object_instance_before)
            object_instance_after = Objects.objects.get(object_id = id)
            form.save()
            equal_name = (object_instance_before.name == object_instance_after.name)
            equal_stock = (object_instance_before.stock == object_instance_after.stock)
            equal_description = (object_instance_before.description == object_instance_after.description)
            equal_image = (object_instance_before.image == object_instance_after.image)
            equal_show_object = (object_instance_before.show_object == object_instance_after.show_object)
            validation = equal_name and equal_stock and equal_description and equal_image and equal_show_object
            if validation == True:
                return render(request,'objects.html',{
                'form' : form,
                'object' : object_instance_after,
                'message' : 'Los cambios hechos en los campos de "nombre","descripción" y "imagen", no podrán ser retrocedidos.¡CUIDADO!.',
                'change_invalid' : 'No se ha realizado ningún cambio, realiza almenos un cambio.',
                'record_object' : record_object
            })
            else:
                if equal_show_object == False:
                    type_instance = Type_Transaction.objects.get(type_id = 5)
                elif  (object_instance_before.name != object_instance_after.name) or (object_instance_before.description != object_instance_after.description) or (object_instance_before.image != object_instance_after.image):
                    type_instance = Type_Transaction.objects.get(type_id = 4)
                elif stock_before < int(request.POST['stock']):
                    type_instance = Type_Transaction.objects.get(type_id = 1)
                elif  stock_before > int(request.POST['stock']):
                    type_instance = Type_Transaction.objects.get(type_id = 2)
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
        return redirect('main')
        