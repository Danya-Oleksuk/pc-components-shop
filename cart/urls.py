from django.urls import path

from .views import cart_add, cart_list, cart_remove

app_name = "cart"
urlpatterns = [
    path("user/cart/", cart_list, name="cart_list"),
    path("cart/add/<int:product_id>/", cart_add, name="cart_add"),
    path("cart/remove/<int:cart_id>/", cart_remove, name="cart_remove"),
]
