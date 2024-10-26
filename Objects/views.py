from django.shortcuts import render,redirect
from Objects.forms import ObjectForm,ModifieObject
from Objects.models import Objects,Transactions,Type_Transaction
from django.contrib.auth.models import AnonymousUser

#This view shows space work, and shows all objects
def main(request):
    
    if request.method == 'GET':
        if str(request.user) != 'AnonymousUser':
            #Filter objects by user
            object_instance = Objects.objects.filter(user_id = request.user)
            return render(request,'main.html',{
                'create_form' : ObjectForm,
                'objects' : object_instance,
                'show' : False
                })
        else:
            return render(request,'error_403.html')
    else:
        #Filter objects by user
        object_instance = Objects.objects.filter(user_id = request.user)
        #Craate an instance of the model "Objects" with the form
        form = ObjectForm(request.POST,request.FILES)
        #Check that the name of objects doesn't exist
        instance_valid = Objects.objects.filter(name = request.POST['name'], user_id = request.user,show_object = True)
        #Verifie that the object stock isn't negative
        if int(request.POST['stock']) < 0:
            return render(request,'main.html',{
                    'create_form' : ObjectForm,
                    'objects' : object_instance,          
                    'number_invalid' : 'El stock no puede ser negativo.',
                    'show' : True
                }) 
        #Verifie that the "instance_valid" doesn't have any object
        if len(instance_valid) == 0:
            #If any data is wrong the object can't be created  
            if form.is_valid():
                #Create object
                post = form.save(commit=False)
                post.user_id = request.user
                post.save()
                #Create an instance into the record
                object_instance_list = Objects.objects.filter(name = request.POST['name'])
                object_instance = object_instance_list[len(object_instance_list) - 1]
                type_instance = Type_Transaction.objects.get(type_id = 3) 
                Transactions.objects.create(object_id = object_instance ,user_id = request.user, type_transaction = type_instance,stock_before = 0, stock_after = request.POST['stock'] )
                return redirect('main')
            else:
                #Filter all items that the user has created
                object_instance = Objects.objects.filter(user_id = request.user)
                return render(request,'main.html',{
                    'create_form' : ObjectForm,
                    'objects' : object_instance,       
                    'is_not_valid' : 'Algunos de los datos ingresados no son válidos',
                    'show' : True
                }) 
        #If instance_valid has some data, is because the name already exists
        else: 
            return render(request,'main.html',{
                    'create_form' : ObjectForm,
                    'objects' : object_instance,
                    'name_invalid' : 'El nombre ya está en uso, ingrese otro por favor',
                    'show' : True
                }) 
            
            
