from django.http import HttpResponseRedirect
from django.shortcuts import render

from .models import Cart

def cart_list(request):
    cart = Cart.objects.filter(user=request.user)
    return render(request, "cart/cart.html", context={"cart": cart})

def cart_add(request, product_id):
    cart = Cart.objects.filter(user=request.user, product_id=product_id)

    if not cart.exists():
        obj = Cart.objects.create(user=request.user, product_id=product_id, quantity=1)
    else:
        obj = cart.first()
        obj.quantity += 1
        obj.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
