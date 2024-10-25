from django.shortcuts import render,redirect
from Objects.forms import ObjectForm,ModifieObject
from Objects.models import Objects,Transactions,Type_Transaction

#This view show space work, here show all objects
def main(request):
    
    #Filter objects by user
    object_instance = Objects.objects.filter(user_id = request.user)
    if request.method == 'GET':
        return render(request,'main.html',{
            'create_or_modifie_form' : ObjectForm,
            'objects' : object_instance,
            'show' : False
        })
    else:
        
        #Craate a instance to the model "Objects" with the form
        form = ObjectForm(request.POST,request.FILES)
        #Check that the name of objects doesn't exist
        instance_valid = Objects.objects.filter(name = request.POST['name'], user_id = request.user)
        #Verifie that the stock of object isn't negative
        if int(request.POST['stock']) < 0:
            return render(request,'main.html',{
                    'create_or_modifie_form' : ObjectForm,
                    'objects' : object_instance,          
                    'number_invalid' : 'El stock no puede ser negativo.',
                    'show' : True
                }) 
        #Verifie that the "instance_valid" don't have any object.
        if len(instance_valid) == 0:
            #If nay data is wrong the object can't be created  
            if form.is_valid():
                #Create object
                post = form.save(commit=False)
                post.user_id = request.user
                post.save()
                
                #Create a instance into the record
                object_instance = Objects.objects.get(name = request.POST['name'])
                type_instance = Type_Transaction.objects.get(type_id = 3) 
                Transactions.objects.create(object_id = object_instance ,user_id = request.user, type_transaction = type_instance,stock_before = 0, stock_after = request.POST['stock'] )
                return redirect('main')
            else:
                #Filter all items that the user has created
                object_instance = Objects.objects.filter(user_id = request.user)
                return render(request,'main.html',{
                    'create_or_modifie_form' : ObjectForm,
                    'objects' : object_instance,       
                    'is_not_valid' : 'Algunos de los datos ingresados no son válidos',
                    'show' : True
                }) 
        #If instance_valid have some data, is because the name already exist
        else: 
            return render(request,'main.html',{
                    'create_or_modifie_form' : ObjectForm,
                    'objects' : object_instance,
                    'name_invalid' : 'El nombre ya está en uso, ingrese otro por favor',
                    'show' : True
                }) 
            
            
