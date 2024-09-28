from django.shortcuts import render
from Objects.forms import Create_or_Modifie_Object,Reverse_Transaction,Untrack_Object
from Objects.models import Objects,Transactions,Type_Transaction
# Create your views here.
def main(request):
    return render(request,'main.html',{
        'create_or_modifie_form' : Create_or_Modifie_Object,
        'reverse_transaction_form' : Reverse_Transaction,
        'untrack_object_form' : Untrack_Object
    })