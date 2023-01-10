from django.shortcuts import render
from store.models import *
from django.http import JsonResponse
import json


def home(request):
    if request.user.is_authenticated:
        products=Product.objects.all()
        totalCartItems=Order.objects.all()[0].get_cart_items
    else:
        products=[]
        totalCartItems=[]
    context={'products':products, 'totalCartItems':totalCartItems}
    return render(request, 'store/home.html', context)

def cart(request):
    
    if request.user.is_authenticated:
        order, created=Order.objects.get_or_create(customer=request.user.customer, completed=False)
        print(order)
        items=order.orderitem_set.all()
        totalCartItems=order.get_cart_items
    else:
        items=[]
        order=[]
        totalCartItems=[]
    context={'items':items,'order':order, 'totalCartItems':totalCartItems}
    return render(request, 'store/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        order, created=Order.objects.get_or_create(customer=request.user.customer, completed=False)
        print(order)
        items=order.orderitem_set.all()
    else:
        items=[]
        order=[]
    context={'items':items,'order':order}
    return render(request, 'store/checkout.html', context)

def product(request, product_category, product_name, product_id):
    product=Product.objects.get(name=product_name, id=product_id, category=product_category)
    context={'product':product}
    return render(request, 'store/product.html', context)


def update_cart(request):
    if request.method == 'POST':
        data=json.loads(request.body)
        productId=data['productId']
        action=data['action']

        customer=request.user.customer
        product=Product.objects.get(id=productId)
        order, created=Order.objects.get_or_create(customer=customer, completed=False)
        
        orderItem, created=OrderItem.objects.get_or_create(product=product,order=order)

        if action == 'add':
            orderItem.quantity = (orderItem.quantity+1)
        elif action == 'replace':
            orderItem.quantity = data['quantity']

        orderItem.save() 
        totalCartItems=order.get_cart_items
        
        return JsonResponse(json.dumps({
            'message':'Cart was updated',
            'totalCartItems':totalCartItems,
            'cartTotal':order.get_cart_total,
            'orderItemTotal':orderItem.get_total,
            'productId':productId,
        }), safe=False)
    return JsonResponse('Nice Try!', safe=False)

def add_to_cart(request):
    if request.method == "POST":
        data=json.loads(request.body)

        product_id=data['product_id']
        product_quantity=data['product_quantity']

        customer = request.user.customer
        product=Product.objects.get(id=product_id)
        order, created=Order.objects.get_or_create(customer=customer, completed=False)
        orderItem, created=OrderItem.objects.get_or_create(order=order, product=product)
        orderItem.quantity=product_quantity
        orderItem.save()
        
        context={
            'status':'carted',
            'message':f'{orderItem.quantity} unit(s) of {orderItem.product.name} added to cart'
        }
        
        return JsonResponse(context, safe=False)


    return JsonResponse('Alright', safe=False)
    
