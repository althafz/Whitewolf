
from ast import keyword
from multiprocessing import context
from unicodedata import category
from django.shortcuts import render,get_object_or_404
from django.db.models import Q

from catagory.models import Catagory
from . models import Products

from django.core.paginator import EmptyPage, PageNotAnInteger,Paginator

# Create your views here.

def store(request, catagory_slug=None):
    catagories = None
    Product = None
    
    if catagory_slug != None:
        catagories = get_object_or_404(Catagory, slug=catagory_slug)
        Product = Products.objects.filter(catagory=catagories, is_available=True)
        paginator = Paginator(Product, 9)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = Product.count()
        
    else:
        Product = Products.objects.all().order_by('id')
        paginator = Paginator(Product, 9)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = Product.count()
    
    context = {
        'products': paged_products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)

def product_detail(request, catagory_slug, product_slug):
   
    try:
        single_product = Products.objects.get(catagory__slug = catagory_slug, slug=product_slug)
        
    except Exception as e:
        raise e
    
    context = {
        'single_product': single_product,
        
    }    
    print(single_product)
    return render(request, 'store/product_detail.html', context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            product = Products.objects.filter(Q(product_name__icontains=keyword) | Q(description__icontains=keyword))
            product_count = product.count()
        else:
            product = Products.objects.all()
            product_count = product.count()
    context = {
        'products': product,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)