def object_instance(request,id):
    #Filter record with the object id. 
    record_object = Transactions.objects.filter(object_id = id)
    if request.method == 'GET':
        #filter obejct with this id
        object_instance = Objects.objects.get(object_id = id)
        form = ModifieObject(instance=object_instance)
        return render(request,'objects.html',{
            'object' : object_instance,
            'message' : 'Los cambios hechos en los campos de "nombre","descripción" y "imagen", no podrán ser retrocedidos.¡CUIDADO!',
            'record_object' : record_object[::-1]
        })
    else:
        # If the user click on "Retroceder cambios" enter on "if"
        try:
            validation_record_button = request.POST['object']
        except:
            validation_record_button = None
        if validation_record_button != None:
            #Filter the object by the object id 
            object_instance = Objects.objects.get(object_id = request.POST['object'])
            #Filter which transaction will be used by the trasaction id
            transaction_instance = Transactions.objects.get(transaction_id = request.POST['transaction'])
            #Go back the stock with the information of transaction
            object_instance.stock = transaction_instance.stock_before
            #Give type transaction "Go_Back"
            type_instance = Type_Transaction.objects.get(type_id = 5)
            #Create instance into record about undone change
            Transactions.objects.create(object_id = object_instance,user_id = request.user,type_transaction = type_instance, stock_before = transaction_instance.stock_after, stock_after = transaction_instance.stock_before  )
            #if the object was delete at the space work, undo this change
            if object_instance.show_object == 0:
                object_instance.show_object = 1
            #save object with all changes
            object_instance.save()
            return redirect('main')
        else:
            #Filter object by id to show its info into the form
            object_instance = Objects.objects.get(object_id = id)
            
            #Create form to modifie the before instance
            form = ModifieObject(request.POST,request.FILES,instance=object_instance)
            
            #Validate that the stock don't be negative
            if int(request.POST['stock']) < 0:
                
                return render(request,'objects.html',{
                'object' : object_instance,
                'message' : 'El stock no puede ser negativo, ingresa un numero mayor o igual a 0.',
                'record_object' : record_object[::-1]
            })
                
            try:
                validation_name_exists = Objects.objects.filter(name = request.POST['name'],user_id = request.user)
                
            except:
                validation_name_exists = []
            if len(validation_name_exists) != 0:
                    return render(request,'objects.html',{
                        'object' : object_instance,
                        'message' : 'El nombre que ingreso ya existe, ingrese otro por favor.',
                        'record_object' : record_object[::-1]
            })
            #Validation that data 'image' exists
            try:
                validation_image_file = request.FILES['image']
                
            #If doesn't exists take a value: ''
            except:
                validation_image_file = ''
            
            
            
            #save stock of this instance to use for create a instance of transaction
            stock_before = object_instance.stock
            #Modifie a object that new data
            
            #Makes all camparasions to kown if the user make some change
            equal_name = (str(request.POST['name']) == object_instance.name)
            equal_stock = (int(request.POST['stock']) == stock_before)
            equal_description = (str(request.POST['description']) == object_instance.description)
            
            
            #validation image
            if validation_image_file == '':
                equal_image = True
            else:
                equal_image = False
                
            #validation of show object status
            try:
                if str(request.POST['show_object']) == 'on':
                    show_object_before = True
                else:
                    show_object_before = False
                    
                #Make comaparasions with the object instance
                equal_show_object = (show_object_before == object_instance.show_object)
            except:
                equal_show_object = False
            
            #If is True the user don't make any change
            validation = equal_name and equal_stock and equal_description and equal_image and equal_show_object
            
            #save all data into database
            form.save() 
            #make all the comparisons to see if there was any change.

            #Enter on this "if" if the user don't make change, and send message to say that
            if validation == True:
                return render(request,'objects.html',{
                'object' : object_instance,
                'message' : 'Los cambios hechos en los campos de "nombre","descripción" y "imagen", no podrán ser retrocedidos.¡CUIDADO!',
                'change_invalid' : 'No se ha realizado ningún cambio, realiza almenos un cambio.',
                'record_object' : record_object[::-1]
            })
            else:
                #Select which that the type of transaction
                if equal_show_object == False:
                    type_instance = Type_Transaction.objects.get(type_id = 6)
                elif  (not equal_name) or (not equal_description) or (not equal_image):
                    type_instance = Type_Transaction.objects.get(type_id = 4)
                elif stock_before < int(request.POST['stock']):
                    type_instance = Type_Transaction.objects.get(type_id = 1)
                elif  stock_before > int(request.POST['stock']):
                    type_instance = Type_Transaction.objects.get(type_id = 2)
                #Create transacion with form data
                Transactions.objects.create(object_id = object_instance,user_id = request.user,type_transaction = type_instance,stock_before = stock_before,stock_after = request.POST['stock'])
                return redirect('main') 
def record(request):
    if request.method =='GET':
        transactions = Transactions.objects.filter(user_id = request.user)
        return render(request,'record.html',{
            'record' : transactions[::-1],
        })
    else: 
        object_instance = Objects.objects.get(object_id = request.POST['object'])
        transaction_instance = Transactions.objects.get(transaction_id = request.POST['transaction'])
        object_instance.stock = transaction_instance.stock_before
        if object_instance.show_object == 0:
            object_instance.show_object = 1
        type_instance = Type_Transaction.objects.get(type_id = 5)
        Transactions.objects.create(object_id = object_instance,user_id = request.user,type_transaction = type_instance, stock_before = transaction_instance.stock_after, stock_after = transaction_instance.stock_before  )
        object_instance.save()
        return redirect('main')
        