from django.urls import include, path

app_name = "v2"

urlpatterns = [
    path("products/", include("api.v2.products.urls")),
]
