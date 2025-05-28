from django.urls import path
from .views import cart_list, cart_add


app_name = 'cart'
urlpatterns = [
    path('user/cart/', cart_list, name='cart_list'),
    path('cart/add/<int:product_id>/', cart_add, name='cart_add'),
]