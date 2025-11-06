from rest_framework import serializers
from api.v2.mixins import (
    ReadOnlySerializerMixin,
)
from products.models import Product


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
