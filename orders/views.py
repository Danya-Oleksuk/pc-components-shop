import stripe
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.views.generic import FormView, TemplateView

from cart.models import Cart
from pc_components_shop import settings

from .forms import OrderForm
from .models import Order
from .novaposhta_service import get_city_suggestions, get_warehouse_suggestions


stripe.api_key = settings.STRIPE_SECRET_KEY

@require_GET
def autocomplete_city(request):
    query = request.GET.get('q', '')
    suggestions = get_city_suggestions(query)
    return JsonResponse(suggestions, safe=False)

@require_GET
def autocomplete_warehouses(request):
    city_ref = request.GET.get('city_ref')
    query = request.GET.get('q', '')
    if not city_ref:
        return JsonResponse([], safe=False)

    warehouses = get_warehouse_suggestions(city_ref, query)
    return JsonResponse(warehouses, safe=False)

class MyOrdesView(TemplateView):
    template_name = "orders/my_orders.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["orders"] = Order.objects.filter(user=self.request.user)
        return context


class SuccessTemplateView(TemplateView):
    template_name = "orders/success.html"


class CancelTemplateView(TemplateView):
    template_name = "orders/cancel.html"


class CheckoutView(FormView):
    template_name = "orders/checkout.html"
    form_class = OrderForm
    success_url = reverse_lazy("orders:order_success")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cart = Cart.objects.filter(user=self.request.user)
        context["cart"] = cart
        context["user_cart_total"] = sum(i.total_price for i in cart)

        return context

    def form_valid(self, form):
        order = form.save(commit=False)
        order.user = self.request.user
        order.first_name = form.cleaned_data["first_name"]
        order.last_name = form.cleaned_data["last_name"]
        order.address = form.cleaned_data["address"]
        order.status = Order.CREATED
        order.save()

        cart = Cart.objects.filter(user=self.request.user)

        line_items = []
        for item in cart:
            line_items.append(
                {
                    "price_data": {
                        "currency": "uah",
                        "unit_amount": int(item.product.price * 100),
                        "product_data": {
                            "name": item.product.name,
                        },
                    },
                    "quantity": item.quantity,
                }
            )

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=line_items,
                mode="payment",
                client_reference_id=str(order.id),
                success_url=self.request.build_absolute_uri(
                    reverse("orders:order_success") + f"?order_id={order.id}"
                ),
                cancel_url=self.request.build_absolute_uri(
                    reverse("orders:order_cancel")
                ),
            )
        except Exception as e:
            return str(e)

        return redirect(checkout_session.url, code=303)


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    if sig_header is None:
        print("❌ Missing Stripe signature header")
        return HttpResponse(status=400)

    try:
        event = stripe.Webhook.construct_event(
            payload=payload, sig_header=sig_header, secret=endpoint_secret
        )
    except ValueError as e:
        print("❌ Invalid payload:", e)
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        print("❌ Invalid signature:", e)
        return HttpResponse(status=400)

    print("✅ Event received:", event["type"])

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        order_id = session.get("client_reference_id")
        print("ℹ️ Order ID from Stripe session:", order_id)

        if order_id:
            from .models import Order

            try:
                order = Order.objects.get(id=order_id, status=Order.CREATED)
                order.update_after_payment()
                print("✅ Order updated successfully")
            except Order.DoesNotExist:
                print("❌ Order not found with ID:", order_id)
                return HttpResponse(status=404)
            except Exception as e:
                print("❌ Error updating order:", e)
                return HttpResponse(status=500)

    return HttpResponse(status=200)
