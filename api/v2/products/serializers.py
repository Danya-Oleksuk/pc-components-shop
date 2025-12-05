from rest_framework import serializers
from api.mixins import (
    ReadOnlySerializerMixin,
    UpdateOnlySerializerMixin,
)
from products.services.crud import (
    product_update,
)

from products.models.product import Product
from products.models.category import Category


class ProductDisplaySerializer(ReadOnlySerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "slug",
            "description",
            "price",
            "available",
            "created_at",
            "category",
        )


class ProductUpdateSerializer(UpdateOnlySerializerMixin, serializers.Serializer):
    name = serializers.CharField(max_length=255, required=False)
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), required=False
    )
    description = serializers.CharField(required=False)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    available = serializers.BooleanField(required=False)
    image = serializers.ImageField(required=False)

    def update(self, instance, validated_data):
        return product_update(product=instance, **validated_data)
