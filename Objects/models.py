from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Objects(models.Model):
    objects_id = models.IntegerField(primary_key=True,editable=False,unique=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50,unique=True,error_messages={'unique' : 'The name already exists'})
    stock = models.IntegerField(null=False,blank=False)
    last_change = models.DateTimeField(max_length=50)
    description = models.TextField(max_length=500)
    image = models.ImageField()
    
class Transaction(models.Model):
    object_id = models.ForeignKey(Objects, on_delete=models.CASCADE)
    stock_before = models.IntegerField()