from django.shortcuts import render

from .models import Cart

def cart_list(request):
    cart = Cart.objects.filter(user=request.user)
    return render(request, "cart/cart.html", context={"cart": cart})