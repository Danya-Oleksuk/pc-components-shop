from django.urls import path
from . import views


app_name = 'orders'
urlpatterns = [
    path('order/checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('order/success/', views.SuccessTemplateView.as_view(), name='order_success'),
    path('user/my-orders/', views.MyOrdesView.as_view(), name='my_orders'),
]