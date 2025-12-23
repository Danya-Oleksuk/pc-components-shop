from django.urls import include, path

app_name = "v2"

urlpatterns = [
    path("products/", include("api.v2.products.urls")),
    path("orders/", include("api.v2.orders.urls")),
    path("users/", include("api.v2.users.urls")),
]
