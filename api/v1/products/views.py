from rest_framework import viewsets, permissions

from products.filters import ProductFilter
from products.models.product import Product
from products.models.category import Category
from products.models.wishlist import Wishlist
from .serializers import ProductSerializer, CategorySerializer, WishlistSerializer

from django_filters.rest_framework import DjangoFilterBackend


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]


class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        return Wishlist.objects.filter(user_id=user_id)

    def perform_create(self, serializer):
        user_id = self.kwargs["user_id"]
        serializer.save(user_id=user_id)
