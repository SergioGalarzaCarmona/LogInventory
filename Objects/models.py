from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Objects(models.Model):
    object_id = models.IntegerField(primary_key=True,editable=False,unique=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50,unique=True,error_messages={'unique' : 'The name already exists'})
    show_object = models.BooleanField(default=True)
    stock = models.IntegerField(null=False,blank=False)
    last_change = models.DateTimeField(max_length=50)
    description = models.TextField(max_length=500)
    image = models.ImageField()

class Type_Transaction(models.Model):
    type_id = models.IntegerField(primary_key=True,editable=False,unique=True)
    status = models.CharField(max_length=20,null=False,blank=False)

class Transactions(models.Model):
    transaction_id = models.IntegerField(primary_key=True,editable=False,unique=True)
    object_id = models.ForeignKey(Objects,on_delete=models.PROTECT,editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    type_transaction = models.ForeignKey(Type_Transaction,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True,editable=False)
    stock_before = models.IntegerField(null=False,blank=False)
    stock_after = models.IntegerField(null=False,blank=False)
