from django.urls import path

from api.v2.orders import views


app_name = "orders"

urlpatterns = [
    path("", views.OrderListApi.as_view(), name="order-list"),
]
