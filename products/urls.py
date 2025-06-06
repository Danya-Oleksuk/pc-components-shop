from django.urls import path

from . import views

app_name = "products"
urlpatterns = [
    path("", views.MainPageView.as_view(), name="main_page"),
    path("products/", views.ProductsListView.as_view(), name="catalog"),
    path(
        "product/<slug:product_slug>/",
        views.ProductDetailView.as_view(),
        name="product_detail",
    ),
]
