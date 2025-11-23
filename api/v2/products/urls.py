from django.urls import path

from api.v2.products import views


app_name = "products"

urlpatterns = [
    path("", views.ProductListApi.as_view(), name="product-list"),
    path("<int:pk>/", views.ProductDetailApi.as_view(), name="product-detail"),
    path("<int:pk>/update/", views.ProductUpdateApi.as_view(), name="product-update"),
]
