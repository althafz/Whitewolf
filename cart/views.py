
from multiprocessing import context
from django.shortcuts import render,redirect,get_object_or_404
from store.models import Products, Variation
from .models import Cart,Cartitem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.http import HttpResponse


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_to_cart(request, product_id):
    product = Products.objects.get(id=product_id) #to get product
    product_variation = []
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]
            
            try:
                variation = Variation.objects.get(product = product ,variation_catagory__iexact=key, variation_value__iexact=value)
                product_variation.append(variation)
            except:
                pass     
   
   
    
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))# to get the cart using the cart_id present in the session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )    
    cart.save()
    
    
    is_cart_item_exists = Cartitem.objects.filter(product=product, cart=cart).exists()
    if is_cart_item_exists:
        cart_item = Cartitem.objects.filter(product=product, cart=cart)
        # existing_variation -> database
        # current variation  -> product_variation
        # item_id            -> database
        ex_var_list = []
        id = []
        for item in cart_item:
            existing_variation = item.variations.all()
            ex_var_list.append(list(existing_variation))
            id.append(item.id)
            
        print(ex_var_list)    
        
        if product_variation in ex_var_list:
            # increase the cart item quantity
            index = ex_var_list.index(product_variation)
            item_id = id[index]
            item = Cartitem.objects.get(product=product, id = item_id)
            item.quantity += 1
            item.save()
            
             # create a new cart item 
        else:
            item = Cartitem.objects.create(product=product, quantity=1, cart=cart)
            if len(product_variation) > 0:
                item.variations.clear()
                item.variations.add(*product_variation)
           
            item.save()
    else:
        cart_item = Cartitem.objects.create(
             product = product,
             quantity = 1,
             cart = cart, 
        )
        if len(product_variation) > 0:
            cart_item.variations.clear()
            cart_item.variations.add(*product_variation )
        cart_item.save()
   
    return redirect('cart')


def remove_cart(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id =_cart_id(request))
    product = get_object_or_404(Products, id=product_id)
    try:
        cart_item = Cartitem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

def remove_cart_item(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Products, id=product_id)
    cart_item = Cartitem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect ('cart')
    
    
def cart(request, total = 0, quantity = 0, cart_items = None):
    try:
        cart = Cart.objects.get(cart_id= _cart_id(request))
        cart_items = Cartitem.objects.filter(cart=cart, is_active = True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (3 * total)/100
        grand_total = total + tax
        
    except ObjectDoesNotExist:
        pass
    
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
            
    return render(request, 'store/cart.html', context)


@login_required(login_url='login')
def checkout(request, total = 0, quantity = 0, cart_items = None):
    try:
        cart = Cart.objects.get(cart_id= _cart_id(request))
        cart_items = Cartitem.objects.filter(cart=cart, is_active = True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (3 * total)/100
        grand_total = total + tax
        
    except ObjectDoesNotExist:
        pass
    
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/checkout.html', context)
