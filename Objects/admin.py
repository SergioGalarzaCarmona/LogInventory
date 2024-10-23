from django.contrib import admin
from Objects.models import Transactions,Objects,Type_Transaction
# Register your models here.



#Register all models into the admin site (The user don´t view this)
admin.site.register(Transactions)
admin.site.register(Objects)
admin.site.register(Type_Transaction)