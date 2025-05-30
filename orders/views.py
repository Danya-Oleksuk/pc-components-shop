from django.views.generic import TemplateView

from cart.models import Cart

class CheckoutView(TemplateView):
    template_name = "orders/checkout.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cart = Cart.objects.filter(user=self.request.user)
        context['cart'] = cart
        context['user_cart_total'] = sum(i.total_price for i in cart)

        return context