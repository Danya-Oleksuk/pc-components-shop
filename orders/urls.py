from django.urls import path

from . import views

app_name = "orders"
urlpatterns = [
    path("order/checkout/", views.CheckoutView.as_view(), name="checkout"),
    path("order/success/", views.SuccessTemplateView.as_view(), name="order_success"),
    path("order/cancel/", views.CancelTemplateView.as_view(), name="order_cancel"),
    path("user/my-orders/", views.MyOrdesView.as_view(), name="my_orders"),
    path("webhooks/stripe/", views.stripe_webhook, name="stripe_webhook"),
    path("ajax/cities/", views.autocomplete_city, name="autocomplete_city"),
    path(
        "ajax/warehouses/", views.autocomplete_warehouses, name="autocomplete_warehouse"
    ),
]
