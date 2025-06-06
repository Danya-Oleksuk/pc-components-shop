from django.urls import path

from .views import CartAddView, CartRemoveView, CartListView

app_name = "cart"
urlpatterns = [
    path("user/cart/", CartListView.as_view(), name="cart_list"),
    path("cart/add/<int:product_id>/", CartAddView.as_view(), name="cart_add"),
    path("cart/remove/<int:cart_id>/", CartRemoveView.as_view(), name="cart_remove"),
]