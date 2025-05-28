from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .models import Cart

@login_required(login_url="/user/login", redirect_field_name=None)
def cart_list(request):
    cart = Cart.objects.filter(user=request.user)
    user_cart_total = cart.aggregate(total=Sum(F('product__price') * F('quantity')))['total'] or 0
    return render(request, "cart/cart.html", context={"cart": cart,
                                                      "user_cart_total": user_cart_total,})

def cart_add(request, product_id):
    cart = Cart.objects.filter(user=request.user, product_id=product_id)

    if not cart.exists():
        obj = Cart.objects.create(user=request.user, product_id=product_id, quantity=1)
    else:
        obj = cart.first()
        obj.quantity += 1
        obj.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def cart_remove(request, cart_id):
    cart = Cart.objects.get(id=cart_id, user=request.user)
    cart.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])