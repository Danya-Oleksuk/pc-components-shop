from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryViewSet, WishlistViewSet

router = DefaultRouter()
router.register("products", ProductViewSet)
router.register("categories", CategoryViewSet)
router.register(r"user/(?P<user_id>\d+)/wishlist", WishlistViewSet)

app_name = "api"

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/token/", obtain_auth_token),
]
