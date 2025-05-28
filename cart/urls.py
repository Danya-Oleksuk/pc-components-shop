from django.urls import path
from .views import cart_list


app_name = 'cart'
urlpatterns = [
    path('user/cart/', cart_list, name='cart_list'),
]