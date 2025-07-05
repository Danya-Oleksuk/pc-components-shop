from rest_framework import viewsets, permissions

from products.filters import ProductFilter
from products.models import Product
from .serializers import ProductSerializer

from django_filters.rest_framework import DjangoFilterBackend

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
