from django.urls import path
from . import views


app_name = 'orders'
urlpatterns = [
    path('order/checkout/', views.CheckoutView.as_view(), name='checkout'),
]