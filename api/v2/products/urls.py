from django.urls import path

from api.v2.products import views


app_name = "products"

urlpatterns = [
    path("", views.ProductListApi.as_view(), name="product-list"),
    path("<int:pk>/", views.ProductDetailApi.as_view(), name="product-detail"),
    path("create/", views.ProductCreateApi.as_view(), name="product-create"),
    path("<int:pk>/update/", views.ProductUpdateApi.as_view(), name="product-update"),
    path("<int:pk>/delete/", views.ProductDeleteApi.as_view(), name="product-delete"),
    path("category/", views.CategoryListApi.as_view(), name="category-list"),
    path(
        "category/<int:pk>/", views.CategoryDetailApi.as_view(), name="category-detail"
    ),
    path("category/create/", views.CategoryCreateApi.as_view(), name="category-create"),
    path(
        "category/<int:pk>/update/",
        views.CategoryUpdateApi.as_view(),
        name="category-update",
    ),
    path(
        "category/<int:pk>/delete/",
        views.CategoryDeleteApi.as_view(),
        name="category-delete",
    ),
]
