from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, Sum
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView

from .models import Cart


class CartListView(LoginRequiredMixin, ListView):
    login_url = "/user/login"
    redirect_field_name = None
    model = Cart
    template_name = "cart/cart.html"
    context_object_name = "cart"

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.get_queryset()
        user_cart_total = (
            cart.aggregate(total=Sum(F("product__price") * F("quantity")))["total"] or 0
        )
        context["user_cart_total"] = user_cart_total
        return context


class CartAddView(LoginRequiredMixin, View):
    login_url = "/user/login"
    redirect_field_name = None

    def get(self, request, product_id):
        action = request.GET.get("action")
        cart_item, created = Cart.objects.get_or_create(
            user=request.user, product_id=product_id, defaults={"quantity": 1}
        )

        if not created:
            if action == "decrease" and cart_item.quantity > 1:
                cart_item.quantity -= 1
            else:
                cart_item.quantity += 1
            cart_item.save()

        return redirect(request.META.get("HTTP_REFERER", "/"))


class CartRemoveView(LoginRequiredMixin, View):
    login_url = "/user/login"
    redirect_field_name = None

    def get(self, request, cart_id):
        cart = get_object_or_404(Cart, id=cart_id, user=request.user)
        cart.delete()
        return redirect(request.META.get("HTTP_REFERER", "/"))