def object_instance(request,id):
    
    #If object doesn't exist raise error 404
    try:
        #Filter obeject by this id
        object_instance = Objects.objects.get(object_id = id)
    except:
        return render(request,'error_404.html')
    
    
    #Filter record by object id 
    record_object = Transactions.objects.filter(object_id = id)
    
    
    if request.method == 'GET':
        #If user is Anonymoususer raise error 403
        if str(request.user) != 'AnonymousUser':
            return render(request,'objects.html',{
                'object' : object_instance,
                'message' : 'Los cambios hechos en los campos de "nombre","descripción" y "imagen", no podrán ser retrocedidos.¡CUIDADO!',
                'record_object' : record_object[::-1]
            })
        else:
            return render(request,'error_403.html')
        
    else:
        #Validate if the input "image_clear" has some value, the varibale doesn't raise an exception
        try:
            validation_image_button = str(request.POST['image_clear'])
        except:
            validation_image_button = None
        # If the user clicks on "Retroceder cambios" enter on "if"
        try:
            validation_record_button = request.POST['object']
        except:
            validation_record_button = None
        
        if validation_record_button != None:
            #Filter which transaction will be used by trasaction id
            transaction_instance = Transactions.objects.get(transaction_id = request.POST['transaction'])
            #Go back stock number with the transaction info
            object_instance.stock = transaction_instance.stock_before
            #Set type transaction "Go_Back"
            type_instance = Type_Transaction.objects.get(type_id = 5)
            #Create an instance into record about an undone change
            Transactions.objects.create(object_id = object_instance,user_id = request.user,type_transaction = type_instance, stock_before = transaction_instance.stock_after, stock_after = transaction_instance.stock_before  )
            #If the object was delete at the space work, undo this change
            if object_instance.show_object == 0:
                object_instance.show_object = 1
            #save object with all changes
            object_instance.save()
            return redirect('main')
        #If the clear image button is clicked, change image to default image
        elif validation_image_button == 'on':
            object_instance.image = 'object_images/image.png'
            #save change 
            object_instance.save()
            return render(request,'objects.html',{
                'object' : object_instance,
                'message' : 'Los cambios hechos en los campos de "nombre","descripción" y "imagen", no podrán ser retrocedidos.¡CUIDADO!',
                'record_object' : record_object[::-1]
            })
        else:
            
            #Create form to modifie the instance before
            form = ModifieObject(request.POST,request.FILES,instance=object_instance)
            
            #Validate that stock isn't negative
            if int(request.POST['stock']) < 0:
                
                return render(request,'objects.html',{
                'object' : object_instance,
                'message' : 'Los cambios hechos en los campos de "nombre","descripción" y "imagen", no podrán ser retrocedidos.¡CUIDADO!',
                'change_invalid' : 'El stock no puede ser negativo.',
                'record_object' : record_object[::-1]
            })
                
            try:
                validation_name_exists = Objects.objects.filter(name = request.POST['name'],user_id = request.user)
                
            except:
                validation_name_exists = []
            if len(validation_name_exists) == 1:
                    object_filter = validation_name_exists[0]
                    if object_instance.object_id != object_filter.object_id:
                        return render(request,'objects.html',{
                            'object' : object_instance,
                            'message' : 'Los cambios hechos en los campos de "nombre","descripción" y "imagen", no podrán ser retrocedidos.¡CUIDADO!',
                            'change_invalid' : 'El nombre que ingreso ya esta en uso, por favor ingrese otro.',
                            'record_object' : record_object[::-1]})
                    else: 
                        pass
            #Validate that data 'image' exists
            try:
                validation_image_file = request.FILES['image']
                
            #If it doesn't exists take a value: ''
            except:
                validation_image_file = ''
            
            
            
            #Save this instance stock number for create a transaction instance 
            stock_before = object_instance.stock
            #Modifie an object with the new data
            
            #Make all camparasions to kown if the user did some change
            equal_name = (str(request.POST['name']) == object_instance.name)
            equal_stock = (int(request.POST['stock']) == stock_before)
            equal_description = (str(request.POST['description']) == object_instance.description)
            
            
            #Image validation
            if validation_image_file == '':
                equal_image = True
            else:
                equal_image = False
                
            #Show object status validation  
            try:
                if str(request.POST['show_object']) == 'on':
                    show_object_before = True
                else:
                    show_object_before = False
                    
                #Do comaparasions with the object instance
                equal_show_object = (show_object_before == object_instance.show_object)
            except:
                equal_show_object = False
            
            #If it is True the user didn't do any change
            validation = equal_name and equal_stock and equal_description and equal_image and equal_show_object
            
            #Save all data into database
            form.save() 
            #Make all the comparisons to know if there was any change

            #Enter on "if" if the user doesn´t do any change, and send message to alert the mistake
            if validation == True:
                return render(request,'objects.html',{
                'object' : object_instance,
                'message' : 'Los cambios hechos en los campos de "nombre","descripción" y "imagen", no podrán ser retrocedidos.¡CUIDADO!',
                'change_invalid' : 'No se ha realizado ningún cambio, realiza almenos un cambio.',
                'record_object' : record_object[::-1]
            })
            else:
                #Select transaction type
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
        if str(request.user) != 'AnonymousUser':
            #Filter all transactions that the user have has done
            transactions = Transactions.objects.filter(user_id = request.user)
            return render(request,'record.html',{
                #Reverse the list to show the last change at top
                'record' : transactions[::-1],
            })
        else:
            return render(request,'error_403.html')
    else: 
        #Filter objects instance and transactions instance by their id
        object_instance = Objects.objects.get(object_id = request.POST['object'])
        transaction_instance = Transactions.objects.get(transaction_id = request.POST['transaction'])
        #Save stock number before change it 
        object_instance.stock = transaction_instance.stock_before
        #If show_object is 0, change it to 1
        if object_instance.show_object == 0:
            object_instance.show_object = 1
        #Type instance for a reversed change
        type_instance = Type_Transaction.objects.get(type_id = 5)
        #Create instance in record
        Transactions.objects.create(object_id = object_instance,user_id = request.user,type_transaction = type_instance, stock_before = transaction_instance.stock_after, stock_after = transaction_instance.stock_before  )
        #Save all changes into DB
        object_instance.save()
        return redirect('main')
        