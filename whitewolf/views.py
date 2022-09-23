
from django.shortcuts import render
from catagory.models import Catagory


def home(request):
    categories = Catagory.objects.all()
    
    context = {
        'categories': categories,
    }
    
    return render(request, 'home.html', context)