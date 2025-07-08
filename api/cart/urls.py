from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CartItemViewSet, CartViewSet

router = DefaultRouter()
router.register(r'cart', CartViewSet, basename='cart-view')
router.register(r'user/(?P<user_id>\d+)/cart', CartItemViewSet, basename='user-cart-view')


urlpatterns = [
    path('api/', include(router.urls)),
]