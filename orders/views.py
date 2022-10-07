from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import redirect, render
from cart.models import Cartitem
from .forms import OrderForm
from .models import Order
import datetime


def payment(request):
    return render(request, 'orders/payment.html')

 


def place_order(request, total = 0, quantity = 0):
    current_user = request.user
    # if cart count is less than or equal to 0 redirect back to shop
    cart_items = Cartitem.objects.filter(user=current_user)
    print(cart_items)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    
    
    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity) 
        quantity += cart_item.quantity
        
    tax = (3 * total)/100
    grand_total = total + tax    
    
    if request.method == 'POST':
        form =OrderForm(request.POST)
        if form.is_valid():
            # store billing info to order table
            data = Order()
            data.user = request.user
            data.first_name  = form.cleaned_data['first_name']
            data.last_name   = form.cleaned_data['last_name']  
            data.phone       = form.cleaned_data['phone']  
            data.email       = form.cleaned_data['email']      
            data.address_1   = form.cleaned_data['address_1']      
            data.address_2   = form.cleaned_data['address_2']      
            data.state       = form.cleaned_data['state']      
            data.city        = form.cleaned_data['city']      
            data.pin         = form.cleaned_data['pin']   
            data.order_total = grand_total
            data.tax         = tax
            data.ip         = request.META.get('REMOTE_ADDR')
            data.save()
            # generate order no
            
            year = int(datetime.date.today().strftime('%Y'))
            date = int(datetime.date.today().strftime('%d'))
            month = int(datetime.date.today().strftime('%m'))
            d  = datetime.date(year,date,month)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            
            
            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
            }
            return render(request, 'orders/payment.html', context)
        else:
            print(form)
        return redirect('checkout')
    
def success(request):
    return render (request,'orders/success.html')
    
        
    
        
                
                
    
