from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView

from cart.models import Cart
from .forms import OrderForm
from .models import Order


class MyOrdesView(TemplateView):
    template_name = "orders/my_orders.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['orders'] = Order.objects.filter(user=self.request.user)

        return context

class SuccessTemplateView(TemplateView):
    template_name = 'orders/success.html'

class CheckoutView(FormView):
    template_name = "orders/checkout.html"
    form_class = OrderForm
    success_url = reverse_lazy("orders:order_success")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cart = Cart.objects.filter(user=self.request.user)
        context['cart'] = cart
        context['user_cart_total'] = sum(i.total_price for i in cart)

        return context

    def form_valid(self, form):
        order = form.save(commit=False)
        order.user = self.request.user
        order.first_name = form.cleaned_data['first_name']
        order.last_name = form.cleaned_data['last_name']
        order.address = form.cleaned_data['address']
        order.status = Order.CREATED
        order.update_after_payment()

        order.save()
        return super().form_valid(form)