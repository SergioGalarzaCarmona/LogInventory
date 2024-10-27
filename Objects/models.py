from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

#Creating object "Objects"
class Objects(models.Model):
    object_id = models.IntegerField(primary_key=True,editable=False,unique=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    show_object = models.BooleanField(default=True)
    stock = models.IntegerField(null=False,blank=False)
    last_change = models.DateTimeField(max_length=50,auto_now_add=True)
    description = models.TextField(max_length=500)
    image = models.ImageField(blank=True,upload_to='object_images/',default='object_images/image.png')
    
    def __str__(self):
        return (self.object_id,self.user_id,self.name,self.show_object,self.stock,self.last_change,self.description,self.image)
#Creating object "Type_Transactions"
class Type_Transaction(models.Model):
    type_id = models.IntegerField(primary_key=True,editable=False,unique=True)
    status = models.CharField(max_length=20,null=False,blank=False)

#Creating object "Transactions"
class Transactions(models.Model):
    transaction_id = models.IntegerField(primary_key=True,editable=False,unique=True)
    object_id = models.ForeignKey(Objects,on_delete=models.PROTECT,editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    type_transaction = models.ForeignKey(Type_Transaction,on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.today())
    stock_before = models.IntegerField(null=False,blank=False)
    stock_after = models.IntegerField(null=False,blank=False)
